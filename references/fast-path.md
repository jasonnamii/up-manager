# FAST_PATH — L1·L2 경량 파이프라인

**목표: 병렬 최대화로 3턴 이내 완결.**

---

## PIPE

```
턴1: [UP파일 읽기 ∥ stability파일 읽기 ∥ 체크리스트 읽기]  ← 병렬 3호출
턴2: [수정 + changelog + 헤더갱신 + 버전범프 + stability갱신 + grep QC + SCOPE_IMPACT 판정]
       ← 순차 의존이므로 1턴 내 직렬 처리
턴3: [전파판정 ∥ 체크리스트 동기화 ∥ 보고]  ← 병렬 3호출

SESSION_CACHE 존재 + stability 변동 없음 예상 → 턴1에서 stability 읽기 스킵 가능 → 실질 2턴
SCOPE_IMPACT=LOW → 턴3 체크리스트 동기화는 frontmatter version 1줄 Edit으로 경량화
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
  ❽ SCOPE_IMPACT 판정 — CHECKLIST_SYNC DETECT 로직으로 HIGH·MID·LOW 분류

  ✗ QC는 ❻❼ 2항목만. 항목 추가·변형·재해석 금지. 보고에 QC:①✓②✓ 형식으로 기록.
  FAIL 시 → 즉시 수정 후 재검증. 턴 추가 ✗ (같은 턴 내 루프)
  SESSION_CACHE.current_version 갱신
```

---

## 턴3: 전파 + 체크리스트 동기화 + 보고 (병렬)

```
PARALLEL (반드시 같은 턴에 2~3개 도구호출 동시 발행):
  ❶ 전파 판정 — 전파맵 조회 → 연쇄대상 리스트
  ❷ 체크리스트 동기화 — SCOPE_IMPACT 분기:
     HIGH·MID → Edit(UP_checklist.md) 영향 항목 + frontmatter `source`·`updated` 갱신
     LOW      → Edit(UP_checklist.md) frontmatter `source`·`updated` 1줄만 갱신
     SKIP 조건: L0_PATH · "체크리스트 스킵" 명시
  ❸ 보고 — 인라인 텍스트로 사용자에게 직접 표시 (파일 저장 없음)
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
시스템프롬프트: [변경부분 코드블록 또는 "스킵"]
미결: [시스템프롬프트 복붙 등 후속 필요사항]

SAVE: 인라인만. 파일 저장 ✗.
```
