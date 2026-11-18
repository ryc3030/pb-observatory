// Cloudflare Worker: 정적 사이트는 그대로 내주고, /api/gdelt 하나만 GDELT DOC API로 대신 요청한다.
// GitHub Actions 러너 IP가 GDELT에 막힐 때(429) Cloudflare 쪽 IP로 하루 한 번 요청하기 위한 통로다.
// 검색식은 고정이고, 같은 날·같은 기간 요청은 Cloudflare 캐시(12시간)로 답해 GDELT에는 하루 한 번만 간다.
const QUERY = '("participatory budgeting" OR "participatory budget")';
const UA = "PB-Observatory/4.1 (+https://github.com/ryc3030/pb-observatory; one request per day)";

async function gdelt(url, ctx) {
  const days = Math.min(90, Math.max(1, parseInt(url.searchParams.get("days") || "1", 10) || 1));
  const day = new Date().toISOString().slice(0, 10);
  const key = new Request(`https://pb-observatory.cache/gdelt?days=${days}&day=${day}`);
  const cache = caches.default;
  const hit = await cache.match(key);
  if (hit) return hit;
  const api = "https://api.gdeltproject.org/api/v2/doc/doc?" + new URLSearchParams({
    query: QUERY, mode: "artlist", format: "json", maxrecords: "250", timespan: `${days}d`, sort: "datedesc",
  });
  let r;
  try {
    r = await fetch(api, { headers: { "User-Agent": UA, Accept: "application/json" } });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e) }), { status: 502, headers: { "content-type": "application/json" } });
  }
  const body = await r.text();
  const res = new Response(body, {
    status: r.status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "public, max-age=43200", "x-gdelt-status": String(r.status) },
  });
  if (r.ok) ctx.waitUntil(cache.put(key, res.clone()));
  return res;
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === "/api/gdelt") return gdelt(url, ctx);
    return env.ASSETS.fetch(request);
  },
};
