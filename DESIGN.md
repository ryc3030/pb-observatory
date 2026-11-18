---
name: 세계 참여예산 관측소
description: 92개국 참여예산의 근거는 투표용지의 한 줄로, 근거 상태는 기표란의 도장으로 읽는 관측 대시보드
colors:
  paper: "#ffffff"
  hover: "#f3f5f8"
  ink: "#14181d"
  ink-2: "#39414b"
  muted: "#58616c"
  rule: "#14181d"
  hair: "#d6dbe1"
  hair-2: "#e7eaee"
  shell: "#1b2a4a"
  shell-2: "#25385f"
  shell-ink: "#eef2f8"
  shell-muted: "#b6c1d6"
  seal: "#c9241b"
  docu: "#2e3a4d"
  signal: "#1d5bb8"
  signal-soft: "#e5eefb"
  ok: "#1f7a4d"
  focus: "#1b2a4a"
typography:
  display:
    fontFamily: "Paperlogy, Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, Apple SD Gothic Neo, Malgun Gothic, system-ui, sans-serif"
    fontSize: "30px"
    fontWeight: 800
    lineHeight: 1.25
    letterSpacing: "-0.025em"
    fontFeature: "\"tnum\" 1"
  headline:
    fontFamily: "Paperlogy, Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, Apple SD Gothic Neo, Malgun Gothic, system-ui, sans-serif"
    fontSize: "24px"
    fontWeight: 800
    letterSpacing: "-0.02em"
    fontFeature: "\"tnum\" 1"
  title:
    fontFamily: "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, Apple SD Gothic Neo, Malgun Gothic, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 700
    lineHeight: 1.45
    fontFeature: "\"tnum\" 1"
  body:
    fontFamily: "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, Apple SD Gothic Neo, Malgun Gothic, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.6
    fontFeature: "\"tnum\" 1"
  meta:
    fontFamily: "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, Apple SD Gothic Neo, Malgun Gothic, system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.5
    fontFeature: "\"tnum\" 1"
  label:
    fontFamily: "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, Apple SD Gothic Neo, Malgun Gothic, system-ui, sans-serif"
    fontSize: "12.5px"
    fontWeight: 700
    fontFeature: "\"tnum\" 1"
  count:
    fontFamily: "Pretendard Variable, Pretendard, -apple-system, BlinkMacSystemFont, Apple SD Gothic Neo, Malgun Gothic, system-ui, sans-serif"
    fontSize: "22px"
    fontWeight: 800
    fontFeature: "\"tnum\" 1"
rounded:
  ballot: "0px"
  slot: "2px"
  control: "4px"
  pill: "999px"
spacing:
  s1: "4px"
  s2: "8px"
  s3: "12px"
  s4: "16px"
  s5: "24px"
  s6: "32px"
  s7: "48px"
  s8: "72px"
components:
  shell:
    backgroundColor: "{colors.shell}"
    textColor: "{colors.shell-ink}"
    height: "60px"
  shell-search:
    backgroundColor: "{colors.shell-2}"
    textColor: "{colors.shell-ink}"
    rounded: "{rounded.control}"
    height: "36px"
  statusline:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.muted}"
    typography: "{typography.meta}"
  ballot-row:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.ballot}"
    padding: "12px 16px"
  ballot-row-hover:
    backgroundColor: "{colors.hover}"
  slot-seal:
    textColor: "{colors.seal}"
    rounded: "{rounded.slot}"
    size: "48px"
  slot-docu:
    textColor: "{colors.docu}"
    rounded: "{rounded.slot}"
    size: "48px"
  slot-monitoring:
    textColor: "{colors.muted}"
    rounded: "{rounded.slot}"
    size: "48px"
  country-row:
    backgroundColor: "{colors.paper}"
    rounded: "{rounded.ballot}"
    padding: "12px 16px"
  country-row-open:
    backgroundColor: "{colors.hover}"
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.control}"
    padding: "0 16px"
    height: "40px"
  button-primary-hover:
    backgroundColor: "{colors.ink-2}"
  button-ghost:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "0 16px"
    height: "40px"
  field:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "0 10px"
    height: "40px"
  quick-chip:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink-2}"
    rounded: "{rounded.pill}"
    padding: "4px 10px"
  quick-chip-pressed:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  signal-badge:
    backgroundColor: "{colors.signal-soft}"
    textColor: "{colors.signal}"
    rounded: "{rounded.pill}"
    padding: "1px 7px"
  filterbar:
    backgroundColor: "{colors.paper}"
    rounded: "{rounded.ballot}"
    padding: "16px"
---

# Design System: 세계 참여예산 관측소

## Overview

**Creative North Star: "투표용지와 기표"**

참여예산의 의식은 투표다. 이 화면에서 모든 근거 레코드는 투표용지의 한 줄이고, 근거 상태는 그 줄 오른쪽 기표란에 찍힌 卜 도장으로 읽는다. 흰 용지 위에 먹색 글자를 쓰고, 행과 행은 굵은 먹선으로 가르며, 화면 맨 위 남색 셸은 기표소 칸막이다. 인주 주홍은 '공식·검증' 도장 한 가지에만 쓰고, 문헌 근거는 같은 도장을 먹색 테두리로만 찍으며, 탐색 모니터링은 아무것도 찍히지 않은 점선 기표란으로 남긴다.

매일 들어오는 뉴스와 논문은 '신호'다. 신호는 개표 청색 한 색으로만 표시하고 근거 표시에는 끼어들지 않는다. 지도에서도 신호 고리는 도장 층 아래에 얇고 옅게 깔린다. 바탕 층(근거)을 신호 층이 덮어쓰지 못한다는 규율이 색과 층 순서 모두에 걸려 있다.

밀도는 높다. 연구자와 실무자가 사무실 데스크톱에서 숫자와 출처를 훑는 화면이라, 숫자는 모두 고정폭으로 맞추고 표·목록이 장식 없이 이어진다. 그림자와 카드 대신 선 굵기(1px 실선, 1.5px 테두리, 2px 행 구분, 3px 머리선)로 위계를 만든다.

**Key Characteristics:**
- 흰 용지 바탕 + 먹색 글자 + 남색 기표소 셸, 세 겹으로 끝나는 바탕
- 기표란 열: 국가·프로그램·집계 행의 오른쪽 끝에 도장 상태가 찍힌다
- 색은 의미에만: 주홍 = 공식·검증, 청색 = 신호, 그 밖의 모든 것은 먹색 계열
- 선 굵기 위계(1 / 1.5 / 2 / 3px)가 그림자를 대신한다
- 서체는 둘: 표제(제목·연도·큰 숫자)는 Paperlogy, 본문·표·입력은 Pretendard. 숫자는 전부 고정폭
- 움직임은 단 하나: 필터를 바꿀 때 도장이 눌리듯 찍히는 200ms

## Colors

먹과 용지의 무채색 위에, 의미가 정해진 두 색(인주 주홍, 개표 청색)만 얹는다.

### Primary
- **인주 주홍** (`seal`): '공식·검증' 도장 전용. 기표란 도장, 지도 공식 도장, 범례의 공식 기호, 본문에서 도장을 설명하는 인라인 도장(`inline-stamp`)에만 칠한다. 브랜드 로고도 이 도장 자체라 같은 계열의 밝은 주홍(#f0574c, 남색 셸 위)으로 찍힌다.

### Secondary
- **개표 청색** (`signal`): 뉴스·논문 신호 전용. 30일 신호 수, 지도의 신호 고리, 범례의 신호 기호, 뉴스 신호 태그(`sigtag`), 논문 배지, 뉴스·논문 제목 링크의 hover, 관측 추이 그래프의 '30일 뉴스' 선. 링크의 기본색도 이 색이지만, 기본 링크가 신호 층(기사·논문 원문)에 속하기 때문이다.
- **신호 옅은 바탕** (`signal-soft`): 논문 배지 바탕 하나에만 쓴다.

### Neutral
- **용지** (`paper`): 모든 바탕. 페이지, 패널, 투표용지, 필터 막대, 표 머리.
- **먹** (`ink`): 본문 글자, 기본 버튼 바탕, 완성도·집계 막대 채움, 확인된 필드 점.
- **먹선** (`rule`): 투표용지 테두리와 행 구분선. 밝은 화면에서는 먹과 같은 값이고 어두운 화면에서 따로 밝아진다.
- **엷은 먹** (`ink-2`): 보조 본문, 설명 문단, 필드 라벨, 메타 중 강조(국가명).
- **회먹** (`muted`): 메타 정보, 날짜, '확인 중' 값, 모니터링 점선 기표란, placeholder.
- **문헌 먹** (`docu`): 문헌·플랫폼 도장(기표란·지도·범례). 어두운 화면에서는 밝은 회색으로 뒤집힌다.
- **실선** (`hair`): 목록 항목 사이 1px 선, 입력 테두리, 패널 머리 아래선.
- **옅은 실선** (`hair-2`): 막대 그래프의 빈 트랙.
- **행 hover** (`hover`): 투표용지 행·국가 행·데이터 표 행 hover, 펼친 국가 행.
- **기표소 남색** (`shell`) / **기표소 남색 2** (`shell-2`): 상단 셸과 푸터 / 셸 검색창 바탕·셸 버튼 hover.
- **셸 글자** (`shell-ink`), **셸 회색** (`shell-muted`): 셸 위 글자, 비활성 탭·placeholder.
- **정상 녹색** (`ok`): 갱신 상태 줄의 살아 있음 점과 수집 상태 정상 점 두 곳뿐.
- **포커스** (`focus`): 포커스 외곽선. 밝은 화면은 남색, 어두운 화면은 거의 흰색.

`--seal-soft`, `--warn`, `--ground`는 정의돼 있으나 화면에 쓰이지 않거나(앞의 둘) `paper`와 같은 값이라 체계에 올리지 않았다.

### Named Rules
**인주는 공식에만 Rule.** 주홍은 '공식·검증' 도장과 그 도장으로 된 로고에만 쓴다. 경고, 강조, 활성 상태, 오류 표시에 주홍을 빌려 쓰지 않는다.

**신호는 근거를 덮지 못한다 Rule.** 청색은 뉴스·논문 신호에만 쓰고 근거 상태 표시에는 절대 쓰지 않는다. 지도에서 신호 층은 도장 층 아래, 1.2px·불투명도 0.7로 깔린다.

**출처는 먹 밑줄 Rule.** 근거의 출처 링크(`src`: 국가 기준 근거 '출처', 비교표 '원문')는 먹색 글자에 회먹 밑줄, hover 때 밑줄만 먹으로 진해진다. 프로그램 출처 링크와 원장·참고문헌 링크도 먹색이다. 근거 쪽 링크를 청색으로 칠하면 신호처럼 보인다.

## Typography

**Display Font:** Paperlogy 700·800 (자체 호스팅 woff2 서브셋: 라틴 + KS X 1001 한글 2,350자 + 사이트 문구, 각 약 110KB; 없으면 Pretendard로 대체)
**Body Font:** Pretendard Variable (jsDelivr 동적 서브셋)

**Character:** 표제만 Paperlogy(한글은 G마켓 산스, 라틴은 Montserrat 계열)로 투표용지 머리글처럼 단단하게 세우고, 읽는 글과 표는 Pretendard로 담백하게 둔다. 적용 대상: 첫 제목, 섹션 제목, 패널 머리, 연표 시대 제목과 연도, 집계 큰 숫자, 브랜드명. 뉴스·논문·국가 이름처럼 매일 바뀌는 글은 서브셋 밖 글자가 나올 수 있어 Pretendard로 둔다. 에스코어 드림은 라이선스가 글꼴 파일 수정(서브셋·변환)을 금해 웹에는 싣지 않았다. Claude 아티팩트판은 외부 글꼴이 Google Fonts로 제한돼 Noto Sans KR로 대체한다.

### Hierarchy
- **Display** (800, 30px, 1.25, -0.025em; 640px 이하 25px): 페이지 첫 제목 하나.
- **Headline** (800, 24px, -0.02em): 섹션 제목(PB 데일리, 논문, 국가·프로그램 근거, 분석, 근거·출처).
- **Title** (700, 16px, 1.45): 패널 머리(근거 지도, 근거 집계), 뉴스·논문 제목, 국가 행 이름. 프로그램 제목은 15px, 소제목(h3)은 13–15px.
- **Body** (400, 15px, 1.6): 기본 본문. 첫 화면 소개 문단은 16px/1.7, 68ch까지. 섹션 설명은 70ch, 논문 초록은 80ch에 2줄 자름.
- **Meta** (400, 13px; 12.5px 변형): 날짜·출처·국가 메타, 결과 줄, 범례, 원문 제목(13.5px).
- **Label** (700, 12.5px): 필터 필드 라벨.
- **Count** (800, 22px, tabular): 집계 행의 국가 수. 기호 번호 20px/700, 분석 큰 수 26px/800, 집계 총수 20px.

### Named Rules
**숫자는 고정폭 Rule.** `body` 전체에 `"tnum" 1`을 걸고, 숫자 요소에는 `font-variant-numeric: tabular-nums`를 다시 건다. 날짜(`time`), 개수, 비율은 세로로 줄이 맞아야 한다.

**어절은 끊지 않는다 Rule.** 본문은 `word-break: keep-all` + `overflow-wrap: break-word`. 제목은 `text-wrap: balance`. 다국어 원문 제목·URL처럼 긴 문자열만 `overflow-wrap: anywhere`로 푼다.

**자동 번역은 원문과 함께 Rule.** 번역 제목(Title) 바로 아래 원문 제목을 Meta 크기 회먹으로 붙인다.

## Layout

- **용기:** 내용 폭 `min(1240px, 100% - 48px)`, 640px 이하는 좌우 16px 여백. 셸 안쪽도 같은 폭.
- **간격 리듬:** 4·8·12·16·24·32·48·72px(`s1`–`s8`). 섹션 위아래 48px, 섹션 머리 아래 24px, 행 안쪽 12px 16px.
- **첫 화면 판:** 지도(유연 폭)와 투표용지(380px) 두 칸, 간격 16px, 높이 맞춤. 지도 패널 최소 520px. 아래 관측 원칙 4칸.
- **PB 데일리:** 왼쪽 필터 막대 260px(셸 아래 76px에 sticky) + 오른쪽 목록.
- **탐색기:** 가로 필터 막대(3 선택 + 검색 + 버튼) 위, 투표용지 표 아래.
- **붙는 요소:** 셸은 top 0 sticky(높이 60px). 뉴스 날짜 머리는 셸 바로 아래(60px, 640px 이하 118px) sticky. 섹션 앵커는 72px(860px 이하 120px) 띄워 멈춘다.

### 반응형 구간
- **1100px 이하:** 판이 한 열로(지도 위, 투표용지 아래), 원칙 2칸, 가로 필터 3칸, 탭 간격 축소.
- **860px 이하:** 셸이 두 줄로 접히고 탭은 가로 스크롤 줄(높이 44px, 오른쪽 15% 페이드 마스크). PB 데일리 두 칸이 한 열, 필터 sticky 해제.
- **640px 이하:** 검색창이 셸 셋째 줄 전체 폭, 로고 영문 부제 숨김. 국가 행은 이름+사실 / 기표란 두 칸으로 줄고 번호·날짜 열 숨김. 논문 행 한 열. 버튼·필드 최소 높이 44px. 갱신 상태 줄은 블록으로 줄바꿈.

## Elevation & Depth

평면이다. 위계는 그림자가 아니라 먹선의 굵기로 만든다. 패널·행·표 어디에도 그림자를 쓰지 않는다. 그림자는 화면 위에 잠깐 떠오르는 것, 즉 '본문 바로가기' 링크와 지도 팝업 두 곳에만 있다.

### Shadow Vocabulary
- **떠 있는 것** (`box-shadow: 0 1px 2px rgba(20,24,29,.06), 0 4px 14px rgba(20,24,29,.06)`; 어두운 화면 `0 1px 2px rgba(0,0,0,.3), 0 6px 18px rgba(0,0,0,.25)`): 바로가기 링크, 지도 팝업.

### Named Rules
**선 굵기가 위계 Rule.** 1px `hair` = 같은 묶음 안 항목 사이. 1.5px `rule` = 투표용지·지도 패널 테두리, 기표란 테두리. 2px `rule` = 투표용지 행 사이, 국가 행 사이, 뉴스 날짜 머리, 표 머리 아래, 집계표 묶음 머리. 3px `rule` = 용지 머리선(투표용지 머리 아래, 신호 상자 위, 뉴스·논문·국가 표·데이터 표·근거 열의 맨 위).

## Shapes

투표용지는 각이 서 있다. 지도 패널, 투표용지, 필터 막대, 국가 표는 반경 0. 기표란은 거의 각진 2px. 조작 요소(버튼, 입력, 셸 검색창, 셸 버튼, 팝업)만 4px로 손에 잡히게 둥글린다. 알약형(999px)은 뉴스 빠른 국가 칩과 논문 배지 두 가지뿐이다.

도장은 원 + 卜 획이다. 기표란 안의 도장은 늘 -3도 기울어져 있고, 지도의 도장은 -6도로 기운다. 사람이 손으로 찍은 흔적이다. 모니터링 기표란은 점선 사각형(1.5px dashed)으로, 찍힌 것이 없다.

## Components

### 셸 (Navigation)
기표소 칸막이. 남색 바탕, 높이 60px, 왼쪽 로고 도장(30px)과 이름(16px/700, 영문 부제 12px), 오른쪽으로 탭·검색·화면 모드 버튼.
- **탭:** 14px/600, 셸 회색 글자. hover 때 셸 글자색. 현재 탭은 흰 글자에 아래 3px 선. 탭을 바꿔도 셸과 필터는 그대로 남는다.
- **검색:** 230px(1100px 이하 180px), 높이 36px, `shell-2` 바탕, 반투명 흰 1px 테두리, 왼쪽 16px 돋보기.
- **셸 버튼:** 36px 정사각, 반투명 흰 테두리, hover 때 `shell-2`. 화면 모드 전환에 `aria-pressed`.
- **포커스:** 셸 위에서는 외곽선이 흰색, 탭은 안쪽으로 -4px.

### 갱신 상태 줄
셸 바로 아래 용지 띠. 13px 회먹, 아래 1px 실선, 최소 높이 40px. 왼쪽 8px 녹색 점(살아 있음) + 갱신 시각·뉴스·논문 수, 오른쪽 RSS·데이터(JSON) 링크(엷은 먹 600, hover 청색). `role="status"`.

### 근거 집계 용지 (Signature)
첫 화면 오른쪽 투표용지. 1.5px 먹 테두리, 반경 0. 머리(16px/700 제목 + 총수 20px 고정폭) 아래 3px 머리선.
- **집계 행(`brow`):** 4열 — 기호 번호(40px: '기호' 12px 회먹 + 숫자 20px), 구분(15px/700 + 12.5px 설명), 국가 수(22px/800 + '개국' 13px), 기표란(48px). 행 사이 2px 먹선. hover 때 `hover` 바탕. 클릭하면 도장이 찍히고 탐색기가 그 상태로 걸러진다.
- **신호 상자:** 위 3px 머리선. 30일 신호 수(청색 18px), '오늘 들어온 신호' 5건(14px 먹, hover 때 제목만 청색 밑줄), 'PB 데일리 전체 보기' 링크.

### 기표란 (Slot)
- **크기:** 집계 행 48px(도장 36px), 국가 행 44px(32px), 프로그램 36px(26px). 테두리 1.5px 먹선, 반경 2px.
- **공식·검증:** 주홍 도장. **문헌·플랫폼:** 문헌 먹 도장, 불투명도 0.75. **탐색 모니터링:** 비어 있고 테두리만 회먹 점선.
- 각 기표란은 `role="img"`와 '근거 상태: …' 라벨을 가진다.

### 국가 행 (탐색기 투표용지)
`details` 펼침 행. 맨 위 3px 머리선, 행 사이 2px 먹선. 요약 줄 5열 — 번호(52px, 13px 회먹 고정폭), 이름(16px/700 + 영문 12.5px), 사실(13px, 신호 수만 청색 700), 최근 날짜(120px), 기표란(64px). hover와 펼친 상태는 `hover` 바탕. 펼친 몸통은 번호 열만큼 들여 쓰고, 기준 근거·최근 신호 목록(작은 사각·원 기호 14px)과 프로그램 하위 행을 담는다.

### 프로그램 하위 행
위아래 1px 먹선으로 묶인다. 두 칸 그리드: 머리(15px/700 제목 + 관할·단계 12.5px + 36px 기표란), 필드 목록, 완성도.
- **필드 목록:** 76px 라벨 열(예산·참여·단계·법적근거). 확인된 필드는 꽉 찬 먹 점, 비어 있으면 회먹 테두리 점과 '확인 중' 회먹 값.
- **근거 완성도:** 6px 트랙(`hair-2`) + 먹 채움 + 고정폭 비율.
- **관련 신호:** 위 1px 점선 실선 아래 청색 링크 목록.
- **바닥:** 출처 유형·확인일(13px 회먹) + 먹색 '출처' 링크와 외부 링크 아이콘.

### 뉴스 목록 (PB 데일리)
맨 위 3px 머리선. 날짜마다 머리 줄(13px/800 먹, 위 2px 먹선, 용지 바탕으로 셸 아래 sticky). 항목 사이 1px 실선. 제목 16px/700 먹(hover 청색 밑줄), 원문 제목 13.5px 회먹, 메타 12.5px(국가는 엷은 먹 700, 신호 태그는 청색 고리 점). 같은 소식 묶음은 `details`로 접고, 펼침 화살표는 180도 돈다.

### 논문 목록
맨 위 3px 머리선, 항목 사이 1px 실선. 3열 — 날짜(86px, 13px 회먹), 본문(제목 16px/700, 원문 제목, 저자 13px, 초록 2줄), 동작(링크 청색 700, 신호 배지). 640px 이하 한 열.

### 개표 집계표 (Tally)
최대 760px 표. 묶음 머리(13px/800, 위 2px 먹선), 행 사이 1px 실선, 항목 열 180px 엷은 먹, 12px 막대(트랙 `hair-2`, 채움 먹, 반경 0), 값 열 64px 오른쪽 정렬 700(분모는 회먹 '/n'). 설명 캡션은 아래쪽, 위 2px 먹선. 막대는 근거 쪽 지표라 청색을 쓰지 않는다.

### 데이터 표 (비교표)
맨 위 3px 머리선, 최대 높이 620px 스크롤, 최소 폭 980px. 머리는 용지 바탕 sticky, 엷은 먹 700, 아래 2px 먹선. 칸 10px 12px, 행 사이 1px 실선, hover `hover`. 숫자 열 오른쪽 정렬 고정폭, '확인 중'은 회먹, 원문 링크는 먹 밑줄(`src`).

### 필터 막대
용지 바탕, 1px 실선 테두리, 반경 0, 안쪽 16px, 간격 12px. 세로형(PB 데일리)과 가로형(탐색기) 두 가지. 세로형 아래쪽에 빠른 국가 칩 줄(위 1px 실선).

### Chips (빠른 국가)
- **Style:** 용지 바탕, 1px 실선, 알약형, 13px 엷은 먹, 4px 10px. 기사 수는 회먹 고정폭.
- **State:** hover 때 테두리 먹. 눌림(`aria-pressed="true"`)은 먹 바탕 + 용지 글자, 숫자는 0.75 불투명도.

### Buttons
- **Shape:** 조작 반경(4px), 최소 높이 40px(640px 이하 44px), 14px/700, 아이콘 16px.
- **Primary:** 먹 바탕 + 용지 글자. '더 보기' 버튼은 가운데 정렬.
- **Hover / Focus:** 바탕이 엷은 먹으로, 0.15초 전환. 포커스는 2px 외곽선 + 2px 간격.
- **Ghost:** 용지 바탕 + 먹 글자 + 실선 테두리, hover 때 테두리 먹.

### Inputs / Fields
- **Style:** 위에 12.5px/700 라벨, 아래 높이 40px 입력·선택. 1px 실선, 반경 4px, 용지 바탕, 14px 먹. 선택 상자의 화살표는 회먹 두 삼각형 그라데이션.
- **Focus:** 공통 2px `focus` 외곽선. hover 때 테두리 회먹.
- **체크박스:** 18px, `accent-color` 먹.

### 지도 표지 (Map markers)
MapLibre 위에 캔버스로 그린 도장(`stampImage`, 44px, pixelRatio 2). 색은 지도를 띄울 때 CSS 변수에서 읽는다.
- **공식·검증:** 용지 원판 위 주홍 고리(3.6px)와 卜 획(3.8px).
- **문헌·플랫폼:** 용지 원판 위 문헌 먹 고리(2.6px)와 卜 획(2.8px).
- **탐색 모니터링:** 용지 바탕 22px 사각, 회먹 점선 테두리(1.6px, 3/2.5 점선).
- **30일 신호:** 도장 층 아래의 투명 원, 청색 1.2px 테두리 불투명도 0.7, 반경 13px + 기사 수×0.25(최대 +7).
- **쌓임:** 공식 > 문헌 > 모니터링 순으로 위. 확대에 따라 1.2→1.6배(모니터링 1→1.3배). 모두 -6도 기울임.
- **바탕 지도:** 밝은 화면 Carto Positron, 어두운 화면 Dark Matter. 팝업은 13px 먹, 반경 4px, '떠 있는 것' 그림자.
- **범례:** 패널 머리에 16px 기호 4개(공식 도장, 문헌 도장, 점선 사각, 청색 고리).

### 상태
- **hover:** 행은 `hover` 바탕, 링크는 밑줄 2px, 신호 제목은 청색 밑줄, 테두리 요소는 테두리가 먹으로.
- **포커스:** 모든 요소 2px `focus` 외곽선 + 2px 간격. 셸 위는 흰색.
- **눌림·현재:** 칩 `aria-pressed`, 탭 `aria-current`, 펼친 국가 행.
- **빈 상태:** 가운데 정렬 회먹 문장, 위아래 32px(`empty`). 지도를 못 불러오면 같은 내용이 있는 표로 안내한다.
- **모르는 값:** '확인 중'을 회먹으로 쓴다. 빈칸이나 0으로 채우지 않는다.
- **수집 상태:** 정상은 녹색 점, 실패는 먹 테두리 빈 점.

### 움직임
- **도장 찍기(`press`):** 200ms, `cubic-bezier(.3,.7,.4,1)`. 1.7배·-14도·투명에서 0.9배·-2도를 거쳐 1배·-3도로 내려앉는다. 집계 행을 누르거나 탐색기 필터가 바뀔 때만 공식·문헌 도장에 걸린다. 처음 그릴 때는 찍지 않는다.
- **그 밖:** 색·테두리 전환 0.15초, 펼침 화살표 0.18초. `prefers-reduced-motion`이면 애니메이션·전환을 모두 끄고 부드러운 스크롤도 끈다.

### 어두운 화면
`html.dark` 클래스로 바꾼다. 저장값(`pb-theme`)이 없으면 시스템 설정을 따르고, 첫 그림 전에 머리 스크립트가 클래스를 붙인다. 용지는 어두운 먹(#161b22), 글자는 밝은 회백(#e9edf2), 먹선은 #c6ccd5로 밝아져 선 위계를 그대로 지킨다. 주홍은 #f0574c, 청색은 #79a8f5, 문헌 먹은 #c6ccd5, 녹색은 #5fc48f, 포커스는 #e9edf2로 바뀐다. 셸은 #121d33, 셸 2는 #1b2944. 지도 도장은 지도를 다시 띄울 때 바뀐 변수로 다시 그린다.

### 접근성
WCAG 2.1 AA, 밝은·어두운 화면 모두 axe 위반 0건을 유지한다. 본문 바로가기, 지도와 같은 내용을 담은 표, 기표란·범례의 텍스트 라벨, 결과 줄 `aria-live`, 터치 기기에서 협동 제스처(지도), 640px 이하 44px 조작 높이가 체계의 일부다.

## Do's and Don'ts

### Do:
- **Do** 근거 레코드는 투표용지 행으로 만들고, 상태는 오른쪽 기표란 도장으로 보여 준다(공식 = 주홍 도장, 문헌 = 문헌 먹 도장, 모니터링 = 빈 점선 기표란).
- **Do** 위계는 먹선 굵기로 만든다: 1px 실선, 1.5px 테두리, 2px 행 구분, 3px 머리선.
- **Do** 투표용지·패널·표·필터 막대는 반경 0, 조작 요소만 4px.
- **Do** 모든 숫자에 고정폭 숫자를 쓰고, 본문에는 `word-break: keep-all`.
- **Do** 근거 출처 링크는 먹 글자 + 회먹 밑줄(`src`)로 쓴다.
- **Do** 자동 번역 제목 아래에 원문 제목을 붙이고, 모르는 값은 '확인 중'으로 쓴다.
- **Do** 도장 찍기 움직임은 상태가 바뀔 때만(200ms) 쓴다.

### Don't:
- **Don't** 주홍을 공식·검증 도장 밖(활성 상태, 경고, 강조, 버튼)에 쓰지 않는다.
- **Don't** 청색을 근거 상태·근거 막대·출처 링크에 쓰지 않는다. 신호 층이 근거 층을 덮지 않는다.
- **Don't** 패널과 행에 그림자를 깔거나 카드로 띄우지 않는다. 그림자는 바로가기 링크와 지도 팝업 같은 떠 있는 것에만.
- **Don't** Pretendard 밖의 두 번째 서체를 들이지 않는다.
- **Don't** 다크 지도 + KPI 카드 + 신문형 뉴스라는 범주 기본 배치로 돌아가지 않는다.
- **Don't** 처음 그릴 때나 스크롤 때 도장을 찍지 않는다. 장식용 움직임을 더하지 않는다.
