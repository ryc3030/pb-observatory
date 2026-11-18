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
/* 세계 참여예산 관측소 v4 — 투표용지·기표 화면. data/*.json(매일 자동 갱신)을 읽어 그립니다. */
const $ = (s, r = document) => r.querySelector(s),
  $$ = (s, r = document) => [...r.querySelectorAll(s)];
const strip = (s) => { const d = document.createElement("div"); d.innerHTML = String(s ?? ""); return d.textContent; };
const esc = (s) =>
  String(s ?? "").replace(/[&<>"']/g, (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[m]);
const svg = (id, cls = "") => `<svg${cls ? ` class="${cls}"` : ""} aria-hidden="true"><use href="#i-${id}"/></svg>`;
const nf = new Intl.NumberFormat("ko-KR");

let META = {}, countries = [], programs = [], news = [], papers = [], ledger = [], health = {}, snaps = [], refs = [], TL = { eras: [], items: [] };
let cases = [], units = [];
let byISO = {};
const ORDER = ["verified", "documented", "monitoring"];
const statusName = { verified: "공식·검증", documented: "문헌·플랫폼", monitoring: "탐색 모니터링" };
const statusHelp = { verified: "정부·공식 기관 원문으로 확인", documented: "연구·국제 플랫폼 문헌으로 확인", monitoring: "근거 탐색 중, 신호만 관측" };
const status = (c) => c.tracking_status || "monitoring";
const slotCls = { verified: "seal", documented: "docu", monitoring: "mon" };
const slot = (st, label) => `<span class="slot ${slotCls[st] || "mon"}" role="img" aria-label="근거 상태: ${esc(label || statusName[st])}">${st === "monitoring" ? "" : svg("stamp")}</span>`;
const LANG_KO = { en: "영어", es: "스페인어", pt: "포르투갈어", fr: "프랑스어", de: "독일어", it: "이탈리아어", pl: "폴란드어", ko: "한국어", ja: "일본어", zh: "중국어", ru: "러시아어", uk: "우크라이나어", cs: "체코어", sk: "슬로바키아어", ro: "루마니아어", nl: "네덜란드어", fi: "핀란드어", sv: "스웨덴어", lt: "리투아니아어", lv: "라트비아어", et: "에스토니아어", hr: "크로아티아어", id: "인도네시아어", tr: "터키어" };
const EXTRA_KO = { RUS: "러시아", TWN: "대만", TUR: "튀르키예" };

const countryName = (iso, fb = "") => byISO[iso]?.name_ko || EXTRA_KO[iso] || fb || iso || "국가 미상";
const regionName = (r) => REGION_KO[r] || r;
const stageName = (v) => STAGE_KO[v] || v || "확인 중";
const levelName = (v) => LEVEL_KO[v] || v || "기타";
const sourceName = (v) => SOURCE_KO[v] || v || "출처";
const metricName = (v) => METRIC_KO[v] || v || "";
const programName = (p) => PROGRAM_KO[p.id] || p.program_name;

const fmtDate = (x, opt = { year: "numeric", month: "short", day: "numeric" }) => {
  if (!x) return "—";
  const d = /^\d{4}$/.test(String(x)) ? new Date(x + "-01-01") : new Date(x);
  if (isNaN(d)) return String(x);
  return new Intl.DateTimeFormat("ko-KR", { ...opt, timeZone: "Asia/Seoul" }).format(d);
};
const shortDate = (x) => fmtDate(x, { month: "numeric", day: "numeric" });
const ago = (x) => {
  const h = (Date.now() - Date.parse(x)) / 36e5;
  if (!isFinite(h)) return "";
  if (h < 1) return "방금";
  if (h < 24) return Math.round(h) + "시간 전";
  return Math.round(h / 24) + "일 전";
};

const known = (v) => v && !/확인 중/.test(v);
const hasBudget = (p) => p.budget?.amount != null || (/\d|%/.test(p.budget?.display || "") && known(p.budget?.display));
function fieldFlags(p) {
  return {
    예산: hasBudget(p),
    참여: p.participants?.count != null,
    단계: !!p.stage && !["monitoring", "documented"].includes((p.stage || "").toLowerCase()),
    법적근거: known(p.legal_basis?.title),
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
  const [m, c, p, n, pa, l, h, hi, rf, cs, el] = await Promise.all([
    getJSON("meta.json", {}), getJSON("countries.json", { items: [] }), getJSON("programs.json", { items: [] }),
    getJSON("news.json", { items: [] }), getJSON("papers.json", { items: [] }), getJSON("ledger.json", []),
    getJSON("health.json", {}), getJSON("history.json", []), getJSON("timeline.json", { eras: [], items: [] }),
    getJSON("cases.json", { items: [] }), getJSON("elections.json", { units: [] }),
  ]);
  cases = cs.items || []; units = el.units || [];
  META = m; countries = c.items || []; programs = p.items || []; news = n.items || []; papers = pa.items || [];
  ledger = l || []; health = h || {}; snaps = hi || []; TL = rf && rf.items ? rf : TL;
  byISO = Object.fromEntries(countries.map((x) => [x.iso3, x]));
  countries.forEach((x) => (x.program_count = programs.filter((p) => p.country_iso3 === x.iso3).length));
}

/* ---------- 셸 ---------- */
function setupShell() {
  const up = META.updated_at;
  const c = META.counts || {};
  $("#updatedLine").innerHTML = up
    ? `<b>${esc(fmtDate(up, { month: "long", day: "numeric", hour: "numeric", minute: "2-digit" }))}</b> 자동 갱신(${esc(ago(up))}) · 뉴스 <b class="tnum">${nf.format(news.length)}</b>건 · 논문 <b class="tnum">${nf.format(papers.length)}</b>편 · 매일 오전 6시 17분 갱신`
    : "갱신 정보를 불러오지 못했습니다. 잠시 뒤 새로고침해 주세요.";
  $("#footUpdated").textContent = up ? `마지막 자동 갱신 ${fmtDate(up, { dateStyle: "long", timeStyle: "short" })} (한국 시간)` : "";
  const langs = new Set(news.map((x) => x.lang));
  $("#langCount").textContent = `지금 ${langs.size}개 언어의 기사가 들어와 있습니다.`;

  const setTheme = () => {
    const d = document.documentElement.classList.contains("dark");
    $("#theme").setAttribute("aria-pressed", d);
    $("#theme").setAttribute("aria-label", d ? "밝은 화면으로 전환" : "어두운 화면으로 전환");
    $("#theme use").setAttribute("href", d ? "#i-sun" : "#i-moon");
  };
  setTheme();
  $("#theme").onclick = () => {
    document.documentElement.classList.toggle("dark");
    setTheme();
    try { localStorage.setItem("pb-theme", document.documentElement.classList.contains("dark") ? "dark" : "light"); } catch {}
    if (evMap) evMap.setStyle(mapStyle(), { diff: false });
    if (histMap) histMap.setStyle(mapStyle(), { diff: false });
    renderTrend();
  };
  $("#globalSearch").addEventListener("keydown", (e) => {
    if (e.key !== "Enter") return;
    $("#search").value = e.currentTarget.value;
    showAllCountries = true; renderTree(); syncURL();
    $("#explorer").scrollIntoView();
  });
  // 현재 위치 탭 표시
  const tabs = $$(".tabs a");
  const io = new IntersectionObserver((ents) => {
    ents.forEach((en) => {
      if (!en.isIntersecting) return;
      tabs.forEach((a) => {
        const on = a.getAttribute("href") === "#" + en.target.id;
        a.setAttribute("aria-current", on ? "true" : "false");
        if (on && $(".tabs").scrollWidth > $(".tabs").clientWidth) $(".tabs").scrollTo({ left: a.offsetLeft - 24, behavior: "smooth" });
      });
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  $$("main section[id]").forEach((s) => io.observe(s));
}

/* ---------- 근거 집계 용지 ---------- */
function renderBallot() {
  const cnt = { verified: 0, documented: 0, monitoring: 0 };
  countries.forEach((c) => cnt[status(c)]++);
  $("#pulseNum").textContent = countries.length;
  $("#statusRows").innerHTML = ORDER.map((k, i) => `<li><button class="brow" type="button" data-status="${k}" aria-label="${statusName[k]} ${cnt[k]}개국 — 국가·프로그램 표에서 보기">
      <span class="no">기호<b>${i + 1}</b></span>
      <span class="lab">${statusName[k]}<small>${statusHelp[k]}</small></span>
      <span class="cnt">${cnt[k]}<small>개국</small></span>
      ${slot(k)}</button></li>`).join("");
  $$("#statusRows .brow").forEach((b) => (b.onclick = () => {
    b.classList.remove("pressing"); void b.offsetWidth; b.classList.add("pressing");
    $("#tracking").value = b.dataset.status; showAllCountries = true;
    renderTree(true); syncURL(); $("#explorer").scrollIntoView();
  }));
  const cut = Date.now() - 30 * 864e5;
  const n30 = news.filter((n) => Date.parse(n.published_at) >= cut).length;
  const act = countries.filter((c) => c.news_30d > 0).length;
  $("#signalSum").innerHTML = `최근 30일 신호 <b>${nf.format(n30)}</b>건 · <b>${act}</b>개국`;
  $("#ticker").innerHTML = news.slice(0, 5).map((x) => `<li><a href="${esc(x.url)}" target="_blank" rel="noopener"><span class="t">${esc(x.title_ko || x.title)}</span><span class="m">${esc(countryName(x.country_iso3))} · ${esc(x.source || "")} · ${esc(shortDate(x.published_at))}</span></a></li>`).join("") || `<li class="note">아직 들어온 신호가 없습니다.</li>`;
}

/* ---------- 지도 ---------- */
let evMap = null, evPopup = null;
const isDark = () => document.documentElement.classList.contains("dark");
const mapStyle = () => `https://basemaps.cartocdn.com/gl/${isDark() ? "dark-matter" : "positron"}-gl-style/style.json`;
function features() {
  const fc = [];
  countries.forEach((c) => {
    if (!c.coord) return;
    fc.push({ type: "Feature", geometry: { type: "Point", coordinates: [c.coord[1], c.coord[0]] },
      properties: { iso3: c.iso3, name: c.name_ko, status: status(c), label: statusName[status(c)], news30: c.news_30d || 0,
        programs: c.program_count || 0, latest: c.latest_news?.date || c.base_signal_date || "—", signal: c.latest_news?.title || c.base_signal || "" } });
  });
  return { type: "FeatureCollection", features: fc };
}
function stampImage(kind, css) {
  const sz = 44, c = document.createElement("canvas"); c.width = c.height = sz;
  const g = c.getContext("2d"), col = kind === "seal" ? css.seal : kind === "docu" ? css.ink : css.mut;
  g.lineCap = "round";
  if (kind === "mon") {
    g.setLineDash([3, 2.5]); g.strokeStyle = col; g.lineWidth = 1.6; g.fillStyle = css.paper; g.fillRect(11, 11, 22, 22); g.strokeRect(11, 11, 22, 22);
  } else {
    if (kind === "seal") { g.fillStyle = css.paper; g.beginPath(); g.arc(22, 22, 16, 0, 7); g.fill(); }
    else { g.fillStyle = css.paper; g.beginPath(); g.arc(22, 22, 15, 0, 7); g.fill(); }
    g.strokeStyle = col; g.lineWidth = kind === "seal" ? 3.6 : 2.6;
    g.beginPath(); g.arc(22, 22, kind === "seal" ? 15 : 13, 0, 7); g.stroke();
    g.lineWidth = kind === "seal" ? 3.8 : 2.8;
    g.beginPath(); g.moveTo(20.5, 12); g.lineTo(20.5, 32); g.moveTo(21.5, 20.5); g.lineTo(28, 24.5); g.stroke();
  }
  return g.getImageData(0, 0, sz, sz);
}
function addMapLayers() {
  const cs = getComputedStyle(document.documentElement), v = (n) => cs.getPropertyValue(n).trim();
  const css = { seal: v("--seal"), ink: v("--docu"), sig: v("--signal"), mut: v("--muted"), paper: v("--paper") };
  ["seal", "docu", "mon"].forEach((k) => { if (!evMap.hasImage("st-" + k)) evMap.addImage("st-" + k, stampImage(k, css), { pixelRatio: 2 }); });
  if (evMap.getSource("pb")) return;
  evMap.addSource("pb", { type: "geojson", data: features() });
  // 신호 층은 도장 층 아래에, 얇고 옅게 — 근거 표시를 덮지 않는다
  evMap.addLayer({ id: "pb-signal", type: "circle", source: "pb", filter: [">", ["get", "news30"], 0],
    paint: { "circle-radius": ["+", 13, ["min", 7, ["*", 0.25, ["get", "news30"]]]], "circle-color": "rgba(0,0,0,0)",
      "circle-stroke-width": 1.2, "circle-stroke-color": css.sig, "circle-stroke-opacity": 0.7 } });
  evMap.addLayer({ id: "pb-country", type: "symbol", source: "pb",
    layout: { "icon-image": ["match", ["get", "status"], "verified", "st-seal", "documented", "st-docu", "st-mon"],
      "icon-size": ["interpolate", ["linear"], ["zoom"], 0.5, ["match", ["get", "status"], "monitoring", 1, 1.2], 4, ["match", ["get", "status"], "monitoring", 1.3, 1.6]],
      "icon-allow-overlap": true, "icon-ignore-placement": true,
      "symbol-sort-key": ["match", ["get", "status"], "verified", 3, "documented", 2, 1], "icon-rotate": -6 } });
}
function renderMap() {
  if (!window.maplibregl) {
    $("#map2d").innerHTML = '<p class="empty">지도를 불러오지 못했습니다. 아래 국가·프로그램 표에서 같은 내용을 볼 수 있습니다.</p>';
    return;
  }
  evMap = new maplibregl.Map({ container: "map2d", style: mapStyle(), center: [10, 22], zoom: 0.9, minZoom: 0.5, maxZoom: 7,
    renderWorldCopies: false, attributionControl: { compact: true }, cooperativeGestures: matchMedia("(pointer:coarse)").matches });
  evMap.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
  evMap.getCanvas().setAttribute("aria-label", "근거 지도");
  evPopup = new maplibregl.Popup({ closeButton: false, closeOnClick: false, offset: 12 });
  evMap.on("load", () => evMap.fitBounds([[-165, -50], [178, 72]], { padding: 16, duration: 0 }));
  evMap.on("style.load", addMapLayers);
  evMap.on("mouseenter", "pb-country", () => (evMap.getCanvas().style.cursor = "pointer"));
  evMap.on("mousemove", "pb-country", (e) => {
    const p = e.features?.[0]?.properties; if (!p) return;
    evPopup.setLngLat(e.lngLat).setHTML(`<b>${esc(p.name)}</b><small>${esc(p.label)} · 프로그램 ${p.programs} · 30일 뉴스 ${p.news30}</small><div style="margin-top:6px">${esc(String(p.signal).slice(0, 120))}</div>`).addTo(evMap);
  });
  evMap.on("mouseleave", "pb-country", () => { evMap.getCanvas().style.cursor = ""; evPopup.remove(); });
  evMap.on("click", "pb-country", (e) => {
    const p = e.features?.[0]?.properties; if (!p) return;
    openCountry(p.iso3);
  });
}
function openCountry(iso) {
  ["#region", "#tracking", "#hasProgram"].forEach((s) => ($(s).value = "all"));
  $("#search").value = "";
  showAllCountries = true; renderTree();
  const d = $(`#tree details[data-iso="${CSS.escape(iso)}"]`);
  if (d) { d.open = true; syncURL(); d.scrollIntoView({ block: "start" }); $("summary", d).focus({ preventScroll: true }); }
}

/* ---------- PB 데일리 ---------- */
let newsLimit = 8;
const tok = (t) => new Set(String(t).toLowerCase().replace(/[^\p{L}\p{N}]+/gu, " ").split(" ").filter((w) => w.length > 2));
function groupNews(rows) {
  // 수집기가 붙인 story(언어와 무관한 같은 소식 묶음)를 쓰고, 없으면 제목 단어 겹침으로 묶는다
  const out = [], byStory = new Map();
  for (const n of rows) {
    if (n.story) {
      const g = byStory.get(n.story);
      if (g) { g.dups.push(n); continue; }
      const item = { ...n, dups: [] }; byStory.set(n.story, item); out.push(item); continue;
    }
    const tk = tok(n.title), t = Date.parse(n.published_at);
    const hit = out.find((g) => !g.story && g.lang === n.lang && g.country_iso3 === n.country_iso3 && Math.abs(g._t - t) < 4 * 864e5 && (() => {
      let inter = 0; tk.forEach((w) => g._tk.has(w) && inter++);
      return inter / Math.max(1, Math.min(tk.size, g._tk.size)) >= 0.5;
    })());
    if (hit) hit.dups.push(n);
    else out.push({ ...n, _tk: tk, _t: t, dups: [] });
  }
  return out;
}
function renderTopStories(rows) {
  const cut = Date.now() - 7 * 864e5, st = new Map();
  rows.forEach((n) => {
    if (!n.story || Date.parse(n.published_at) < cut) return;
    const g = st.get(n.story) || { items: [] }; g.items.push(n); st.set(n.story, g);
  });
  const top = [...st.values()].map((g) => {
    g.items.sort((a, b) => (b.published_at > a.published_at ? 1 : -1));
    g.src = [...new Set(g.items.map((x) => x.source))]; g.langs = [...new Set(g.items.map((x) => x.lang))];
    return g;
  }).filter((g) => g.src.length > 1).sort((a, b) => b.src.length - a.src.length || (b.items[0].published_at > a.items[0].published_at ? 1 : -1)).slice(0, 4);
  $("#topStories").hidden = !top.length;
  $("#topList").innerHTML = top.map((g) => {
    const x = g.items.find((i) => i.title_ko) || g.items[0];
    return `<li><b class="n" aria-label="매체 ${g.src.length}곳">${g.src.length}</b><div><a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(strip(x.title_ko || x.title))}</a>
      <p class="meta"><span class="cty">${esc(countryName(x.country_iso3))}</span><span>매체 ${g.src.length}곳 · 기사 ${g.items.length}건${g.langs.length > 1 ? ` · ${g.langs.map((l) => LANG_KO[l] || l).join("·")}` : ""}</span><span>${esc(shortDate(g.items[0].published_at))}</span></p>
      <p class="srcs">${g.src.slice(0, 5).map(esc).join(" · ")}${g.src.length > 5 ? " 등" : ""}</p></div></li>`;
  }).join("");
}
function setupNews() {
  const langs = {}; news.forEach((n) => (langs[n.lang] = (langs[n.lang] || 0) + 1));
  Object.entries(langs).sort((a, b) => b[1] - a[1]).forEach(([l, v]) => $("#newsLang").insertAdjacentHTML("beforeend", `<option value="${esc(l)}">${esc(LANG_KO[l] || l)} (${v})</option>`));
  const cs = {}; news.forEach((n) => n.country_iso3 && (cs[n.country_iso3] = (cs[n.country_iso3] || 0) + 1));
  const top = Object.entries(cs).sort((a, b) => b[1] - a[1]);
  top.forEach(([i, v]) => $("#newsCountry").insertAdjacentHTML("beforeend", `<option value="${esc(i)}">${esc(countryName(i))} (${v})</option>`));
  $("#newsQuick").innerHTML = top.slice(0, 8).map(([i, v]) => `<button type="button" data-iso="${esc(i)}" aria-pressed="false">${esc(countryName(i))}<span class="c">${v}</span></button>`).join("");
  $$("#newsQuick button").forEach((b) => (b.onclick = () => {
    $("#newsCountry").value = $("#newsCountry").value === b.dataset.iso ? "all" : b.dataset.iso;
    newsLimit = 8; renderNews(); syncURL();
  }));
  ["#newsKind", "#newsLang", "#newsCountry", "#newsGroup"].forEach((s) => ($(s).onchange = () => { newsLimit = 8; renderNews(); syncURL(); }));
  $("#newsSearch").oninput = () => { newsLimit = 8; renderNews(); syncURL(); };
  $("#moreNews").onclick = () => { newsLimit += 12; renderNews(); };
}
function renderNews() {
  const L = $("#newsLang").value, C = $("#newsCountry").value, q = $("#newsSearch").value.trim().toLowerCase();
  $$("#newsQuick button").forEach((b) => b.setAttribute("aria-pressed", b.dataset.iso === C));
  const K = $("#newsKind").value;
  let rows = news.filter((n) => (K === "all" || (n.kind || "signal") === K) && (L === "all" || n.lang === L) && (C === "all" || n.country_iso3 === C) &&
    (!q || (n.title + " " + (n.title_ko || "")).toLowerCase().includes(q)));
  const raw = rows.length;
  renderTopStories(rows);
  if ($("#newsGroup").checked) rows = groupNews(rows);
  $("#newsResult").textContent = rows.length === raw ? `기사 ${nf.format(raw)}건` : `기사 ${nf.format(raw)}건 · 같은 소식 묶어 ${nf.format(rows.length)}건`;
  $("#moreNews").hidden = rows.length <= newsLimit;
  if (!rows.length) {
    $("#newsgrid").innerHTML = `<li class="empty">조건에 맞는 기사가 없습니다. 언어나 국가를 '전체'로 바꾸거나 검색어를 줄여 보세요.</li>`;
    return;
  }
  let lastDay = "";
  $("#newsgrid").innerHTML = rows.slice(0, newsLimit).map((x) => {
    const thisYear = String(x.published_at).slice(0, 4) === String(new Date().getFullYear());
    const day = fmtDate(x.published_at, thisYear ? { month: "long", day: "numeric", weekday: "short" } : { year: "numeric", month: "long", day: "numeric", weekday: "short" });
    const head = day !== lastDay ? `<li class="dhead"><time datetime="${esc(String(x.published_at).slice(0, 10))}">${esc(day)}</time></li>` : "";
    lastDay = day;
    const ko = x.title_ko && x.title_ko !== x.title;
    const dup = x.dups?.length ? `<details class="dup"><summary>같은 소식 ${x.dups.length}건 더 · ${esc([...new Set(x.dups.map((d) => d.source))].slice(0, 3).join(", "))}${x.dups.length > 3 ? " 등" : ""}${svg("chev")}</summary><ul>${x.dups.map((d) => `<li><a href="${esc(d.url)}" target="_blank" rel="noopener">${esc(d.source)} · ${esc(shortDate(d.published_at))}</a></li>`).join("")}</ul></details>` : "";
    return `${head}<li><div>
      <h3><a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(strip(ko ? x.title_ko : x.title))}</a></h3>
      ${ko ? `<p class="orig" lang="${esc(x.lang)}">${esc(x.title)}</p>` : ""}
      ${x.kind === "org" && x.summary ? `<p class="orig" lang="en">${esc(strip(x.summary).slice(0, 160))}${x.summary.length > 160 ? "…" : ""}</p>` : ""}
      <p class="meta"><span class="sigtag">${x.kind === "org" ? "기관 소식" : "신호"}</span><span class="cty"${x.iso_basis ? ` title="국가 판정 근거: ${esc(x.iso_basis)}"` : ""}>${esc(countryName(x.country_iso3))}${x.iso_basis && x.iso_basis !== "제목" ? `<small> (${esc(x.iso_basis)})</small>` : ""}</span><span>${esc(LANG_KO[x.lang] || x.lang)}</span><span>${esc(x.source || "")}</span></p>${dup}</div></li>`;
  }).join("");
}

/* ---------- 논문 ---------- */
let paperLimit = 5;
function renderResearch() {
  const rows = papers.slice(0, paperLimit);
  $("#morePapers").hidden = papers.length <= paperLimit;
  $("#morePapers").onclick = () => { paperLimit += 10; renderResearch(); };
  if (!rows.length) { $("#researchGrid").innerHTML = '<li class="empty">아직 수집된 논문이 없습니다. 매일 오전 6시 17분 수집 뒤 채워집니다.</li>'; return; }
  $("#researchGrid").innerHTML = rows.map((r) => {
    const ko = r.title_ko && r.title_ko !== r.title;
    const abs = r.abstract_snippet ? `<p class="abs">${esc(r.abstract_snippet)}</p>` : "";
    return `<li><time datetime="${esc(r.published_at || "")}">${esc(fmtDate(r.published_at, { year: "numeric", month: "numeric", day: "numeric" }))}</time><div>
      <h3>${esc(strip(ko ? r.title_ko : r.title))}</h3>${ko ? `<p class="orig">${esc(strip(r.title))}</p>` : ""}
      <p class="by">${esc([(r.authors || []).join(", "), r.venue].filter(Boolean).join(" · ") || "저자·학술지 정보 없음")}</p>${abs}</div>
      <div class="act">${r.open_access ? '<span class="badge">오픈액세스</span>' : ""}<a href="${esc(r.url)}" target="_blank" rel="noopener">원문 ${svg("out")}</a>${r.doi ? `<span class="note">DOI ${esc(r.doi)}</span>` : ""}</div></li>`;
  }).join("");
}

/* ---------- 국가·프로그램 (투표용지 행) ---------- */
let showAllCountries = false;
function renderTree(press = false) {
  const region = $("#region").value, tracking = $("#tracking").value, has = $("#hasProgram").value, q = $("#search").value.trim().toLowerCase();
  const filtered = countries.filter((c) => {
    if (region !== "all" && c.region !== region) return false;
    if (tracking === "review" ? !c.review_hint : tracking !== "all" && status(c) !== tracking) return false;
    const ps = programs.filter((p) => p.country_iso3 === c.iso3);
    if (has === "with" && !ps.length) return false;
    if (has === "without" && ps.length) return false;
    if (q && ![c.name_ko, c.name_en, c.base_signal, ...(c.aliases || [])].join(" ").toLowerCase().includes(q) &&
      !ps.some((p) => [p.jurisdiction_name, p.program_name, programName(p)].join(" ").toLowerCase().includes(q))) return false;
    return true;
  }).sort((a, b) => ORDER.indexOf(status(a)) - ORDER.indexOf(status(b)) || (b.news_30d || 0) - (a.news_30d || 0) || a.name_ko.localeCompare(b.name_ko, "ko"));
  const nprog = filtered.reduce((a, c) => a + (c.program_count || 0), 0);
  $("#count").textContent = `${filtered.length}개국 · 프로그램 ${nprog}건`;
  const narrowed = region !== "all" || tracking !== "all" || has !== "all" || q;
  const shown = narrowed || showAllCountries ? filtered : filtered.slice(0, 30);
  const more = $("#moreCountries");
  more.hidden = shown.length === filtered.length;
  more.textContent = `나머지 ${filtered.length - shown.length}개국 더 보기`;
  more.onclick = () => { showAllCountries = true; renderTree(); };
  if (!filtered.length) {
    $("#tree").innerHTML = `<p class="empty">조건에 맞는 국가가 없습니다. 검색어를 지우거나 필터를 '전체'로 바꿔 보세요.</p>`;
    return;
  }
  $("#tree").innerHTML = shown.map((c, i) => {
    const ps = programs.filter((p) => p.country_iso3 === c.iso3).sort((a, b) => completeness(b) - completeness(a));
    const ln = c.latest_news;
    const marks = `<ul class="mark-list">
      <li>${svg("sq", "mk2")}<span><b>기준 근거</b> ${esc(c.base_signal || "—")}${c.primary_source ? ` · <a class="src" href="${esc(c.primary_source)}" target="_blank" rel="noopener">출처</a>` : ""}${c.base_signal_date ? ` <span class="note">(${esc(c.base_signal_date)})</span>` : ""}</span></li>
      ${ln ? `<li>${svg("ci", "mk2")}<span><b>최근 뉴스 신호</b> <a href="${esc(ln.url)}" target="_blank" rel="noopener">${esc(ln.title)}</a> <span class="note">${esc(ln.source)} · ${esc(ln.date)}</span></span></li>` : ""}
      <li>${svg("ci", "mk2")}<span><b>신호 집계</b> 최근 30일 기사 ${c.news_30d || 0}건 · 1년 ${c.news_365d || 0}건</span></li>
      ${registryLine(c)}</ul>`;
    return `<details class="crow" data-status="${status(c)}" data-iso="${c.iso3}">
      <summary><span class="no">${i + 1}</span>
        <span class="name"><b>${esc(c.name_ko)}</b><small>${esc(regionName(c.region))} · ${esc(c.name_en)}</small></span>
        <span class="facts"><span>프로그램 ${ps.length}</span>${c.review_hint ? '<span class="rv" title="레지스트리에 사례가 있어 근거 상태를 사람이 검토할 대상">검토 필요</span>' : ""}${c.news_30d ? `<span class="s">30일 신호 ${c.news_30d}</span>` : '<span class="note">신호 없음</span>'}</span>
        <span class="when">${c.activity_date ? "최근 " + esc(c.activity_date) : "—"}</span>
        ${slot(status(c))}</summary>
      <div class="cbody">${marks}${ps.length ? `<div class="progs">${ps.map(renderProgram).join("")}</div>` : `<p class="note">아직 프로그램 단위 근거가 없습니다. 원문 근거가 확인되면 프로그램 레지스트리(data/programs.seed.json)에 추가됩니다.</p>`}</div></details>`;
  }).join("");
  if (press) { const t = $("#tree"); t.classList.remove("pressing"); void t.offsetWidth; t.classList.add("pressing"); }
}
function renderProgram(p) {
  const f = fieldFlags(p), score = completeness(p);
  const part = p.participants?.count != null ? `${nf.format(p.participants.count)} ${esc(metricName(p.participants.metric))}` : "확인 중";
  const legal = p.legal_basis?.title ? esc(p.legal_basis.title) + (p.legal_basis.year ? ` (${p.legal_basis.year})` : "") : "확인 중";
  const seen = new Set();
  const rel = (p.related_news || []).filter((n) => !seen.has(n.title) && seen.add(n.title)).map((n) => `<a href="${esc(n.url)}" target="_blank" rel="noopener">${esc(n.date)} · ${esc(n.title)}</a>`).join("");
  return `<article class="prog"><header style="display:flex;justify-content:space-between;gap:12px"><div><h3>${esc(programName(p))}</h3><p class="sub">${esc(p.jurisdiction_name)} · ${esc(levelName(p.jurisdiction_level))} · ${esc(stageName(p.stage))}</p></div>${slot(p.tracking_status || "monitoring")}</header>
    <dl class="fields">
      <dt class="${f.예산 ? "on" : ""}">예산</dt><dd class="${f.예산 ? "" : "unk"}">${esc(p.budget?.display || "확인 중")}${p.budget?.source_url ? ` <a class="src" href="${esc(p.budget.source_url)}" target="_blank" rel="noopener">근거</a>` : ""}</dd>
      <dt class="${f.참여 ? "on" : ""}">참여</dt><dd class="${f.참여 ? "" : "unk"}">${part}</dd>
      <dt class="${f.단계 ? "on" : ""}">단계</dt><dd class="${f.단계 ? "" : "unk"}">${esc(stageName(p.stage))}</dd>
      <dt class="${f.법적근거 ? "on" : ""}">법적근거</dt><dd class="${f.법적근거 ? "" : "unk"}">${legal}</dd>
    </dl>
    <div class="complete" title="예산·참여·단계·법적근거 중 확인된 필드 비율"><span>근거 완성도</span><span class="track"><span class="fill" style="width:${score}%;display:block"></span></span><b>${score}%</b></div>
    ${officialBlock(p)}${pabuLine(p.pabulib)}
    ${p.cases?.length ? `<div class="relnews cases"><span class="note">Participedia 사례</span>${p.cases.map((x) => `<a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(x.title)}</a>`).join("")}</div>` : ""}
    ${rel ? `<div class="relnews"><span class="note">관련 신호</span>${rel}</div>` : ""}
    <footer><span>${esc(sourceName(p.source_type))}${p.last_verified ? " · " + esc(p.last_verified) + " 확인" : " · 확인일 미기재"}</span>${p.primary_url ? `<a href="${esc(p.primary_url)}" target="_blank" rel="noopener">출처 ${svg("out")}</a>` : ""}</footer></article>`;
}

/* ---------- 외부 레지스트리 근거 ---------- */
const money = (v, cur) => v == null ? "—" : cur === "EUR" ? `€${nf.format(v)}` : cur === "PLN" ? `${nf.format(v)} zł` : nf.format(v);
const CUR = { FIN: "EUR", NLD: "EUR", FRA: "EUR", POL: "PLN" };
function pabuLine(u) {
  if (!u) return "";
  const l = u.latest || {}, cur = CUR[u.iso3];
  const y = u.last_year_total;
  return `<p class="regline"><span class="note">Pabulib 투표 기록</span> ${esc(u.unit)} ${u.elections}회(${u.first_year}–${u.last_year}) · 누적 투표지 ${nf.format(u.votes)}${y ? ` · ${u.last_year}년 ${y.elections}개 투표 예산 합계 ${esc(money(y.budget, cur))}, 후보 사업 ${nf.format(y.projects)}건` : ""} <a class="src" href="https://pabulib.org/" target="_blank" rel="noopener">출처</a></p>`;
}
function officialBlock(p) {
  const o = p.official_api;
  if (!o?.cycles?.length) return "";
  const cur = CUR[p.country_iso3];
  const hasNum = o.cycles.some((c) => c.budget_total != null);
  const rows = o.cycles.slice(0, 5).map((c) => `<tr><th scope="row"><a href="${esc(c.url)}" target="_blank" rel="noopener">${esc(c.title || c.slug)}</a></th><td>${esc(String(c.start || "").slice(0, 7))}</td>${hasNum ? `<td>${esc(money(c.budget_total, cur))}</td><td>${c.projects != null ? nf.format(c.projects) : "—"}</td><td>${c.selected != null ? nf.format(c.selected) : "—"}</td>` : ""}</tr>`).join("");
  return `<div class="official"><p class="note">공식 플랫폼 API(${esc(o.platform)}) · ${esc(fmtDate(o.checked_at))} 조회</p>
    <table class="ctable"><thead><tr><th scope="col">회차</th><th scope="col">시작</th>${hasNum ? '<th scope="col">예산</th><th scope="col">제안</th><th scope="col">선정</th>' : ""}</tr></thead><tbody>${rows}</tbody></table></div>`;
}
function registryLine(c) {
  const r = c.registry;
  if (!r || (!r.participedia && !r.pabulib)) return "";
  const cs = cases.filter((x) => x.iso3 === c.iso3).slice(0, 3);
  const us = units.filter((u) => u.iso3 === c.iso3).slice(0, 4);
  const links = cs.map((x) => `<a class="src" href="${esc(x.url)}" target="_blank" rel="noopener">${esc(x.title)}</a>`).join(" · ");
  const pabu = us.length ? ` · Pabulib 투표 기록 ${nf.format(r.pabulib)}회(${us.map((u) => esc(u.unit)).join(", ")}${c.registry.pabulib_units > us.length ? " 등" : ""})` : "";
  const more = r.participedia > cs.length ? ` <a class="src" href="https://participedia.net/search?selectedCategory=case&query=participatory%20budgeting%20${encodeURIComponent(c.name_en)}" target="_blank" rel="noopener">사례 ${r.participedia}건 모두 보기</a>` : "";
  return `<li>${svg("sq", "mk2")}<span><b>플랫폼 근거</b> Participedia 사례 ${r.participedia}건${r.participedia_verified ? `(검수 ${r.participedia_verified})` : ""}${pabu}${links ? `<br>${links}` : ""}${more}${c.review_hint ? `<br><span class="note">모니터링 국가에서 레지스트리 근거가 보여 검토 대상으로 표시했습니다. 상태는 자동으로 바뀌지 않습니다.</span>` : ""}</span></li>`;
}

/* ---------- 역사 연표 ---------- */
const firstYear = (y) => { const m = String(y).match(/\d{4}/); return m ? Math.max(1978, +m[0]) : 1978; };
const tlId = (i, n) => `tl-${n}-${firstYear(i.year)}`;
const fmtN = (v) => nf.format(v);
function renderStrip(items) {
  const W = 1200, H = 150, L = 16, R = 16, y0 = 1975, y1 = 2027;
  const x = (y) => L + ((y - y0) / (y1 - y0)) * (W - L - R);
  const ko = $("#koOnly").checked;
  const bands = TL.eras.map((e, k) => {
    const ys = TL.items.filter((i) => i.era === e.id).map((i) => firstYear(i.year));
    const a = k === 0 ? y0 : Math.min(...ys), b = k === TL.eras.length - 1 ? y1 : Math.min(...TL.items.filter((i) => i.era === TL.eras[k + 1].id).map((i) => firstYear(i.year)));
    return { e, a, b };
  });
  const stack = {};
  const ticks = TL.items.map((it, n) => {
    const yr = firstYear(it.year), lvl = (stack[yr] = (stack[yr] || 0) + 1) - 1, cx = x(yr) + lvl * 7, cy = 100 - lvl * 12;
    const kr = it.iso3 === "KOR", dim = ko && !kr;
    const mark = kr ? `<rect class="kr" x="${cx - 5}" y="${cy - 5}" width="10" height="10"/>` : `<circle cx="${cx}" cy="${cy}" r="5"/>`;
    return `<a href="#${tlId(it, n)}" class="tick${dim ? " dim" : ""}" aria-label="${esc(it.year)} ${esc(it.title)}"><rect class="hit" x="${cx - 9}" y="${cy - 9}" width="18" height="18"/><line x1="${cx}" x2="${cx}" y1="${cy + 5}" y2="118"/>${mark}<title>${esc(it.year)} · ${esc(it.title)}</title></a>`;
  }).join("");
  const axis = [];
  for (let y = 1980; y <= 2020; y += 10) axis.push(`<line x1="${x(y)}" x2="${x(y)}" y1="118" y2="124"/><text x="${x(y)}" y="140" text-anchor="middle">${y}</text>`);
  $("#tlStrip").innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="group" aria-label="참여예산 연표: 1975년부터 지금까지 ${TL.items.length}개 사건. 표시를 누르면 해당 항목으로 이동합니다.">
    ${bands.map(({ e, a, b }, k) => `<a href="#era-${esc(e.id)}" aria-label="${esc(e.label)} ${esc(e.span)}"><rect class="band${k % 2 ? " alt" : ""}" x="${x(a)}" y="0" width="${x(b) - x(a)}" height="118"/><text class="band-label" x="${x(a) + 8}" y="22">${esc(e.label)}</text><text class="band-span" x="${x(a) + 8}" y="38">${esc(e.span)}</text></a>${k ? `<line class="rule" x1="${x(a)}" x2="${x(a)}" y1="0" y2="118"/>` : ""}`).join("")}
    <line class="rule" x1="${L}" x2="${W - R}" y1="118" y2="118"/>
    <g class="axis">${axis.join("")}</g>${ticks}</svg>`;
  $("#tlCount").textContent = ko ? `한국 ${items.length}건 / 전체 ${TL.items.length}건` : `${TL.items.length}건 · 원문 근거 포함`;
}
function vizPOA() {
  const D = TL.data?.poa; if (!D) return "";
  const W = 640, H = 230, L = 52, R = 96, T = 14, B = 28, ys = D.years, v = D.series["포르투알레그리"];
  const x = (k) => L + (k / (ys.length - 1)) * (W - L - R), max = 30000, y = (n) => T + (1 - n / max) * (H - T - B);
  const grid = [0, 10000, 20000, 30000].map((g) => `<line x1="${L}" x2="${W - R}" y1="${y(g)}" y2="${y(g)}"/><text x="${L - 8}" y="${y(g) + 4}" text-anchor="end">${g ? g / 10000 + "만" : "0"}</text>`).join("");
  const xa = ys.map((yr, k) => (k % 2 === 0 || k === ys.length - 1) ? `<text x="${x(k)}" y="${H - 8}" text-anchor="middle">${yr}</text>` : "").join("");
  const d = v.map((n, k) => `${k ? "L" : "M"}${x(k).toFixed(1)},${y(n).toFixed(1)}`).join("");
  const last = v.length - 1;
  const rows = ys.map((yr, k) => `<tr><td>${yr}</td>${Object.values(D.series).map((s) => `<td>${s[k] == null ? "—" : fmtN(s[k])}</td>`).join("")}</tr>`).join("");
  return `<figure class="tlviz" data-viz="poa"><figcaption>포르투알레그리 참여예산 참여자 수, 1990–2003 (명)</figcaption>
    <div class="chartwrap"><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="포르투알레그리 참여자 수가 1990년 976명에서 2002년 2만 8,549명으로 늘었다. 자세한 값은 아래 표에 있다.">
      <g class="grid">${grid}</g><g class="xaxis">${xa}</g>
      <path class="line" d="${d}"/>${v.map((n, k) => `<circle class="pt" cx="${x(k)}" cy="${y(n)}" r="4"/>`).join("")}
      <text class="lbl" x="${x(12) + 8}" y="${y(v[12]) - 8}">2002년 ${fmtN(v[12])}명</text>
      <line class="cross" x1="0" x2="0" y1="${T}" y2="${H - B}" hidden/><rect class="hover" x="${L}" y="${T}" width="${W - L - R}" height="${H - T - B}" fill="transparent"/>
    </svg><div class="tip" hidden></div></div>
    <details><summary>표로 보기 — 브라질 5개 도시 비교</summary><table><thead><tr><th scope="col">연도</th>${Object.keys(D.series).map((k) => `<th scope="col">${esc(k)}</th>`).join("")}</tr></thead><tbody>${rows}</tbody></table><p class="srcline">—: 해당 연도 운영 안 함 또는 자료 없음. 출처: ${esc(D.source)}</p></details></figure>`;
}
function bindPOA(fig) {
  const D = TL.data.poa, v = D.series["포르투알레그리"], svgEl = $("svg", fig), tip = $(".tip", fig), cross = $(".cross", fig), hov = $(".hover", fig);
  const W = 640, L = 52, R = 96;
  hov.addEventListener("pointermove", (ev) => {
    const pt = svgEl.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY;
    const p = pt.matrixTransform(svgEl.getScreenCTM().inverse());
    const k = Math.max(0, Math.min(v.length - 1, Math.round(((p.x - L) / (W - L - R)) * (v.length - 1))));
    const cx = L + (k / (v.length - 1)) * (W - L - R);
    cross.setAttribute("x1", cx); cross.setAttribute("x2", cx); cross.hidden = false;
    const r = svgEl.getBoundingClientRect(), sc = r.width / W;
    tip.style.left = cx * sc + "px"; tip.style.top = (14 + (1 - v[k] / 30000) * (230 - 42)) * sc - 8 + "px"; tip.hidden = false;
    tip.textContent = `${D.years[k]}년 · ${fmtN(v[k])}명`;
  });
  hov.addEventListener("pointerleave", () => { tip.hidden = true; cross.hidden = true; });
}
function vizPercap() {
  const D = TL.data?.percap; if (!D) return "";
  const max = Math.max(...D.rows.map((r) => r[1]));
  return `<figure class="tlviz"><figcaption>${esc(D.title)}</figcaption>${D.rows.map(([k, v]) => `<div class="hbar"><span>${esc(k)}</span><span class="t"><span class="f" style="width:${(v / max) * 100}%"></span></span><b>${v}달러</b></div>`).join("")}<p class="srcline">출처: ${esc(D.source)}</p></figure>`;
}
function vizBrArc() {
  const D = TL.data?.brarc; if (!D) return "";
  const W = 640, H = 240, L = 40, R = 8, T = 22, B = 30, n = D.terms.length, max = 150;
  const bw = (W - L - R) / n, w = Math.min(44, bw - 14), y = (v) => T + (1 - v / max) * (H - T - B);
  const grid = [0, 50, 100, 150].map((g) => `<line x1="${L}" x2="${W - R}" y1="${y(g)}" y2="${y(g)}"/><text x="${L - 8}" y="${y(g) + 4}" text-anchor="end">${g}</text>`).join("");
  const cols = D.terms.map((t, k) => {
    const cx = L + bw * k + bw / 2, x0 = cx - w / 2, tot = D.total[k], pt = D.pt[k], oth = tot - pt;
    const yPt = y(pt), yTop = y(tot);
    return `<g class="col"><title>${esc(t)} · 전체 ${tot}곳 (노동자당 ${pt} · 다른 정당 ${oth})</title>
      <rect class="hit" x="${cx - bw / 2}" y="${T}" width="${bw}" height="${H - T - B}"/>
      ${pt ? `<rect class="seg-pt" x="${x0}" y="${yPt}" width="${w}" height="${y(0) - yPt}"/>` : ""}
      ${oth ? `<rect class="seg-oth" x="${x0 + 0.75}" y="${yTop + 0.75}" width="${w - 1.5}" height="${Math.max(0, yPt - yTop - 2.5)}"/>` : ""}
      <text class="lbl" x="${cx}" y="${yTop - 6}" text-anchor="middle">${tot}</text>
      <text class="xt" x="${cx}" y="${H - 10}" text-anchor="middle">${esc(t)}</text></g>`;
  }).join("");
  const rows = D.terms.map((t, k) => `<tr><td>${esc(t)}</td><td>${D.total[k]}</td><td>${D.pt[k]}</td><td>${Math.round((D.pt[k] / D.total[k]) * 100)}%</td></tr>`).join("");
  return `<figure class="tlviz brarc"><figcaption>${esc(D.title)} (곳)</figcaption>
    <ul class="legend"><li><span class="sw pt" aria-hidden="true"></span>노동자당 시정부</li><li><span class="sw oth" aria-hidden="true"></span>다른 정당 시정부</li></ul>
    <div class="chartwrap"><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="브라질 참여예산 운영 도시 수는 1989–92년 12곳에서 2001–04년 138곳으로 정점을 찍은 뒤 2017–20년 43곳으로 줄었다. 노동자당 시정부 몫은 55곳에서 3곳으로 줄었다. 자세한 값은 아래 표에 있다.">
      <g class="grid">${grid}</g>${cols}</svg></div>
    <details><summary>표로 보기</summary><table><thead><tr><th scope="col">임기</th><th scope="col">전체</th><th scope="col">노동자당</th><th scope="col">노동자당 비중</th></tr></thead><tbody>${rows}</tbody></table><p class="srcline">출처: ${esc(D.source)}</p></details></figure>`;
}
function renderHistory() {
  const ko = $("#koOnly").checked;
  const items = TL.items.map((it, n) => ({ it, n })).filter(({ it }) => !ko || it.iso3 === "KOR");
  renderStrip(items);
  $("#timeline").innerHTML = TL.eras.map((e) => {
    const its = items.filter(({ it }) => it.era === e.id);
    if (!its.length) return "";
    return `<section class="era" id="era-${esc(e.id)}" aria-labelledby="era-h-${esc(e.id)}"><header><h3 id="era-h-${esc(e.id)}">${esc(e.label)}<span class="span">${esc(e.span)}</span></h3><p>${esc(e.summary)}</p></header>
      <ol class="tl">${its.map(({ it: i, n }) => `<li id="${tlId(i, n)}" class="${i.iso3 === "KOR" ? "kor" : ""}"><div class="yr">${esc(i.year)}${i.iso3 === "KOR" ? '<br><span class="kr">한국</span>' : `<small>${i.iso3 ? esc(countryName(i.iso3)) : "국제"}</small>`}</div>
        <div><h4>${esc(i.title)}</h4><p class="body">${esc(i.body)}</p>${i.viz === "poa" ? vizPOA() : i.viz === "percap" ? vizPercap() : i.viz === "brarc" ? vizBrArc() : ""}</div>
        <div class="src"><b>근거</b>${(i.sources || []).map((s) => `<a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.label)}</a>`).join("")}</div></li>`).join("")}</ol></section>`;
  }).join("") || '<p class="empty">연표 자료를 불러오지 못했습니다.</p>';
  const f = $('#timeline [data-viz="poa"]'); if (f) bindPOA(f);
  updateHistMap();
}


/* 역사 지도 */
let histMap = null, histEra = "all";
function histGeo() {
  const ko = $("#koOnly").checked, origin = [-51.22, -30.03];
  const groups = {};
  TL.items.forEach((it, n) => {
    if (!it.coord) return;
    const k = it.coord.join(",");
    (groups[k] ??= { coord: it.coord, place: it.place, list: [] }).list.push({ it, n });
  });
  const pts = [], lines = [];
  Object.values(groups).forEach((g) => {
    const vis = g.list.filter(({ it }) => (histEra === "all" || it.era === histEra) && (!ko || it.iso3 === "KOR"));
    const first = g.list[0];
    pts.push({ type: "Feature", geometry: { type: "Point", coordinates: [g.coord[1], g.coord[0]] },
      properties: { place: g.place, count: g.list.length, on: vis.length ? 1 : 0, kr: first.it.iso3 === "KOR" ? 1 : 0,
        target: tlId((vis[0] || first).it, (vis[0] || first).n),
        html: g.list.map(({ it }) => `<div${(histEra === "all" || it.era === histEra) && (!ko || it.iso3 === "KOR") ? "" : ' style="opacity:.55"'}><b style="display:inline">${esc(it.year)}</b> ${esc(it.title)}</div>`).join("") } });
    if (vis.length && g.place !== "포르투알레그리") lines.push({ type: "Feature", geometry: { type: "LineString", coordinates: [origin, [g.coord[1], g.coord[0]]] }, properties: {} });
  });
  return { pts: { type: "FeatureCollection", features: pts }, lines: { type: "FeatureCollection", features: lines } };
}
function addHistLayers() {
  const cs = getComputedStyle(document.documentElement), v = (n) => cs.getPropertyValue(n).trim();
  if (histMap.getSource("hp")) return;
  const g = histGeo();
  histMap.addSource("hl", { type: "geojson", data: g.lines });
  histMap.addSource("hp", { type: "geojson", data: g.pts });
  histMap.addLayer({ id: "hl", type: "line", source: "hl", paint: { "line-color": v("--ink"), "line-width": 1, "line-opacity": 0.35 } });
  histMap.addLayer({ id: "hp", type: "circle", source: "hp", paint: {
    "circle-radius": ["+", 5, ["*", 2.2, ["get", "count"]]],
    "circle-color": ["case", ["==", ["get", "on"], 1], v("--ink"), v("--paper")],
    "circle-opacity": ["case", ["==", ["get", "on"], 1], 0.9, 1],
    "circle-stroke-width": 2, "circle-stroke-color": ["case", ["==", ["get", "on"], 1], v("--paper"), v("--muted")] } });
}
function updateHistMap() {
  if (!histMap || !histMap.getSource("hp")) return;
  const g = histGeo();
  histMap.getSource("hp").setData(g.pts); histMap.getSource("hl").setData(g.lines);
}
function renderHistMap() {
  const eras = [{ id: "all", label: "전체" }, ...TL.eras];
  $("#tlEraSeg").innerHTML = eras.map((e) => `<button type="button" data-era="${esc(e.id)}" aria-pressed="${e.id === histEra}">${esc(e.label)}</button>`).join("");
  $$("#tlEraSeg button").forEach((b) => (b.onclick = () => { histEra = b.dataset.era; $$("#tlEraSeg button").forEach((x) => x.setAttribute("aria-pressed", x === b)); updateHistMap(); }));
  if (!window.maplibregl) { $("#tlMap").innerHTML = '<p class="empty">지도를 불러오지 못했습니다. 아래 연표에 같은 내용이 있습니다.</p>'; return; }
  histMap = new maplibregl.Map({ container: "tlMap", style: mapStyle(), center: [10, 20], zoom: 0.8, minZoom: 0.5, maxZoom: 6, renderWorldCopies: false,
    attributionControl: { compact: true }, cooperativeGestures: matchMedia("(pointer:coarse)").matches });
  histMap.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");
  histMap.getCanvas().setAttribute("aria-label", "참여예산 역사 지도");
  histMap.on("load", () => histMap.fitBounds([[-110, -40], [140, 62]], { padding: 20, duration: 0 }));
  histMap.on("style.load", addHistLayers);
  const pop = new maplibregl.Popup({ closeButton: false, closeOnClick: false, offset: 12, maxWidth: "320px" });
  histMap.on("mouseenter", "hp", () => (histMap.getCanvas().style.cursor = "pointer"));
  histMap.on("mousemove", "hp", (e) => { const p = e.features?.[0]?.properties; if (p) pop.setLngLat(e.lngLat).setHTML(`<b>${esc(p.place)}</b><div style="margin-top:4px;display:grid;gap:3px">${p.html}</div>`).addTo(histMap); });
  histMap.on("mouseleave", "hp", () => { histMap.getCanvas().style.cursor = ""; pop.remove(); });
  histMap.on("click", "hp", (e) => { const p = e.features?.[0]?.properties; if (!p) return; const el = document.getElementById(p.target); if (el) { if ($("#koOnly").checked && !el) return; el.scrollIntoView({ block: "start" }); location.hash = p.target; } });
}

/* ---------- 분석 ---------- */
function renderAnalytics() {
  const groups = [];
  const b = { "75–100%": 0, "50%": 0, "25%": 0, "0%": 0 };
  programs.forEach((p) => { const s = completeness(p); b[s >= 75 ? "75–100%" : s >= 50 ? "50%" : s >= 25 ? "25%" : "0%"]++; });
  groups.push(["근거 완성도 (프로그램 수)", Object.entries(b)]);
  const g = { 예산: 0, 참여자: 0, 진행단계: 0, 법적근거: 0 };
  programs.forEach((p) => { const f = fieldFlags(p); if (!f.예산) g.예산++; if (!f.참여) g.참여자++; if (!f.단계) g.진행단계++; if (!f.법적근거) g.법적근거++; });
  groups.push(["검증 빈칸 (“확인 중”인 프로그램 수)", Object.entries(g)]);
  const st = {}; programs.forEach((p) => (st[p.stage || "unknown"] = (st[p.stage || "unknown"] || 0) + 1));
  groups.push(["진행 단계", Object.entries(st).sort((a, b) => b[1] - a[1]).slice(0, 6).map(([k, v]) => [stageName(k), v])]);
  const lv = {}; programs.forEach((p) => (lv[p.jurisdiction_level || "other"] = (lv[p.jurisdiction_level || "other"] || 0) + 1));
  groups.push(["관할 단위", Object.entries(lv).sort((a, b) => b[1] - a[1]).slice(0, 6).map(([k, v]) => [levelName(k), v])]);
  const rc = {}, ra = {};
  countries.forEach((c) => { rc[c.region] = (rc[c.region] || 0) + 1; if (status(c) !== "monitoring") ra[c.region] = (ra[c.region] || 0) + 1; });
  groups.push(["지역별 근거 확보 (공식·문헌 / 추적 국가)", Object.entries(rc).sort((a, b) => (ra[b[0]] || 0) - (ra[a[0]] || 0)).map(([r, v]) => [regionName(r), ra[r] || 0, v])]);
  const cap = $("#tally caption").outerHTML;
  $("#tally").innerHTML = cap + groups.map(([title, rows]) => {
    const max = Math.max(1, ...rows.map((r) => r[2] || r[1]));
    return `<tbody><tr><th scope="rowgroup" colspan="3">${esc(title)}</th></tr>${rows.map(([k, v, of]) => `<tr><td>${esc(k)}</td><td><span class="t"><span class="f" style="width:${(v / (of || max)) * 100}%"></span></span></td><td class="v">${v}${of ? `<span class="note">/${of}</span>` : ""}</td></tr>`).join("")}</tbody>`;
  }).join("");
  const sel = $("#region");
  Object.keys(rc).sort().forEach((r) => sel.insertAdjacentHTML("beforeend", `<option value="${esc(r)}">${esc(regionName(r))}</option>`));
  renderTrend();
  renderCompare();
}
function renderTrend() {
  const el = $("#trend"), H = snaps.slice(-120);
  if (H.length < 2) {
    el.hidden = true;
    $("#trendNote").textContent = H.length ? `관측 추이: 오늘 30일 뉴스 ${H[0].news_30d}건 · 신호 국가 ${H[0].countries_with_signal_30d}개 · 누적 논문 ${H[0].papers_total}편. 일별 추이 그래프는 갱신이 이틀 이상 쌓이면 나타납니다.` : "";
    return;
  }
  el.hidden = false;
  const W = 1000, Ht = 170, pl = 8, pr = 210, pt = 12, pb = 26;
  const css = getComputedStyle(document.documentElement);
  const S = [["news_30d", "30일 뉴스", css.getPropertyValue("--signal")], ["countries_with_signal_30d", "신호 국가", css.getPropertyValue("--ink")], ["papers_total", "누적 논문", css.getPropertyValue("--muted")]];
  const x = (i) => pl + (i / (H.length - 1)) * (W - pl - pr);
  const lines = S.map(([k, name, col], si) => {
    const v = H.map((h) => h[k] || 0), mx = Math.max(1, ...v);
    const y = (n) => pt + (1 - n / mx) * (Ht - pt - pb);
    const d = v.map((n, i) => `${i ? "L" : "M"}${x(i).toFixed(1)},${y(n).toFixed(1)}`).join("");
    return `<path d="${d}" fill="none" stroke="${col}" stroke-width="${si ? 1.5 : 2.5}"/><circle cx="${x(v.length - 1)}" cy="${y(v.at(-1))}" r="3.5" fill="${col}"/><text x="${W - pr + 14}" y="${pt + 18 + si * 22}" font-size="13" fill="${col}">${name} ${nf.format(v.at(-1))}</text>`;
  }).join("");
  el.innerHTML = `<svg viewBox="0 0 ${W} ${Ht}" width="100%" height="100%" role="img" aria-label="일별 관측 추이">${lines}<line x1="${pl}" x2="${W - pr}" y1="${Ht - pb}" y2="${Ht - pb}" stroke="var(--hair)"/><text x="${pl}" y="${Ht - 6}" font-size="12" fill="var(--muted)">${H[0].date}</text><text x="${W - pr}" y="${Ht - 6}" font-size="12" text-anchor="end" fill="var(--muted)">${H.at(-1).date}</text></svg>`;
  $("#trendNote").textContent = "선마다 자기 최댓값을 기준으로 그렸습니다. 오른쪽 숫자가 오늘 값입니다.";
}
function renderCompare() {
  const rows = [...programs].sort((a, b) => completeness(b) - completeness(a));
  const u = (v) => (known(v) ? esc(v) : `<span class="unk">확인 중</span>`);
  $("#compare").innerHTML = rows.map((p) => `<tr><td><b>${esc(countryName(p.country_iso3))}</b><br><span class="note">${esc(p.jurisdiction_name || "")}</span></td><td>${esc(programName(p))}</td><td class="num">${completeness(p)}%</td><td>${u(p.budget?.display)}</td><td>${p.participants?.count != null ? nf.format(p.participants.count) + " " + esc(metricName(p.participants.metric)) : '<span class="unk">확인 중</span>'}</td><td>${esc(stageName(p.stage))}</td><td>${u(p.legal_basis?.title)}</td><td>${p.primary_url ? `<a class="src" href="${esc(p.primary_url)}" target="_blank" rel="noopener">원문</a>` : "—"}</td></tr>`).join("");
}

/* ---------- 근거·출처 ---------- */
function renderEvidence() {
  const hs = ["news", "orgs", "gdelt", "papers", "participedia", "pabulib", "decidim", "build"].map((k) => health[k]).filter(Boolean);
  $("#health").innerHTML = hs.length ? hs.map((x) => {
    const detail = x.added != null ? `검색어 ${x.queries_ok}/${x.queries} 성공 · 오늘 새 기사 ${x.added}${x.gdelt_added ? ` (GDELT ${x.gdelt_added})` : ""} · 보관 ${nf.format(x.total)}` : x.queries != null ? `검색어 ${x.queries_ok}/${x.queries} 성공 · 새 기사 ${x.fetched}${x.timespan_days ? ` · 최근 ${x.timespan_days}일 범위` : ""}${x.fails_in_row > 1 ? ` · ${x.fails_in_row}일 연속 실패` : ""}` : x.fetched != null ? `오늘 수집 ${x.fetched} · 보관 ${nf.format(x.total)}` : "";
    return `<div class="hrow"><span class="st ${x.ok ? "" : "bad"}" aria-hidden="true"></span><b>${esc(x.name)} — ${x.ok ? "정상" : "실패"}</b><p>${esc(fmtDate(x.checked_at, { month: "numeric", day: "numeric", hour: "numeric", minute: "2-digit" }))}${detail ? " · " + esc(detail) : ""}${!x.ok && x.last_success_at ? " · 마지막 성공 " + esc(fmtDate(x.last_success_at)) : ""}</p></div>`;
  }).join("") : '<p class="note">수집 상태 정보가 아직 없습니다.</p>';
  const SRC = [
    ["Google News RSS", "https://news.google.com/", "27개 검색어·24개 언어 기사 제목", "PB 데일리, 국가 신호", "news"],
    ["참여예산 기관 피드 6곳", "https://www.participatorybudgeting.org/", "PBP·PB Scotland 전체 글, newDemocracy·Decidim·CONSUL·OGP의 참여예산 글", "PB 데일리 '기관 소식'", "orgs"],
    ["GDELT DOC 2.0", "https://www.gdeltproject.org/", "원문 직링크·발행국·언어 (하루 1회 요청)", "PB 데일리 보강, 국가 판정(발행국)", "gdelt"],
    ["OpenAlex · Crossref", "https://openalex.org/", "논문 서지·초록·DOI", "논문", "papers"],
    ["Participedia", "https://participedia.net/", `PB 사례 ${nf.format(cases.length)}건(좌표·검수 여부)`, "국가·프로그램 '플랫폼 근거', 검토 필요 표시", "participedia"],
    ["Pabulib (pabuviz)", "https://pabulib.org/", `투표 기록 ${nf.format(units.reduce((a, u) => a + u.elections, 0))}회(예산·사업·투표 수)`, "폴란드·네덜란드·프랑스 도시 근거", "pabulib"],
    ["Decidim GraphQL", "https://docs.decidim.org/en/develop/develop/api/", "회차별 예산·제안·선정 사업", "헬싱키 OmaStadi, 뉴욕 The People's Money 공식 수치", "decidim"],
  ];
  $("#srcRows").innerHTML = SRC.map(([n, u, what, where, k]) => { const h = health[k]; return `<tr><th scope="row"><a class="src" href="${u}" target="_blank" rel="noopener">${esc(n)}</a></th><td>${esc(what)}</td><td>${esc(where)}</td><td>${h ? (h.ok ? "정상" : "실패") + " · " + esc(fmtDate(h.checked_at, { month: "numeric", day: "numeric" })) : "첫 수집 대기"}</td></tr>`; }).join("");
  $("#ledger").innerHTML = ledger.slice(0, 12).map((o) => `<li><a href="${esc(o.url)}" target="_blank" rel="noopener">${esc(strip(o.text).slice(0, 110))}</a><span class="m">${esc(o.type)} · ${esc(o.label)} · 관측 ${esc(o.observed_at || "—")} · 기록 ${esc(o.date)}</span></li>`).join("") || '<li class="note">원장 기록이 아직 없습니다.</li>';
}

/* ---------- 주소 상태 ---------- */
const URL_KEYS = { region: "#region", status: "#tracking", program: "#hasProgram", q: "#search", nkind: "#newsKind", nlang: "#newsLang", ncountry: "#newsCountry", nq: "#newsSearch" };
function syncURL() {
  const u = new URLSearchParams();
  for (const [k, sel] of Object.entries(URL_KEYS)) { const v = $(sel).value.trim(); if (v && v !== "all") u.set(k, v); }
  if (!$("#newsGroup").checked) u.set("group", "0");
  const open = $$("#tree details[open]").map((d) => d.dataset.iso);
  if (open.length === 1) u.set("c", open[0]);
  const qs = u.toString();
  history.replaceState(null, "", location.pathname + (qs ? "?" + qs : "") + location.hash);
}
function restoreURL() {
  const u = new URLSearchParams(location.search);
  for (const [k, sel] of Object.entries(URL_KEYS)) if (u.has(k)) $(sel).value = u.get(k);
  if (u.get("group") === "0") $("#newsGroup").checked = false;
  return u.get("c");
}
function bind() {
  ["#region", "#tracking", "#hasProgram"].forEach((s) => ($(s).onchange = () => { renderTree(s === "#tracking"); syncURL(); }));
  $("#search").oninput = () => { renderTree(); syncURL(); };
  $("#tree").addEventListener("toggle", (e) => { if (e.target.matches("details.crow")) syncURL(); }, true);
  $("#openVerified").onclick = () => {
    if ($("#tracking").value === "monitoring") { $("#tracking").value = "all"; renderTree(); }
    $$("#tree details").forEach((d) => (d.open = d.dataset.status === "verified"));
    syncURL();
  };
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
  setupShell(); bind(); setupNews();
  renderAnalytics();
  const openIso = restoreURL();
  renderBallot(); renderMap(); renderNews(); renderResearch(); renderTree(); renderHistory(); renderHistMap(); renderEvidence();
  $("#koOnly").onchange = renderHistory;
  if (openIso && byISO[openIso]) openCountry(openIso);
})();
