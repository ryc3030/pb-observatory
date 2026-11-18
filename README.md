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

- 뉴스·논문은 **신호**로만 저장하며, 국가의 근거 상태(공식/검증·문헌·모니터링)를 자동으로 올리지 않습니다.
- 근거 상태와 프로그램 수치는 `*.seed.json`을 사람이 검토해 고칩니다. GitHub 웹에서 파일을 열어 연필 아이콘으로 편집하면 됩니다.
- 프로그램 수치 중 `"확인 중"`은 아직 원문 출처로 검증하지 않은 값입니다.
- 단, `"확인 중"`인 예산 칸은 공식 플랫폼 API(Decidim) 또는 Pabulib 집계로 자동 채우고 값 옆에 출처를 붙입니다. 사람이 적은 값은 덮어쓰지 않습니다.
- Participedia·Pabulib에 사례가 있는 모니터링 국가는 '검토 필요'로만 표시합니다(국가·프로그램 탭 근거 상태 필터).

## 연결된 데이터 원천 (모두 키 없음)

| 원천 | 얻는 것 | 비고 |
|---|---|---|
| Google News RSS | 27개 검색어·24개 언어 기사 제목 | 기본 뉴스 신호 |
| GDELT DOC 2.0 API | 원문 직링크, 발행국(sourcecountry), 언어 | 5초당 1회 제한, 연속 3회 실패 시 그날은 생략 |
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
