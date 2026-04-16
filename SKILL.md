---
name: up-manager
description: |
  UP(User Preferences) 통합 관리 + 본질 기능 보호. DSL수정→INVARIANT_GUARD→버전범프→경로갱신→QC→안정도갱신→전파→보고 1회실행. KR 단독 마스터(v35.7~). L1·L2 수정은 FAST_PATH로 1턴 일괄처리.
  P1: UP, UP수정, UP관리, 본질기능, 버전범프, user preferences, 인버리언트, invariant guard. P2: 수정해줘, update, modify, 고쳐줘. P3: version bump, DSL edit, invariant protection. P5: Before/After.
  NOT: 일반번역(→multilingual-translator), 프로젝트CLAUDE.md(→직접수행).
vault_dependency: HARD
---

# UP Manager

UP수정·UP관리(버전·경로·검증·전파·보고)를 단일 파이프라인으로 실행. **v35.7부터 KR 단독 마스터** (이전 v29.0~v35.6은 EN 단독 마스터). **본질기능** 훼손 방지를 위해 **INVARIANT_GUARD (인버리언트 가드)** 가 모든 Edit에 선행한다.

---

## ⛔ 절대 규칙

| # | 규칙 | 이유 |
|---|------|------|
| 1 | **DSL 문법으로만 수정** | 자연어 산문 → Claude 해석 편차 |
| 2 | **QC 통과 전 보고 ✗** | 미검증 상태 전달 = 오류 전파 |
| 3 | **상대경로만 사용** | 머신간 불일치 방지 |
| 4 | **INVARIANT_GUARD 선행** — 모든 Edit 호출 전 3중 검사(키워드·엄격도·라인수) 통과 필수. HIGH·MID 감지 시 사용자 "본질 변경 확인함" 명시 전 진행 금지 | UP 본질 기능 훼손 방지 |

---

## INVARIANT_GUARD (UP 본질 기능 보호)

UP의 본질 기능을 5축(MECE)으로 담지하여, 이를 훼손하는 수정을 감지·차단한다. **모든 Edit 호출 전 선행 필수.**

```
AXIS: ①USER ②TRUTH ③FILES ④FLOW ⑤QUALITY

DETECT (3중 검사 — 1건↑ 매치 → 경고):
  ❶ 키워드 보존: 담지 규칙 핵심키워드 old_string에 있고 new_string에서 소실
  ❷ 엄격도 라벨: new_string의 FAIL·✗ 개수 < old_string
  ❸ 규칙 라인수: new_string 줄수 < old_string × 0.7 (30%↑ 축약)

SEVERITY:
  HIGH: 담지 규칙 전체 삭제·FAIL 라벨 제거·✗ 금지조항 삭제 → 차단 + 사용자 명시 필요
  MID : 엄격도 완화·서브규칙 1건↑ 삭제 → 경고 + 사용자 확인
  LOW : 표현 순화·동의어 교체 → 로그만 (사용자 출력 ✗, cry-wolf 방지)

BYPASS: 사용자가 "본질 변경 확인함" 문자열 명시 → 1건 1회 허가 (세션 연속 ✗)
        세션브리핑에 자동 기록 — 반복 BYPASS 누적 시 해당 규칙 재평가 플래그
```

**상세 규정:** `→ references/invariant-guard.md 참조`

**적용 시점:** FAST_PATH 턴2 ⓪, FULL_PATH A단계 직전. Edit 호출 전 IG 선행 확인 없이 수정 착수 = FAIL.

---

## SESSION_CACHE (세션 내 재발동 가속)

같은 세션에서 UP 2회 이상 수정 시, 매번 INIT부터 재실행하면 도구호출이 중복된다. 첫 발동에서 확정한 상태를 캐싱하여 2회차부터 INIT을 스킵한다.

```
CACHE_FIELDS:
  up_path: INIT에서 확정한 UP 파일 절대경로
  stability_path: UP_stability.md 절대경로
  current_version: 현재 버전 번호
  last_stability_snapshot: 직전 수정 후 stability 상태
  cache_timestamp: 캐시 저장 시각

LIFECYCLE:
  첫 발동 → INIT 실행 → CACHE_FIELDS 저장 (cache_timestamp 포함)
  2회차↑ → CACHE_FIELDS 존재 확인 → 외부변경 감지(아래) → 존재시 INIT 스킵, 캐시값 사용
  버전 범프 완료 → current_version 갱신

INVALIDATION:
  세션 종료 시 자동 소멸 (세션 컨텍스트 한정)
  형이 "INIT 다시" 명시 → 캐시 무효화 후 재탐색
  외부변경 감지 시 → 캐시 무효화 + 재로드

**외부변경 감지:** 캐시 사용 전 파일 mtime 비교. `stat -f %m` (macOS) 또는 `stat -c %Y` (Linux)로 UP 파일 수정시각 확인. 캐시 저장 시각보다 신규 → 캐시 무효화 + 재로드. mtime 확인 불가 환경 → 캐시 미사용, 매번 원본 로드.
```

---

## INIT (파이프라인 착수 전 필수)

스킬 발동 직후, 본격 수정 전에 **볼트 마운트를 확인**하고 **파일경로를 확정**한다. SESSION_CACHE 존재 시 STEP 1~2 스킵(STEP 0은 항상 선행).

```
STEP 0 — 마운트 확인 (최우선, 항상 선행):
  Agent-Ops/ 디렉토리 접근 가능? (ls 또는 glob 1회로 확인)
    → YES: STEP 1 진행
    → NO (마운트 미확인): `mcp__cowork__request_cowork_directory` 도구 호출로 사용자에게 볼트 마운트 요청
       → 마운트 성공 → STEP 1 진행
       → 사용자 거부·실패 → STOP + 보고 (파일 접근 불가로 파이프라인 진행 불가)
  RULE: 마운트 미확인 상태에서 STEP 1 진입 ✗. 파일 탐색 실패 루프 방지.

STEP 1 — 캐시 확인:
  SESSION_CACHE.up_path 존재? → YES: INIT 스킵, 캐시값 사용 → 경로 분기로 직행
                              → NO: STEP 2 진행

STEP 2 — 파일경로 확정:
  Agent-Ops/ 디렉토리를 탐색 → UP_user-preferences_v*.md 파일명 확정
  → SESSION_CACHE에 저장

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
| L1·L2 (맥락0~약) | **FAST_PATH** | 병렬 3턴 완결, 경량QC 2항목, 보고=브리핑 통합 |
| L3·L4 (맥락중~강) | **FULL_PATH** | 병렬화된 순차, 4항목 QC, 풀보고 |
| L0 (QC교정) | **L0_PATH** | A만 실행, 버전·경로·전파·브리핑 스킵 |

---

## FAST_PATH (L1·L2)

**목표: 병렬 최대화로 3턴 이내 완결.**

```
PIPE:
  턴1: [UP파일 읽기 ∥ stability파일 읽기]  ← 병렬 2호출
  턴2: [수정 + changelog + 헤더갱신 + 버전범프 + stability갱신 + grep QC]  ← 순차 의존이므로 1턴 내 직렬 처리
  턴3: [전파판정 ∥ 보고=브리핑 통합저장]  ← 병렬 2호출

  SESSION_CACHE 존재 + stability 변동 없음 예상 → 턴1에서 stability 읽기 스킵 가능 → 실질 2턴
```

### 턴1: 병렬 읽기

```
PARALLEL:
  ❶ UP 파일 읽기
  ❷ UP_stability.md 읽기
  SESSION_CACHE에 stability 스냅샷 있으면 ❷ 스킵
```

### 턴2: 수정 + QC 통합

```
SEQUENCE (단일 턴 내):
  ⓪ INVARIANT_GUARD 3중 검사 → HIGH·MID 감지 시 사용자 확인 요청 후 대기
  ❶ UP 해당 규칙 수정
  ❷ changelog 행 추가
  ❸ 코드블록 헤더 `# UP vX.X` 버전 갱신
  ❹ 파일명 버전 범프 (rename)
  ❺ stability 해당 행 갱신 (frozen→stable 강등 등)
  ❻ grep old 텍스트 잔존 확인 (QC ②)
  ❼ DSL순도 확인 (QC ①) — 수정 내용을 눈으로 확인
  ✗ QC는 위 ❻❼ 2항목만. 항목 추가·변형·재해석 금지. 보고에 QC:①✓②✓ 형식으로 기록.

  FAIL 시 → 즉시 수정 후 재검증. 턴 추가 ✗ (같은 턴 내 루프)
  SESSION_CACHE.current_version 갱신
```

### 턴3: 전파 + 보고=브리핑 통합

```
PARALLEL (반드시 같은 턴에 2개 도구호출 동시 발행):
  ❶ 전파 판정 — 전파맵 조회 → 연쇄대상 리스트
  ❷ 보고=브리핑 통합 저장:
     보고 텍스트를 구성한 뒤, 동일 텍스트를 브리핑 파일로 저장
     별도 구성 단계 없음 — 보고 포맷 = 브리핑 포맷

전파 판정:
  | 판정 | 조치 |
  |------|------|
  | UP → 시스템프롬프트 (내용 변경) | "Cowork 설정에 UP본 반영해주세요" 안내 |
  | UP → 시스템프롬프트 (파일명만 변경) | 스킵 |
  | 전파대상 0건 | "전파대상 없음" 1줄 |
```

### 보고=브리핑 통합 포맷

```
FORMAT (인라인 보고 + 브리핑 파일 공용):
  v{old} → v{new}
  Before/After 테이블 (변경위치·Before·After 3열)
  QC: ①✓ ②✓
  stability: [변동사항 또는 "변동 없음"]
  전파: [대상 또는 "없음"]
  시스템프롬프트: [변경부분 코드블록 또는 "스킵"]
  미결: [시스템프롬프트 복붙 등 후속 필요사항]

SAVE:
  인라인 → 형에게 직접 표시
  파일 → @ref UP §B.④세션브리핑 PATH (YYMMDD-HHmm 포맷)으로 저장
  2개를 별도로 구성하지 않음 — 동일 텍스트 1회 생성, 2곳에 출력
```

---

## FULL_PATH (L3·L4)

L3·L4는 구조적 변경이므로 형 컨펌이 필요하다.

```
PIPE:
  IG(INVARIANT_GUARD) → A(수정) → C(버전범프) → [E(풀QC 4항목) ∥ S(stability 행 갱신)] → [F(전파맵 실행) ∥ D(경로 갱신+grep)] → G(보고=브리핑)
  RULE: IG HIGH·MID → 사용자 "본질 변경 확인함" 명시 전 A 차단 | E검증 실패 → A수정 복귀 (루프)
  ∥ = 병렬 실행 (독립 단계를 같은 턴에 동시 호출)
  ✗ 단계 이름·역할 변형 금지. IG·A~G 정의를 아래에서 정확히 따를 것.
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
Minor(내용수정): 파일명 버전 갱신 + 코드블록 헤더 `# UP vX.X` 갱신 + changelog 행 추가. .9→.10
Major(구조변경): 이전→_archive/ + 새파일 v{M+1}.0
CHANGELOG: "v{버전} | §{섹션} {변경요약 1줄}"
```

### E+S 병렬 (검증 + 안정도)

```
PARALLEL:
  ❶ E. 풀QC (4항목)
    | # | 항목 |
    |---|------|
    | ① | DSL순도: 자연어 산문 잔류 0건 |
    | ② | 규칙보존: 원본 모든 규칙 수정본에 존재 |
    | ③ | 참조무결: @ref 대상 실재 (grep) |
    | ④ | DSL문법: 신규/수정 규칙 구문사양 준수 |
    ✗ 이 4항목만. 항목 추가·변형·재해석 금지. 보고에 QC:①~④✓ 형식으로 기록.

  ❷ S. 안정도 갱신
    FAST_PATH §턴2와 동일 규칙 + 아래 추가:
    L3_RULE: frozen 섹션 수정 → stable 강등은 자동. 보고에서 강조 표시
    L4_RULE: 구조 변경 → 영향받는 모든 섹션 stability 재평가
    MAJOR_VERSION: Major 버전 범프 시 → "stability 전체 리뷰 필요?" 1줄 제안
```

### F+D 병렬 (전파 + 경로)

```
PARALLEL:
  ❶ F. 전파
    전파맵 조회 + 실행
    depth 1(자율): UP→시스템프롬프트, 파일명→참조경로
    depth 2(보고): UP→관련스킬
    BATCH: 2건↑ 병렬 | POST_VERIFY 통합1회

  ❷ D. 경로
    원칙: 볼트 루트 기준 상대경로만
    갱신대상: ❶UP 본문 @ref ❷프로젝트 CLAUDE.md(해당시)
    VERIFY: grep old버전번호 잔존 → 1건↑ = FAIL
```

### G. 보고=브리핑 통합

```
FORMAT:
  v{old}→v{new} | QC:①~④✓ | 전파:[대상] | stability:[변동사항] | 복붙:[대상 또는 스킵]
  REASON: L3/L4는 게이트에서 Before/After를 이미 제시·합의 완료. 보고에서 중복출력 ✗.
  시스템프롬프트 변경시: 변경 섹션 코드블록 1개만 첨부

SAVE: FAST_PATH 보고=브리핑 통합과 동일 방식.
  인라인 표시 + 브리핑 파일 저장. 동일 텍스트, 별도 구성 ✗.
```

---

## Gotchas

- **마운트 미확인 직행 금지:** Agent-Ops/ 접근 불가 상태에서 INIT STEP 1 진입 시 파일 탐색 실패·글롭 0건 루프. STEP 0에서 마운트 상태 선확인 + 필요시 `request_cowork_directory` 호출로 사용자에게 요청. SESSION_CACHE 존재 시에도 STEP 0은 스킵 불가.
- **INIT 스킵 금지 (첫 발동):** 첫 발동에서 경로 확정 건너뛰면 파일 탐색 루프. SESSION_CACHE가 있을 때만 스킵 허용.
- **SESSION_CACHE 과신 금지:** 캐시는 같은 세션 내에서만 유효. 형이 세션 밖에서 UP 파일을 직접 수정했을 가능성이 있으면 캐시를 무효화하고 INIT 재실행.
- **병렬 호출 누락:** ∥로 표기된 단계를 직렬로 실행하면 속도 이점 소멸. 반드시 같은 턴에 복수 도구호출로 발행.
- **보고=브리핑 불일치:** 보고 텍스트를 수정한 뒤 브리핑 파일에 다른 버전을 저장하면 불일치. 동일 텍스트 변수를 2곳에 출력하는 원칙 준수.
- **Cowork 지침은 UP 관할 밖:** `Agent-Ops/Cowork Claude_v2.0.md`는 머신별 VAULT 경로만 보관하는 최소 파일. UP 수정 파이프라인 대상 아님. 변경 필요시 직접 수정.
- **Stability 파일 경로 고정:** `Agent-Ops/UP_stability.md`. UP 파일과 동일 폴더. 경로 탐색 시도 불필요.
- **L0은 S단계 스킵:** L0_PATH는 QC교정이므로 stability 갱신 대상 아님. S단계를 실행하면 불필요한 도구 호출.
