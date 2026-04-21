---
name: up-manager
description: |
  UP(User Preferences) 통합 관리 + 본질 기능 보호 + 체크리스트 동기화 + 팀공유 UP 자동 동기화. DSL수정→INVARIANT_GUARD→버전범프→QC→체크리스트동기화→TEAM_SYNC→보고 1회실행. DSL_LANG=EN 마스터(v39.1~, 고유명사·호칭 원문). L1·L2는 FAST_PATH로 1턴 일괄.
  P1: UP, UP수정, UP관리, 본질기능, 버전범프, user preferences, 인버리언트, invariant guard, DSL_LANG, 영문DSL, DSL영문화, KR-EN glossary, 팀공유UP, 팀UP, UP_team, team sync, 팀싱크, PERSONAL_FILTER. P2: 수정해줘, update, modify, 팀에도 반영. P3: version bump, DSL edit, invariant protection, checklist sync, team UP sync. P5: Before/After.
  NOT: 일반번역(→multilingual-translator), 프로젝트CLAUDE.md(→직접수행).
vault_dependency: HARD
version: "2.2"
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

## 판정 흐름 (요약)

```
UP 수정 요청 입력
  → STEP 0: 마운트 확인 (references/init-protocol.md)
  → STEP 1: 캐시 확인
  → STEP 2: UP_user-preferences_v*.md 경로 확정
  → INVARIANT_GUARD 3중 검사 (references/invariant-guard.md)
     + DSL_LANG 위반 검사 (신규)
  → 경로 판정: FAST_PATH(L1·L2) / FULL_PATH(L3·L4) / L0(QC만)
  → 실행: 해당 references 파일 로드
  → CHECKLIST_SYNC (references/checklist-sync.md)
  → TEAM_SYNC (references/team-sync.md, L0 제외·BYPASS "팀싱크 스킵" 허용)
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

