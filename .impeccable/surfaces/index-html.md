---
version: 1
slug: "index-html"
primary_target: "index.html"
related_targets: []
---

# Surface brief: index.html (관측소 대시보드)

Mode: Operate. 사무실 낮 시간 데스크톱(연구자·공무원)과 낮 시간 휴대폰(시민·언론). 밝은 화면 기본, 어두운 화면 지원.
Task: 오늘 들어온 신호 훑기 → 국가·프로그램 근거 확인 → 원문 출처로 이동. 근거와 신호를 혼동하지 않는 것이 성공.
Untouched: 데이터 구조(data/*.json), 원칙 문구, 주소 공유·RSS·CSV, WCAG AA.
Build path: code-led (이미지 생성 없음).

## Direction contract
THESIS: 참여예산의 의식은 '투표'다. 모든 근거 레코드는 투표용지의 한 줄이고, 근거 상태는 기표란에 찍힌 도장으로 읽는다. 다크 지도 + KPI 카드 + 신문형 뉴스라는 범주 기본 배치를 거부한다.
OWN-WORLD: 흰 용지(#FFFFFF) 위 먹색 글자(#14181D), 행을 가르는 굵은 먹선, 셸은 기표소 남색(#1B2A4A). 인주 주홍(#D3261C)은 '공식·검증' 도장에만, 문헌은 같은 도장의 테두리만, 모니터링은 빈 점선 기표란. 신호(뉴스·논문)는 개표 청색(#1F5FBF) 한 색만 쓰고 근거 표시에는 쓰지 않는다(오리엔티어링 지도에서 가져온 규율: 바탕 층은 신호 층이 덮어쓰지 못한다). 서체 Pretendard 하나, 숫자는 모두 고정폭(데이터마틱스에서 가져온 규율: 숫자 밀도를 겁내지 않는다).
STORY: 첫 화면에서 '어디가 공식으로 확인됐고, 오늘 무슨 신호가 들어왔나'를 안다. 행을 펼쳐 필드별 출처를 확인하고 원문으로 간다.
FIRST VIEWPORT: 남색 셸(로고 도장·탭 내비·검색·화면 모드) 아래 갱신 상태 줄. 왼쪽 8칸 지도(밝은 바탕, 국가는 도장 상태 기호), 오른쪽 4칸 '근거 집계 용지'(기호·구분·국가 수·기표란 3행 + 30일 신호 행)와 '오늘 들어온 신호' 5건. 주 행동은 집계 행 클릭 = 탐색기 필터.
FORM: 투표용지·기표, 내 목록 1순위(IMPECCABLE'S PICK). seed:d8017aef27db0691. 시그니처: 기표란 열과 卜 도장 — 국가·프로그램 행 오른쪽 기표란에 상태가 찍히고, 필터를 바꾸면 해당 도장이 눌리듯 찍힌다(180ms). 탭을 바꿔도 셸·필터는 그대로(콘솔에서 가져온 규율).
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
