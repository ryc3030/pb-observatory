#!/usr/bin/env python3
"""Claude 아티팩트 버전 만들기.

아티팩트는 외부 데이터·지도 타일·외부 글꼴을 불러올 수 없으므로,
메인 사이트(index.html, assets/)를 그대로 가져와 다음만 바꿉니다.
  - 글꼴: Google Fonts의 Noto Sans KR(아티팩트가 허용하는 유일한 외부 글꼴)
  - 지도: CARTO 타일 대신 artifact/assets/world.json 바탕 지도
  - 지도 스타일시트: 직접 쓴 artifact/assets/map.css
  - CSV 내려받기 → CSV 복사(아티팩트는 다운로드를 막음)
  - RSS·데이터 링크 → GitHub 주소
결과: artifact/index.html, artifact/assets/{style.css,app.js}, artifact/data/*.json
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "artifact"
SITE = "https://ryc3030.github.io/pb-observatory/"
REPO = "https://github.com/ryc3030/pb-observatory"
DATA_FILES = ["meta.json", "countries.json", "programs.json", "news.json", "papers.json",
              "ledger.json", "health.json", "history.json", "timeline.json", "cases.json", "elections.json"]


def sub(text: str, old: str, new: str) -> str:
    if old not in text:
        raise SystemExit(f"build_artifact: 바꿀 문자열을 찾지 못함: {old[:70]!r}")
    return text.replace(old, new)


def build_html() -> None:
    h = (ROOT / "index.html").read_text("utf-8")
    h = sub(h, '<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>\n', "")
    h = sub(h, '<link rel="preconnect" href="https://basemaps.cartocdn.com" crossorigin>\n', "")
    h = sub(h, '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">',
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&display=swap">')
    h = sub(h, '<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@5.7.1/dist/maplibre-gl.css">',
            '<link rel="stylesheet" href="assets/map.css">')
    h = sub(h, '<link rel="icon" href="assets/stamp.svg" type="image/svg+xml">\n', "")
    h = sub(h, 'href="feed.xml"><svg', f'href="{SITE}feed.xml"><svg')
    h = sub(h, 'href="feed.xml">', f'href="{SITE}feed.xml">')
    h = sub(h, '<svg aria-hidden="true"><use href="#i-down"/></svg>CSV 내려받기', '<svg aria-hidden="true"><use href="#i-down"/></svg>CSV 복사')
    for f in ["countries", "programs", "news", "papers"]:
        h = sub(h, f'href="data/{f}.json"', f'href="{REPO}/blob/main/data/{f}.json"')
    h = sub(h, '<b>세계 참여예산 관측소 v4</b>', '<b>세계 참여예산 관측소 v4</b> · Claude 아티팩트판')
    h = sub(h, '<p>완전성보다 먼저 검증 가능성을 확보합니다.</p>',
            f'<p>완전성보다 먼저 검증 가능성을 확보합니다. 원본 사이트: <a href="{SITE}">{SITE.replace("https://", "")}</a></p>')
    (OUT / "index.html").write_text(h, "utf-8")


def build_css() -> None:
    c = (ROOT / "assets/style.css").read_text("utf-8")
    # 아티팩트는 Google Fonts만 외부 글꼴로 허용 → Noto Sans KR을 앞에 둠
    c = sub(c, '--font:"Pretendard Variable",Pretendard,', '--font:"Noto Sans KR","Pretendard Variable",Pretendard,')
    # 자체 호스팅 표제 서체(Paperlogy)는 아티팩트에 싣지 않음 → @font-face를 빼고 Noto Sans KR로 대체
    c = re.sub(r'@font-face\{font-family:"Paperlogy";[^}]*\}\n', "", c)
    c = sub(c, '--display:"Paperlogy",', '--display:"Noto Sans KR",')
    (OUT / "assets/style.css").write_text(c, "utf-8")


def build_js() -> None:
    j = (ROOT / "assets/app.js").read_text("utf-8")
    j = sub(j, 'const mapStyle = () => `https://basemaps.cartocdn.com/gl/${isDark() ? "dark-matter" : "positron"}-gl-style/style.json`;',
            '''const mapStyle = () => {
  const d = isDark();
  return { version: 8, sources: { world: { type: "geojson", data: new URL("assets/world.json", location.href).href } },
    layers: [
      { id: "bg", type: "background", paint: { "background-color": d ? "#1b222b" : "#eef1f4" } },
      { id: "land", type: "fill", source: "world", paint: { "fill-color": d ? "#2a333e" : "#ffffff" } },
      { id: "border", type: "line", source: "world", paint: { "line-color": d ? "#3d4754" : "#c9d0d8", "line-width": 0.6 } },
    ] };
};''')
    j = sub(j, 'history.replaceState(null, "", location.pathname + (qs ? "?" + qs : "") + location.hash);',
            'try { history.replaceState(null, "", location.pathname + (qs ? "?" + qs : "") + location.hash); } catch {}')
    # 아티팩트는 다운로드를 막으므로 CSV는 클립보드로 복사
    j = sub(j, '''    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob(["\ufeff" + csv], { type: "text/csv" }));
    a.download = "global-pb-observatory-programs.csv"; a.click(); URL.revokeObjectURL(a.href);''',
            '''    const btn = $("#csv"), label = btn.lastChild;
    navigator.clipboard.writeText(csv).then(() => { label.nodeValue = "복사됨 — 스프레드시트에 붙여 넣으세요"; },
      () => { label.nodeValue = "복사하지 못함 — GitHub의 data 폴더를 이용하세요"; })
      .finally(() => setTimeout(() => (label.nodeValue = "CSV 복사"), 3500));''')
    (OUT / "assets/app.js").write_text(j, "utf-8")


def copy_data() -> None:
    (OUT / "data").mkdir(parents=True, exist_ok=True)
    for f in DATA_FILES:
        src = ROOT / "data" / f
        if f == "news.json":  # 화면에 쓰지 않는 필드만 덜어 냄
            d = json.loads(src.read_text("utf-8"))
            for it in d["items"]:
                for k in ("_tr_tried", "collected_at", "gl", "default_iso", "source_url"):
                    it.pop(k, None)
            (OUT / "data" / f).write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")), "utf-8")
        else:
            shutil.copy(src, OUT / "data" / f)


if __name__ == "__main__":
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    build_html(); build_css(); build_js(); copy_data()
    print("artifact/ built")
