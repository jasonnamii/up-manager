---
name: up-manager
description: |
  UP(User Preferences) 통합 관리. DSL수정→버전범프→경로갱신→QC→안정도갱신→전파→보고 1회실행. EN 단독 마스터(v29.0~). L1·L2 수정은 FAST_PATH로 1턴 일괄처리.
  P1: UP, UP수정, UP관리, 버전범프, user preferences. P2: 수정해줘, update, modify. P3: version bump, DSL edit. P5: Before/After.
  NOT: 일반번역(→multilingual-translator), 프로젝트CLAUDE.md(→deliverable-engine 또는 직접수행).
---

# UP Manager

UP 수정·버전·경로·검증·전파·보고를 단일 파이프라인으로 실행. v29.0부터 EN 단독 마스터(KR 폐지).

---

## ⛔ 절대 규칙

| # | 규칙 | 이유 |
|---|------|------|
| 1 | **DSL 문법으로만 수정** | 자연어 산문 → Claude 해석 편차 |
| 2 | **QC 통과 전 보고 ✗** | 미검증 상태 전달 = 오류 전파 |
| 3 | **상대경로만 사용** | 머신간 불일치 방지 |

---

## INIT (파이프라인 착수 전 필수)

스킬 발동 직후, 본격 수정 전에 **파일경로를 확정**한다. 이 단계를 건너뛰면 파일 탐색 반복으로 시간을 낭비한다.

```
STEP 1 — 파일경로 확정:
  Agent-Ops/ 디렉토리를 탐색 → UP_user-preferences_v*.md 파일명 확정

  RULE: 이후 파이프라인 전체에서 확정 경로를 재사용. 재탐색 ✗
```

---

## 발동 조건

```
TRIGGER ::= 아래 중 1개↑ 해당시 자동발동
  ❶ "UP 수정/추가/변경/삭제" 명시 요청
  ❷ UP 규칙 내용에 대한 수정 의도 감지
  ❸ "버전 범프", "한영 동기화" 명시
  ❹ UP 파일 경로·참조 관련 요청

  TIMING: UP 파일 읽기 시작 전 본 스킬 발동 완료 필수 | 미발동 상태에서 UP 읽기·수정 착수 = FAIL
  EXEMPT: UP 규칙을 참조만 하는 경우 (수정 의도 없음) → 미발동
```

---

## 경로 분기 (FAST vs FULL)

수정4 레벨 판정 후 즉시 경로를 결정한다.

| 조건 | 경로 | 차이 |
|------|------|------|
| L1·L2 (맥락0~약) | **FAST_PATH** | A+C 1턴 일괄, 경량QC 2항목, 인라인 보고 |
| L3·L4 (맥락중~강) | **FULL_PATH** | 순차, 4항목 QC, 풀보고 |
| L0 (QC교정) | **L0_PATH** | A만 실행, 버전·경로·전파·브리핑 스킵 |

---

## FAST_PATH (L1·L2)

**목표: 1턴에 수정→버전범프→보고 완결.**

```
PIPE: [A수정 + C버전] → E경량QC → S안정도갱신 → [F전파판정 + G인라인보고 + H브리핑]
  괄호 안 = 1턴 일괄실행. 형과 대화 주고받기 최소화.
```

### A+C 일괄

1. UP 해당 규칙 읽기
2. 해당 부분 수정
3. changelog 행 추가
4. 파일명 버전 범프 (rename)

### E. 경량QC (2항목)

| # | 항목 | 방법 |
|---|------|------|
| ① | DSL순도 | 수정부분에 자연어 산문 잔류 0건 |
| ② | old잔존 | grep으로 old 텍스트 잔존 0건 |

FAIL 시 → 즉시 수정 후 재검증.

### S. 안정도 갱신

```
TARGET: Agent-Ops/UP_stability.md
ACTION:
  수정된 섹션의 현재 stability 확인 → 아래 규칙 적용:
    frozen → stable 자동 강등 + 보고에 "stability: §X frozen→stable" 1줄
    stable → 유지 (보고 생략)
    trial → 유지 (보고 생략)
    신규 규칙 추가 → trial 태깅 + "stability: §X 신규 trial" 1줄
  linked_to frontmatter의 UP 버전 갱신
  PROMOTION_CHECK: trial 항목 중 5세션 연속 무수정 확인 → stable 승격 + 보고
TOOL: UP_stability.md 해당 행 수정
SKIP: L0_PATH에서는 실행하지 않음
```

### F. 전파 판정 (간소화)

전파맵 조회 → 연쇄대상 리스트 출력. 실행이 필요한 건만 1줄씩 보고.

| 판정 | 조치 |
|------|------|
| UP → 시스템프롬프트 (내용 변경) | "Cowork 설정에 UP본 반영해주세요" 안내 |
| UP → 시스템프롬프트 (파일명만 변경) | 스킵 |
| 전파대상 0건 | "전파대상 없음" 1줄 |

### G. 인라인 보고 (1블록)

```
FORMAT:
  v{old} → v{new}
  Before/After 테이블 (변경위치·Before·After 3열)
  QC: ①✓ ②✓ ③✓
  stability: [변동사항 또는 "변동 없음"]
  전파: [대상 또는 "없음"]
  시스템프롬프트: [변경부분 코드블록 또는 "스킵"]
```

모든 보고를 **1개 응답 블록**에 통합. 별도 턴 소비 ✗.

### H. 브리핑

```
PATH: @ref UP §B.④세션브리핑 PATH (YYMMDD-HHmm 포맷)
CONTENT: 변경사항 + 미결(시스템프롬프트 복붙 등) + 컨텍스트포인터
RULE: 자동실행 | 브리핑 없이 종료 = 컨텍스트 소실
```

---

## FULL_PATH (L3·L4)

L3·L4는 구조적 변경이므로 형 컨펌이 필요하다.

```
PIPE: A수정 → C버전 → E검증 → F전파 → S안정도갱신 → D경로 → G보고 → H브리핑
  RULE: E검증 실패 → A수정 복귀 (루프)
```

### A. 수정

```
TARGET: Agent-Ops/UP_user-preferences_v{현재}.md
EDIT_RULE:
  FORMAT: DSL only (@ref references/dsl-spec.md)
  SCOPE: 형 요청 범위 + 절대자 확장(MECE 누락 탐색)
  L3 = Before/After테이블 → 형 컨펌 후 진행
  L4 = 내용논의 → 합의 후 진행
```

### C. 버전

```
Minor(내용수정): 파일명 버전 갱신 + changelog 행 추가. .9→.10
Major(구조변경): 이전→_archive/ + 새파일 v{M+1}.0
CHANGELOG: "v{버전} | §{섹션} {변경요약 1줄}"
```

### D. 경로

```
원칙: 볼트 루트 기준 상대경로만
갱신대상: ❶UP 본문 @ref ❷프로젝트 CLAUDE.md(해당시)
VERIFY: grep old버전번호 잔존 → 1건↑ = FAIL
```

### E. 풀QC (4항목)

| # | 항목 |
|---|------|
| ① | DSL순도: 자연어 산문 잔류 0건 |
| ② | 규칙보존: 원본 모든 규칙 수정본에 존재 |
| ③ | 참조무결: @ref 대상 실재 (grep) |
| ④ | DSL문법: 신규/수정 규칙 구문사양 준수 |

### F. 전파

```
전파맵 조회 + 실행
depth 1(자율): UP→시스템프롬프트, 파일명→참조경로
depth 2(보고): UP→관련스킬
BATCH: 2건↑ 병렬 | POST_VERIFY 통합1회
```

### S. 안정도 갱신

FAST_PATH §S와 동일 규칙 적용. FULL_PATH 추가 판단:

```
L3_RULE: frozen 섹션 수정 → stable 강등은 자동. 보고에서 강조 표시
L4_RULE: 구조 변경 → 영향받는 모든 섹션 stability 재평가. 필요시 다수 행 일괄 갱신
MAJOR_VERSION: Major 버전 범프 시 → "stability 전체 리뷰 필요?" 1줄 제안
```

### G. 보고 (FAST와 동일 인라인 포맷)

```
FORMAT:
  v{old}→v{new} | QC:①~④✓ | 전파:[대상] | stability:[변동사항] | 복붙:[대상 또는 스킵]
  REASON: L3/L4는 게이트에서 Before/After를 이미 제시·합의 완료. 보고에서 중복출력 ✗.
  시스템프롬프트 변경시: 변경 섹션 코드블록 1개만 첨부
```

### H. 브리핑

FAST_PATH와 동일.

---

## Gotchas

- **INIT 스킵 금지:** 경로 확정 건너뛰면 파일 탐색 루프.
- **Cowork 지침은 UP 관할 밖:** `Agent-Ops/Cowork Claude_v2.0.md`는 머신별 VAULT 경로만 보관하는 최소 파일. UP 수정 파이프라인 대상 아님. 변경 필요시 직접 수정.
- **Stability 파일 경로 고정:** `Agent-Ops/UP_stability.md`. UP 파일과 동일 폴더. 경로 탐색 시도 불필요.
- **L0은 S단계 스킵:** L0_PATH는 QC교정이므로 stability 갱신 대상 아님. S단계를 실행하면 불필요한 도구 호출.
- (초기 — 실수 발견 시 이 섹션에 직접 추가)
