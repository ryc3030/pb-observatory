# 세계 참여예산 관측소 (Global Participatory Budgeting Observatory) v4

92개국 참여예산(PB) 근거 레지스트리, 다국어 뉴스 신호, 최신 연구를 **매일 자동으로 갱신**하는 공개 대시보드입니다.

## 구조

```
index.html              페이지
assets/                 스타일·스크립트 (app.js가 data/*.json을 읽어 렌더링)
data/
  countries.seed.json   ← 직접 편집: 92개국 기준 근거·상태·별칭
  programs.seed.json    ← 직접 편집: PB 프로그램 레지스트리(예산·참여·법적근거·출처)
  countries.json        자동 생성: 기준 근거 + 국가별 최신 뉴스 신호 + 레지스트리 근거·검토 필요 표시
  programs.json         자동 생성: 프로그램 + 관련 뉴스 + 공식 API 회차 수치·Pabulib 집계·Participedia 사례
  news.json             자동 생성: Google News RSS + GDELT 다국어 수집(최근 400일 보관, 국가 판정 근거 iso_basis 포함)
  cases.json            자동 생성: Participedia PB 사례(좌표·검수 여부)
  elections.json        자동 생성: Pabulib 투표 기록 도시별 집계(연도별 예산·투표지·후보 사업)
  papers.json           자동 생성: OpenAlex·Crossref 논문
  ledger.json           자동 생성: 근거 원장(새 신호 누적)
  history.json          자동 생성: 일별 스냅숏(추이 차트)
  health.json, meta.json
scripts/collect.py      수집기 (표준 라이브러리만 사용)
.github/workflows/update.yml   매일 06:17(KST) 실행
```

## 운영 원칙

- 뉴스·논문은 **신호**로 저장하며 '공식·검증'·'문헌·플랫폼'으로는 올리지 않습니다.
- 다만 '탐색 모니터링' 국가가 최근 6개월(183일) 안에 ① 매체 2곳 이상이 다룬 같은 소식이 있거나 ② 서로 다른 소식이 2건 이상이면 **'보도 확인'**으로 자동 표시합니다. 국가 판정이 확실한 기사(제목·발행국·도메인·같은 소식)만 셉니다. 6개월 동안 조건을 못 채우면 되돌리고, 올리고 내린 기록은 근거 원장에 남깁니다. 나라마다 참여예산 주기가 달라 한 주기를 덮는 6개월로 정했습니다.
- 근거 상태와 프로그램 수치는 `*.seed.json`을 사람이 검토해 고칩니다. GitHub 웹에서 파일을 열어 연필 아이콘으로 편집하면 됩니다.
- 프로그램 수치 중 `"확인 중"`은 아직 원문 출처로 검증하지 않은 값입니다.
- 단, `"확인 중"`인 예산 칸은 공식 플랫폼 API(Decidim) 또는 Pabulib 집계로 자동 채우고 값 옆에 출처를 붙입니다. 사람이 적은 값은 덮어쓰지 않습니다.
- Participedia·Pabulib에 사례가 있는 모니터링 국가는 '검토 필요'로만 표시합니다(국가·프로그램 탭 근거 상태 필터).

## 연결된 데이터 원천 (모두 키 없음)

| 원천 | 얻는 것 | 비고 |
|---|---|---|
| Google News RSS | 27개 검색어·24개 언어 기사 제목 | 기본 뉴스 신호 |
| 참여예산 기관 피드 6곳 | PBP·PB Scotland 전체 글, newDemocracy·Decidim·CONSUL·OGP의 참여예산 글 | PB 데일리 '기관 소식'. 미래 날짜가 붙은 고정 글은 뺌 |
| GDELT DOC 2.0 API | 원문 직링크, 발행국(sourcecountry), 언어 | `scripts/gdelt.py`가 하루 한 번(12:41 KST) 요청 한 건만 보냄. 재시도 없음. 검색 기간은 마지막 성공 이후 전체(최대 90일)라 실패한 날의 기사도 다음 성공 때 받음. 같은 날 두 번 실행하면 요청 없이 끝남 |
| OpenAlex · Crossref | 논문 서지·초록·DOI | |
| Participedia 검색 JSON | PB 사례 제목·도시·국가·좌표·검수 여부 | 제목·요약에 PB 용어가 있는 사례만 채택 |
| Pabulib (pabuviz API) | 투표 회차별 예산·사업·투표지·투표 방식 | 폴란드·네덜란드·프랑스 중심 |
| Decidim GraphQL | 회차별 예산·제안·선정 사업 | 헬싱키 OmaStadi, 뉴욕 The People's Money. 다른 Decidim 도시는 `scripts/collect.py`의 `DECIDIM`에 추가 |

국가 판정 순서: 제목 속 지명 → GDELT 발행국 → 출처 도메인 → 단일국가 검색어 → 언어판 기본값. 화면의 PB 데일리에서 국가명 옆 괄호가 판정 근거입니다.

## 수동 실행

GitHub → Actions → "일일 자동 수집" → Run workflow. 로컬에서는 `python scripts/collect.py`.



## 선택 설정

- Settings → Secrets and variables → Actions
  - 변수 `OPENALEX_MAILTO`: 본인 이메일(OpenAlex 우선 처리 풀)
  - 시크릿 `OPENALEX_API_KEY`: OpenAlex 무료 API 키(속도 제한 완화)

## Claude 아티팩트판 (회사망 등 github.io가 막힌 곳용)

- 주소: https://claude.ai/artifact/AWjk8zvEAoegyF1AdWHfvF (소유자 공유 설정에 따라 열람)
- 아티팩트는 외부 데이터·지도 타일을 못 불러오므로 `python scripts/build_artifact.py`가 `artifact/`에 전용판을 만든다
  (지도는 `artifact/assets/world.json`, 지도 스타일은 직접 쓴 `artifact/assets/map.css`, 글꼴은 Google Fonts의 Noto Sans KR).
- 갱신: Claude에게 "아티팩트 갱신해줘"라고 하거나, 예약 작업(매일 오전 7시 12분 KST)을 켜면 이 저장소를 받아 빌드하고 아티팩트 파일을 바꿔 올린다.

## 글꼴

- 본문·표: Pretendard (OFL, jsDelivr 동적 서브셋)
- 표제(제목·연표 연도·큰 숫자): Paperlogy 7 Bold·8 ExtraBold (OFL). `assets/fonts/`에 라틴 + KS X 1001 한글 2,350자 + 사이트 문구로 줄인 woff2 서브셋과 라이선스(`OFL-Paperlogy.txt`)를 둠. 다시 만들려면 `pyftsubset Paperlogy-7Bold.ttf --text-file=글자목록.txt --flavor=woff2 --layout-features='*'`.
- 에스코어 드림은 라이선스가 글꼴 파일의 수정을 금해(서브셋·woff2 변환 불가) 웹에 싣지 않음.

## GDELT 대리 요청 (선택)

GitHub Actions 러너 IP는 여럿이 함께 써서 GDELT가 요청 한 건에도 429로 막을 수 있다. 이때는 Cloudflare Worker(`worker/index.js`)가 `/api/gdelt`로 GDELT에 대신 요청한다. 검색식은 고정이고, 같은 날 같은 범위 요청은 Cloudflare 캐시로 답해 GDELT에는 하루 한 번만 간다.

1. Cloudflare에서 이 저장소로 만든 Worker가 새로 배포됐는지 확인한다(주소 예: `https://pb-observatory.<계정>.workers.dev`).
2. GitHub 저장소 Settings → Secrets and variables → Actions → Variables에 `GDELT_PROXY` = Worker 주소를 넣는다.
3. 그 뒤 `scripts/gdelt.py`는 Worker로 먼저 한 번, 실패하면 직접 한 번 요청한다(IP마다 하루 한 건).

## 같은 소식 묶기

수집기가 기사마다 `story`(같은 소식 묶음)와 `story_n`(묶음 안 매체 수)을 붙인다. 번역된 한국어 제목(없으면 원문)의 단어와 한글 글자쌍으로 TF-IDF 코사인 유사도를 재고, 5일 안에 나온 같은 국가(또는 국가 미상) 기사끼리 0.45 이상이면 한 소식으로 묶는다. 그래서 언어가 달라도 같은 소식이면 묶이고, 국가를 정하지 못한 기사는 같은 소식 기사들의 국가로 채운다(판정 근거 '같은 소식'). PB 데일리 위쪽의 '여러 매체가 다룬 소식'은 최근 7일 동안 매체 2곳 이상이 다룬 소식을 매체 수 순으로 보여 준다. 여러 매체가 다룬 소식을 골라 보여 준다는 착상은 NewsCollector(elisemercury, MIT)에서 가져왔고, 구현은 표준 라이브러리로 새로 썼다.


## 번역 제목 다듬기

기계 번역(Google → MyMemory) 결과는 `title_ko_mt`에 그대로 두고, 화면에 쓰는 `title_ko`는 매번 `scripts/ko_style.py`로 다시 다듬는다. 규칙을 고치면 다음 수집 때 모든 제목에 다시 적용된다.

- 용어 통일: '참여 예산' → '참여예산', '주민/시민/청소년 참여 예산' 붙여 쓰기, '시민 예산'(폴란드 budżet obywatelski) → '시민예산', 지명(포르투알레그리·상파울루·벨루오리존치) 표기 통일
- 뉴스 제목 끝: 존댓말 문장(~시작됩니다.) → 신문 제목체(~ 시작), '~하고 있습니다' → '~ 중', '~할 것입니다' → '~할 전망', 주어 조사는 쉼표로('칼리는 … 추진' → '칼리, … 추진'), 끝 마침표 삭제
- 인용부호 안, 숫자, 고유명은 고치지 않는다. 논문 제목은 용어 통일만 한다.
- 정문 v2.8의 원칙(의미 보존, 번역투 N06 사전)을 제목에 맞게 줄였다. 회귀 시험: `python3 scripts/test_ko_style.py`(일일 수집 전에 자동 실행)
