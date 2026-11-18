# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
- 연구자·대학원생: 국가·도시별 참여예산 제도 근거와 최신 논문을 찾고, 출처를 따라가 인용한다.
- 공무원·정책 담당자(한국 국민참여예산·주민참여예산 실무 포함): 해외 제도와 운영 동향을 비교하고 한국 동향을 빠르게 확인한다.
- 일반 시민·언론: 오늘 전 세계 참여예산에서 무슨 일이 있었는지 한눈에 보고 원문 기사로 이동한다.
모두 한국어 사용자이며, 원문은 24개 언어다.

## Product Purpose
92개국 참여예산(PB) 제도·프로그램의 근거를 국가→관할→프로그램 단위로 추적하고, 다국어 뉴스와 최신 연구를 매일 자동 수집해 누구나 무료로 볼 수 있게 한다. 성공은 "검증된 근거"와 "자동 수집 신호"를 혼동하지 않고 원문 출처까지 도달하는 것이다.

## Positioning
뉴스·검색 결과를 제도 판단에 섞지 않는다. 국가 근거 상태(공식/검증·문헌·플랫폼·탐색 모니터링)는 사람이 검토해 올리고, 매일 들어오는 뉴스·논문은 '신호'로 분리해 보여 준다. 필드(예산·참여·단계·법적근거)마다 출처를 붙이고, 확인 안 된 값은 "확인 중"으로 둔다.

## Operating Context
- 정적 사이트(GitHub Pages, https://ryc3030.github.io/pb-observatory/). GitHub Actions가 매일 06:17 KST에 scripts/collect.py를 돌려 data/*.json과 feed.xml을 갱신한다.
- 수집원: Google News RSS(24개 언어 검색어), OpenAlex·Crossref, 자동 번역(Google→MyMemory 대체).
- 사람이 고치는 파일: data/countries.seed.json, data/programs.seed.json.
- 링크 공유(주소에 필터·열린 국가), RSS 구독, CSV 내려받기, JSON 자유 이용.

## Capabilities and Constraints
- 빌드 도구 없음: index.html + assets/(CSS·JS) + data/. 외부 라이브러리는 MapLibre GL(지도)만.
- 92개국 레지스트리, 프로그램 39건(대부분 수치 "확인 중"), 뉴스 약 500건(최근 30일), 논문 약 220편.
- 자동 번역 제목은 원문과 함께 보여야 한다.
- 역사적 기준선: World Atlas 2019의 11,690–11,825건(현재 수와 합산하지 않음).

## Brand Commitments
- 이름: 세계 참여예산 관측소 (Global Participatory Budgeting Observatory).
- 원칙 문구: 근거 우선 · 필드 단위 출처 · 자동값/검증값 분리 · 뉴스 신호 ≠ 전수 통계.

## Evidence on Hand
실데이터는 data/ 폴더뿐이다. 이용자 수, 기관 협력, 추천사 등은 없으며 만들어 넣지 않는다.

## Product Principles
1. 근거와 신호를 섞지 않는다.
2. 모든 숫자는 출처까지 한 번에 간다.
3. 모르는 값은 모른다고 쓴다("확인 중").
4. 한국 사용자가 해외 동향을 한국어로 빠르게 훑고, 원문으로 깊게 들어갈 수 있어야 한다.

## Accessibility & Inclusion
WCAG 2.1 AA. 밝은·어두운 화면 모두 axe 위반 0건을 유지한다.
