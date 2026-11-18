#!/usr/bin/env python3
"""세계 참여예산 관측소 — 일일 자동 수집기.

GitHub Actions가 매일 실행합니다. 외부 패키지 없이 표준 라이브러리만 씁니다.

수집 대상
  1) 뉴스 신호  : Google News RSS, 21개 언어 검색어
  2) 연구 논문  : OpenAlex (실패 시 Crossref)
  3) 국가 신호  : 뉴스 제목을 국가 별칭과 대조해 국가별 최신 신호·30일 건수 산출
  4) 근거 원장  : 새로 관측된 국가 신호·논문을 날짜와 함께 누적
  5) 출처 상태  : 소스별 성공/실패, 건수, 시각

원칙: 뉴스 신호는 국가의 근거 상태(verified/documented/monitoring)를 자동으로 올리지 않습니다.
"""
from __future__ import annotations

import email.utils
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NOW = datetime.now(timezone.utc)
TODAY = NOW.date().isoformat()
UA = "Mozilla/5.0 (compatible; PB-Observatory/4.0; +https://github.com)"
MAILTO = os.environ.get("OPENALEX_MAILTO", "pb-observatory@example.org")
TRANSLATE = os.environ.get("PB_TRANSLATE", "1") == "1"
NEWS_KEEP_DAYS = 400
NEWS_MAX = 1500

# (언어코드, 검색어, hl, gl, ceid, 단일국가 기본값)
NEWS_QUERIES = [
    ("en", '"participatory budgeting"', "en-US", "US", "US:en", None),
    ("en", '"participatory budget"', "en-GB", "GB", "GB:en", None),
    ("es", '"presupuesto participativo"', "es-419", "MX", "MX:es-419", None),
    ("es", '"presupuestos participativos"', "es", "ES", "ES:es", None),
    ("pt", '"orçamento participativo"', "pt-BR", "BR", "BR:pt-419", None),
    ("pt", '"orçamento participativo"', "pt-PT", "PT", "PT:pt-150", "PRT"),
    ("fr", '"budget participatif"', "fr", "FR", "FR:fr", None),
    ("de", '"Bürgerhaushalt" OR "Bürgerbudget"', "de", "DE", "DE:de", None),
    ("it", '"bilancio partecipativo"', "it", "IT", "IT:it", "ITA"),
    ("pl", '"budżet obywatelski"', "pl", "PL", "PL:pl", "POL"),
    ("ko", '"주민참여예산" OR "국민참여예산" OR "시민참여예산"', "ko", "KR", "KR:ko", "KOR"),
    ("ja", '"参加型予算"', "ja", "JP", "JP:ja", "JPN"),
    ("zh", '"参与式预算" OR "參與式預算"', "zh-TW", "TW", "TW:zh-Hant", None),
    ("ru", '"инициативное бюджетирование"', "ru", "RU", "RU:ru", None),
    ("uk", '"громадський бюджет"', "uk", "UA", "UA:uk", "UKR"),
    ("cs", '"participativní rozpočet"', "cs", "CZ", "CZ:cs", "CZE"),
    ("sk", '"participatívny rozpočet"', "sk", "SK", "SK:sk", "SVK"),
    ("ro", '"buget participativ" OR "bugetare participativă"', "ro", "RO", "RO:ro", "ROU"),
    ("nl", '"burgerbegroting" OR "participatief budget"', "nl", "NL", "NL:nl", None),
    ("fi", '"osallistuva budjetointi" OR "OmaStadi"', "fi", "FI", "FI:fi", "FIN"),
    ("sv", '"medborgarbudget"', "sv", "SE", "SE:sv", "SWE"),
    ("lt", '"dalyvaujamasis biudžetas"', "lt", "LT", "LT:lt", "LTU"),
    ("lv", '"līdzdalības budžets"', "lv", "LV", "LV:lv", "LVA"),
    ("et", '"kaasav eelarve"', "et", "EE", "EE:et", "EST"),
    ("hr", '"participativni proračun" OR "participativno budžetiranje"', "hr", "HR", "HR:hr", None),
    ("id", '"penganggaran partisipatif" OR "anggaran partisipatif"', "id", "ID", "ID:id", "IDN"),
    ("tr", '"katılımcı bütçe"', "tr", "TR", "TR:tr", None),
]
LANG_NAMES = {"en": "영어", "es": "스페인어", "pt": "포르투갈어", "fr": "프랑스어", "de": "독일어", "it": "이탈리아어",
              "pl": "폴란드어", "ko": "한국어", "ja": "일본어", "zh": "중국어", "ru": "러시아어", "uk": "우크라이나어",
              "cs": "체코어", "sk": "슬로바키아어", "ro": "루마니아어", "nl": "네덜란드어", "fi": "핀란드어",
              "sv": "스웨덴어", "lt": "리투아니아어", "lv": "라트비아어", "et": "에스토니아어", "hr": "크로아티아어",
              "id": "인도네시아어", "tr": "터키어"}

# 제목에 PB 관련어가 실제로 들어 있어야 채택 (검색엔진의 느슨한 매칭 제거)
PB_TERMS = re.compile(
    r"participatory budget|participative budget|presupuesto[s]? participativo|orçamento[s]? participativo|"
    r"budget[s]? participatif|bürgerhaushalt|bürgerbudget|bilancio partecipativo|budżet[u]? obywatelsk|"
    r"budżecie obywatelskim|참여예산|参加型予算|参与式预算|參與式預算|инициативн\w* бюджет|громадськ\w* бюджет|"
    r"participativní rozpoč|participatívn\w* rozpoč|buget\w* participativ|bugetare participativ|burgerbegroting|"
    r"participatief budget|osallistuva\w* budjetoin|omastadi|medborgarbudget|dalyvaujam\w* biudžet|līdzdalības budžet|"
    r"kaasav\w* eelarve|participativn\w* proračun|participativno budžetiranje|anggaran partisipatif|"
    r"penganggaran partisipatif|katılımcı bütçe|people'?s money",
    re.I,
)


def log(*a):
    print("[collect]", *a, file=sys.stderr, flush=True)


def http_get(url: str, timeout: int = 30, retries: int = 2, accept: str = "*/*") -> bytes:
    last = None
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
            if i == retries:
                break
            wait = 6 * (i + 1)
            if "429" in str(e):
                wait = 40
            time.sleep(wait)
    raise last  # type: ignore[misc]


def load(name: str, default):
    p = DATA / name
    if p.exists():
        try:
            return json.loads(p.read_text("utf-8"))
        except Exception:  # noqa: BLE001
            pass
    return default


def save(name: str, obj) -> None:
    (DATA / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", "utf-8")


def clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", html.unescape(html.unescape(s or "")))
    return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------- 번역 (선택)
TRANS_CACHE: dict = {}
TRANS_FAILS = [0]


def to_ko(text: str, src: str = "auto") -> str | None:
    if not TRANSLATE or not text or src == "ko" or TRANS_FAILS[0] >= 3:
        return None
    key = hashlib.sha1(text.encode()).hexdigest()[:16]
    if key in TRANS_CACHE:
        return TRANS_CACHE[key]
    try:
        q = urllib.parse.urlencode({"client": "gtx", "sl": src, "tl": "ko", "dt": "t", "q": text[:900]})
        raw = http_get("https://translate.googleapis.com/translate_a/single?" + q, timeout=15, retries=0)
        j = json.loads(raw)
        out = "".join(seg[0] for seg in j[0] if seg and seg[0]).strip()
        TRANS_CACHE[key] = out or None
        TRANS_FAILS[0] = 0
        time.sleep(0.4)
        return out or None
    except Exception as e:  # noqa: BLE001
        TRANS_FAILS[0] += 1  # 3회 실패 시 이번 실행에서는 번역 중단
        log("translate fail", type(e).__name__, str(e)[:120])
        return None


# ---------------------------------------------------------------- 국가 매칭
def build_matcher(countries):
    pats = []
    for c in countries:
        for a in c["aliases"]:
            a = a.strip()
            if len(a) < 3 and not re.search(r"[^\x00-\x7f]", a):
                continue
            if re.search(r"[぀-鿿가-힯]", a):  # CJK·한글: 경계 없이
                pats.append((re.compile(re.escape(a)), c["iso3"], len(a)))
            else:
                pats.append((re.compile(r"(?<![\w])" + re.escape(a) + r"(?![\w])", re.I), c["iso3"], len(a)))
    pats.sort(key=lambda x: -x[2])

    def match(text: str):
        for rx, iso, _ in pats:
            if rx.search(text):
                return iso
        return None

    return match


# ---------------------------------------------------------------- 1) 뉴스
TLD_ISO = {"es": "ESP", "fr": "FRA", "de": "DEU", "it": "ITA", "pt": "PRT", "br": "BRA", "mx": "MEX", "ar": "ARG",
           "cl": "CHL", "co": "COL", "pe": "PER", "uy": "URY", "ec": "ECU", "bo": "BOL", "py": "PRY", "do": "DOM",
           "gt": "GTM", "hn": "HND", "sv": "SLV", "ni": "NIC", "cr": "CRI", "pa": "PAN", "ve": "VEN", "pl": "POL",
           "cz": "CZE", "sk": "SVK", "ro": "ROU", "ua": "UKR", "lt": "LTU", "lv": "LVA", "ee": "EST", "fi": "FIN",
           "se": "SWE", "no": "NOR", "dk": "DNK", "nl": "NLD", "be": "BEL", "ch": "CHE", "at": "AUT", "hr": "HRV",
           "si": "SVN", "rs": "SRB", "ba": "BIH", "mk": "MKD", "al": "ALB", "bg": "BGR", "md": "MDA", "hu": "HUN",
           "gr": "GRC", "ie": "IRL", "is": "ISL", "lu": "LUX", "uk": "GBR", "ca": "CAN", "au": "AUS", "nz": "NZL",
           "kr": "KOR", "jp": "JPN", "cn": "CHN", "in": "IND", "id": "IDN", "ph": "PHL", "my": "MYS", "th": "THA",
           "vn": "VNM", "np": "NPL", "bd": "BGD", "pk": "PAK", "lk": "LKA", "mn": "MNG", "kz": "KAZ", "kg": "KGZ",
           "ke": "KEN", "za": "ZAF", "ng": "NGA", "gh": "GHA", "ug": "UGA", "tz": "TZA", "zm": "ZMB", "zw": "ZWE",
           "sn": "SEN", "ma": "MAR", "tn": "TUN", "mz": "MOZ", "ao": "AGO", "cv": "CPV", "cm": "CMR", "bj": "BEN",
           "bf": "BFA", "mg": "MDG", "ml": "MLI", "ru": "RUS", "tw": "TWN", "tr": "TUR"}
# 레지스트리 밖이지만 뉴스 신호가 많은 국가(라벨용)
EXTRA_COUNTRIES = {"RUS": "러시아", "TWN": "대만", "TUR": "튀르키예"}


def tld_country(url: str):
    host = urllib.parse.urlparse(url).hostname or ""
    tld = host.rsplit(".", 1)[-1].lower() if "." in host else ""
    if host.endswith(".gub.uy"):
        return "URY"
    return TLD_ISO.get(tld)


def edition_default(gl: str, lang: str):
    # 단일 국가 언어 에디션의 약한 기본값 (제목·도메인 매칭이 모두 실패했을 때만)
    return {"ES": "ESP", "FR": "FRA", "DE": "DEU", "RU": "RUS", "TW": "TWN", "TR": "TUR", "HR": "HRV", "NL": "NLD"}.get(gl)


def parse_date(s: str) -> str:
    try:
        return email.utils.parsedate_to_datetime(s).astimezone(timezone.utc).isoformat()
    except Exception:  # noqa: BLE001
        return NOW.isoformat()


def collect_news(countries, match, health):
    old = load("news.json", {"items": []}).get("items", [])
    by_id = {x["id"]: x for x in old}
    added = 0
    per_lang = {}
    ok_q = 0
    for lang, q, hl, gl, ceid, default_iso in NEWS_QUERIES:
        url = "https://news.google.com/rss/search?" + urllib.parse.urlencode(
            {"q": f"{q} when:30d", "hl": hl, "gl": gl, "ceid": ceid})
        try:
            root = ET.fromstring(http_get(url, timeout=25))
            ok_q += 1
        except Exception as e:  # noqa: BLE001
            log("news fail", lang, q, e)
            continue
        n = 0
        for it in root.iter("item"):
            title_full = clean(it.findtext("title") or "")
            src_el = it.find("source")
            source = clean(src_el.text if src_el is not None else "")
            title = title_full
            if source and title.endswith(" - " + source):
                title = title[: -len(" - " + source)].strip()
            if not PB_TERMS.search(title):
                continue
            link = (it.findtext("link") or "").strip()
            nid = hashlib.sha1((re.sub(r"\W+", "", title.lower()) + "|" + source.lower()).encode()).hexdigest()[:14]
            if nid in by_id:
                continue
            src_url = src_el.get("url", "") if src_el is not None else ""
            iso = match(title) or tld_country(src_url) or default_iso or edition_default(gl, lang)
            pub = parse_date(it.findtext("pubDate") or "")
            row = {
                "id": nid, "title": title, "title_ko": None, "lang": lang, "source": source,
                "url": link, "source_url": src_url, "gl": gl, "default_iso": default_iso,
                "published_at": pub, "country_iso3": iso, "collected_at": NOW.isoformat(),
                "kind": "signal",
            }
            by_id[nid] = row
            added += 1
            n += 1
        per_lang[lang] = per_lang.get(lang, 0) + n
        time.sleep(1.2)

    # 별칭 사전이 바뀌어도 반영되도록 전체 재태깅
    for row in by_id.values():
        row["country_iso3"] = (match(row["title"]) or tld_country(row.get("source_url", ""))
                               or row.get("default_iso") or edition_default(row.get("gl", ""), row["lang"]))

    # 신규 항목만 번역 (최대 120건/일)
    budget = 120
    for row in sorted(by_id.values(), key=lambda x: x["published_at"], reverse=True):
        if budget <= 0:
            break
        if row.get("title_ko") is None and row["lang"] != "ko" and not row.get("_tr_tried"):
            row["title_ko"] = to_ko(row["title"], row["lang"])
            row["_tr_tried"] = row["title_ko"] is not None
            budget -= 1

    cutoff = (NOW - timedelta(days=NEWS_KEEP_DAYS)).isoformat()
    items = sorted((x for x in by_id.values() if x["published_at"] >= cutoff),
                   key=lambda x: x["published_at"], reverse=True)[:NEWS_MAX]
    save("news.json", {"updated_at": NOW.isoformat(), "count": len(items), "items": items})
    health["news"] = {
        "name": "Google News RSS (다국어)", "ok": ok_q > 0, "queries_ok": ok_q, "queries": len(NEWS_QUERIES),
        "added": added, "total": len(items), "checked_at": NOW.isoformat(),
        "languages": sorted({q[0] for q in NEWS_QUERIES}),
    }
    if ok_q > 0:
        health["news"]["last_success_at"] = NOW.isoformat()
    log("news", "added", added, "total", len(items), per_lang)
    return items, added


# ---------------------------------------------------------------- 2) 논문
def inv_abstract(inv):
    if not inv:
        return ""
    pos = []
    for w, idx in inv.items():
        for i in idx:
            pos.append((i, w))
    return " ".join(w for _, w in sorted(pos))


PAPER_TERMS = ["participatory budgeting", "participatory budget", "presupuesto participativo", "presupuestos participativos",
               "orçamento participativo", "budget participatif", "bilancio partecipativo", "budżet obywatelski",
               "Bürgerhaushalt", "initiative budgeting", "주민참여예산", "참여예산"]
NOISE_VENUES = re.compile(r"zenodo|figshare|research square|preprints\.org|ssrn electronic", re.I)


def norm_title(t: str) -> str:
    return re.sub(r"[^0-9a-z\u00c0-\uffff]+", "", (t or "").lower())[:120]


def keep_paper(title: str, abstract: str, venue: str) -> bool:
    if PB_TERMS.search(title) or re.search(r"initiative budgeting|참여예산", title, re.I):
        return True
    return bool(PB_TERMS.search(abstract[:600])) and not NOISE_VENUES.search(venue or "")


def collect_papers(health):
    old = load("papers.json", {"items": []}).get("items", [])
    for x in old:
        x["title"] = clean(x["title"])
    by_id = {x["id"]: x for x in old}
    titles = {norm_title(x["title"]): x["id"] for x in old}
    since = (NOW - timedelta(days=540)).date().isoformat()
    stats = {"OpenAlex": 0, "Crossref": 0}
    errs = []

    def put(pid, row):
        nt = norm_title(row["title"])
        if nt in titles and titles[nt] != pid:  # 같은 논문의 다른 판(프리프린트 등)은 건너뜀
            return False
        cur = by_id.get(pid, {})
        cur.update(row)
        cur.setdefault("first_seen", TODAY)
        by_id[pid] = cur
        titles[nt] = pid
        return True

    # OpenAlex: 언어별 검색어를 제목·초록에서 찾음
    for term in PAPER_TERMS:
        try:
            params = {"filter": f'title_and_abstract.search:"{term}",from_publication_date:{since}',
                      "sort": "publication_date:desc", "per_page": "50", "mailto": MAILTO}
            if os.environ.get("OPENALEX_API_KEY"):
                params["api_key"] = os.environ["OPENALEX_API_KEY"]
            j = json.loads(http_get("https://api.openalex.org/works?" + urllib.parse.urlencode(params), timeout=40, retries=2))
            for w in j.get("results", []):
                title = clean(w.get("display_name") or w.get("title") or "")
                abstract = clean(inv_abstract(w.get("abstract_inverted_index")))
                loc = (w.get("primary_location") or {})
                venue = ((loc.get("source") or {}).get("display_name")) or ""
                if not title or not keep_paper(title, abstract, venue):
                    continue
                doi = (w.get("doi") or "").replace("https://doi.org/", "") or None
                pid = "doi:" + doi.lower() if doi else "oa:" + w["id"].rsplit("/", 1)[-1]
                authors = [a["author"]["display_name"] for a in (w.get("authorships") or [])[:4] if a.get("author")]
                if put(pid, {
                    "id": pid, "title": title, "authors": authors, "venue": venue,
                    "published_at": w.get("publication_date"), "doi": doi,
                    "url": (f"https://doi.org/{doi}" if doi else loc.get("landing_page_url") or w["id"]),
                    "open_access": bool((w.get("open_access") or {}).get("is_oa")),
                    "lang": w.get("language"), "cited_by": w.get("cited_by_count", 0),
                    "abstract_snippet": abstract[:420], "source": "OpenAlex", "type": w.get("type"),
                    "concepts": [t.get("display_name") for t in (w.get("topics") or [])[:3]],
                }):
                    stats["OpenAlex"] += 1
        except Exception as e:  # noqa: BLE001
            errs.append(f"OpenAlex[{term}]: {e}")
            log("openalex fail", term, e)
            if "429" in str(e):  # 속도 제한이면 이번 실행에서는 중단
                break
        time.sleep(1.5)

    # Crossref: 보완 수집 (항상 실행)
    for term in ["participatory budgeting", "presupuesto participativo", "orçamento participativo", "budget participatif"]:
        try:
            params = {"query.bibliographic": term, "filter": f"from-pub-date:{since}",
                      "sort": "relevance", "order": "desc", "rows": "100", "mailto": MAILTO}
            j = json.loads(http_get("https://api.crossref.org/works?" + urllib.parse.urlencode(params), timeout=40))
            for w in j["message"]["items"]:
                title = clean((w.get("title") or [""])[0])
                venue = (w.get("container-title") or [""])[0]
                if not title or not PB_TERMS.search(title):
                    continue
                doi = w.get("DOI")
                pid = "doi:" + doi.lower()
                if pid in by_id and by_id[pid].get("source") == "OpenAlex":
                    continue
                dp = (w.get("published") or w.get("issued") or {}).get("date-parts", [[None]])[0]
                pub = "-".join(f"{x:02d}" if i else str(x) for i, x in enumerate(dp) if x) if dp and dp[0] else None
                if put(pid, {
                    "id": pid, "title": title,
                    "authors": [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in (w.get("author") or [])[:4]],
                    "venue": venue, "published_at": pub, "doi": doi, "url": f"https://doi.org/{doi}",
                    "open_access": None, "lang": None, "cited_by": w.get("is-referenced-by-count", 0),
                    "abstract_snippet": clean(w.get("abstract") or "")[:420], "source": "Crossref",
                    "type": w.get("type"), "concepts": [],
                }):
                    stats["Crossref"] += 1
        except Exception as e:  # noqa: BLE001
            errs.append(f"Crossref[{term}]: {e}")
            log("crossref fail", term, e)
        time.sleep(1.0)

    # 기존 레코드 중 잡음 판정된 것 정리
    for k in [k for k, v in by_id.items() if not keep_paper(v["title"], v.get("abstract_snippet", ""), v.get("venue", ""))]:
        by_id.pop(k)

    budget = 40
    for row in sorted(by_id.values(), key=lambda x: x.get("published_at") or "", reverse=True):
        if budget <= 0:
            break
        if not row.get("_tr_tried"):
            row["title_ko"] = to_ko(row["title"])
            row["_tr_tried"] = row["title_ko"] is not None
            budget -= 1

    items = sorted(by_id.values(), key=lambda x: x.get("published_at") or "", reverse=True)[:400]
    got = stats["OpenAlex"] + stats["Crossref"]
    save("papers.json", {"updated_at": NOW.isoformat(), "count": len(items), "items": items})
    health["papers"] = {"name": "학술 DB (OpenAlex·Crossref)", "ok": got > 0, "fetched": got, "by_source": stats,
                        "total": len(items), "checked_at": NOW.isoformat(),
                        "error": "; ".join(errs)[:400] if errs else None,
                        "last_success_at": NOW.isoformat() if got > 0 else (health.get("papers") or {}).get("last_success_at")}
    log("papers", stats, "total", len(items))
    return items


# ---------------------------------------------------------------- 3) 국가 신호·4) 원장
def build_countries(seed, news, papers, ledger):
    cut30 = (NOW - timedelta(days=30)).isoformat()
    cut365 = (NOW - timedelta(days=365)).isoformat()
    by_iso = {}
    for n in news:
        if n.get("country_iso3"):
            by_iso.setdefault(n["country_iso3"], []).append(n)
    prev = {c["iso3"]: c for c in load("countries.json", {"items": []}).get("items", [])}
    seen_ledger = {e["key"] for e in ledger}
    out = []
    for c in seed:
        ns = sorted(by_iso.get(c["iso3"], []), key=lambda x: x["published_at"], reverse=True)
        latest = ns[0] if ns else None
        row = dict(c)
        row["news_30d"] = sum(1 for x in ns if x["published_at"] >= cut30)
        row["news_365d"] = sum(1 for x in ns if x["published_at"] >= cut365)
        row["latest_news"] = ({"title": latest.get("title_ko") or latest["title"], "title_original": latest["title"],
                               "date": latest["published_at"][:10], "url": latest["url"], "source": latest["source"]}
                              if latest else None)
        row["activity_date"] = max(filter(None, [c.get("base_signal_date"), latest and latest["published_at"][:10]]), default=None)
        out.append(row)
        if latest:
            key = f"news:{c['iso3']}:{latest['id']}"
            if key not in seen_ledger and (prev.get(c["iso3"], {}).get("latest_news") or {}).get("url") != latest["url"]:
                ledger.append({"key": key, "date": TODAY, "iso3": c["iso3"], "type": "뉴스 신호",
                               "label": c["name_ko"], "text": latest.get("title_ko") or latest["title"],
                               "url": latest["url"], "observed_at": latest["published_at"][:10]})
                seen_ledger.add(key)
    for p in papers:
        key = f"paper:{p['id']}"
        if key not in seen_ledger and p.get("first_seen") == TODAY and (p.get("published_at") or "") >= (NOW - timedelta(days=30)).date().isoformat():
            ledger.append({"key": key, "date": TODAY, "iso3": None, "type": "연구 신호",
                           "label": (p.get("venue") or "논문")[:60], "text": p.get("title_ko") or p["title"],
                           "url": p["url"], "observed_at": p.get("published_at")})
            seen_ledger.add(key)
    save("countries.json", {"updated_at": NOW.isoformat(), "count": len(out), "items": out})
    return out


def snapshot_history(countries, news, papers, programs):
    hist = load("history.json", [])
    hist = [h for h in hist if h["date"] != TODAY]
    by_status = {}
    for c in countries:
        by_status[c["tracking_status"]] = by_status.get(c["tracking_status"], 0) + 1
    cut30 = (NOW - timedelta(days=30)).isoformat()
    hist.append({"date": TODAY, "countries": len(countries), "status": by_status, "programs": len(programs),
                 "news_total": len(news), "news_30d": sum(1 for n in news if n["published_at"] >= cut30),
                 "countries_with_signal_30d": sum(1 for c in countries if c["news_30d"] > 0),
                 "papers_total": len(papers)})
    hist = sorted(hist, key=lambda h: h["date"])[-730:]
    save("history.json", hist)


def attach_program_news(programs, news):
    for p in programs:
        kws = [k.lower() for k in p.get("keywords", [])]
        hits = [n for n in news if n.get("country_iso3") == p["country_iso3"]
                and any(k in (n["title"] or "").lower() for k in kws)]
        hits.sort(key=lambda x: x["published_at"], reverse=True)
        p["related_news"] = [{"title": h.get("title_ko") or h["title"], "date": h["published_at"][:10], "url": h["url"],
                              "source": h["source"]} for h in hits[:3]]
        p["latest_signal_date"] = hits[0]["published_at"][:10] if hits else None
    save("programs.json", {"updated_at": NOW.isoformat(), "count": len(programs), "items": programs})


def main():
    DATA.mkdir(exist_ok=True)
    seed = load("countries.seed.json", [])
    programs = load("programs.seed.json", [])
    match = build_matcher(seed)
    health = load("health.json", {})
    ledger = load("ledger.json", [])

    news, added = collect_news(seed, match, health)
    papers = collect_papers(health)
    countries = build_countries(seed, news, papers, ledger)
    attach_program_news(programs, news)
    snapshot_history(countries, news, papers, programs)

    ledger = sorted(ledger, key=lambda e: (e["date"], e.get("observed_at") or ""), reverse=True)[:1500]
    save("ledger.json", ledger)
    health["build"] = {"name": "일일 빌드", "ok": True, "checked_at": NOW.isoformat(), "last_success_at": NOW.isoformat()}
    save("health.json", health)
    save("meta.json", {
        "updated_at": NOW.isoformat(), "version": "4.0",
        "counts": {"countries": len(countries), "programs": len(programs), "news": len(news),
                   "papers": len(papers), "ledger": len(ledger), "news_added_today": added},
    })
    log("translated", "news", sum(1 for x in news if x.get("title_ko")), "papers", sum(1 for x in papers if x.get("title_ko")))
    log("done")


if __name__ == "__main__":
    main()
