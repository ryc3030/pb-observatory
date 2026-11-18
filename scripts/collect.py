#!/usr/bin/env python3
"""세계 참여예산 관측소 — 일일 자동 수집기.

GitHub Actions가 매일 실행합니다. 외부 패키지 없이 표준 라이브러리만 씁니다.

수집 대상
  1) 뉴스 신호  : Google News RSS(27개 검색어·24개 언어) + 참여예산 기관 소식 피드 6곳. GDELT는 scripts/gdelt.py가 하루 한 번 따로 수집
                 같은 소식은 언어와 상관없이 묶어(story) 여러 매체가 다룬 소식을 가려낸다
  2) 연구 논문  : OpenAlex (실패 시 Crossref)
  3) 국가 신호  : 뉴스 제목을 국가 별칭과 대조해 국가별 최신 신호·30일 건수 산출
  4) 근거 원장  : 새로 관측된 국가 신호·논문을 날짜와 함께 누적
  5) 출처 상태  : 소스별 성공/실패, 건수, 시각
  6) 외부 레지스트리 : Participedia(사례), Pabulib(투표 기록), Decidim GraphQL(공식 플랫폼 수치)

원칙: 뉴스·논문·레지스트리 신호는 '공식·검증'(verified)·'문헌·플랫폼'(documented)으로 올리지 않습니다.
최근 6개월 보도로 운영이 확인된 모니터링 국가만 '보도 확인'(reported)으로 따로 표시하고, 보도가 끊기면 되돌립니다.
레지스트리에서 근거가 보이면 '검토 필요' 표시와 원장 기록만 남기고, 상태 변경은 사람이 seed 파일에서 합니다.
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ko_style import polish as ko_polish  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NOW = datetime.now(timezone.utc)
TODAY = NOW.date().isoformat()
UA = "Mozilla/5.0 (compatible; PB-Observatory/4.0; +https://github.com)"
MAILTO = os.environ.get("OPENALEX_MAILTO") or "pb-observatory@example.org"
REAL_MAILTO = "@" in MAILTO and not MAILTO.endswith("example.org")
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
TRANS_FAILS = {"google": 0, "mymemory": 0}


def _google(text, src):
    q = urllib.parse.urlencode({"client": "gtx", "sl": src or "auto", "tl": "ko", "dt": "t", "q": text[:900]})
    j = json.loads(http_get("https://translate.googleapis.com/translate_a/single?" + q, timeout=15, retries=0))
    return "".join(seg[0] for seg in j[0] if seg and seg[0]).strip()


def _mymemory(text, src):
    params = {"q": text[:480], "langpair": f"{src or 'en'}|ko"}
    if REAL_MAILTO:  # 실제 이메일이 있으면 일일 한도 5천→5만 자
        params["de"] = MAILTO
    q = urllib.parse.urlencode(params)
    j = json.loads(http_get("https://api.mymemory.translated.net/get?" + q, timeout=20, retries=0))
    if j.get("quotaFinished"):
        raise RuntimeError("MyMemory quota finished")
    out = (j.get("responseData") or {}).get("translatedText") or ""
    if not out or "MYMEMORY WARNING" in out.upper() or "INVALID" in out.upper()[:20]:
        raise RuntimeError("MyMemory: " + out[:80])
    return html.unescape(out).strip()


def ko_style_pass(items, kind: str) -> int:
    """기계 번역 원문(title_ko_mt)을 보관하고, 화면에 쓰는 title_ko는 늘 원문에서 다시 다듬는다(ko_style.py)."""
    n = 0
    for x in items:
        if not x.get("title_ko"):
            continue
        if not x.get("title_ko_mt"):
            x["title_ko_mt"] = x["title_ko"]
        new = ko_polish(x["title_ko_mt"], kind)
        n += new != x["title_ko_mt"]
        x["title_ko"] = new
    return n


def to_ko(text: str, src: str | None = None) -> str | None:
    """제목 자동 번역. Google → MyMemory 순으로 시도하고, 각 서비스가 3회 실패하면 이번 실행에서는 건너뜀."""
    if not TRANSLATE or not text or src == "ko":
        return None
    key = hashlib.sha1(text.encode()).hexdigest()[:16]
    if TRANS_CACHE.get(key):
        return TRANS_CACHE[key]
    for name, fn in (("google", _google), ("mymemory", _mymemory)):
        if TRANS_FAILS[name] >= 3:
            continue
        try:
            out = fn(text, src)
            if out:
                TRANS_CACHE[key] = out
                TRANS_FAILS[name] = 0
                time.sleep(0.5)
                return out
        except Exception as e:  # noqa: BLE001
            TRANS_FAILS[name] += 1
            log("translate fail", name, str(e)[:120])
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


NAME_ISO: dict[str, str] = {}  # 영문 국가명·별칭 → ISO3 (main에서 seed로 채움)
NAME_ISO_EXTRA = {"united states": "USA", "united kingdom": "GBR", "south korea": "KOR", "korea": "KOR",
                  "czech republic": "CZE", "czechia": "CZE", "tchéquia": "CZE", "germania": "DEU", "italia": "ITA",
                  "taiwan": "TWN", "russia": "RUS", "turkey": "TUR", "türkiye": "TUR", "cape verde": "CPV",
                  "dominican republic": "DOM", "ivory coast": "CIV", "côte d'ivoire": "CIV", "vietnam": "VNM",
                  "democratic republic of the congo": "COD", "afghanistan": "AFG", "bosnia-herzegovina": "BIH",
                  "macedonia": "MKD", "north macedonia": "MKD", "slovak republic": "SVK"}


def name_iso(name: str):
    n = (name or "").strip().lower()
    return NAME_ISO.get(n) or NAME_ISO_EXTRA.get(n)


def tag_country(row, match):
    """국가 판정 우선순위: 제목 속 지명 → GDELT 발행국 → 출처 도메인 → 단일국가 검색어 → 언어판 기본값."""
    t = match(row["title"])
    if t:
        return t, "제목"
    if row.get("src_country_iso"):
        return row["src_country_iso"], "발행국"
    t = tld_country(row.get("source_url", "") or row.get("url", ""))
    if t:
        return t, "도메인"
    if row.get("default_iso"):
        return row["default_iso"], "검색어"
    t = edition_default(row.get("gl", ""), row["lang"])
    return (t, "언어판") if t else (None, None)


GDELT_LANG = {"English": "en", "Spanish": "es", "Portuguese": "pt", "French": "fr", "German": "de", "Italian": "it",
              "Polish": "pl", "Korean": "ko", "Japanese": "ja", "Chinese": "zh", "Russian": "ru", "Ukrainian": "uk",
              "Czech": "cs", "Slovak": "sk", "Romanian": "ro", "Dutch": "nl", "Finnish": "fi", "Swedish": "sv",
              "Lithuanian": "lt", "Latvian": "lv", "Estonian": "et", "Croatian": "hr", "Indonesian": "id", "Turkish": "tr"}
def parse_date(s: str) -> str:
    try:
        return email.utils.parsedate_to_datetime(s).astimezone(timezone.utc).isoformat()
    except Exception:  # noqa: BLE001
        return NOW.isoformat()


# 참여예산 전문 기관·플랫폼의 소식 피드(검색이 아니라 출처 고정). pb_only=True면 모든 글, 아니면 PB 용어가 있는 글만.
ORG_FEEDS = [
    ("Participatory Budgeting Project", "https://www.participatorybudgeting.org/feed/", True, None),
    ("PB Scotland", "https://pbscotland.scot/blog?format=rss", True, "GBR"),
    ("newDemocracy Foundation", "https://www.newdemocracy.com.au/feed/", False, "AUS"),
    ("Decidim", "https://www.decidim.org/blog/feed.xml", False, None),
    ("CONSUL Democracy", "https://www.consuldemocracy.org/feed", False, None),
    ("Open Government Partnership", "https://www.opengovpartnership.org/feed/", False, None),
]


def collect_org_feeds(by_id, health):
    ok, got, errs = 0, 0, []
    atom = "{http://www.w3.org/2005/Atom}"
    for name, url, pb_only, iso in ORG_FEEDS:
        try:
            root = ET.fromstring(http_get(url, timeout=25, retries=1))
            ok += 1
        except Exception as e:  # noqa: BLE001
            errs.append(f"{name}: {str(e)[:50]}")
            continue
        entries = list(root.iter("item")) or list(root.iter(atom + "entry"))
        for it in entries:
            title = clean(it.findtext("title") or it.findtext(atom + "title") or "")
            link = (it.findtext("link") or "").strip()
            if not link:
                le = it.find(atom + "link")
                link = le.get("href", "") if le is not None else ""
            desc = clean(it.findtext("description") or it.findtext(atom + "summary") or "")[:400]
            if not title or not link or (not pb_only and not PB_TERMS.search(title + " " + desc)):
                continue
            pub_raw = it.findtext("pubDate") or it.findtext(atom + "published") or it.findtext(atom + "updated") or ""
            try:
                pub = (datetime.fromisoformat(pub_raw.replace("Z", "+00:00")).astimezone(timezone.utc).isoformat()
                       if "T" in pub_raw[:20] else parse_date(pub_raw))
            except ValueError:
                pub = parse_date(pub_raw)
            if pub > (NOW + timedelta(days=2)).isoformat():  # 고정 글에 붙은 미래 날짜(예: 2029-12-31)는 날짜를 믿을 수 없어 뺀다
                continue
            nid = hashlib.sha1(("org|" + link).encode()).hexdigest()[:14]
            if nid in by_id:
                continue
            by_id[nid] = {"id": nid, "title": title, "title_ko": None, "lang": "en", "source": name, "url": link,
                          "source_url": url, "gl": "", "default_iso": iso, "published_at": pub, "summary": desc[:240],
                          "collected_at": NOW.isoformat(), "kind": "org", "via": "기관 피드"}
            got += 1
        time.sleep(0.8)
    health["orgs"] = {"name": "참여예산 기관 소식 피드", "ok": ok > 0, "queries_ok": ok, "queries": len(ORG_FEEDS),
                      "added": got, "total": sum(1 for x in by_id.values() if x.get("kind") == "org"),
                      "checked_at": NOW.isoformat(), "error": "; ".join(errs)[:300] or None,
                      "last_success_at": NOW.isoformat() if ok else (health.get("orgs") or {}).get("last_success_at")}
    log("org feeds", ok, "/", len(ORG_FEEDS), "new", got)
    return got


# 같은 소식 묶기: 번역된 한국어 제목(없으면 원문)의 단어·글자쌍으로 TF-IDF 코사인 유사도를 재고,
# 5일 안·같은 국가(또는 국가 미상) 기사끼리 0.45 이상이면 한 소식으로 묶는다. 언어가 달라도 묶인다.
STORY_STOP = set("참여예산 주민참여예산 시민참여예산 국민참여예산 예산 participatory budget budgeting presupuesto "
                 "participativo orçamento budżet obywatelski the of and de la el en do da 년 위한 대한 및".split())


def cluster_stories(items, threshold=0.45, window_days=5):
    import math
    from collections import Counter
    def feats(x):
        t = re.sub(r"\s+-\s+[^-]+$", "", (x.get("title_ko") or x["title"]).lower())
        f = Counter()
        for w in re.findall(r"\w+", t):
            if w in STORY_STOP or len(w) < 2 or w.isdigit():
                continue
            f["w:" + w] += 1
            if re.search(r"[가-힣]", w):
                for i in range(len(w) - 1):
                    f["b:" + w[i:i + 2]] += 0.5
        return f
    rows = sorted(items, key=lambda x: x["published_at"])
    F = [feats(x) for x in rows]
    df = Counter(k for f in F for k in f)
    n = len(rows)
    V = []
    for f in F:
        v = {k: c * math.log((n + 1) / (df[k] + 0.5)) for k, c in f.items()}
        norm = math.sqrt(sum(a * a for a in v.values())) or 1
        V.append({k: a / norm for k, a in v.items()})
    T = [datetime.fromisoformat(x["published_at"]).timestamp() for x in rows]
    par = list(range(n))
    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for i in range(n):
        j = i + 1
        while j < n and T[j] - T[i] <= window_days * 86400:
            ci, cj = rows[i].get("country_iso3"), rows[j].get("country_iso3")
            if not (ci and cj and ci != cj):
                a, b = (V[i], V[j]) if len(V[i]) <= len(V[j]) else (V[j], V[i])
                if sum(w * b.get(k, 0) for k, w in a.items()) >= threshold:
                    par[find(i)] = find(j)
            j += 1
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(rows[i])
    multi = 0
    for g in groups.values():
        g.sort(key=lambda x: x["published_at"])
        sources = {x["source"] for x in g}
        isos = Counter(x["country_iso3"] for x in g if x.get("country_iso3"))
        for x in g:
            x["story"] = g[0]["id"]
            x["story_n"] = len(sources)
            # 국가를 못 정한 기사는 같은 소식 기사들의 국가로 보충(근거: 같은 소식)
            if not x.get("country_iso3") and isos:
                x["country_iso3"], x["iso_basis"] = isos.most_common(1)[0][0], "같은 소식"
        multi += len(sources) > 1
    return multi


def collect_news(countries, match, health):
    old = load("news.json", {"items": []}).get("items", [])
    by_id = {x["id"]: x for x in old}
    added = 0
    per_lang = {}
    ok_q = 0
    # 평소에는 최근 30일. PB_BACKFILL_MONTHS=12면 지난 12개월을 한 달씩 나눠 한 번 소급 수집한다(1년 기록용).
    months = int(os.environ.get("PB_BACKFILL_MONTHS") or 0)
    windows = [("when:30d", None)]
    for k in range(1, months + 1):
        end = (NOW - timedelta(days=30 * (k - 1))).date()
        start = (NOW - timedelta(days=30 * k)).date()
        windows.append((f"after:{start.isoformat()} before:{end.isoformat()}", k))
    jobs = [(w, qq) for w, _ in windows for qq in NEWS_QUERIES]
    for when, (lang, q, hl, gl, ceid, default_iso) in jobs:
        url = "https://news.google.com/rss/search?" + urllib.parse.urlencode(
            {"q": f"{q} {when}", "hl": hl, "gl": gl, "ceid": ceid})
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
            iso = None  # 아래 재태깅에서 결정
            pub = parse_date(it.findtext("pubDate") or "")
            row = {
                "id": nid, "title": title, "title_ko": None, "lang": lang, "source": source,
                "url": link, "source_url": src_url, "gl": gl, "default_iso": default_iso,
                "published_at": pub, "country_iso3": iso, "collected_at": NOW.isoformat(),
                "kind": "signal", "via": "Google News",
            }
            by_id[nid] = row
            added += 1
            n += 1
        per_lang[lang] = per_lang.get(lang, 0) + n
        time.sleep(1.2)

    # 참여예산 전문 기관의 소식 피드
    added += collect_org_feeds(by_id, health)

    # GDELT 기사는 scripts/gdelt.py가 하루 한 번 따로 넣는다(호출 제한 때문). 여기서는 재태깅만 함께 받는다.

    # 별칭 사전이 바뀌어도 반영되도록 전체 재태깅. 근거(iso_basis)를 함께 남겨 화면에서 판단 근거를 보여 줌
    for row in by_id.values():
        row["country_iso3"], row["iso_basis"] = tag_country(row, match)

    # 신규 항목만 번역 (최대 120건/일)
    budget = 150
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
    log("ko style news", ko_style_pass(items, "news"))
    stories = cluster_stories(items)
    log("stories with 2+ sources", stories)
    save("news.json", {"updated_at": NOW.isoformat(), "count": len(items), "items": items})
    health["news"] = {
        "name": "Google News RSS (다국어)", "ok": ok_q > 0, "queries_ok": ok_q, "queries": len(jobs),
        "backfill_months": months or None,
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
            row["title_ko"] = to_ko(row["title"], (row.get("lang") or "en").split("-")[0])
            row["_tr_tried"] = row["title_ko"] is not None
            budget -= 1

    items = sorted(by_id.values(), key=lambda x: x.get("published_at") or "", reverse=True)[:400]
    log("ko style papers", ko_style_pass(items, "paper"))
    got = stats["OpenAlex"] + stats["Crossref"]
    save("papers.json", {"updated_at": NOW.isoformat(), "count": len(items), "items": items})
    health["papers"] = {"name": "학술 DB (OpenAlex·Crossref)", "ok": got > 0, "fetched": got, "by_source": stats,
                        "total": len(items), "checked_at": NOW.isoformat(),
                        "error": "; ".join(errs)[:400] if errs else None,
                        "last_success_at": NOW.isoformat() if got > 0 else (health.get("papers") or {}).get("last_success_at")}
    log("papers", stats, "total", len(items))
    return items


# ---------------------------------------------------------------- 3) 국가 신호·4) 원장
# 보도 확인: 정부 원문이 없어도 최근 6개월 보도로 운영이 확인되면 '보도 확인'(reported)으로 올린다.
# 나라마다 참여예산 주기(공모·투표 시기)가 달라 6개월이면 한 주기 안의 흔적을 잡는다.
# 조건: 국가 판정이 확실한 기사(제목·발행국·도메인·같은 소식)가 1건 이상.
#   (근거 강도는 소식 수·매체 수로 함께 보여 준다)
# 6개월 동안 조건을 채우지 못하면 다시 탐색 모니터링으로 내려간다. 공식·검증, 문헌·플랫폼은 건드리지 않는다.
PRESS_DAYS = 183
PRESS_YEAR_DAYS = 365  # 1년 기록(상태는 6개월로 판정, 1년치는 근거 기록·추이로 남김)
STRONG_BASIS = {"제목", "발행국", "도메인", "같은 소식"}


def press_evidence(ns):
    """최근 6개월(상태 판정)과 최근 1년(기록) 두 기간의 보도 근거를 함께 센다."""
    def window(days):
        cut = (NOW - timedelta(days=days)).isoformat()
        st = {}
        for x in ns:
            if x["published_at"] >= cut and x.get("iso_basis") in STRONG_BASIS:
                st.setdefault(x.get("story") or x["id"], []).append(x)
        return st
    s6, s12 = window(PRESS_DAYS), window(PRESS_YEAR_DAYS)
    multi = lambda st: sum(1 for v in st.values() if len({x["source"] for x in v}) >= 2)
    ranked = sorted(s12.values(), key=lambda v: (max(x["published_at"] for x in v) >= (NOW - timedelta(days=PRESS_DAYS)).isoformat(),
                                                len({x["source"] for x in v}), max(x["published_at"] for x in v)), reverse=True)
    ev = []
    for v in ranked[:3]:
        top = max(v, key=lambda x: x["published_at"])
        ev.append({"title": top.get("title_ko") or top["title"], "url": top["url"], "source": top["source"],
                   "date": top["published_at"][:10], "outlets": len({x["source"] for x in v})})
    months = sorted({x["published_at"][:7] for v in s12.values() for x in v})
    return {"confirmed": len(s6) >= 1, "stories": len(s6), "multi_outlet": multi(s6),
            "stories_12m": len(s12), "multi_outlet_12m": multi(s12), "months_12m": len(months),
            "last": max((x["published_at"][:10] for v in s12.values() for x in v), default=None),
            "window_days": PRESS_DAYS, "evidence": ev}


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
        row["seed_status"] = c["tracking_status"]
        row["press"] = press_evidence(ns)
        if c["tracking_status"] == "monitoring" and row["press"]["confirmed"]:
            row["tracking_status"] = "reported"
        was = (prev.get(c["iso3"]) or {}).get("tracking_status")
        if row["tracking_status"] == "reported" and was != "reported":
            e = row["press"]["evidence"][0]
            ledger.append({"key": f"reported:{c['iso3']}:{TODAY}", "date": TODAY, "iso3": c["iso3"], "type": "보도 확인",
                           "label": c["name_ko"], "text": f"{c['name_ko']}: 최근 6개월 보도로 참여예산 운영 확인 — {e['title']}",
                           "url": e["url"], "observed_at": e["date"]})
        elif was == "reported" and row["tracking_status"] != "reported":
            ledger.append({"key": f"unreported:{c['iso3']}:{TODAY}", "date": TODAY, "iso3": c["iso3"], "type": "보도 확인 해제",
                           "label": c["name_ko"], "text": f"{c['name_ko']}: 최근 6개월 보도 근거가 부족해 탐색 모니터링으로 되돌림",
                           "url": "", "observed_at": TODAY})
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
                 "countries_press_6m": sum(1 for c in countries if (c.get("press") or {}).get("stories")),
                 "countries_press_12m": sum(1 for c in countries if (c.get("press") or {}).get("stories_12m")),
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


def write_feed(news, countries):
    """PB 데일리 최신 60건을 RSS 2.0으로 내보냄 (feed.xml)."""
    from xml.sax.saxutils import escape as x
    site = os.environ.get("PB_SITE_URL", "https://ryc3030.github.io/pb-observatory/")
    names = {c["iso3"]: c["name_ko"] for c in countries}
    items = []
    for n in news[:60]:
        title = n.get("title_ko") or n["title"]
        country = names.get(n.get("country_iso3") or "", "")
        desc = f"{country} · {n.get('source', '')} · 원문: {n['title']}" if n.get("title_ko") else f"{country} · {n.get('source', '')}"
        pub = email.utils.format_datetime(datetime.fromisoformat(n["published_at"]))
        items.append(f"<item><title>{x(title)}</title><link>{x(n['url'])}</link><guid isPermaLink=\"false\">{n['id']}</guid>"
                     f"<pubDate>{pub}</pubDate><description>{x(desc)}</description>"
                     + (f"<category>{x(country)}</category>" if country else "") + "</item>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel>'
           f"<title>세계 참여예산 관측소 — PB 데일리</title><link>{x(site)}</link>"
           "<description>전 세계 참여예산 뉴스 신호 (매일 자동 수집, 제목은 자동 번역)</description><language>ko</language>"
           f"<lastBuildDate>{email.utils.format_datetime(NOW)}</lastBuildDate>" + "".join(items) + "</channel></rss>\n")
    (ROOT / "feed.xml").write_text(xml, "utf-8")


# ---------------------------------------------------------------- 6) 외부 레지스트리
def http_post_json(url: str, payload: dict, timeout: int = 90):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST",
                                 headers={"User-Agent": UA, "Content-Type": "application/json", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


PB_CASE_RX = re.compile(r"particip\w*[ -]budget|presupuesto|orçamento|budget participatif|bilancio partecipativo|"
                        r"bürgerhaushalt|budżet obywatelski|참여예산|\bPB\b", re.I)


def collect_participedia(health):
    """Participedia 검색 JSON(무키). 제목·요약에 PB 용어가 있는 사례만 남김."""
    prev = load("cases.json", {"items": []})
    items, errs, page, pages = {}, [], 1, 1
    while page <= min(pages, 40):
        url = "https://participedia.net/search?" + urllib.parse.urlencode(
            {"selectedCategory": "case", "query": "participatory budgeting", "returns": "json", "page": page})
        try:
            d = json.loads(http_get(url, timeout=60, retries=1, accept="application/json"))
            pages = int(d.get("pages") or 1)
        except Exception as e:  # noqa: BLE001
            errs.append(f"p{page}: {str(e)[:60]}")
            break
        for r in d.get("results", []):
            text = f"{r.get('title') or ''} {r.get('description') or ''}"
            if not PB_CASE_RX.search(text):
                continue
            try:
                lat, lon = float(r.get("latitude")), float(r.get("longitude"))
            except (TypeError, ValueError):
                lat = lon = None
            items[str(r["id"])] = {
                "id": str(r["id"]), "title": clean(r.get("title") or "")[:200], "city": r.get("city") or "",
                "country": r.get("country") or "", "iso3": name_iso(r.get("country")), "lat": lat, "lon": lon,
                "verified": str(r.get("verified")) == "True", "completeness": r.get("completeness") or "",
                "updated": (r.get("updated_date") or "")[:10], "url": f"https://participedia.net/case/{r['id']}"}
        page += 1
        time.sleep(0.8)
    ok = bool(items)
    rows = sorted(items.values(), key=lambda x: x["updated"], reverse=True) if ok else prev.get("items", [])
    by_iso = {}
    for x in rows:
        if x.get("iso3"):
            by_iso[x["iso3"]] = by_iso.get(x["iso3"], 0) + 1
    save("cases.json", {"updated_at": NOW.isoformat() if ok else prev.get("updated_at"), "source": "Participedia",
                        "source_url": "https://participedia.net/", "count": len(rows), "by_iso": by_iso, "items": rows})
    health["participedia"] = {"name": "Participedia 사례 레지스트리", "ok": ok, "fetched": len(items), "total": len(rows),
                              "checked_at": NOW.isoformat(), "error": "; ".join(errs)[:300] or None,
                              "last_success_at": NOW.isoformat() if ok else (health.get("participedia") or {}).get("last_success_at")}
    log("participedia", len(items), "cases", len(by_iso), "countries")
    return rows


def collect_pabulib(health):
    """Pabulib 투표 기록 DB(pabuviz API, 무키). 도시별 회차·투표 수·최근 회차 예산을 집계."""
    prev = load("elections.json", {"units": []})
    try:
        d = json.loads(http_get("https://db.pabuviz.org/api/elections/?filters=%7B%7D", timeout=90, retries=1,
                                accept="application/json"))
        data = d.get("data") or []
    except Exception as e:  # noqa: BLE001
        data, err = [], str(e)[:200]
    else:
        err = None
    units = {}
    for x in data:
        iso = name_iso(x.get("country"))
        key = (iso or x.get("country"), x.get("unit") or "")
        u = units.setdefault(key, {"iso3": iso, "country": x.get("country"), "unit": x.get("unit"), "elections": 0,
                                   "years": set(), "votes": 0, "projects": 0, "latest": None, "by_year": {}})
        u["elections"] += 1
        yr = (x.get("date_begin") or x.get("date_end") or "")[:4]
        if yr.isdigit():
            u["years"].add(int(yr))
            y = u["by_year"].setdefault(yr, {"elections": 0, "budget": 0, "votes": 0, "projects": 0})
            y["elections"] += 1
            y["budget"] += int(x.get("budget") or 0)
            y["votes"] += int(x.get("num_votes") or 0)
            y["projects"] += int(x.get("num_projects") or 0)
        u["votes"] += int(x.get("num_votes") or 0)
        u["projects"] += int(x.get("num_projects") or 0)
        if not u["latest"] or (x.get("date_end") or "") > (u["latest"].get("date_end") or ""):
            u["latest"] = {k: x.get(k) for k in ("name", "subunit", "instance", "budget", "num_projects", "num_votes",
                                                  "date_begin", "date_end", "ballot_type", "rule")}
    out = []
    for u in units.values():
        ys = sorted(u.pop("years"))
        u["first_year"], u["last_year"] = (ys[0], ys[-1]) if ys else (None, None)
        u["last_year_total"] = u["by_year"].get(str(ys[-1])) if ys else None
        out.append(u)
    out.sort(key=lambda u: -u["elections"])
    ok = bool(out)
    if not ok:
        out = prev.get("units", [])
    by_iso = {}
    for u in out:
        if u.get("iso3"):
            by_iso[u["iso3"]] = by_iso.get(u["iso3"], 0) + u["elections"]
    save("elections.json", {"updated_at": NOW.isoformat() if ok else prev.get("updated_at"), "source": "Pabulib",
                            "source_url": "https://pabulib.org/", "count": sum(u["elections"] for u in out),
                            "by_iso": by_iso, "units": out})
    health["pabulib"] = {"name": "Pabulib 투표 기록 DB", "ok": ok, "fetched": len(data), "total": sum(u["elections"] for u in out),
                         "checked_at": NOW.isoformat(), "error": err,
                         "last_success_at": NOW.isoformat() if ok else (health.get("pabulib") or {}).get("last_success_at")}
    log("pabulib", len(data), "elections", len(out), "units")
    return out


# 공식 플랫폼이 Decidim으로 운영되는 프로그램 → GraphQL API 주소
DECIDIM = {"fin-helsinki-omastadi": "https://omastadi.hel.fi/api",
           "usa-nyc-peoples-money": "https://www.participate.nyc.gov/api"}
CURRENCY = {"FIN": ("EUR", "€{:,}"), "POL": ("PLN", "{:,} zł"), "NLD": ("EUR", "€{:,}"), "FRA": ("EUR", "€{:,}"),
            "USA": ("USD", "${:,}")}


def fill_from_official(p):
    """seed에 '확인 중'인 예산 칸만 공식 API·투표 기록 값으로 채움. 사람이 적은 값은 덮어쓰지 않음."""
    if "확인 중" not in (p.get("budget") or {}).get("display", "확인 중"):
        return
    cur = CURRENCY.get(p["country_iso3"])
    cyc = next((c for c in (p.get("official_api") or {}).get("cycles", []) if c.get("budget_total")), None)
    if cyc and cur:
        p["budget"] = {"display": cur[1].format(cyc["budget_total"]) + f" ({cyc['title'] or cyc['slug']}, 공식 API)",
                       "amount": cyc["budget_total"], "currency": cur[0], "source": "official_api", "source_url": cyc["url"]}
        return
    lt = (p.get("pabulib") or {}).get("last_year_total")
    if lt and lt.get("budget") and cur:
        y = p["pabulib"]["last_year"]
        p["budget"] = {"display": cur[1].format(lt["budget"]) + f" ({y}년 {lt['elections']}개 투표 합계, Pabulib)",
                       "amount": lt["budget"], "currency": cur[0], "source": "pabulib", "source_url": "https://pabulib.org/"}
DECIDIM_Q = ('{ participatoryProcesses { slug startDate endDate title { translation(locale:"en") } components { '
             '__typename ... on Budgets { budgets { nodes { total_budget projects { selected budget_amount } } } } } } }')


def decidim_cycles(api: str):
    d = http_post_json(api, {"query": DECIDIM_Q})
    if d.get("errors"):
        raise RuntimeError(str(d["errors"])[:200])
    cycles = []
    for pr in (d.get("data") or {}).get("participatoryProcesses") or []:
        bs = [b for c in pr.get("components") or [] for b in (((c or {}).get("budgets") or {}).get("nodes") or [])]
        projs = [x for b in bs for x in (b.get("projects") or [])]
        cycles.append({
            "slug": pr.get("slug"), "title": ((pr.get("title") or {}).get("translation") or "")[:120],
            "start": pr.get("startDate"), "end": pr.get("endDate"),
            "budget_total": sum(int(b.get("total_budget") or 0) for b in bs) if bs else None,
            "areas": len(bs) or None, "projects": len(projs) or None,
            "selected": sum(1 for x in projs if x.get("selected")) if projs else None,
            "selected_amount": sum(int(x.get("budget_amount") or 0) for x in projs if x.get("selected")) if projs else None,
            "url": api.rsplit("/api", 1)[0] + f"/processes/{pr.get('slug')}"})
    return sorted(cycles, key=lambda c: c.get("start") or "", reverse=True)


def collect_decidim(programs, health):
    ok, errs = 0, []
    for p in programs:
        api = DECIDIM.get(p["id"])
        if not api:
            continue
        try:
            p["official_api"] = {"platform": "Decidim GraphQL", "api": api, "checked_at": NOW.isoformat(),
                                 "cycles": decidim_cycles(api)}
            ok += 1
        except Exception as e:  # noqa: BLE001
            errs.append(f"{p['id']}: {str(e)[:80]}")
            old = next((x for x in load("programs.json", {"items": []}).get("items", []) if x["id"] == p["id"]), {})
            if old.get("official_api"):
                p["official_api"] = old["official_api"]
    health["decidim"] = {"name": "Decidim 공식 플랫폼 API", "ok": ok > 0, "fetched": ok, "total": len(DECIDIM),
                         "checked_at": NOW.isoformat(), "error": "; ".join(errs)[:300] or None,
                         "last_success_at": NOW.isoformat() if ok else (health.get("decidim") or {}).get("last_success_at")}
    log("decidim", ok, "/", len(DECIDIM), errs)


def attach_registry(countries, programs, cases, units, ledger):
    """레지스트리 근거를 국가·프로그램에 붙이고, 모니터링 국가에 근거가 보이면 '검토 필요'만 표시."""
    seen = {e["key"] for e in ledger} | {k for e in ledger for k in e.get("keys", [])}
    fresh = []
    cby, uby = {}, {}
    for x in cases:
        if x.get("iso3"):
            cby.setdefault(x["iso3"], []).append(x)
    for u in units:
        if u.get("iso3"):
            uby.setdefault(u["iso3"], []).append(u)
    for c in countries:
        cs, us = cby.get(c["iso3"], []), uby.get(c["iso3"], [])
        c["registry"] = {"participedia": len(cs), "participedia_verified": sum(1 for x in cs if x["verified"]),
                         "pabulib": sum(u["elections"] for u in us), "pabulib_units": len(us)}
        c["review_hint"] = None
        if c["tracking_status"] == "monitoring" and (cs or us):
            c["review_hint"] = f"플랫폼 사례 {len(cs)}건" + (f" · 투표 기록 {c['registry']['pabulib']}회" if us else "")
            key = f"review:{c['iso3']}:{len(cs)}:{c['registry']['pabulib']}"
            if key not in seen:
                fresh.append({"key": key, "date": TODAY, "iso3": c["iso3"], "type": "검토 필요", "label": c["name_ko"],
                              "text": f"{c['name_ko']}: 모니터링 국가에서 {c['review_hint']} 확인 — 근거 상태 검토 대상",
                              "url": (cs[0]["url"] if cs else "https://pabulib.org/"), "observed_at": TODAY})
                seen.add(key)
    if len(fresh) > 5:  # 한꺼번에 많이 잡히면 원장에는 한 줄로 묶어 기록(뉴스 신호가 밀려나지 않게)
        site = os.environ.get("PB_SITE_URL", "https://ryc3030.github.io/pb-observatory/")
        ledger.append({"key": f"review-batch:{TODAY}", "keys": [e["key"] for e in fresh], "date": TODAY, "iso3": None,
                       "type": "검토 필요", "label": f"{len(fresh)}개국",
                       "text": f"모니터링 국가 {len(fresh)}곳에서 Participedia·Pabulib 근거 확인 — 근거 상태 검토 대상 "
                               f"({', '.join(e['label'] for e in fresh[:6])} 등)",
                       "url": site + "?status=review#explorer", "observed_at": TODAY})
    else:
        ledger.extend(fresh)
    for p in programs:
        kws = [k.lower() for k in p.get("keywords", []) if len(k) > 3]
        rxs = [re.compile(r"(?<!\w)" + re.escape(k) + r"(?!\w)", re.I) for k in kws]
        hit = [u for u in uby.get(p["country_iso3"], []) if (u.get("unit") or "").lower() in kws]
        p["pabulib"] = {k: v for k, v in hit[0].items() if k != "by_year"} if hit else None
        fill_from_official(p)
        p["cases"] = [{"title": x["title"], "url": x["url"], "updated": x["updated"]}
                      for x in cby.get(p["country_iso3"], [])
                      if any(r.search(x["title"]) for r in rxs) or (x["city"] or "").lower() in kws][:3]
    save("countries.json", {"updated_at": NOW.isoformat(), "count": len(countries), "items": countries})


def main():
    DATA.mkdir(exist_ok=True)
    seed = load("countries.seed.json", [])
    programs = load("programs.seed.json", [])
    match = build_matcher(seed)
    health = load("health.json", {})
    ledger = load("ledger.json", [])

    for c in seed:
        for a in [c["name_en"], *c.get("aliases", [])]:
            NAME_ISO.setdefault(a.strip().lower(), c["iso3"])

    news, added = collect_news(seed, match, health)
    papers = collect_papers(health)
    countries = build_countries(seed, news, papers, ledger)
    cases = collect_participedia(health)
    units = collect_pabulib(health)
    collect_decidim(programs, health)
    attach_registry(countries, programs, cases, units, ledger)
    attach_program_news(programs, news)
    write_feed(news, countries)
    snapshot_history(countries, news, papers, programs)

    ledger = sorted(ledger, key=lambda e: (e["date"], e.get("observed_at") or ""), reverse=True)[:1500]
    save("ledger.json", ledger)
    health["build"] = {"name": "일일 빌드", "ok": True, "checked_at": NOW.isoformat(), "last_success_at": NOW.isoformat()}
    save("health.json", health)
    save("meta.json", {
        "updated_at": NOW.isoformat(), "version": "4.0",
        "counts": {"countries": len(countries), "programs": len(programs), "news": len(news),
                   "papers": len(papers), "ledger": len(ledger), "news_added_today": added,
                   "cases": len(cases), "elections": sum(u["elections"] for u in units)},
    })
    log("translated", "news", sum(1 for x in news if x.get("title_ko")), "papers", sum(1 for x in papers if x.get("title_ko")))
    log("done")


if __name__ == "__main__":
    main()
