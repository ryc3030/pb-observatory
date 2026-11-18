# 세계 참여예산 관측소 (Global Participatory Budgeting Observatory) v4

92개국 참여예산(PB) 근거 레지스트리, 다국어 뉴스 신호, 최신 연구를 **매일 자동으로 갱신**하는 공개 대시보드입니다.

## 구조

```
index.html              페이지
assets/                 스타일·스크립트 (app.js가 data/*.json을 읽어 렌더링)
data/
  countries.seed.json   ← 직접 편집: 92개국 기준 근거·상태·별칭
  programs.seed.json    ← 직접 편집: PB 프로그램 레지스트리(예산·참여·법적근거·출처)
  countries.json        자동 생성: 기준 근거 + 국가별 최신 뉴스 신호
  programs.json         자동 생성: 프로그램 + 관련 뉴스
  news.json             자동 생성: Google News RSS 다국어 수집(최근 400일 보관)
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

## 수동 실행

GitHub → Actions → "일일 자동 수집" → Run workflow. 로컬에서는 `python scripts/collect.py`.

## 선택 설정

- Settings → Secrets and variables → Actions
  - 변수 `OPENALEX_MAILTO`: 본인 이메일(OpenAlex 우선 처리 풀)
  - 시크릿 `OPENALEX_API_KEY`: OpenAlex 무료 API 키(속도 제한 완화)
