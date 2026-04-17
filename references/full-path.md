# FULL_PATH — L3·L4 풀 파이프라인

L3·L4는 구조적 변경이므로 사용자 컨펌이 필요하다.

---

## PIPE

```
IG(INVARIANT_GUARD) → A(수정) → C(버전범프) → [E(풀QC 4항목) ∥ S(stability 행 갱신)]
   → [F(전파맵 실행) ∥ D(경로 갱신+grep) ∥ K(체크리스트 동기화)] → G(보고)

RULE: IG HIGH·MID → 사용자 "본질 변경 확인함" 명시 전 A 차단
      E검증 실패 → A수정 복귀 (루프)
      K는 SCOPE_IMPACT 판정 후 분기 실행
∥ = 병렬 실행 (독립 단계를 같은 턴에 동시 호출)
✗ 단계 이름·역할 변형 금지.
```

---

## A. 수정

```
TARGET: Agent-Ops/UP_user-preferences_v{현재}.md
EDIT_RULE:
  FORMAT: DSL only (@ref references/dsl-spec.md)
  SCOPE: 사용자 요청 범위 + 절대자 확장(MECE 누락 탐색)
  L3 = Before/After테이블 → 사용자 컨펌 후 진행
  L4 = 내용논의 → 합의 후 진행
```

---

## C. 버전

```
Minor(내용수정):
  파일명 버전 갱신 + 코드블록 헤더 `# UP vX.X` 갱신 + changelog 행 추가
  .9 → .10

Major(구조변경):
  이전 → _archive/
  새파일 v{M+1}.0

CHANGELOG: "v{버전} | §{섹션} {변경요약 1줄}"
```

---

## E+S 병렬 (검증 + 안정도)

```
PARALLEL:
  ❶ E. 풀QC (4항목)
  ❷ S. 안정도 갱신
```

### E. 풀QC

| # | 항목 |
|---|------|
| ① | DSL순도: 자연어 산문 잔류 0건 |
| ② | 규칙보존: 원본 모든 규칙 수정본에 존재 |
| ③ | 참조무결: @ref 대상 실재 (grep) |
| ④ | DSL문법: 신규/수정 규칙 구문사양 준수 |

✗ 이 4항목만. 항목 추가·변형·재해석 금지. 보고에 QC:①~④✓ 형식으로 기록.

### S. 안정도 갱신 규칙

```
FAST_PATH §턴2와 동일 규칙 + 아래 추가:
L3_RULE: frozen 섹션 수정 → stable 강등은 자동. 보고에서 강조 표시
L4_RULE: 구조 변경 → 영향받는 모든 섹션 stability 재평가
MAJOR_VERSION: Major 버전 범프 시 → "stability 전체 리뷰 필요?" 1줄 제안
```

---

## F+D+K 병렬 (전파 + 경로 + 체크리스트)

```
PARALLEL:
  ❶ F. 전파
  ❷ D. 경로
  ❸ K. 체크리스트 동기화
```

### F. 전파

```
전파맵 조회 + 실행
depth 1(자율): UP → 시스템프롬프트, 파일명 → 참조경로
depth 2(보고): UP → 관련스킬
BATCH: 2건↑ 병렬 | POST_VERIFY 통합 1회
```

### D. 경로

```
원칙: 볼트 루트 기준 상대경로만
갱신대상:
  ❶ UP 본문 @ref
  ❷ 프로젝트 CLAUDE.md (해당시)
VERIFY: grep old버전번호 잔존 → 1건↑ = FAIL
```

### K. 체크리스트 동기화

```
TARGET: Agent-Ops/UP_checklist.md

A단계에서 판정된 SCOPE_IMPACT에 따라 분기:
  HIGH → 영향 항목 Before/After 제시 + Edit + frontmatter `source`·`updated` 갱신
  MID  → 영향 항목 After 제시 + Edit + frontmatter 갱신
  LOW  → frontmatter `source`·`updated` 1줄 Edit만 수행

VERIFY: 체크리스트 frontmatter `source:` 필드가 신규 UP 파일명과 일치
SKIP: "체크리스트 스킵" BYPASS 명시 시
```

---

## G. 보고

```
FORMAT:
  v{old}→v{new} | QC:①~④✓ | 전파:[대상] | stability:[변동사항]
    | 체크리스트:[HIGH·MID·LOW+동기화/스킵] | 복붙:[대상 또는 스킵]

  REASON: L3/L4는 게이트에서 Before/After를 이미 제시·합의 완료. 보고에서 중복출력 ✗.
  시스템프롬프트 변경시: 변경 섹션 코드블록 1개만 첨부

SAVE: 인라인만. 파일 저장 ✗.
```
