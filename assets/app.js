const REGION_KO = {
  Europe: "유럽",
  Africa: "아프리카",
  Asia: "아시아",
  "North America": "북아메리카",
  "South America": "남아메리카",
  "Central America & Caribbean": "중앙아메리카·카리브",
  Oceania: "오세아니아",
};
const STAGE_KO = {
  implementation: "이행",
  results: "결과 공개",
  "results / implementation": "결과 공개·이행",
  monitoring: "모니터링",
  documented: "문헌 확인",
  historical: "역사 사례",
  completed: "완료",
  "completed / documented": "완료·문헌 확인",
  "annual cycle": "연례 운영",
  "annual / electoral cycle": "연례·선거주기",
  recurring: "반복 운영",
  "recurring / mixed": "반복·혼합형",
  "recurring municipal framework": "반복형 지방정부 체계",
  "budget participation / monitoring": "예산참여·모니터링",
  "2026 cycle / legal framework tracked": "2026 회차·법적근거 추적",
};
const LEVEL_KO = {
  city: "시",
  "city districts": "도시 자치구",
  "city/community": "도시·지역공동체",
  "city/state": "시·주",
  community: "지역공동체",
  county: "카운티",
  district: "구역",
  "district municipality": "구역 지방정부",
  local: "지방",
  "metropolitan city": "광역시",
  "municipal / villages": "지방정부·마을",
  municipality: "지방정부",
  national: "국가",
  "national municipal framework": "국가-지방정부 법정체계",
  neighbourhood: "근린지역",
  school: "학교",
  "school district": "교육구",
  state: "주",
};
const SOURCE_KO = {
  official: "공식",
  "research-platform": "연구 플랫폼",
  "research-synthesis": "연구 종합",
  network: "국제 네트워크",
};
const METRIC_KO = {
  voters: "투표자",
  "participants/voters": "참여자·투표자",
  participants: "참여자",
  "participation rate": "참여율",
  "residents reached": "도달 주민",
  students: "학생",
};
const PROGRAM_KO = {
  "usa-nyc-peoples-money": "더 피플스 머니(The People’s Money)",
  "fin-helsinki-omastadi": "오마스타디(OmaStadi)",
  "bra-porto-alegre": "포르투알레그리 참여예산",
  "bra-santa-catarina": "산타카타리나 참여예산",
  "prt-palmela": "팔멜라 「Eu Participo」 참여예산",
  "hrv-trogir": "트로기르 참여예산",
  "gbr-lancaster-pots": "랭커스터 「Your Pots」 참여예산 2025",
  "gbr-manchester-cheetham": "치덤 청년 참여예산 2025",
  "gbr-dundee-climate": "던디 기후기금 3.0",
  "pol-krakow-civic": "크라쿠프 시민예산(Budżet Obywatelski)",
  "fra-paris-bp": "파리 참여예산",
  "esp-madrid-decide": "마드리드 참여예산 / Decide Madrid",
  "kor-national-pb": "국민참여예산",
  "kor-seoul-pb": "서울시 시민참여예산 / 주민참여예산",
  "mex-cdmx": "멕시코시티 참여예산",
  "cze-prague": "프라하 자치구 참여예산",
  "svn-maribor": "마리보르 참여예산",
  "isl-reykjavik": "베터 레이캬비크 참여예산 계보",
  "rou-cluj": "클루지나포카 참여예산",
  "arg-rosario": "로사리오 참여예산",
  "ury-montevideo": "몬테비데오 참여예산",
  "can-guelph": "궬프 참여예산 사례",
  "chn-chengdu": "청두 특별기금정책 / 대규모 참여예산",
  "ken-kwale": "Tupo.Tusikizwe 참여형 성인지예산",
  "zaf-vulekamali": "Vulekamali 공공예산 참여 포털",
  "aus-local": "호주 지방정부 참여예산 실험군",
  "nzl-local": "뉴질랜드 지방 참여형 배분 사례군",
  "deu-buergerhaushalt": "독일 시민예산(Bürgerhaushalt) 생태계",
  "ita-school-pb": "이탈리아 학교 참여예산 이니셔티브",
  "ltu-school-pb": "리투아니아 학교 참여예산",
  "uga-wamala": "와말라 지구 참여예산",
  "nld-maastricht": "마스트리흐트 참여예산",
  "fin-lahti": "라흐티 참여예산 2020~2022",
  "usa-central-falls": "Voces Con Poder 프로젝트",
  "gbr-so18": "SO18 Big Local 참여예산",
  "est-tartu": "타르투 참여예산(Kaasav eelarve)",
  "lva-riga": "리가 참여예산",
  "per-san-borja-2026": "산보르하 참여예산 2026",
  "dom-ppm-framework": "도미니카공화국 지방정부 참여예산 체계(PPM)",
};
/* 세계 참여예산 관측소 v4 — 정적 데이터(data/*.json)를 읽어 렌더링합니다.
   data/ 폴더는 GitHub Actions가 매일 자동으로 갱신합니다. */
const $ = (s) => document.querySelector(s),
  $$ = (s) => [...document.querySelectorAll(s)];
const esc = (s) =>
  String(s ?? "").replace(/[&<>"']/g, (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[m]);

let META = {}, countries = [], programs = [], news = [], papers = [], ledger = [], health = {}, history = [], refs = [];
let byISO = {};
const statusName = { verified: "공식/검증", documented: "문헌·플랫폼", monitoring: "탐색 모니터링" };
const status = (c) => c.tracking_status || "monitoring";
const LANG_KO = { en: "영어", es: "스페인어", pt: "포르투갈어", fr: "프랑스어", de: "독일어", it: "이탈리아어", pl: "폴란드어", ko: "한국어", ja: "일본어", zh: "중국어", ru: "러시아어", uk: "우크라이나어", cs: "체코어", sk: "슬로바키아어", ro: "루마니아어", nl: "네덜란드어", fi: "핀란드어", sv: "스웨덴어", lt: "리투아니아어", lv: "라트비아어", et: "에스토니아어", hr: "크로아티아어", id: "인도네시아어", tr: "터키어" };

const countryName = (iso, fb = "") => byISO[iso]?.name_ko || fb || iso || "글로벌";
const regionName = (r) => REGION_KO[r] || r;
const stageName = (v) => STAGE_KO[v] || v || "확인 중";
const levelName = (v) => LEVEL_KO[v] || v || "기타";
const sourceName = (v) => SOURCE_KO[v] || v || "출처";
const metricName = (v) => METRIC_KO[v] || v || "";
const programName = (p) => PROGRAM_KO[p.id] || p.program_name;

const fmtDate = (x, opt = { dateStyle: "medium" }) => {
  if (!x) return "—";
  try {
    const d = /^\d{4}$/.test(String(x)) ? new Date(x + "-01-01") : new Date(x);
    if (isNaN(d)) return x;
    return new Intl.DateTimeFormat("ko-KR", { ...opt, timeZone: "Asia/Seoul" }).format(d);
  } catch { return x; }
};
const ago = (x) => {
  const d = (Date.now() - Date.parse(x)) / 36e5;
  if (!isFinite(d)) return "";
  if (d < 1) return "방금";
  if (d < 24) return Math.round(d) + "시간 전";
  return Math.round(d / 24) + "일 전";
};

const hasBudget = (p) => p.budget?.amount != null || (/\d|%/.test(p.budget?.display || "") && !/확인 중/.test(p.budget?.display || ""));
function fieldFlags(p) {
  return {
    예산: hasBudget(p),
    참여: p.participants?.count != null,
    단계: !!p.stage && !["monitoring", "documented"].includes((p.stage || "").toLowerCase()),
    법: !!(p.legal_basis?.title && !/확인 중/.test(p.legal_basis.title)),
  };
}
const completeness = (p) => Math.round((Object.values(fieldFlags(p)).filter(Boolean).length / 4) * 100);

async function getJSON(name, fb) {
  try {
    const r = await fetch("data/" + name + "?v=" + Math.floor(Date.now() / 6e5), { cache: "no-cache" });
    if (!r.ok) throw new Error(r.status);
    return await r.json();
  } catch (e) {
    console.warn("load fail", name, e);
    return fb;
  }
}

async function loadAll() {
  const [m, c, p, n, pa, l, h, hi, rf] = await Promise.all([
    getJSON("meta.json", {}), getJSON("countries.json", { items: [] }), getJSON("programs.json", { items: [] }),
    getJSON("news.json", { items: [] }), getJSON("papers.json", { items: [] }), getJSON("ledger.json", []),
    getJSON("health.json", {}), getJSON("history.json", []), getJSON("design_refs.json", []),
  ]);
  META = m; countries = c.items || []; programs = p.items || []; news = n.items || []; papers = pa.items || [];
  ledger = l || []; health = h || {}; history = hi || []; refs = rf || [];
  byISO = Object.fromEntries(countries.map((x) => [x.iso3, x]));
  countries.forEach((x) => (x.program_count = programs.filter((p) => p.country_iso3 === x.iso3).length));
}

/* ---------- 상단·요약 ---------- */
function setupHeader() {
  const up = META.updated_at;
  $("#buildDate").textContent = up ? fmtDate(up) + " 갱신" : "—";
  $("#buildDate").title = up ? fmtDate(up, { dateStyle: "full", timeStyle: "short" }) : "";
  $("#paperDate").textContent = up ? fmtDate(up, { dateStyle: "full" }) : "—";
  $("#footUpdated").textContent = up ? `마지막 자동 갱신: ${fmtDate(up, { dateStyle: "long", timeStyle: "short" })} (KST, ${ago(up)})` : "";
  const langs = new Set(news.map((x) => x.lang));
  $("#langCount").textContent = `${langs.size}개 언어 신호 탐색`;
  $("#globalSearch").addEventListener("keydown", (e) => {
    if (e.key === "Enter") { $("#search").value = e.currentTarget.value; location.hash = "explorer"; renderTree(); }
  });
  const saved = (() => { try { return localStorage.getItem("pb-theme"); } catch { return null; } })();
  if (saved === "dark") document.documentElement.classList.add("dark");
  $("#theme").onclick = () => {
    document.documentElement.classList.toggle("dark");
    try { localStorage.setItem("pb-theme", document.documentElement.classList.contains("dark") ? "dark" : "light"); } catch {}
  };
}

function renderPulse() {
  const cnt = { verified: 0, documented: 0, monitoring: 0 };
  countries.forEach((c) => cnt[status(c)]++);
  const N = countries.length || 1;
  $("#pulseNum").firstChild.nodeValue = String(countries.length);
  $("#donut").style.setProperty("--verifiedDeg", (cnt.verified / N) * 360 + "deg");
  $("#donut").style.setProperty("--docDeg", ((cnt.verified + cnt.documented) / N) * 360 + "deg");
  $("#verifiedShare").textContent = Math.round((cnt.verified / N) * 100) + "%";
  const active = countries.filter((c) => c.news_30d > 0).length;
  $("#statusLegend").innerHTML =
    Object.entries(cnt).map(([k, v]) => `<div><span>${statusName[k]}</span><b>${v}</b></div>`).join("") +
    `<div><span>30일 뉴스 신호 국가</span><b>${active}</b></div>`;
  $("#kCountries").textContent = cnt.verified + cnt.documented;
  $("#kPrograms").textContent = programs.length;
  $("#kJuris").textContent = new Set(programs.map((p) => p.jurisdiction_name)).size;
  $("#kObs").textContent = programs.reduce((a, p) => a + Object.values(fieldFlags(p)).filter(Boolean).length, 0);
}

/* ---------- 지도 ---------- */
let evMap = null, evPopup = null;
function features() {
  const fc = [];
  countries.forEach((c) => {
    if (!c.coord) return;
    fc.push({ type: "Feature", geometry: { type: "Point", coordinates: [c.coord[1], c.coord[0]] },
      properties: { kind: "country", iso3: c.iso3, name: c.name_ko, status: status(c), statusLabel: statusName[status(c)],
        news30: c.news_30d || 0, latest: c.latest_news?.date || c.base_signal_date || "—",
        signal: c.latest_news?.title || c.base_signal || "", programs: c.program_count || 0 } });
  });
  programs.forEach((p) => {
    if (!Number.isFinite(p.lat)) return;
    fc.push({ type: "Feature", geometry: { type: "Point", coordinates: [p.lon, p.lat] },
      properties: { kind: "program", iso3: p.country_iso3, name: programName(p), status: p.tracking_status || "monitoring",
        statusLabel: statusName[p.tracking_status || "monitoring"], city: p.jurisdiction_name, latest: p.last_verified || "—",
        signal: stageName(p.stage), news30: 0, programs: 1 } });
  });
  return { type: "FeatureCollection", features: fc };
}
function renderMap() {
  if (!window.maplibregl) {
    $("#map2d").innerHTML = '<div style="display:grid;place-items:center;height:100%;color:#d9e8e1;font-size:12px">세계지도 라이브러리를 불러오지 못했습니다.</div>';
    return;
  }
  evMap = new maplibregl.Map({ container: "map2d", style: "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
    center: [8, 18], zoom: 0.8, minZoom: 0.45, maxZoom: 7, renderWorldCopies: false, attributionControl: true });
  evMap.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
  evPopup = new maplibregl.Popup({ closeButton: false, closeOnClick: false, offset: 10 });
  const color = ["match", ["get", "status"], "verified", "#38ce9d", "documented", "#7ea0c7", "#778983"];
  evMap.on("load", () => {
    evMap.fitBounds([[-170, -55], [180, 76]], { padding: 18, duration: 0 });
    evMap.addSource("pb", { type: "geojson", data: features() });
    evMap.addLayer({ id: "pb-country", type: "circle", source: "pb", filter: ["==", ["get", "kind"], "country"],
      paint: { "circle-radius": ["+", ["match", ["get", "status"], "verified", 6, "documented", 5, 4], ["min", 6, ["*", 0.6, ["get", "news30"]]]],
        "circle-color": color, "circle-opacity": ["match", ["get", "status"], "monitoring", 0.6, 0.9],
        "circle-stroke-width": ["case", [">", ["get", "news30"], 0], 2.2, 0.8],
        "circle-stroke-color": ["case", [">", ["get", "news30"], 0], "#f4d27a", "#f2fff9"] } });
    evMap.addLayer({ id: "pb-program", type: "circle", source: "pb", filter: ["==", ["get", "kind"], "program"],
      paint: { "circle-radius": ["interpolate", ["linear"], ["zoom"], 0.5, 2.2, 5, 5], "circle-color": "#ffffff",
        "circle-stroke-color": color, "circle-stroke-width": 1.4 } });
    ["pb-country", "pb-program"].forEach((L) => {
      evMap.on("mouseenter", L, () => (evMap.getCanvas().style.cursor = "pointer"));
      evMap.on("mousemove", L, (e) => {
        const p = e.features?.[0]?.properties; if (!p) return;
        const sub = p.kind === "program" ? `${esc(p.city)} · ${esc(p.statusLabel)}` : `${esc(p.statusLabel)} · 프로그램 ${p.programs} · 30일 뉴스 ${p.news30}`;
        evPopup.setLngLat(e.lngLat).setHTML(`<b>${esc(p.name)}</b><small>${sub}</small><div style="margin-top:6px">최근 ${esc(p.latest)}</div><div style="margin-top:4px">${esc(String(p.signal).slice(0, 140))}</div>`).addTo(evMap);
      });
      evMap.on("mouseleave", L, () => { evMap.getCanvas().style.cursor = ""; evPopup.remove(); });
      evMap.on("click", L, (e) => {
        const p = e.features?.[0]?.properties; if (!p) return;
        $("#search").value = countryName(p.iso3); renderTree();
        const d = $(`#tree details[data-iso="${p.iso3}"]`); if (d) d.open = true;
        location.hash = "explorer";
      });
    });
  });
}

function renderRegions() {
  const counts = {}, active = {};
  countries.forEach((c) => { counts[c.region] = (counts[c.region] || 0) + 1; if (status(c) !== "monitoring") active[c.region] = (active[c.region] || 0) + 1; });
  const max = Math.max(...Object.values(counts));
  $("#regionBars").innerHTML = Object.entries(counts).sort((a, b) => b[1] - a[1]).map(([r, v]) =>
    `<div class="barrow" title="근거 확보 ${active[r] || 0} / 추적 ${v}"><span>${esc(regionName(r))}</span><div class="bartrack"><div class="barfill" style="width:${(v / max) * 100}%"></div></div><b>${active[r] || 0}/${v}</b></div>`).join("");
  const sel = $("#region");
  Object.keys(counts).sort().forEach((r) => sel.insertAdjacentHTML("beforeend", `<option value="${esc(r)}">${esc(regionName(r))}</option>`));
}

function renderTicker() {
  const items = news.slice(0, 5);
  $("#ticker").innerHTML = items.length
    ? items.map((x) => `<a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(countryName(x.country_iso3, "글로벌"))} · ${esc(x.title_ko || x.title)}</a>`).join("<span aria-hidden='true'>   •   </span>")
    : "새로운 신호를 기다리는 중입니다.";
}

/* ---------- PB 데일리 ---------- */
let newsLimit = 24;
function setupNewsFilters() {
  const langs = {}; news.forEach((n) => (langs[n.lang] = (langs[n.lang] || 0) + 1));
  Object.entries(langs).sort((a, b) => b[1] - a[1]).forEach(([l, v]) => $("#newsLang").insertAdjacentHTML("beforeend", `<option value="${l}">${esc(LANG_KO[l] || l)} (${v})</option>`));
  const cs = {}; news.forEach((n) => n.country_iso3 && (cs[n.country_iso3] = (cs[n.country_iso3] || 0) + 1));
  Object.entries(cs).sort((a, b) => b[1] - a[1]).forEach(([i, v]) => $("#newsCountry").insertAdjacentHTML("beforeend", `<option value="${i}">${esc(countryName(i))} (${v})</option>`));
  ["#newsLang", "#newsCountry"].forEach((s) => ($(s).onchange = () => { newsLimit = 24; renderNews(); }));
  $("#newsSearch").oninput = () => { newsLimit = 24; renderNews(); };
  $("#moreNews").onclick = () => { newsLimit += 24; renderNews(); };
}
function renderNews() {
  const L = $("#newsLang").value, C = $("#newsCountry").value, q = $("#newsSearch").value.trim().toLowerCase();
  const rows = news.filter((n) => (L === "all" || n.lang === L) && (C === "all" || n.country_iso3 === C) &&
    (!q || (n.title + " " + (n.title_ko || "")).toLowerCase().includes(q)));
  const n = rows.slice(0, newsLimit);
  $("#moreNews").style.display = rows.length > newsLimit ? "" : "none";
  if (!n.length) { $("#newsgrid").innerHTML = "<p>조건에 맞는 뉴스 신호가 없습니다.</p>"; return; }
  $("#newsgrid").innerHTML = `<div class="newsstream">${n.map((x, i) => {
    const ko = x.title_ko && x.title_ko !== x.title;
    return `<article class="story newsrow ${i === 0 ? "is-latest" : ""}"><time class="newsdate" datetime="${esc(x.published_at)}">${esc(fmtDate(x.published_at))}</time><div class="tag">자동수집 · ${esc(countryName(x.country_iso3, "국가 미상"))} · ${esc(LANG_KO[x.lang] || x.lang)} · ${esc(x.source || "")}</div><h3>${esc(ko ? x.title_ko : x.title)}</h3>${ko ? `<p lang="${esc(x.lang)}">${esc(x.title)}</p>` : ""}<a href="${esc(x.url)}" target="_blank" rel="noopener">원문 확인 ↗</a></article>`;
  }).join("")}</div>`;
}

/* ---------- 논문 ---------- */
let paperLimit = 10;
function renderResearch() {
  const root = $("#researchGrid");
  const rows = papers.slice(0, paperLimit);
  $("#morePapers").style.display = papers.length > paperLimit ? "" : "none";
  $("#morePapers").onclick = () => { paperLimit += 10; renderResearch(); };
  if (!rows.length) { root.innerHTML = '<p class="empty-research">아직 수집된 논문이 없습니다. 다음 자동 갱신 때 채워집니다.</p>'; return; }
  root.innerHTML = rows.map((r, i) => {
    const ko = r.title_ko && r.title_ko !== r.title;
    return `<article class="paper-card ${i === 0 ? "paper-lead" : ""}"><div class="paper-meta"><time>${esc(fmtDate(r.published_at))}</time><span>${esc(r.open_access ? "오픈액세스" : (r.concepts?.[0] || "참여예산 연구"))}</span></div><h3>${esc(ko ? r.title_ko : r.title)}</h3>${ko ? `<div class="paper-original">${esc(r.title)}</div>` : ""}<p class="paper-by">${esc([(r.authors || []).join(", "), r.venue].filter(Boolean).join(" · "))}</p>${r.abstract_snippet ? `<p class="paper-summary">${esc(r.abstract_snippet.slice(0, 260))}${r.abstract_snippet.length > 260 ? "…" : ""}</p>` : ""}<footer>${r.doi ? `<span>DOI ${esc(r.doi)}</span>` : `<span>${esc(r.source)}</span>`}<a href="${esc(r.url)}" target="_blank" rel="noopener">논문 원문 ↗</a></footer></article>`;
  }).join("");
}

/* ---------- 탐색기 ---------- */
function renderTree() {
  const region = $("#region").value, tracking = $("#tracking").value, has = $("#hasProgram").value, q = $("#search").value.trim().toLowerCase();
  const filtered = countries.filter((c) => {
    if (region !== "all" && c.region !== region) return false;
    if (tracking !== "all" && status(c) !== tracking) return false;
    const ps = programs.filter((p) => p.country_iso3 === c.iso3);
    if (has === "with" && !ps.length) return false;
    if (has === "without" && ps.length) return false;
    if (q && ![c.name_ko, c.name_en, c.base_signal, ...(c.aliases || [])].join(" ").toLowerCase().includes(q) &&
      !ps.some((p) => [p.jurisdiction_name, p.program_name, programName(p)].join(" ").toLowerCase().includes(q))) return false;
    return true;
  }).sort((a, b) => ["verified", "documented", "monitoring"].indexOf(status(a)) - ["verified", "documented", "monitoring"].indexOf(status(b)) || (b.news_30d || 0) - (a.news_30d || 0) || a.name_ko.localeCompare(b.name_ko, "ko"));
  $("#count").textContent = `${filtered.length}개 국가 · ${filtered.reduce((a, c) => a + (c.program_count || 0), 0)}개 프로그램 표시`;
  $("#tree").innerHTML = filtered.map((c) => {
    const ps = programs.filter((p) => p.country_iso3 === c.iso3).sort((a, b) => completeness(b) - completeness(a));
    const ln = c.latest_news;
    const sig = `<div class="countrysignal" style="font-size:11px;margin:0 0 10px;color:var(--muted)"><b style="color:var(--ink)">기준 근거</b> ${esc(c.base_signal || "—")}${c.primary_source ? ` · <a href="${esc(c.primary_source)}" target="_blank" rel="noopener">출처 ↗</a>` : ""}${ln ? `<br><b style="color:var(--ink)">최근 뉴스 신호</b> ${esc(ln.date)} · <a href="${esc(ln.url)}" target="_blank" rel="noopener">${esc(ln.title)}</a> <span>(${esc(ln.source)})</span>` : ""}</div>`;
    return `<details class="country" data-status="${status(c)}" data-iso="${c.iso3}"><summary><div class="ctitle"><b>${esc(c.name_ko)}</b><small>${esc(regionName(c.region))} · ${esc(c.base_status || "")} · 최근 ${esc(c.activity_date || "—")}</small></div><span class="pill ${status(c)}">${statusName[status(c)]}</span><span class="hide-sm">프로그램 ${ps.length} · 30일 뉴스 ${c.news_30d || 0}</span><span>＋</span></summary><div class="countrybody">${sig}${ps.length ? `<div class="programgrid">${ps.map(renderProgram).join("")}</div>` : `<p style="font-size:10px;color:var(--muted)">프로그램 단위 근거가 아직 충분하지 않아 탐색 모니터링 상태입니다.</p>`}</div></details>`;
  }).join("");
}
function renderProgram(p) {
  const score = completeness(p), f = fieldFlags(p);
  const rel = (p.related_news || []).map((n) => `<li><a href="${esc(n.url)}" target="_blank" rel="noopener">${esc(n.date)} · ${esc(n.title)}</a></li>`).join("");
  return `<article class="program"><div class="proghead"><div><div class="eyebrow">${esc(levelName(p.jurisdiction_level))}</div><h4>${esc(programName(p))}</h4><div style="font-size:9px;color:var(--muted)">${esc(p.jurisdiction_name)} · ${esc(statusName[p.tracking_status] || "")}</div></div><span class="stage">${esc(stageName(p.stage))}</span></div><div class="metricgrid"><div class="metric"><span>예산</span><b>${esc(p.budget?.display || "확인 중")}</b></div><div class="metric"><span>참여</span><b>${p.participants?.count != null ? Number(p.participants.count).toLocaleString() + " " + esc(metricName(p.participants.metric)) : "확인 중"}</b></div><div class="metric"><span>법적근거</span><b>${esc(p.legal_basis?.title || "확인 중")}${p.legal_basis?.year ? ` (${p.legal_basis.year})` : ""}</b></div><div class="metric"><span>최종 확인</span><b>${esc(p.last_verified || "—")}</b></div></div><div class="evidencebar"><header><span>근거 완성도</span><b>${score}%</b></header><div class="evtrack"><div class="evfill" style="width:${score}%"></div></div><div class="fields">${Object.entries(f).map(([k, v]) => `<span class="fielddot ${v ? "on" : ""}">${v ? "✓" : "·"} ${k}</span>`).join("")}</div></div>${rel ? `<ul class="relnews">${rel}</ul>` : ""}<footer><span>${esc(sourceName(p.source_type))}</span>${p.primary_url ? `<a href="${esc(p.primary_url)}" target="_blank" rel="noopener">출처 ↗</a>` : ""}</footer></article>`;
}

/* ---------- 분석 ---------- */
function distBars(container, rows) {
  const max = Math.max(1, ...rows.map((x) => x[1]));
  $(container).innerHTML = rows.map(([k, v]) => `<div class="stagebar"><span>${esc(k)}</span><div class="bartrack"><div class="barfill" style="width:${(v / max) * 100}%"></div></div><b>${v}</b></div>`).join("");
}
function renderAnalytics() {
  const buckets = { "75–100%": 0, "50%": 0, "25%": 0, "0%": 0 };
  programs.forEach((p) => { const s = completeness(p); buckets[s >= 75 ? "75–100%" : s >= 50 ? "50%" : s >= 25 ? "25%" : "0%"]++; });
  distBars("#completeBars", Object.entries(buckets));
  const st = {}; programs.forEach((p) => (st[p.stage || "unknown"] = (st[p.stage || "unknown"] || 0) + 1));
  distBars("#stageBars", Object.entries(st).sort((a, b) => b[1] - a[1]).slice(0, 7).map(([k, v]) => [stageName(k), v]));
  const lv = {}; programs.forEach((p) => (lv[p.jurisdiction_level || "other"] = (lv[p.jurisdiction_level || "other"] || 0) + 1));
  distBars("#levelBars", Object.entries(lv).sort((a, b) => b[1] - a[1]).slice(0, 7).map(([k, v]) => [levelName(k), v]));
  const gaps = { 예산: 0, 참여자: 0, 진행단계: 0, 법적근거: 0 };
  programs.forEach((p) => { const f = fieldFlags(p); if (!f.예산) gaps.예산++; if (!f.참여) gaps.참여자++; if (!f.단계) gaps.진행단계++; if (!f.법) gaps.법적근거++; });
  distBars("#gapBars", Object.entries(gaps));
  renderTrend();
}
function renderTrend() {
  const el = $("#trend"), H = history.slice(-120);
  if (H.length < 2) {
    el.innerHTML = `<div style="display:grid;place-items:center;height:100%;font-size:11px;color:var(--muted)">추이는 자동 갱신이 이틀 이상 쌓이면 표시됩니다. (현재 ${H.length}일)</div>`;
    $("#trendNote").textContent = H.length ? `오늘 스냅숏: 30일 뉴스 ${H[0].news_30d}건 · 신호 국가 ${H[0].countries_with_signal_30d}개 · 논문 ${H[0].papers_total}편` : "";
    return;
  }
  const W = 900, Ht = 150, pad = 26;
  const series = [["news_30d", "30일 뉴스 신호", "var(--accent)"], ["countries_with_signal_30d", "신호 국가 수", "var(--blue)"], ["papers_total", "누적 논문", "var(--amber)"]];
  const x = (i) => pad + (i / (H.length - 1)) * (W - pad * 2);
  const lines = series.map(([k, name, col]) => {
    const vals = H.map((h) => h[k] || 0), mx = Math.max(1, ...vals);
    const d = vals.map((v, i) => `${i ? "L" : "M"}${x(i).toFixed(1)},${(Ht - pad - (v / mx) * (Ht - pad * 2)).toFixed(1)}`).join("");
    return `<path d="${d}" fill="none" stroke="${col}" stroke-width="2"/><text x="${W - pad}" y="${(Ht - pad - (vals.at(-1) / mx) * (Ht - pad * 2) - 4).toFixed(1)}" text-anchor="end" font-size="11" fill="${col}">${name} ${vals.at(-1)}</text>`;
  }).join("");
  el.innerHTML = `<svg viewBox="0 0 ${W} ${Ht}" width="100%" height="100%" role="img" aria-label="관측 추이"><line x1="${pad}" y1="${Ht - pad}" x2="${W - pad}" y2="${Ht - pad}" stroke="var(--line)"/>${lines}<text x="${pad}" y="${Ht - 8}" font-size="10" fill="var(--muted)">${H[0].date}</text><text x="${W - pad}" y="${Ht - 8}" font-size="10" text-anchor="end" fill="var(--muted)">${H.at(-1).date}</text></svg>`;
  $("#trendNote").textContent = "각 선은 자체 최댓값 기준으로 정규화했습니다. 값은 오른쪽 끝 라벨을 보십시오.";
}
function renderCompare() {
  const rows = [...programs].sort((a, b) => completeness(b) - completeness(a));
  $("#compare").innerHTML = rows.map((p) => `<tr><td><b>${esc(countryName(p.country_iso3))}</b><br>${esc(p.jurisdiction_name || "")}</td><td>${esc(programName(p))}</td><td><b>${completeness(p)}%</b></td><td>${esc(p.budget?.display || "—")}</td><td>${p.participants?.count != null ? Number(p.participants.count).toLocaleString() + " " + esc(metricName(p.participants.metric)) : "—"}</td><td>${esc(stageName(p.stage))}</td><td>${esc(p.legal_basis?.title || "—")}</td><td>${p.primary_url ? `<a href="${esc(p.primary_url)}" target="_blank" rel="noopener">원문</a>` : "—"}</td></tr>`).join("");
}

/* ---------- 근거 ---------- */
function renderEvidence() {
  const hs = ["news", "papers", "build"].map((k) => health[k]).filter(Boolean);
  $("#health").innerHTML = hs.length ? hs.map((x) => {
    const ok = x.ok;
    const detail = x.queries != null ? `검색어 ${x.queries_ok}/${x.queries} 성공 · 신규 ${x.added} · 보관 ${x.total}` : x.fetched != null ? `수집 ${x.fetched} · 보관 ${x.total}` : "";
    return `<div class="listitem"><b>${ok ? "●" : "○"} ${esc(x.name)}</b><span>${ok ? "정상" : "실패"} · ${esc(fmtDate(x.checked_at, { dateStyle: "short", timeStyle: "short" }))}${detail ? " · " + esc(detail) : ""}${!ok && x.last_success_at ? " · 마지막 성공 " + esc(fmtDate(x.last_success_at)) : ""}</span></div>`;
  }).join("") : '<div class="listitem">자동수집 상태 확인 중</div>';
  $("#ledger").innerHTML = ledger.slice(0, 12).map((o) => `<div class="listitem"><b>${esc(o.type)} · ${esc(o.label)}</b><span><a href="${esc(o.url)}" target="_blank" rel="noopener">${esc(String(o.text).slice(0, 110))}</a> · 관측 ${esc(o.observed_at || "")} · 기록 ${esc(o.date)}</span></div>`).join("") || '<div class="listitem">원장 기록이 아직 없습니다.</div>';
  $("#refs").innerHTML = refs.map((r) => `<a class="osref" href="${esc(r.repo)}" target="_blank" rel="noopener"><b>${esc(r.name)}</b><span>${esc(r.pattern)} ↗</span></a>`).join("");
}

function bind() {
  ["region", "tracking", "hasProgram"].forEach((id) => ($("#" + id).onchange = renderTree));
  $("#search").oninput = renderTree;
  $("#openVerified").onclick = () => $$("#tree details").forEach((d) => (d.open = d.dataset.status === "verified"));
  $("#csv").onclick = () => {
    const rows = [["country", "jurisdiction", "program", "completeness", "budget", "participants", "stage", "legal_basis", "source", "last_verified"]];
    programs.forEach((p) => rows.push([countryName(p.country_iso3), p.jurisdiction_name, p.program_name, completeness(p), p.budget?.display || "", p.participants?.count ?? "", p.stage || "", p.legal_basis?.title || "", p.primary_url || "", p.last_verified || ""]));
    const csv = rows.map((r) => r.map((v) => '"' + String(v ?? "").replace(/"/g, '""') + '"').join(",")).join("\n");
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob(["﻿" + csv], { type: "text/csv" }));
    a.download = "global-pb-observatory-programs.csv"; a.click(); URL.revokeObjectURL(a.href);
  };
}

(async () => {
  await loadAll();
  setupHeader(); bind(); setupNewsFilters();
  renderPulse(); renderMap(); renderRegions(); renderTicker(); renderNews(); renderResearch();
  renderTree(); renderAnalytics(); renderCompare(); renderEvidence();
})();
