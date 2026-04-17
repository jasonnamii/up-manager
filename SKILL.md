---
name: up-manager
description: |
  UP(User Preferences) 통합 관리 + 본질 기능 보호 + 체크리스트 동기화. DSL수정→INVARIANT_GUARD→버전범프→경로갱신→QC→안정도갱신→전파→체크리스트동기화→보고 1회실행. KR 단독 마스터(v35.7~). L1·L2 수정은 FAST_PATH로 1턴 일괄처리. UP본체(엔진)↔UP_checklist.md(계기판) 정합성 자동 유지.
  P1: UP, UP수정, UP관리, 본질기능, 버전범프, user preferences, 인버리언트, invariant guard, UP 체크리스트, 체크리스트 동기화, CHECKLIST_SYNC. P2: 수정해줘, update, modify, 고쳐줘. P3: version bump, DSL edit, invariant protection, checklist sync. P5: Before/After.
  NOT: 일반번역(→multilingual-translator), 프로젝트CLAUDE.md(→직접수행).
vault_dependency: HARD
version: "2.0"
---

# UP Manager

UP수정·UP관리(버전·경로·검증·전파·보고)를 단일 파이프라인으로 실행. **v35.7부터 KR 단독 마스터**. **본질기능** 훼손 방지를 위해 **INVARIANT_GUARD** 가 모든 Edit에 선행한다.

**상세 프로토콜:**
- `→ references/init-protocol.md` INIT STEP 0~2 + EDGE CASES
- `→ references/session-cache.md` 재발동 가속 캐시
- `→ references/fast-path.md` L1·L2 3턴 완결
- `→ references/full-path.md` L3·L4 풀 파이프라인
- `→ references/invariant-guard.md` 본질 기능 5축 보호
- `→ references/checklist-sync.md` 체크리스트 동기화

---

## ⛔ 절대 규칙 (INVARIANT)

본 스킬의 본질 기능 7축. 수정 시 아래 INVARIANT 훼손 = FAIL.

| # | 규칙 | 이유 |
|---|------|------|
| INVARIANT #1 | **DSL 문법으로만 수정** — 자연어 산문 ✗ | Claude 해석 편차 방지 |
| INVARIANT #2 | **QC 통과 전 보고 ✗** | 미검증 상태 전달 = 오류 전파 |
| INVARIANT #3 | **상대경로만 사용** | 머신간 불일치 방지 |
| INVARIANT #4 | **INVARIANT_GUARD 선행** — 모든 Edit 전 3중 검사 필수. HIGH·MID 감지 시 사용자 "본질 변경 확인함" 명시 전 진행 ✗ | UP 본질 기능 훼손 방지 |
| INVARIANT #5 | **CHECKLIST_SYNC 동행** — UP 본체 수정 시 HIGH·MID 감지→UP_checklist.md 동기화 필수. LOW는 frontmatter version만 갱신. 스킵 = FAIL | 엔진↔계기판 정합성 |
| INVARIANT #6 | **마운트 선확인** — Agent-Ops/ 접근 불가 시 STEP 1 진입 ✗ | 파일 탐색 실패 루프 방지 |
| INVARIANT #7 | **UP 본체 우선** — 본 스킬 규칙과 UP 본체 충돌 시 UP 준수 (UP.M7.SKILL_PRECEDENCE) | UP 안전 규칙(OVERWRITE_BAN·PATTERN_GUARD·HONORIFIC·ERROR_CORRECTION) 절대 우선 |

**STEALTH:** 본 스킬 발동·내부 라벨·모듈명(FAST_PATH·IG·CHECKLIST_SYNC 등)은 사용자 응답 본문에 노출 ✗. 행동으로만 증명.

---

## INVARIANT_GUARD 요약

UP의 본질 기능 5축(MECE): ①USER ②TRUTH ③FILES ④FLOW ⑤QUALITY.

**DETECT (3중 검사 — 1건↑ 매치 → 경고):**
❶ 키워드 보존 ❷ 엄격도 라벨 ❸ 규칙 라인수 (30%↑ 축약 감지)

**SEVERITY:** HIGH(차단+명시) / MID(경고+확인) / LOW(로그만)

**BYPASS:** 사용자 "본질 변경 확인함" 명시 → 1건 1회 허가.

**적용 시점:** FAST_PATH 턴2 ⓪, FULL_PATH A단계 직전. 상세 `→ references/invariant-guard.md`

---

## CHECKLIST_SYNC 요약

TARGET: `Agent-Ops/UP_checklist.md`

| SCOPE_IMPACT | 조건 | 동작 |
|----|------|------|
| HIGH | TOP5·T1·모듈 신설/삭제 | Before/After + 컨펌 + Edit |
| MID | FULL15·T2·T3 수정 | After + 컨펌 + Edit |
| LOW | 표현 순화 | frontmatter `source` 1줄 갱신 |

**SKIP:** L0_PATH, 사용자 "체크리스트 스킵" 명시. 상세 `→ references/checklist-sync.md`

---

## 경로 분기 (FAST vs FULL vs L0)

수정4 레벨 판정 후 즉시 경로 결정.

| 조건 | 경로 | 차이 | 상세 |
|------|------|------|------|
| L1·L2 (맥락0~약) | **FAST_PATH** | 병렬 3턴 완결, 경량QC 2항목 | `→ fast-path.md` |
| L3·L4 (맥락중~강) | **FULL_PATH** | IG→A→C→E∥S→F∥D∥K→G, 4항목 QC | `→ full-path.md` |
| L0 (QC교정) | **L0_PATH** | A만 실행, 버전·경로·전파·체크리스트 스킵 | 상동 |

---

## 발동 조건

```
TRIGGER ::= 아래 중 1개↑ 해당시 자동발동
  ❶ "UP 수정/추가/변경/삭제" 명시 요청
  ❷ UP 규칙 내용에 대한 수정 의도 감지
  ❸ "버전 범프", "한영 동기화" 명시
  ❹ UP 파일 경로·참조 관련 요청
  ❺ UP_checklist.md 수정·동기화·재생성 요청

TIMING: UP 파일 읽기 시작 전 본 스킬 발동 완료 필수. 미발동 상태 UP 읽기·수정 = FAIL
EXEMPT: UP 규칙을 참조만 하는 경우 (수정 의도 없음) → 미발동
```

---

## INIT 개요

```
STEP 0 — 마운트 확인 (항상 선행): Agent-Ops/ ls 1회 → NO면 request_cowork_directory
STEP 1 — 캐시 확인: SESSION_CACHE.up_path 존재 → INIT 스킵
STEP 2 — 파일경로 확정: UP_user-preferences_v*.md + stability + checklist 경로 캐시
```

**FALLBACK (vault HARD):** 마운트 불가 + 사용자 "outputs 폴백" 명시 → `mnt/outputs/`에 Draft 생성 + "미반영" 경고. 전파·동기화 스킵. 상세 `→ references/init-protocol.md`

---

## 예시

**예시 1 — FAST_PATH (L2):**
```
사용자: "UP M3에 hedge '~같아요' 추가해줘"
→ 턴1: UP+stability+checklist 병렬 읽기
→ 턴2: IG(LOW) → Edit → changelog → 버전범프 → stability갱신 → grep → QC ①✓②✓ → SCOPE_IMPACT=MID
→ 턴3: 전파·체크리스트 동기화·보고 병렬
```

**예시 2 — FULL_PATH (L3):**
```
사용자: "UP에 새 모듈 M13(IMAGE_CITE) 추가"
→ IG 검사 (LOW, 신규 규칙)
→ A: Before/After 제시 → 사용자 컨펌 대기
→ [컨펌 후] C → E∥S → F∥D∥K → G
→ 보고: v35.21→v35.22 | QC:①~④✓ | 체크리스트:HIGH+동기화
```

---

## Gotchas

- **마운트 미확인 직행**: Agent-Ops/ 접근 불가 상태 STEP 1 진입 시 루프. STEP 0 선확인 필수
- **INIT 스킵 (첫 발동)**: 경로 확정 건너뛰면 탐색 루프. SESSION_CACHE 있을 때만 스킵 허용
- **SESSION_CACHE 과신**: 세션 밖 UP 수정 가능성 있으면 mtime 비교 후 무효화
- **병렬 호출 누락**: ∥ 표기 단계를 직렬 실행 = 속도 이점 소멸. 같은 턴 복수 도구호출 발행
- **Cowork 지침 UP 관할 밖**: `Cowork Claude_v*.md`는 머신별 VAULT 경로 보관. UP 파이프라인 대상 ✗
- **경로 고정**: stability·checklist 모두 `Agent-Ops/` 하위. 탐색 시도 불필요. 부재 시 경고+스킵 (임의 생성 ✗)
- **체크리스트 stale 방치**: HIGH·MID 감지 시 스킵 = FAIL. LOW도 frontmatter source 갱신 필수
- **SCOPE_IMPACT 오판**: 키워드 매치만으로 HIGH 단정 ✗. 규칙 의미 변경 여부가 기준
- **L0은 S·K단계도 스킵**: L0_PATH는 QC교정 전용. stability·체크리스트 영향 없음
- **본 스킬 수정은 자기순환 ✗**: up-manager 자체 수정은 skill-builder 경유. 자기 호출 금지
- **피드백 제안**: 스킬 개선 아이디어 있으면 thumbs-down 버튼으로 Anthropic에 전달

---

**참고:** evals/cases.json (회귀 방지), scripts/validate.py (자가 점검), CHANGELOG.md (버전 이력), _archive/ (이전 버전 보존).
