---
name: up-manager
description: |
  UP 통합 관리 + 본질 보호 + 팀UP 자동 동기 + Single-block DSL(KR-only). 단방향 선형: INIT→IG→편집→QC→TEAM_SYNC→보고. 1턴 완결.
    P1: UP, UP수정, UP관리, 버전범프, 버전명체계, YYMMDD, 260503, user preferences, invariant guard, DSL_LANG, KR단일블록, single block, 한글DSL, 팀UP, team sync, PERSONAL_FILTER, CODEBLOCK_WRAP, 유저프리퍼런스, 사용자설정, 사용자선호, UP편집, UP갱신, UP업데이트, UP버전, UP백업, UP동기화.
    P2: 수정해줘, update, 한글로 써줘, UP 고쳐줘, 사용자설정 바꿔줘, 선호도 수정해줘, UP 업데이트해줘, 버전 올려줘.
    P3: version bump, single-block sync, date-based versioning, user preferences management, invariant guard, DSL synchronization.
    P4: UP 수정·버전업·백업이 필요할 때, 팀 UP 동기가 필요할 때.
    P5: .md로, UP파일로.
    NOT: 일반번역(→translator-skill), 프로젝트CLAUDE.md(→project-updater), UP진단(→up-doctor).
---

# up-manager v3.1 (260503 버전명 체계 신설)

**DSL_LANG ::= KR** (v3.0~ 마스터). 축명·키·규칙 한국어. 영문 블록 폐지. 고유명사·호칭 원문.

상세: `→ references/dsl-lang-policy.md` · 용어: `→ references/dsl-glossary.md`

## 핵심 규칙

| # | 규칙 | 위반 시 |
|---|------|--------|
| 1 | 축명 한국어 고정: 진실성·독립성·통화성·간결성 | INVARIANT #1 HIGH |
| 2 | 키워드 한국어: 정정·미상·가정·FAIL·TOP-LEVEL FAIL·통화단위 위반·규칙충돌 | INVARIANT #2 HIGH |
| 3 | 고유명사 원문 보존: 형·피디님·Jason·Choi Nam-hee·Kim Hyung-seok·회사명 | INVARIANT #3 HIGH |
| 4 | ADDRESS 값 원문 ("형"·"피디님") | INVARIANT #4 호칭 정체성 FAIL |
| 5 | DSL 기호 보존: `::=` `★` `✗` `→` `∨` `∧` `①~④` `•` | INVARIANT #5 구문 오류 |
| 6 | DSL 본문 4-backtick 코드블록 래핑 상시 — 미래핑·3-backtick 감지 시 자동 보정 | INVARIANT #6 코드블록래핑 |
| 7 | 팀공유 UP 동기 = 자동 강행. "팀싱크 스킵" BYPASS 명령 무시 | INVARIANT #7 팀싱크 자동 강행 |
| 8 | Single-block DSL 구조: `## DSL (KR)` + `## Changelog (KR)` 2섹션. KR=master. EN 블록 폐지(v3.0~) | INVARIANT #8 단일블록 |
| 9 | 버전명 체계: `YYMMDD_NN` (260503~). 같은 날 N번째 수정 = `_NN` 증분 · 다음 날 첫 수정 = `_01` 재시작. v숫자.숫자 폐기 | INVARIANT #9 버전명 체계 |

산문 설명·changelog 한글. 영문 키워드 잔존 → 한국어 치환 강제.

## 버전명 체계 (260503~)

**형식 ::= `UP_user-preferences_YYMMDD_NN.md`**

- YY = 연 2자 (26 = 2026년)
- MM = 월 2자 (05 = 5월)
- DD = 일 2자 (03 = 3일)
- NN = 같은 날 수정 순번 2자 (01부터)

**규칙 :**

- 같은 날 추가 수정 → `_NN` 증분 (260503_01 → 260503_02 → 260503_03)
- 다음 날 첫 수정 → `_01` 재시작 (260503_03 → 260504_01)
- 메이저/마이너 구분 폐기 — 모든 변경이 동일 위계
- v숫자.숫자 형식 폐기 — 신규 파일 작성 시 사용 ✗

**구버전 처리 :**

- 신버전 작성 시 직전 버전 → `Agent-Ops/_archive/UP_versions/`로 이동
- changelog `PREV_CHANGELOG:` 라인에 archive 경로 명시
- 같은 날 _02 작성 시 _01도 archive 이동 (현재 운영본 1개만 Agent-Ops/ 직속)

**예시 :**

- 2026-05-03 첫 수정 → `UP_user-preferences_260503_01.md`
- 같은 날 두 번째 → `UP_user-preferences_260503_02.md` (_01은 archive)
- 2026-05-04 첫 수정 → `UP_user-preferences_260504_01.md`

**위반 시 INVARIANT #9 FAIL :** v숫자.숫자 형식 신규 작성 시도·날짜 형식 오류·_NN 미증분 시 STOP+보고.

## 파이프라인 (단방향 선형)

```
① INIT        — 볼트 마운트 + UP_user-preferences_v*.md 경로 확정 (캐시 있으면 스킵)
② IG          — INVARIANT_GUARD 3중 검사 (DSL_LANG=KR + SINGLE_BLOCK 포함)
③ EDIT        — KR 단일 블록 편집 + changelog 1줄 추가 + 버전 범프(필요시)
④ QC          — 2항목 + WRAP 게이트 (자동 보정)
⑤ TEAM_SYNC   — 팀 UP 동기 (자동·BYPASS ✗ · 3종만 스킵)
⑥ REPORT      — 인라인 보고
```

- 루프 없음. QC 실패 시 같은 턴 자동 보정 1회. 2회차 실패 = STOP+보고.
- 분기 없음. L0~L4·SCOPE_IMPACT 판정 제거.
- 파일 1개만. UP_user-preferences_v*.md만 읽음.

상세: `→ references/pipeline.md`

## 스포크

- `references/init-protocol.md` — ① INIT (마운트·경로 확정)
- `references/pipeline.md` — ②~⑥ 편집·QC·팀싱크·보고
- `references/invariant-guard.md` — 8축 본질 보호 + DSL_LANG·SINGLE_BLOCK 가드
- `references/dsl-lang-policy.md` — DSL 언어 정책 (KR master)
- `references/dsl-glossary.md` — KR↔EN 용어 매핑 (역호환·읽기 전용)
- `references/single-block-policy.md` — KR 단일 블록 구조
- `references/team-sync.md` — 팀 UP 동기 + PERSONAL_FILTER 3축
- `references/session-cache.md` — 세션 캐시 (2회차+ 가속)

## 마이그레이션 (v2.x EN+KR Dual → v3.0 KR Single)

기존 UP 파일에 `## DSL (EN)` 블록 잔존 시:
1. EN 블록 + 직후 `---` 구분선 삭제
2. KR 블록의 영문 키워드 한국어 치환 (역방향 매핑은 dsl-glossary 참조)
3. 헤더 `## DSL (KR)` 단일화
4. changelog 1줄 추가: "v?-patch | DSL_LANG = KR 단일 블록 전환 (EN 블록 폐지)"

## Gotchas

| 함정 | 대응 |
|------|------|
| EN DSL 축명 잔존 (TRUTH·BREVITY 등) | INVARIANT #1 HIGH. 한국어 치환 + 글로서리 매핑 |
| 고유명사 로마자화 (형→Hyung) | INVARIANT #3 호칭 정체성 FAIL. 원문 유지 |
| changelog까지 영문화 | 불필요. 형 가독성 우선. 한글 |
| DSL 기호 변경 (::=→=) | INVARIANT #5 구문 오류. 기호 보존 |
| EN·KR 혼재 | v3.0~ EN 블록 자체 금지. 잔존 시 즉시 삭제 |
| 팀 UP에 호칭·고유명사 유입 | PERSONAL_FILTER 3축(호칭·고유명사·개인마커) 전수 차단 |
| 개인·팀 UP 버전 동기 범프 | 버전 독립 원칙 |
| 팀 UP 부재 시 스킵 누락 | `UP_team_v*.md` 0건 = 경고 1줄 후 전면 스킵 |
| "팀싱크 스킵" 명령 | BYPASS 비활성. 자동 강행, 보고에 "BYPASS 요청 감지·무시" 1줄 |
| 범프 시 코드블록 래핑 누락 | WRAP 게이트가 QC에서 자동 보정 |
| 3-backtick 래핑 | 4-backtick(````) 강제 |
| 섹션 헤더 누락 | `## DSL (KR)` + `## Changelog (KR)` 2섹션 + `---` 구분선 필수 |
| 시스템 설정에 EN 붙여넣기 | v3.0~ KR 블록 직접 붙여넣기 |
| v숫자.숫자 형식 신규 작성 (예: v123.0) | INVARIANT #9 FAIL. YYMMDD_NN으로 강제 (260504_01 등) |
| 같은 날 _01·_02 둘 다 Agent-Ops/ 직속 | 운영본 1개 원칙. 구버전은 _archive/UP_versions/로 이동 |
| _NN 미증분으로 같은 파일 덮어쓰기 | INVARIANT #9 FAIL. 같은 날 추가 수정 시 _02·_03 증분 강제 |
