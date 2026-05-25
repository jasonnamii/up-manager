---
name: up-manager
description: |
  UP 통합 관리 1턴 완결. 마운트 강제 → 양쪽(MBP·MBA) 파일 in-place 부분수정 → 검증 2단계. 새 파일·복제·archive·changelog·git·버전증분 전면 폐지. 내장도구 100%·DC bash 전면 ✗. 초고속·심플.
    P1: UP, UP수정, UP관리, user preferences, 한글DSL, 팀UP, 유저프리퍼런스, 사용자설정, UP편집, UP갱신, 듀얼파일, MBP, MBA, 양쪽동기, 싱크, 자동마운트, in-place수정.
    P2: 수정해줘, UP 고쳐줘, 사용자설정 바꿔줘, 선호도 수정해줘, UP 업데이트해줘, 양쪽 다, 싱크해.
    P3: in-place edit, dual-file sync, user preferences, machine-scoped files.
    P4: UP 룰 추가·삭제·재배치·팀 동기·머신 분기 필요할 때.
    P5: .md로, UP파일로.
    NOT: 일반번역(→translator-skill), 프로젝트CLAUDE.md(→project-updater), UP진단(→up-doctor), 스킬편집(→skill-builder).
metadata:
  author: jason
  version: "6.0.0"
license: Proprietary. LICENSE.txt has complete terms
---

# up-manager v6.0 (in-place 초고속·새파일/복제/archive/changelog/git 전면 폐지)

**DSL_LANG ::= KR**. 축명·키·규칙 한국어. 고유명사·호칭 원문.

**v6.0 핵심 (2026-05-25):** 형 운영방침 전면 수용. ① **새 파일·복제 ✗** — 현행 운영본을 그 자리에서 내장 Edit 부분수정. cp·신버전 생성 폐지 ② **archive 이동 ✗** — _archive 단계 전면 삭제 ③ **changelog ✗** — `## Changelog (KR)` 섹션 강제 해제. DSL 단일블록만 ④ **git ✗** — auto-commit·archive·이력 관리 전면 폐지. 롤백은 형 수동 백업 책임 ⑤ **버전증분 ✗** — 같은 날 `_NN` 증분 폐지. 같은 날은 같은 파일 in-place. 날짜 바뀐 첫 수정에만 파일명 날짜 갱신 1회 ⑥ **MBP·MBA 항상 싱크** — 트리거어 없어도 양쪽 동시 in-place 디폴트 ⑦ **2단계 파이프라인** — 마운트+편집 → 검증. INIT·COMMIT 단계 흡수·삭제.

**폐지 (v5.1 → v6.0):** 복제 후 부분수정·_NN 증분·archive 이동·changelog 섹션·git auto-commit·4단계 파이프라인 — **전부 폐기.**

## Skill Boundaries

- **하는 것** — 현행 UP 운영본 in-place 부분수정·양쪽(MBP·MBA) 동시 반영·팀UP 동기·검증
- **안 하는 것** — UP 진단(→ up-doctor) · 프로젝트 CLAUDE.md(→ project-updater) · 일반 번역(→ translator-skill) · 스킬 편집(→ skill-builder) · git 이력 관리(형 수동)

## When to Use

- 형이 "UP 수정해줘·UP 고쳐줘·선호도 바꿔줘" 등 명시
- UP 룰 추가·삭제·재배치 요청
- 팀 UP과 동기 필요 시
- **안 쓸 때** — UP 진단만 원함(→ up-doctor) · 산출물 일반 텍스트 작성

## Prerequisites

진입 전 자동 체크. 미충족 시 STOP + 자동 보정 1회.

**⛔ #1 BLOCKING GATE — 마운트 안 되면 그 다음 전부 작동 ✗.** in-place Edit·Glob 모두 마운트된 볼트 경로(`/sessions/{SID}/mnt/...`) 의존. 마운트 0 = 즉시 STOP.

| # | 체크 | 미충족 시 |
|---|------|-----------|
| 1 | **볼트 마운트 자동 호출 (선행 조건)** — `mcp__cowork__request_cowork_directory` 무조건 자동 호출. 형 트리거어·입력 ✗. **마운트 성공 확인 전 편집 진입 ✗** | 호출 실패·미응답 = 즉시 STOP·INVARIANT #5 FAIL. 재시도 ✗ |
| 2 | **현행 운영본 확인** — Glob `Agent-Ops/UP_user-preferences_*_MBP.md`·`*_MBA.md` 각 최신 1건 | 0건 = STOP·보고 |
| 3 | **오늘 날짜 추출** — `<env> Today's date` verbatim → YYMMDD. 파일명 날짜와 비교 | 같은 날 = 파일명 그대로 in-place / 다른 날 = 그날 첫 수정에만 파일명 날짜 갱신 1회 |
| 4 | **항상 양쪽** — MBP·MBA 둘 다 대상. 트리거어 불요(디폴트 싱크) | 한쪽만 수정 = INVARIANT #6 FAIL |

## ⛔ 핵심 규칙 (7)

| # | 규칙 | 위반 시 |
|---|------|--------|
| 1 | **in-place만** — 현행 운영본을 그 자리에서 내장 Edit. 새 파일·복제·cp·신버전 생성 ✗ | INVARIANT #1 새파일·복제 |
| 2 | **archive·changelog·git·버전증분 전면 ✗** — _archive 이동·`## Changelog` 섹션·git commit·`_NN` 증분 전부 안 함 | INVARIANT #2 폐지룰 부활 |
| 3 | **내장도구 100%·DC bash 전면 ✗** — 본문 편집·읽기·치환·검사 = Read·Write·Edit·Grep·Glob. 폴백 = Obsidian MCP(.md 한정). DC bash·Bash 동원 ✗ | INVARIANT #3 DC bash·Bash 동원 |
| 4 | **헤더 자기 머신 경로 1개·교차박제 ✗** — _MBP에 MBP볼트=만, _MBA에 MBA볼트=만 | INVARIANT #4 교차박제 |
| 5 | **마운트 게이트** — 진입 시 `mcp__cowork__request_cowork_directory` 자동 호출·성공 확인 후 편집 | INVARIANT #5 마운트 누락 |
| 6 | **MBP·MBA 항상 동시** — 트리거어 없어도 양쪽 in-place. 한쪽만 = FAIL | INVARIANT #6 한쪽만 수정 |
| 7 | **DSL 구조 보존** — `## DSL (KR)` 섹션 + 4-backtick 코드블록 래핑 + 기호(`::= ✗ → ●`) 보존 | INVARIANT #7 구조 깨짐 |

## 파일명 체계 (in-place·날짜 유지)

**형식 ::= `UP_user-preferences_YYMMDD_NN_{MBP|MBA}.md`** (현행 유지·새로 안 만듦)

- **같은 날 수정** → 현행 파일 그대로 in-place Edit. `_NN` 증분 ✗·새 파일 ✗
- **다른 날 첫 수정** → 그날 첫 1회만 파일명 날짜 갱신(현행 파일을 신날짜명으로 rename = 내장 Bash `mv` 1회). 이후 같은 날은 in-place
- **archive·git ✗** — 구파일 이동·이력 보존 안 함

## 머신 식별 (런타임 자동)

| 볼트 경로 (마운트) | 머신 | 운영 파일 | 헤더 경로 |
|---|---|---|---|
| `/Users/jason/ObsidianVault` | MBP | `UP_user-preferences_*_MBP.md` | `MBP볼트=/Users/jason/ObsidianVault` |
| `/Users/jason/Library/CloudStorage/Dropbox/ObsidianVault` | MBA | `UP_user-preferences_*_MBA.md` | `MBA볼트=/Users/jason/Library/CloudStorage/Dropbox/ObsidianVault` |

Dropbox 동기로 한 볼트에 양쪽 파일이 함께 있을 수 있음 → 그 자리에서 둘 다 in-place 편집.

**헤더 형식**:

```
※ UP vYYMMDD_NN_{MBP|MBA} [{MBP|MBA}] · YYYY-MM-DD · {MBP|MBA}볼트=/절대/경로 · 룰 메모 · PREV: 직전버전
```

**교차박제 금지**: _MBA에 `MBP볼트=` ✗, _MBP에 `MBA볼트=` ✗.

## 파이프라인 (2단계)

```
① 마운트+편집 — ⓐ 볼트 마운트 자동 호출 (`mcp__cowork__request_cowork_directory`)·성공 확인
                 ⓑ <env> Today's date 추출 → 같은 날=in-place / 다른 날=파일명 날짜 갱신 1회(mv)
                 ⓒ MBP·MBA 현행 운영본 Glob 확정
                 ⓓ 양쪽 파일에 동일 변경 내장 Edit 부분수정 (변경 부분만·헤더 메모 갱신)
② 검증        — Grep 3항목: 4-backtick 2건 / 교차박제 0건 / 양쪽 동일 반영
```

- 복제·archive·git·_NN 증분 **전 단계 없음**
- 양쪽 동시가 디폴트. 트리거어 불요
- 본문 편집·검사 = 내장도구 100%. 파일명 갱신(다른 날)만 내장 Bash `mv` 1회 예외

## ② 검증 (Grep 3항목·내장도구)

1. **4-backtick 래핑** — Grep `^\`\`\`\`` count = 2 (각 파일)
2. **교차박제 0** — _MBP에 Grep `MBA볼트=` 0건 / _MBA에 Grep `MBP볼트=` 0건
3. **양쪽 동일 반영** — 변경 룰 키워드를 양쪽 파일에서 Grep hit 확인

실패 시 같은 턴 자동 보정 1회. 2회차 실패 = STOP+보고.

## Output Path

| 산출물 | 경로 | 비고 |
|---|---|---|
| 운영본 UP (머신별 1개) | `Agent-Ops/UP_user-preferences_YYMMDD_NN_{MBP|MBA}.md` | in-place·새로 안 만듦 |
| 팀 UP | `Agent-Ops/UP_team_vN.md` | 동기 시 갱신 |

archive·git 산출물 **없음**.

## Reference Index

| 파일 | 내용 | 언제 |
|---|---|---|
| `references/init-protocol.md` | 마운트·경로 확정 | 진입 시 |
| `references/team-sync.md` | 팀 UP 동기 + PERSONAL_FILTER 3축 | 팀싱크 시 |

(pipeline.md·invariant-guard.md 등은 v6.0에서 본문에 흡수·참조 최소화)

## Next Phase

- **UP 진단** → `up-doctor`
- **스킬 동기 영향** → `skill-builder`
- **세션 마무리** → `session-briefing`

## Failure Modes (Gotchas)

| 함정 | 대응 |
|---|---|
| 새 파일·복제 생성 | **INVARIANT #1 FAIL.** 현행 파일 in-place Edit만 |
| _NN 증분으로 신파일 | **폐지.** 같은 날은 같은 파일 그대로 |
| archive 이동 시도 | **폐지.** 구파일 이동 안 함 |
| changelog 섹션 추가 | **폐지.** DSL 단일블록만 |
| git add·commit 시도 | **폐지.** 이력 관리 안 함. DC bash·Bash로 git ✗ |
| 한쪽 머신만 수정 | **INVARIANT #6 FAIL.** 항상 MBP·MBA 양쪽 |
| 교차박제 | **INVARIANT #4 FAIL.** 자기 머신 경로만 |
| DC bash sed로 본문 치환 | **INVARIANT #3 FAIL.** 내장 Edit만 |
| 본문 편집·검사를 Bash로 | **INVARIANT #3 FAIL.** Read·Grep·Edit |
| 마운트 없이 진입 | **INVARIANT #5 FAIL.** 진입 즉시 자동 마운트 호출 |
| 4-backtick 래핑 누락 | **INVARIANT #7.** 검증 ①에서 자동 보정 |
| 다른 날인데 파일명 안 바꿈 | 그날 첫 수정에만 mv 1회로 날짜 갱신. 이후 in-place |
| 다른 날인데 매 수정 파일명 갱신 | 첫 1회만. 같은 날 이후는 in-place |

## 모프 적용

- 트리거 → "모프로·모프 모드·Morph로" hit 시에만. 없으면 내장도구(Edit·Write·replace_all)
- 정본 보호 → UP*.md는 단일 정본. 모프 ✗ 디폴트, 내장 Edit 우선
- 폴백 → Morph 실패 시 내장도구 → Obsidian MCP. 동일 도구 1회 실패 시 재시도 ✗
