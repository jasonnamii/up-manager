# PIPELINE — 단방향 선형 파이프라인 (v2.5~)

**원칙: 1턴 완결, 분기 없음, 루프 없음.** L레벨·SCOPE_IMPACT 판정 제거. UP 파일 1개만 읽고, QC 실패 시 같은 턴 내 자동 보정 1회만 허용.

---

## PIPE

```
① INIT      → ② IG → ③ EDIT → ④ QC → ⑤ TEAM_SYNC → ⑥ REPORT
  (캐시 스킵)    차단    병행    자동보정  자동         인라인
```

- 각 단계는 **앞 단계 성공** 전제에서만 진입.
- IG HIGH 감지 → 사용자 "본질 변경 확인함" 명시 전 ③ 차단.
- QC 2회차 실패 → STOP + 보고 (루프 금지).

---

## ① INIT

`→ references/init-protocol.md` 참조.

- STEP 0: 볼트 마운트 확인 (실패 시 `request_cowork_directory`)
- STEP 1: SESSION_CACHE.up_path 존재 시 ②로 직행
- STEP 2: `Agent-Ops/UP_user-preferences_*.md` + `UP_team_v*.md` 경로 확정 → 캐시 저장

**제거 (v2.5):** `UP_stability.md`·`UP_checklist.md` 경로 탐색·캐싱 삭제. 파일 부재 경고도 발생하지 않음.

---

## ② IG — INVARIANT_GUARD

`→ references/invariant-guard.md` 참조.

- 8축 본질 검사 (DSL_LANG·DUAL_BLOCK_SYNC 포함)
- HIGH → 사용자 명시 확인 전 ③ 차단
- MID → 경고 + 사용자 확인 요청
- LOW → 내부 로그만

---

## ③ EDIT — 편집 (단일 턴 직렬)

```
SEQUENCE (같은 턴 내 순차):
  ❶ UP 본문 Edit — EN·KR 양블록 동시 편집 (한쪽만 수정 = DUAL_BLOCK_SYNC FAIL)
  ❷ changelog 행 추가 (KR 평문)
  ❸ 코드블록 헤더 `# UP vX.X` 버전 갱신
  ❹ 파일명 버전 범프 (rename): Minor=.9→.10 / Major=이전→_archive/ + 새파일 v{M+1}.0
```

**Dual-block 편집 원칙:** EN master 먼저 수정 → KR mirror 동기. 의미 동일성 검증은 ④ QC에서.

**Major 판정:** 구조 변경(섹션 신설·삭제·재배치) · 규칙 폐기 · 축 재설계.
**Minor 판정:** 규칙 내용 수정 · 표현 순화 · changelog만 추가.

---

## ④ QC — 검증 (2항목 + WRAP 게이트)

```
CHECK (같은 턴 내 순차):
  ❶ DSL순도     — 자연어 산문 잔류 0건 (규칙 라인은 DSL 문법 준수)
  ❷ 규칙보존     — grep old_string 잔존 0건 + 원본 모든 규칙 존재
  ❸ WRAP 게이트 — DSL 본문 4-backtick(````) 래핑 무결
      파일 첫 줄=```` / DSL 본문 종료 직후 닫는 ```` / changelog는 래핑 밖
      미래핑·3-backtick 감지 시 **자동 보정** (사용자 확인 ✗) → 재검증

FAIL 처리:
  1회차 FAIL → 같은 턴 내 자동 수정 → 재검증
  2회차 FAIL → STOP + 보고 (루프 하드캡)
```

**제거 (v2.5):** 풀QC 5항목(①DSL순도·②규칙보존·③참조무결·④DSL문법·⑤WRAP) → **2항목 + WRAP 게이트**로 압축. `@ref 참조무결 grep`·`DSL문법 신규규칙 준수`는 ❶❷에 흡수.

보고 표기: `QC: ①✓ ②✓ | WRAP:✓`

---

## ⑤ TEAM_SYNC — 팀 UP 동기

`→ references/team-sync.md` 참조.

**실행 조건 (AND):**
- `up_team_path ≠ None` (팀 UP 파일 존재)
- PERSONAL_FILTER 통과분 ≥1건 (공통 변경분 존재)

**스킵 조건 (OR — 유일 3종):**
- `up_team_path = None` (팀 UP 부재)
- PERSONAL_FILTER 통과분 0건 (전부 개인 커스텀)
- 수정 내용이 EN 블록 changelog/표현 다듬기만 (의미 변경 없음)

**BYPASS 비활성:** "팀싱크 스킵"·"나중에" 등 명령 무시. 인라인 보고에 "BYPASS 요청 감지·무시" 1줄 기록.

STEP 1~8은 `team-sync.md` §PIPE 준수 (경로→diff→PERSONAL_FILTER→역방향IG→Edit→범프→QC→보고).

---

## ⑥ REPORT — 인라인 보고

```
v{old} → v{new}
Before/After 표 (변경위치 · Before · After 3열)
QC: ①✓ ②✓ | WRAP:✓
IG: [HIGH·MID 감지 건수 또는 "없음"]
팀싱크: [팀 v{old}→v{new} + 공통분 N건 + 제외 목록 또는 "스킵(사유)"]
시스템프롬프트: [변경 부분 코드블록 또는 "스킵"]
미결: [시스템프롬프트 복붙 등 후속 필요사항 또는 "없음"]

SAVE: 인라인만. 파일 저장 ✗.
```

**제거 (v2.5):** `stability: [변동사항]` · `체크리스트: [SCOPE_IMPACT+동기화]` 행 제거.

---

## 전파 (UP → 시스템프롬프트)

UP 본문 의미 변경 시 보고 `시스템프롬프트:` 항목에 변경 섹션 코드블록 1개 첨부 + "Cowork 설정에 UP본 반영해주세요" 안내. 파일명만 변경 시 스킵.

**제거 (v2.5):** 전파맵·depth 1/2 구분·POST_VERIFY 로직 삭제. 시스템프롬프트 1대상 단순 안내로 축소.

---

## Gotchas

| 함정 | 대응 |
|------|------|
| 파이프라인 중간 루프 복귀 | 단방향 선형 원칙. QC 실패 시 같은 턴 내 자동보정 1회만 허용 |
| IG 실패 상태에서 ③ 진입 | 차단. 사용자 "본질 변경 확인함" 명시 전 EDIT ✗ |
| EN만 수정하고 ④로 진입 | DUAL_BLOCK_SYNC FAIL. 양블록 동시 편집 강제 |
| 풀QC 5항목 복원 시도 | v2.5~ 2항목+WRAP 게이트만 운용. 참조무결·DSL문법은 ❶❷에 흡수 |
| 팀싱크 스킵 BYPASS 수용 | BYPASS 비활성. 명령 무시·자동 강행 |
| stability·checklist 단계 복원 시도 | v2.5~ 제거. 해당 파일 읽기·쓰기 전량 차단 |
