---
name: up-manager
description: |
  UP 통합 관리 + 본질 보호 + 팀UP 자동 동기 + Dual-block DSL(EN master+KR mirror). 단방향 선형: INIT→IG→편집→QC→TEAM_SYNC→보고. 1턴 완결.
  P1: UP, UP수정, UP관리, 버전범프, user preferences, invariant guard, DSL_LANG, 영문DSL, 이중블록, dual block, 미러블록, 팀UP, team sync, PERSONAL_FILTER, CODEBLOCK_WRAP. P2: 수정해줘, update, 영문으로 써줘. P3: version bump, dual-block sync.
  NOT: 일반번역(→multilingual-translator), 프로젝트CLAUDE.md(→직접수행).
vault_dependency: HARD
version: "2.5"
---

# up-manager

**DSL_LANG ::= EN** (v39.1~ 마스터). 축명·키·규칙은 영문. 고유명사·호칭·한국어 사용자 지시문은 원문.

상세: `→ references/dsl-lang-policy.md` · 용어: `→ references/dsl-glossary.md`

## 핵심 규칙

| # | 규칙 | 위반 시 |
|---|------|--------|
| 1 | 축명 영문 고정: TRUTH · INDEPENDENCE · CURRENCY · BREVITY | INVARIANT #1 HIGH |
| 2 | 키워드 영문: CORRECTION · UNKNOWN · ASSUMPTION · FAIL · TOP-LEVEL FAIL · FX_UNIT_CRIT · CONFLICT_RULES | INVARIANT #2 HIGH |
| 3 | 고유명사 원문 보존: 형 · 피디님 · Jason · Choi Nam-hee · Kim Hyung-seok · 회사명 | INVARIANT #3 HIGH |
| 4 | ADDRESS 값은 원문 ("형"·"피디님") | INVARIANT #4 호칭 정체성 FAIL |
| 5 | DSL 기호 보존: `::=` `★` `✗` `→` `∨` `∧` `①~④` `•` | INVARIANT #5 구문 오류 |
| 6 | DSL 본문 4-backtick 코드블록 래핑 상시 유지 (v40.5 원칙) — 미래핑·3-backtick 감지 시 **자동 보정** | INVARIANT #6 CODEBLOCK_WRAP |
| 7 | 팀공유 UP 동기화 = 무조건 자동 실행. "팀싱크 스킵" 등 BYPASS 명령 전량 무시 | INVARIANT #7 TEAM_SYNC_AUTO_FORCED |
| 8 | Dual-block DSL 구조: `## DSL (EN)` + `## DSL (KR)` + `## Changelog (KR)` 3섹션. EN=master, KR=mirror. 의미 동기 필수 | INVARIANT #8 DUAL_BLOCK_SYNC |

산문 설명·changelog은 한글 허용 (형 가독성 우선).

## 파이프라인 (단방향 선형)

```
① INIT        — 볼트 마운트 확인 + UP_user-preferences_v*.md 경로 확정 (캐시 있으면 스킵)
② IG          — INVARIANT_GUARD 3중 검사 (DSL_LANG + DUAL_BLOCK_SYNC 포함)
③ EDIT        — EN·KR 양블록 동시 편집 + changelog 1줄 추가 + 버전 범프
④ QC          — 2항목 + WRAP 게이트 (자동 보정)
⑤ TEAM_SYNC   — 팀 UP 동기 (AUTO·BYPASS ✗ · 3종만 스킵)
⑥ REPORT      — 인라인 보고
```

- **루프 없음.** QC 실패 시 같은 턴 내 자동 보정 1회. 2회차 실패 = STOP+보고.
- **분기 없음.** L0/L1/L2/L3/L4 레벨·SCOPE_IMPACT 판정 제거 (v2.5~).
- **파일은 1개만.** UP_user-preferences_v*.md만 읽는다. stability·checklist 파일 읽기 제거 (v2.5~).

상세: `→ references/pipeline.md`

## 스포크

- `references/init-protocol.md` — ① INIT (마운트·경로 확정)
- `references/pipeline.md` — ②~⑥ 편집·QC·TEAM_SYNC·보고
- `references/invariant-guard.md` — 8축 본질 보호 + DSL_LANG·DUAL_BLOCK 가드
- `references/dsl-lang-policy.md` — DSL 언어 정책
- `references/dsl-glossary.md` — KR↔EN 용어 매핑
- `references/dual-block-policy.md` — EN master + KR mirror 구조
- `references/team-sync.md` — 팀 UP 동기 + PERSONAL_FILTER 3축
- `references/session-cache.md` — 세션 캐시 (2회차+ 재발동 가속)

## Gotchas

| 함정 | 대응 |
|------|------|
| 한국어 DSL 축명 사용 (진실성·독립성…) | INVARIANT #1 HIGH. 영문 고정 + 글로서리 매핑 참조 |
| 고유명사 로마자화 (형→Hyung) | INVARIANT #3 호칭 정체성 FAIL. 원문 유지 |
| changelog까지 영문화 | 불필요. 형 가독성 우선. 한글 유지 |
| DSL 기호 변경 (::=→=) | INVARIANT #5 구문 오류. 기호 보존 |
| KR·EN DSL 혼재 | 한 UP 안에 혼재 = FAIL. 전체 EN 이행 후 범프 |
| 팀 UP에 호칭·고유명사 유입 | PERSONAL_FILTER 3축(HONORIFIC·PROPER_NOUN·PERSONAL_MARKER) 전수 차단. 역방향 IG 필수 |
| 개인·팀 UP 버전 동기 범프 | 버전 독립 원칙. 개인 v39.2 ↔ 팀 v12.5 정상 |
| 팀 UP 부재 시 스킵 누락 | `UP_team_v*.md` 0건 = 경고 1줄 후 전면 스킵. 임의 생성 ✗ |
| "팀싱크 스킵" 명령 | BYPASS 비활성. 명령 무시·자동 강행, 보고에 "BYPASS 요청 감지·무시" 1줄 |
| 범프 시 코드블록 래핑 누락 | WRAP 게이트가 QC에서 자동 보정. v40.5 이후 상시 유지 |
| 3-backtick 래핑 | §3.5 예시 코드블록 중첩 파손. 4-backtick(````) 강제 |
| EN 블록만 수정·KR 미러 방치 | DUAL_BLOCK_SYNC FAIL. 양쪽 동시 편집 강제 |
| 섹션 헤더 누락 | `## DSL (EN)` / `## DSL (KR)` / `## Changelog (KR)` 3섹션 + `---` 구분선 필수 |
| stability·checklist 파일 참조 시도 | v2.5~ 운용 중단. 스킵 (임의 생성 ✗) |
| SCOPE_IMPACT·L레벨 분기 | v2.5~ 제거. 단방향 선형 파이프라인 |
