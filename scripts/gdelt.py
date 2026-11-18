#!/usr/bin/env python3
"""GDELT DOC 2.0 수집기 — 하루에 요청 한 건만 보낸다.

GDELT는 같은 IP의 반복 호출을 막는다(429). GitHub Actions 러너는 여러 사용자가 IP를 나눠 쓰므로
재시도할수록 더 막히기 쉽다. 그래서 이 스크립트는
  - 하루(UTC)에 한 번만 시도한다. 같은 날 다시 실행하면 요청 없이 끝난다(PB_GDELT_FORCE=1이면 예외).
  - 요청은 한 건, 재시도 없음.
  - 검색 기간은 마지막 성공 시점부터 지금까지로 잡아(최대 90일) 실패한 날의 기사도 다음 성공 때 함께 받는다.
  - GDELT는 65개 언어 기사를 영어로 기계 번역해 검색하므로 영어 검색어 하나로 여러 언어 기사를 찾는다.
가져온 기사는 data/news.json에 합치고, 상태는 data/health.json의 gdelt 항목과 data/gdelt_state.json에 남긴다.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import collect as C  # noqa: E402

QUERY = '("participatory budgeting" OR "participatory budget")'
UA = "PB-Observatory/4.1 (+https://github.com/ryc3030/pb-observatory; one request per day)"
FIRST_DAYS = 30
MAX_DAYS = 90


def state_load():
    return C.load("gdelt_state.json", {"last_attempt": None, "last_success": None, "fails_in_row": 0, "history": []})


def timespan_days(st) -> int:
    if not st.get("last_success"):
        return FIRST_DAYS
    gap = (C.NOW - datetime.fromisoformat(st["last_success"])).total_seconds() / 86400
    return max(1, min(MAX_DAYS, math.ceil(gap + 0.25)))  # 6시간 겹쳐 빠짐 방지


def request(days: int):
    url = "https://api.gdeltproject.org/api/v2/doc/doc?" + urllib.parse.urlencode(
        {"query": QUERY, "mode": "artlist", "format": "json", "maxrecords": 250, "timespan": f"{days}d", "sort": "datedesc"})
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read().decode("utf-8", "ignore").strip()
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except Exception as e:  # noqa: BLE001
        return None, str(e)[:120]
    if not body:
        return [], None  # 결과 0건이면 빈 응답이 온다
    try:
        return json.loads(body).get("articles", []), None
    except ValueError:
        return None, "JSON 아님: " + body[:120]  # 검색식 오류 등은 일반 텍스트로 온다


def to_rows(arts):
    rows = []
    for a in arts:
        title = C.clean(a.get("title") or "")
        link = a.get("url") or ""
        # GDELT는 본문(번역문)에서 찾으므로 제목이나 주소에도 PB 용어가 있는 기사만 남긴다
        if not title or not (C.PB_TERMS.search(title) or C.PB_TERMS.search(link.replace("-", " ").replace("_", " "))):
            continue
        try:
            pub = datetime.strptime(a["seendate"], "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc).isoformat()
        except Exception:  # noqa: BLE001
            pub = C.NOW.isoformat()
        dom = a.get("domain") or urllib.parse.urlparse(link).hostname or ""
        nid = hashlib.sha1((re.sub(r"\W+", "", title.lower()) + "|" + dom.lower()).encode()).hexdigest()[:14]
        rows.append({"id": nid, "title": title, "title_ko": None, "lang": C.GDELT_LANG.get(a.get("language", ""), "en"),
                     "source": dom, "url": link, "source_url": "https://" + dom, "gl": "", "default_iso": None,
                     "published_at": pub, "src_country": a.get("sourcecountry") or None,
                     "src_country_iso": C.name_iso(a.get("sourcecountry")), "collected_at": C.NOW.isoformat(),
                     "kind": "signal", "via": "GDELT"})
    return rows


def main():
    st = state_load()
    force = os.environ.get("PB_GDELT_FORCE") == "1"
    if (st.get("last_attempt") or "")[:10] == C.TODAY and not force:
        C.log("gdelt: 오늘 이미 요청함 — 건너뜀")
        return
    seed = C.load("countries.seed.json", [])
    for c in seed:
        for a in [c["name_en"], *c.get("aliases", [])]:
            C.NAME_ISO.setdefault(a.strip().lower(), c["iso3"])
    match = C.build_matcher(seed)
    health = C.load("health.json", {})
    days = timespan_days(st)
    arts, err = request(days)
    st["last_attempt"] = C.NOW.isoformat()
    added = 0
    if arts is not None:
        nd = C.load("news.json", {"items": []})
        items = nd.get("items", [])
        ids = {x["id"] for x in items}
        titles = {C.norm_title(x["title"]) for x in items}
        rows = to_rows(arts)
        for r in rows:
            k = C.norm_title(r["title"])
            if r["id"] in ids or k in titles:
                continue
            r["country_iso3"], r["iso_basis"] = C.tag_country(r, match)
            if C.TRANSLATE and r["lang"] != "ko" and added < 60:
                r["title_ko"] = C.to_ko(r["title"], r["lang"])
                r["_tr_tried"] = r["title_ko"] is not None
            items.append(r)
            ids.add(r["id"])
            titles.add(k)
            added += 1
        items.sort(key=lambda x: x["published_at"], reverse=True)
        nd.update({"updated_at": C.NOW.isoformat(), "count": len(items), "items": items})
        C.save("news.json", nd)
        st["last_success"] = C.NOW.isoformat()
        st["fails_in_row"] = 0
        C.log("gdelt ok", days, "일 범위", len(arts), "건 중 PB 기사", len(rows), "새로 추가", added)
    else:
        st["fails_in_row"] = st.get("fails_in_row", 0) + 1
        C.log("gdelt 실패", err)
    st["history"] = ([{"at": st["last_attempt"], "ok": arts is not None, "days": days,
                       "fetched": len(arts) if arts is not None else 0, "added": added, "error": err}]
                     + st.get("history", []))[:30]
    C.save("gdelt_state.json", st)
    health["gdelt"] = {"name": "GDELT DOC 2.0 (하루 1회 요청)", "ok": arts is not None, "queries_ok": 1 if arts is not None else 0,
                       "queries": 1, "fetched": added, "checked_at": C.NOW.isoformat(), "error": err,
                       "fails_in_row": st["fails_in_row"], "timespan_days": days,
                       "last_success_at": st.get("last_success")}
    C.save("health.json", health)


if __name__ == "__main__":
    main()
