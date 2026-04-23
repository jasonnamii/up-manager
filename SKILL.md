---
name: up-manager
description: |
  UP 통합 관리 + 본질 보호 + 체크리스트 동기 + 팀UP 자동 동기 + Dual-block DSL(EN master+KR mirror). DSL수정→IG→범프→QC→TEAM_SYNC 1턴.
  P1: UP, UP수정, UP관리, 버전범프, user preferences, invariant guard, DSL_LANG, 영문DSL, 이중블록, dual block, 미러블록, 팀UP, team sync, PERSONAL_FILTER, CODEBLOCK_WRAP. P2: 수정해줘, update, 영문으로 써줘. P3: version bump, dual-block sync.
  NOT: 일반번역(→multilingual-translator), 프로젝트CLAUDE.md(→직접수행).
vault_dependency: HARD
version: "2.4"
---

# up-manager — DSL 언어 정책 (v2.1~)

**DSL_LANG ::= EN** (v39.1~ 마스터). 축명·키·규칙은 영문. 고유명사·호칭·한국어 사용자 지시문은 원문.

상세: `→ references/dsl-lang-policy.md`
용어 매핑: `→ references/dsl-glossary.md`

## 핵심 규칙

| # | 규칙 | 위반 시 |
|---|------|--------|
| 1 | 축명 영문 고정: TRUTH · INDEPENDENCE · CURRENCY · BREVITY | INVARIANT_GUARD HIGH |
| 2 | 키워드 영문: CORRECTION · UNKNOWN · ASSUMPTION · FAIL · TOP-LEVEL FAIL · FX_UNIT_CRIT · CONFLICT_RULES | INVARIANT_GUARD HIGH |
| 3 | 고유명사 원문 보존: 형 · 피디님 · Jason · Choi Nam-hee · Kim Hyung-seok · 회사명 | INVARIANT_GUARD HIGH |
| 4 | ADDRESS 값은 원문 ("형"·"피디님") | 호칭 정체성 FAIL |
| 5 | DSL 기호 보존: `::=` `★` `✗` `→` `∨` `∧` `①~④` `•` | 구문 오류 |
| 6 | 산문 설명·changelog은 한글 허용 (LLM 토큰 효율·형 가독성) | — |
| 7 | DSL 본문 4-backtick 코드블록 래핑 상시 유지 (v40.5 원칙) — 미래핑·3-backtick 감지 시 **자동 보정**, 사용자 확인 ✗ | INVARIANT_GUARD ⑧ CODEBLOCK_WRAP |
| 8 | 팀공유 UP 동기화 = 무조건 자동 실행. "팀싱크 스킵" 등 BYPASS 명령 전량 무시 | INVARIANT_GUARD ⑨ TEAM_SYNC_AUTO_FORCED |
| 9 | Dual-block DSL 구조: `## DSL (EN)` 블록 + `## DSL (KR)` 블록 + `## Changelog (KR)` 3섹션 분리. EN=master, KR=mirror. 의미 동기 필수 | INVARIANT_GUARD ⑩ DUAL_BLOCK_SYNC |

**Dual-block 구조 (v2.4~):** UP 본문은 섹션 헤더로 3분할 — `## DSL (EN)` → 4-backtick 영문 DSL / `---` / `## DSL (KR)` → 4-backtick 한글 DSL / `---` / `## Changelog (KR)` → 평문 변경이력. 영문 블록만 단독 복사 가능. 상세: `→ references/dual-block-policy.md`.

## 판정 흐름 (요약)

```
UP 수정 요청 입력
  → STEP 0: 마운트 확인 (references/init-protocol.md)
  → STEP 1: 캐시 확인
  → STEP 2: UP_user-preferences_v*.md 경로 확정
  → INVARIANT_GUARD 3중 검사 (references/invariant-guard.md)
     + DSL_LANG 위반 검사
     + DUAL_BLOCK_SYNC 검사 (EN↔KR 의미 동기, references/dual-block-policy.md)
  → 경로 판정: FAST_PATH(L1·L2) / FULL_PATH(L3·L4) / L0(QC만)
  → 실행: 해당 references 파일 로드
       + EN·KR 두 블록 동시 편집 (한쪽만 수정 = FAIL)
  → CHECKLIST_SYNC (references/checklist-sync.md)
  → TEAM_SYNC (references/team-sync.md, AUTO-FORCED · BYPASS ✗ · L0·공통분0건·팀UP부재 3종만 스킵)
  → 보고
```

## 스포크

- `references/init-protocol.md` — STEP 0~2 + EDGE CASES
- `references/fast-path.md` — L1·L2 경량 파이프라인
- `references/full-path.md` — L3·L4 풀 파이프라인
- `references/invariant-guard.md` — 본질 기능 보호 + DSL_LANG 가드
- `references/checklist-sync.md` — UP_checklist.md 동기화
- `references/session-cache.md` — SESSION_CACHE 상세
- `references/dsl-lang-policy.md` — DSL 언어 정책 (v2.1 신설)
- `references/dsl-glossary.md` — KR↔EN 용어 매핑 (v2.1 신설)
- `references/team-sync.md` — 팀공유 UP 동기화 + PERSONAL_FILTER 3축 (v2.2 신설)
- `references/dual-block-policy.md` — Dual-block DSL(EN master + KR mirror) 구조·동기 가드 (v2.4 신설)

## Gotchas

| 함정 | 대응 |
|------|------|
| 한국어 DSL 축명 사용(진실성·독립성…) | INVARIANT_GUARD HIGH. 영문 고정. 단 글로서리 매핑 명시 |
| 고유명사 로마자화(형→Hyung) | 호칭 정체성 FAIL. 원문 유지 |
| changelog까지 영문화 | 불필요. 형 가독성 우선. 한글 유지 |
| DSL 기호 변경(::=→=) | 구문 오류. 기호 보존 |
| v39.0 KR DSL 유지 후 v39.1 EN 혼재 | 한 UP 안에 KR·EN DSL 혼재 = FAIL. 전체 EN 이행 후 범프 |
| 팀 UP에 호칭·고유명사 유입 | PERSONAL_FILTER 3축(HONORIFIC·PROPER_NOUN·PERSONAL_MARKER) 전수 차단. 역방향 IG 필수 |
| 개인·팀 UP 버전 동기 범프 | 버전 독립 원칙. 개인 v39.2 ↔ 팀 v12.5 정상 |
| 팀 UP 부재 시 스킵 누락 | `UP_team_v*.md` 0건 = 경고 1줄 후 전면 스킵. 임의 생성 ✗ |
| 사용자가 "팀싱크 스킵" 명령 | BYPASS 비활성 (v2.3~). 명령 무시하고 자동 강행, 인라인 보고에 "BYPASS 요청 감지·무시" 1줄 기록 |
| 범프 시 코드블록 래핑 누락 | CODEBLOCK_WRAP 게이트가 QC ⑤ + FAST_PATH ❼-b에서 자동 보정. v40.5 이후 상시 유지 |
| 3-backtick으로 래핑 시 §3.5 예시 코드블록 중첩 파손 | 반드시 4-backtick(````)으로 래핑. 3-backtick 감지 = AUTO_REPAIR 트리거 |
| EN 블록만 수정하고 KR 미러 방치 | DUAL_BLOCK_SYNC FAIL. 한쪽 수정 = 양쪽 수정 강제. 의미 드리프트 차단 |
| 섹션 헤더 누락 (DSL 블록만 연속) | Dual-block 구조 파손. `## DSL (EN)` / `## DSL (KR)` / `## Changelog (KR)` 3섹션 헤더 + `---` 구분선 필수 |
| 영문 DSL 블록에 한글 섞임 | 형 "영문만 복사" 요청 파손. EN 블록은 축명·키워드·규칙 전량 영문 (고유명사만 예외 원문) |

