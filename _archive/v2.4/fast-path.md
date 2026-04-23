# FAST_PATH — L1·L2 경량 파이프라인

**목표: 병렬 최대화로 3턴 이내 완결.**

---

## PIPE

```
턴1: [UP파일 읽기 ∥ stability파일 읽기 ∥ 체크리스트 읽기]  ← 병렬 3호출
턴2: [수정 + changelog + 헤더갱신 + 버전범프 + stability갱신 + grep QC + SCOPE_IMPACT 판정]
       ← 순차 의존이므로 1턴 내 직렬 처리
턴3: [전파판정 ∥ 체크리스트 동기화 ∥ TEAM_SYNC ∥ 보고]  ← 병렬 4호출

SESSION_CACHE 존재 + stability 변동 없음 예상 → 턴1에서 stability 읽기 스킵 가능 → 실질 2턴
SCOPE_IMPACT=LOW → 턴3 체크리스트 동기화는 frontmatter version 1줄 Edit으로 경량화
TEAM_SYNC: up_team_path=None 또는 공통분 0건일 때만 스킵 (BYPASS ✗, AUTO 기본)
```

---

## 턴1: 병렬 읽기

```
PARALLEL:
  ❶ UP 파일 읽기
  ❷ UP_stability.md 읽기
  ❸ UP_checklist.md 읽기 (SCOPE_IMPACT 판정 입력)

  SESSION_CACHE에 stability 스냅샷 있으면 ❷ 스킵
  SCOPE_IMPACT=LOW 확실 예상 + 체크리스트 frontmatter만 갱신 예정 → ❸도 스킵 가능
```

---

## 턴2: 수정 + QC 통합 (단일 턴 내 순차)

```
SEQUENCE:
  ⓪ INVARIANT_GUARD 3중 검사 → HIGH·MID 감지 시 사용자 확인 요청 후 대기
  ❶ UP 해당 규칙 수정
  ❷ changelog 행 추가
  ❸ 코드블록 헤더 `# UP vX.X` 버전 갱신
  ❹ 파일명 버전 범프 (rename)
  ❺ stability 해당 행 갱신 (frozen→stable 강등 등)
  ❻ grep old 텍스트 잔존 확인 (QC ②)
  ❼ DSL순도 확인 (QC ①) — 수정 내용을 눈으로 확인
  ❼-b CODEBLOCK_WRAP 검증 (필수) — DSL 본문 전체가 4-backtick(````) 코드블록으로 래핑됐는지 확인
       · 파일 첫 줄=```` · DSL 본문 종료 직후 닫는 ```` 존재 · changelog는 래핑 밖
       · 미래핑·3-backtick(```) 래핑 감지 시 자동 보정 (사용자 확인 ✗) → 재검증
       · v40.5 원칙(코드블록 래핑) 상시 유지 게이트
  ❽ SCOPE_IMPACT 판정 — CHECKLIST_SYNC DETECT 로직으로 HIGH·MID·LOW 분류

  ✗ QC는 ❻❼ 2항목만. 항목 추가·변형·재해석 금지. 보고에 QC:①✓②✓ 형식으로 기록.
  ✓ CODEBLOCK_WRAP(❼-b)은 QC 항목이 아닌 **게이트** — 자동 보정 후 재검증, 보고에 "WRAP:✓" 1토큰 표기.
  FAIL 시 → 즉시 수정 후 재검증. 턴 추가 ✗ (같은 턴 내 루프)
  SESSION_CACHE.current_version 갱신
```

---

## 턴3: 전파 + 체크리스트 동기화 + TEAM_SYNC + 보고 (병렬)

```
PARALLEL (반드시 같은 턴에 2~4개 도구호출 동시 발행):
  ❶ 전파 판정 — 전파맵 조회 → 연쇄대상 리스트
  ❷ 체크리스트 동기화 — SCOPE_IMPACT 분기:
     HIGH·MID → Edit(UP_checklist.md) 영향 항목 + frontmatter `source`·`updated` 갱신
     LOW      → Edit(UP_checklist.md) frontmatter `source`·`updated` 1줄만 갱신
     SKIP 조건: L0_PATH · "체크리스트 스킵" 명시
  ❸ TEAM_SYNC — 팀 UP **자동** 동기화 (references/team-sync.md), 기본 AUTO · BYPASS ✗
     STEP 1~8 강제 실행 (경로→diff→PERSONAL_FILTER→역방향IG→Edit→범프→QC→보고)
     SKIP 조건 (축소): up_team_path=None · L0_PATH · PERSONAL_FILTER 통과분 0건
     ✗ "팀싱크 스킵" 명령 비활성 · 사용자 재확인 요청 금지 · 공통분 ≥1건이면 무조건 실행
  ❹ 보고 — 인라인 텍스트로 사용자에게 직접 표시 (파일 저장 없음)
```

### 전파 판정 표

| 판정 | 조치 |
|------|------|
| UP → 시스템프롬프트 (내용 변경) | "Cowork 설정에 UP본 반영해주세요" 안내 |
| UP → 시스템프롬프트 (파일명만 변경) | 스킵 |
| 전파대상 0건 | "전파대상 없음" 1줄 |

---

## 보고 포맷 (인라인 전용)

```
v{old} → v{new}
Before/After 테이블 (변경위치·Before·After 3열)
QC: ①✓ ②✓
stability: [변동사항 또는 "변동 없음"]
전파: [대상 또는 "없음"]
체크리스트: [SCOPE_IMPACT + 동기화 여부 또는 "영향 없음"]
팀싱크: [팀 v{old}→v{new} + 공통분 N건 + 제외 목록 또는 "스킵(사유)"]
시스템프롬프트: [변경부분 코드블록 또는 "스킵"]
미결: [시스템프롬프트 복붙 등 후속 필요사항]

SAVE: 인라인만. 파일 저장 ✗.
```
