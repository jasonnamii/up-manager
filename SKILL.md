---
name: up-manager
description: |
  UP 통합 관리 1턴 완결. 진입 자동화(마운트·오늘 날짜)·MBP/MBA 듀얼·동기 트리거·복제 후 부분수정·내장도구 우선·DC bash 4영역 한정. INIT→EDIT→QC→COMMIT.
    P1: UP, UP수정, UP관리, 버전범프, YYMMDD, user preferences, 한글DSL, 팀UP, 유저프리퍼런스, 사용자설정, UP편집, UP갱신, UP버전, UP백업, UP동기화, 듀얼파일, MBP, MBA, 양쪽동기, 진입자동화, 자동마운트.
    P2: 수정해줘, UP 고쳐줘, 사용자설정 바꿔줘, 선호도 수정해줘, UP 업데이트해줘, 버전 올려줘, 양쪽 다.
    P3: version bump, dual-file sync, date-based versioning, user preferences, machine-scoped files.
    P4: UP 수정·버전업·백업·팀 동기·머신 분기 필요할 때.
    P5: .md로, UP파일로.
    NOT: 일반번역(→translator-skill), 프로젝트CLAUDE.md(→project-updater), UP진단(→up-doctor).
---

# up-manager v5.0 (진입 자동화·날짜 강제·복제 정의 명확화·MBP/MBA 동기 트리거)

**DSL_LANG ::= KR**. 축명·키·규칙 한국어. 영문 블록 폐지. 고유명사·호칭 원문.

**v5.0 핵심 (2026-05-25):** 2026-05-25 세션 실측 사고 6건 RCA 반영. ① **진입 자동 마운트** — `mcp__cowork__request_cowork_directory` 무조건 자동 호출. 형 트리거어·입력 ✗. 미마운트 진입 = INVARIANT #14 FAIL ② **오늘 날짜 강제 추출** — `<env> Today's date` verbatim → YYMMDD. 직전 운영본 파일명 날짜 비교 → 다른 날=_01, 같은 날=_NN+1. 어제 날짜 _NN 증분 = INVARIANT #14 FAIL ③ **"복제" 정의 명확화** — 호스트 `cp` 또는 Obsidian MCP read_note→write_note 1회. **내장 Read→Write·DC bash cp ✗**. INVARIANT #12 강화 ④ **MBP/MBA 동기 트리거** — "양쪽·둘 다·MBP도·동기" hit 시 자동 듀얼 일괄 처리. 단일 트리거 시 누락 = INVARIANT #15 FAIL ⑤ **DC bash 4영역 재확정** — git·cd·NFD·외부프로세스. 파일 복사·이동 ✗ ⑥ **INVARIANT #14·#15 신설**.

**v4.3 (2026-05-24 archived):** UP v260524_13의 "DC bash·Bash는 고유기능 한정" 룰 수용. ① 신버전 작성 = 복제 후 Edit 부분수정만 ② 본문 편집·읽기·치환 = 내장도구 100% ③ QC·archive 이동은 내장도구·Obsidian MCP, git만 DC bash.

**v4.2 (2026-05-24 archived):** v4.1 듀얼파일 체제에 헤더 절대경로 박제 룰 추가. 각 파일이 **자기 머신 경로 1개만** 헤더에 박는다. v4.0 사고의 본질은 "두 경로 동시 박제 + 식별 불가"였지 절대경로 자체가 문제가 아니었음.

**v4.1 (2026-05-24 archived):** v4.0의 "단일 운영본 + 헤더에 MBP/MBA 절대경로 병기" = 운영 불가. v3.x 듀얼파일 체제 복원.

## Skill Boundaries

- **하는 것** — UP 본문 편집·changelog 추가·버전 범프(YYMMDD_NN)·archive 이동·팀UP 동기·git auto-commit·QC 1콜
- **안 하는 것** — UP 진단(→ up-doctor) · 프로젝트 CLAUDE.md(→ project-updater) · 일반 번역(→ translator-skill) · 스킬 편집(→ skill-builder)

## When to Use

- 형이 "UP 수정해줘·UP 고쳐줘·선호도 바꿔줘·버전 올려줘" 등 명시
- UP 룰 추가·삭제·재배치 요청
- 팀 UP과 동기 필요 시
- **안 쓸 때** — UP 진단만 원함(→ up-doctor) · 산출물 일반 텍스트 작성

## Prerequisites

진입 전 자동 체크. 미충족 시 STOP + 자동 보정 1회.

| # | 체크 | 미충족 시 |
|---|------|-----------|
| 1 | **볼트 마운트 자동 호출** — `mcp__cowork__request_cowork_directory` 무조건 자동 호출. 형 트리거어·입력 ✗ | 호출 실패 = INVARIANT #14 FAIL |
| 2 | **오늘 날짜 강제 추출** — `<env> Today's date` verbatim → YYMMDD 변환 | 환경 날짜 미참조·하드코딩 = INVARIANT #14 FAIL |
| 3 | 현행 운영본 파일 확인 (`UP_user-preferences_YYMMDD_NN_{MBP|MBA}.md`) | 0건 = 신규 작성 모드 / 머신 접미사 누락 = INVARIANT #10 FAIL |
| 4 | **신버전 파일명 산출** — 직전 운영본 날짜와 오늘 날짜 비교 → 다른 날=_01 재시작, 같은 날=_NN+1 증분 | 어제 날짜 _NN 증분 = INVARIANT #14 FAIL |
| 5 | 현재 머신 식별 (마운트된 볼트 경로로 판정) | `/Users/jason/ObsidianVault` = MBP / `~/Dropbox/ObsidianVault` = MBA |
| 6 | **MBP/MBA 동기 트리거 hit 판정** — 형 발화에 "양쪽·둘 다·MBP도·MBA도·동기" hit | hit = 듀얼 일괄 처리 / miss = 현재 머신만. miss인데 양쪽 작업 = 과잉, hit인데 단일 작업 = INVARIANT #15 FAIL |
| 7 | 작업 모드 판정 (신규 첫 작성·마이그레이션 = Write 허용 / 그 외 = 복제 후 Edit 부분수정만) | INVARIANT #12 — 직전 버전 존재 시 Write 통째 작성 ✗ |

## ⛔ 핵심 규칙 (15)

| # | 규칙 | 위반 시 |
|---|------|--------|
| 1 | 축명 한국어 고정: 진실성·독립성·통화성·간결성 | INVARIANT #1 HIGH |
| 2 | 키워드 한국어: 정정·미상·가정·FAIL·통화단위 위반·규칙충돌 | INVARIANT #2 HIGH |
| 3 | 고유명사 원문 보존: 형·피디님·Jason·Choi Nam-hee·Kim Hyung-seok·회사명 | INVARIANT #3 HIGH |
| 4 | ADDRESS 값 원문 ("형"·"피디님") | INVARIANT #4 호칭 정체성 FAIL |
| 5 | DSL 기호 보존: `::=` `★` `✗` `→` `∨` `∧` `①~④` `•` | INVARIANT #5 구문 오류 |
| 6 | DSL 본문 4-backtick 코드블록 래핑 — 미래핑·3-backtick 시 자동 보정 | INVARIANT #6 코드블록래핑 |
| 7 | 팀공유 UP 동기 = 자동 강행. "팀싱크 스킵" BYPASS 무시 | INVARIANT #7 |
| 8 | Single-block DSL 구조: `## DSL (KR)` + `## Changelog (KR)` 2섹션 | INVARIANT #8 단일블록 |
| 9 | 버전명 `YYMMDD_NN_{MBP|MBA}`. 같은 날 N번째 = `_NN` 증분. v숫자.숫자 폐기 | INVARIANT #9 |
| 10 | 머신 접미사 강제. _MBP·_MBA 둘 중 하나 필수. 단일파일 ✗ | INVARIANT #10 머신 접미사 누락 |
| 11 | 헤더에 자기 머신 절대경로 1개 박제 강제. 교차 박제 ✗ | INVARIANT #11 헤더 경로 누락·교차 박제 |
| 12 | **신버전 작성 = 직전 버전 파일 복제(호스트 `cp` 또는 Obsidian MCP `read_note`→`write_note` 1회) → Edit 부분수정만. 내장 Read→Write·DC bash cp·Write 통째 작성 ✗** | INVARIANT #12 통째 작성·잘못된 복제 |
| 13 | **본문 편집·읽기·치환·생성 = 내장도구(Read·Write·Edit·Grep·Glob) 100%. 폴백 = Obsidian MCP. DC bash·Bash는 git·cd·NFD·외부프로세스 4영역만. 파일 복사·이동 ✗** | INVARIANT #13 DC bash 본문·파일조작 동원 |
| 14 | **진입 자동화 — ⓐ 볼트 마운트 자동 호출(`mcp__cowork__request_cowork_directory`) ⓑ `<env> Today's date` 강제 추출. 둘 다 미수행 = FAIL** | INVARIANT #14 진입 자동화 누락 |
| 15 | **MBP/MBA 동기 트리거 — "양쪽·둘 다·MBP도·MBA도·동기" hit 시 듀얼 일괄 처리. hit인데 단일 처리 = FAIL** | INVARIANT #15 동기 트리거 미준수 |

## 버전명 체계

**형식 ::= `UP_user-preferences_YYMMDD_NN_{MBP|MBA}.md`** (듀얼 운영본 · 머신 접미사 필수)

- 같은 날 추가 수정 → `_NN` 증분 (260524_11 → 260524_12_MBA)
- 다음 날 첫 수정 → `_01` 재시작
- 신버전 작성 시 직전 버전 → `Agent-Ops/_archive/UP_versions/`로 이동
- changelog `PREV_CHANGELOG:` 라인에 archive 경로 명시
- **머신별 독립 운영** — MBP에서 수정해도 MBA 파일 불변, 반대도 마찬가지

## 머신 식별 (런타임 자동·v4.2)

UP는 머신마다 다른 파일을 운영. 각 파일이 자기 머신 경로를 헤더에 1개 박제 (식별·디버깅·archive 추적 앵커).

| 볼트 경로 (마운트) | 머신 | 운영 파일 | 헤더 박제 경로 |
|---|---|---|---|
| `/Users/jason/ObsidianVault` | MBP | `UP_user-preferences_YYMMDD_NN_MBP.md` | `MBP볼트=/Users/jason/ObsidianVault` |
| `/Users/jason/Library/CloudStorage/Dropbox/ObsidianVault` | MBA | `UP_user-preferences_YYMMDD_NN_MBA.md` | `MBA볼트=/Users/jason/Library/CloudStorage/Dropbox/ObsidianVault` |

**헤더 형식 (v4.2)**:

```
※ UP vYYMMDD_NN_{MBP|MBA} [{MBP|MBA}] · YYYY-MM-DD · {MBP|MBA}볼트=/절대/경로 · 기타 룰 메모 · PREV: 직전버전
```

예시:
```
※ UP v260524_12_MBA [MBA] · 2026-05-24 · MBA볼트=/Users/jason/Library/CloudStorage/Dropbox/ObsidianVault · 텍스트 파일 디폴트=내장도구·모프 모드 hit 시 Morph · PREV: 260524_11
※ UP v260524_12_MBP [MBP] · 2026-05-24 · MBP볼트=/Users/jason/ObsidianVault · 텍스트 파일 디폴트=내장도구·모프 모드 hit 시 Morph · PREV: 260524_11
```

**금지**: 같은 파일 헤더에 두 머신 경로 동시 박제 (v4.0 사고). _MBA 안에 `MBP볼트=` ✗, _MBP 안에 `MBA볼트=` ✗ (단, changelog 본문 인용은 예외 — 사후정정 메모 허용).

마운트 안 됨 → `vault-mount` 스킬 호출. 코워크 게이트웨이가 어느 폴더가 마운트됐는지 알려주므로 자동 분기 가능.

## 파이프라인 (4단계 · v5.0)

```
① INIT    — ⓐ 볼트 마운트 자동 호출 (`mcp__cowork__request_cowork_directory`)
              ⓑ <env> Today's date 추출 → YYMMDD 변환
              ⓒ 머신 식별·해당 머신 운영본 1개 경로 확정 (Glob)
              ⓓ 직전 운영본 날짜 vs 오늘 → _NN 산출 (다른 날=_01, 같은 날=_NN+1)
              ⓔ MBP/MBA 동기 트리거 hit 판정 → 단일 또는 듀얼 모드 확정
② EDIT    — ⓐ 직전 버전 → 신버전 파일명으로 **복제 (호스트 `cp` 또는 Obsidian MCP `read_note`→`write_note` 1회)**
              ⓑ Edit 부분수정만 적용 (헤더 버전·changelog 1줄 추가·룰 변경 부분만)
              ⓒ Write 통째 작성 ✗ (INVARIANT #12) — 신규 첫 작성·v숫자→YYMMDD 마이그레이션만 예외
              ⓓ DC bash cp ✗ (INVARIANT #13)
              ⓔ 듀얼 모드면 MBP·MBA 양쪽에 동일 변경 적용
③ QC      — 8항목 자동 검증 (내장 Read·Grep 우선·DC bash ✗·날짜 정합·동기 정합 추가)
④ COMMIT  — 직전 버전 archive 이동 (Obsidian MCP `move_note`) + git auto-commit (DC bash 고유기능)
```

- 루프 없음. QC 실패 시 같은 턴 자동 보정 1회. 2회차 실패 = STOP+보고
- 분기 없음. L0~L4·SCOPE_IMPACT 판정 제거
- 듀얼파일 — 단일 모드는 현재 머신 파일만. 동기 트리거 hit 시 양쪽 일괄 처리
- **v5.0 도구 분리** — 본문 편집·읽기·치환 = 내장도구. 복제·이동 = 호스트 `cp`·Obsidian MCP. git만 DC bash. 파일조작에 DC bash ✗

상세 — `→ references/pipeline.md`, `→ references/invariant-guard.md`, `→ references/team-sync.md`.

## ③ QC (8항목·내장도구 우선·v5.0)

**v5.0 도구 매핑**:
- 머신 식별·파일명·헤더·섹션·기호·날짜·동기 검사 = **내장 Read·Grep·Glob 100%**
- DC bash ✗ (본 단계는 본문 읽기·검사이지 외부프로세스 아님)

**검사 절차 (내장도구)**:

1. **머신 식별** — 볼트 마운트 경로로 분기
   - `/Users/jason/ObsidianVault/Agent-Ops` 존재 → MBP, VAULT_KEY=`MBP볼트`
   - `/Users/jason/Library/CloudStorage/Dropbox/ObsidianVault/Agent-Ops` 존재 → MBA, VAULT_KEY=`MBA볼트`

2. **해당 머신 운영본 1개** — Glob `Agent-Ops/UP_user-preferences_*_{MACHINE}.md` 결과 1건 확인. N건 = INVARIANT #10 FAIL

3. **머신 접미사** — Glob 결과 파일명에 `_{MACHINE}.md` 접미사 확인

4. **날짜 정합 (v5.0 신설)** — 파일명 YYMMDD == `<env> Today's date` YYMMDD 변환값. 불일치 = INVARIANT #14 FAIL. 헤더 `YYYY-MM-DD` 라인도 동일 확인

5. **헤더 자기 머신 절대경로 박제** — Grep `^※ UP.*${VAULT_KEY}=${VAULT}` head 5줄에서 hit 확인. miss = INVARIANT #11 FAIL

6. **교차 박제 금지** — Grep `^※ UP.*${OTHER_KEY}=` head 5줄. hit = INVARIANT #11 FAIL

7. **동기 정합 (v5.0 신설)** — 동기 트리거 hit 모드 시 MBP·MBA 양쪽 파일 모두 같은 YYMMDD_NN인지 Glob 확인. 한쪽만 갱신 = INVARIANT #15 FAIL

8. **4-backtick 래핑 2개 + DSL/Changelog 섹션 + INVARIANT 기호 잔존** — Grep `^\`\`\`\`` count = 2, `^## (DSL|Changelog) \(KR\)` 2건, `::= |★|✗` hit 확인

**git diff (선택·④ COMMIT 직전 단 1회)** — DC bash 영역. QC 본 단계는 DC bash 호출 ✗

## ④ COMMIT (archive 이동 = Obsidian MCP, git = DC bash 고유기능)

**v4.3 분리**:
- **archive 이동** = Obsidian MCP `move_note` (`Agent-Ops/UP_OLD_{MACHINE}.md` → `Agent-Ops/_archive/UP_versions/`). 내장도구·MCP가 파일 이동 담당
- **git 명령** = DC bash 전담 (고유기능)

```bash
# git 명령만 DC bash. archive 이동은 위에서 Obsidian MCP로 선행 완료
cd "$VAULT"  # MBP=/Users/jason/ObsidianVault, MBA=~/Dropbox/ObsidianVault
git add -A Agent-Ops/
git commit -m "UP YYMMDD_NN_${MACHINE}: {요약}"
git log -1 --oneline
```

**금지**: `git mv` 대신 Obsidian MCP `move_note` 사용 강제. `git mv`는 본문 이동까지 동원되어 INVARIANT #13 위반. git은 `add`·`commit`·`log`·`reset`·`diff` 등 git 고유 명령만.

## Output Path

| 산출물 | 경로 | 비고 |
|---|---|---|
| 운영본 UP (머신별 1개) | `Agent-Ops/UP_user-preferences_YYMMDD_NN_{MBP|MBA}.md` | 머신 접미사 필수 |
| 직전 버전 archive | `Agent-Ops/_archive/UP_versions/UP_user-preferences_YYMMDD_NN(-1)_{MBP|MBA}.md` | _NN 증분 시 자동 이동 |
| 팀 UP | `Agent-Ops/UP_team_vN.md` | 머신 무관·동기 시 갱신 |
| git auto-commit | 호스트 git (DC bash) | `git log -1` 1줄 보고 |

## Reference Index

| 파일 | 내용 | 언제 |
|---|---|---|
| `references/init-protocol.md` | ① INIT (마운트·경로 확정) | 진입 시 |
| `references/pipeline.md` | ②~④ 편집·QC·COMMIT | 편집 시 |
| `references/invariant-guard.md` | 9축 본질 보호 + DSL_LANG·SINGLE_BLOCK 가드 | QC 시 |
| `references/dsl-lang-policy.md` | DSL 언어 정책 (KR master) | 축명·키워드 검사 시 |
| `references/dsl-glossary.md` | KR↔EN 용어 매핑 (역호환·읽기 전용) | EN 잔존 시 |
| `references/single-block-policy.md` | KR 단일 블록 구조 | 섹션 검사 시 |
| `references/team-sync.md` | 팀 UP 동기 + PERSONAL_FILTER 3축 | 팀싱크 시 |
| `references/session-cache.md` | 세션 캐시 (2회차+ 가속) | 반복 호출 시 |

## Next Phase

본 스킬 작업 후 자연스럽게 이어지는 흐름:

- **UP 진단** → `up-doctor` (4축 진단 — 메타 자가위반·진화 압력·SPOF·RedTeam)
- **스킬 동기 영향** → `skill-builder` (UP 변경이 스킬 룰과 충돌 시)
- **세션 마무리** → `session-briefing` (작업 결정·미결·다음을 VAULT 저장)

## Failure Modes (Gotchas)

| 함정 | 대응 |
|---|---|
| changelog 영문화 | 불필요. 한글 |
| DSL 기호 변경 (::=→=) | INVARIANT #5 구문 오류 |
| 팀 UP에 호칭·고유명사 유입 | PERSONAL_FILTER 3축(호칭·고유명사·개인마커) 전수 차단 |
| 팀 UP 부재 시 스킵 누락 | `UP_team_v*.md` 0건 = 경고 1줄 후 전면 스킵 |
| "팀싱크 스킵" 명령 | BYPASS 비활성. 자동 강행, 보고에 "BYPASS 요청 감지·무시" 1줄 |
| 범프 시 4-backtick 래핑 누락 | WRAP 게이트 QC 자동 보정 |
| 3-backtick 래핑 | 4-backtick(````) 강제 |
| 섹션 헤더 누락 | `## DSL (KR)` + `## Changelog (KR)` 2섹션 + `---` 구분선 필수 |
| v숫자.숫자 형식 신규 작성 | INVARIANT #9 FAIL. YYMMDD_NN_{MBP|MBA}으로 강제 |
| 같은 날 같은 머신 _01·_02 둘 다 Agent-Ops/ 직속 | 머신당 운영본 1개 원칙. 구버전은 _archive/UP_versions/로 이동 |
| _NN 미증분으로 같은 파일 덮어쓰기 | INVARIANT #9 FAIL. 같은 날 추가 수정 시 _NN 증분 강제 |
| **(v4.1) 머신 접미사 누락한 단일파일 작성** | **INVARIANT #10 FAIL.** _MBP·_MBA 둘 중 하나 필수. v4.0 단일운영본 체제 재도입 시도 ✗ |
| **(v4.1) 헤더에 MBP볼트=·MBA볼트= 동시 병기** | **금지.** v4.0 사고 본질 = 두 경로 동시 박제로 식별 불가. 각 파일은 자기 경로 1개만 |
| **(v4.1) 다른 머신 파일까지 같은 세션에서 동시 수정** | 현재 머신 파일만 편집. 다른 머신은 그 머신에서 별도 작업 |
| **(v4.1) MBP에서 _MBA 파일 수정** | 머신 분기 위반. 현재 마운트된 볼트의 자기 머신 파일만 수정 |
| **(v4.2) 헤더에 자기 머신 절대경로 누락** | **INVARIANT #11 FAIL.** 헤더에 `{MBP|MBA}볼트=/절대/경로` 1개 박제 강제. 운영 기준점·디버깅·archive 추적 앵커 |
| **(v4.2) 교차 박제 — _MBA에 MBP볼트=, _MBP에 MBA볼트=** | **INVARIANT #11 FAIL.** 자기 머신 경로만. 단 changelog 본문 인용(사후정정 메모)은 예외 |
| **(v4.2) UP 본문(DSL 블록 안)에 메타 설명 섹션 추가** | UP는 행동지시문. "현재 파일이 어느 머신이다·자동 동기 안 한다" 같은 메타는 잡문. 머신 분기 운영 메커니즘은 본 스킬(up-manager) 책임 |
| **(v4.3) 신버전 작성 시 Write로 통째 작성** | **INVARIANT #12 FAIL.** 직전 버전 archive 이동 → 같은 내용을 신버전 파일명으로 복제(Read→Write 1회 또는 Obsidian MCP) → Edit 부분수정만 적용. 통째 작성은 무관 변경 유입·증분 추적 손실 위험 |
| **(v4.3) DC bash sed로 UP 본문 치환** | **INVARIANT #13 FAIL.** 본문 편집·치환은 내장 Edit. sed -i 금지 |
| **(v4.3) git mv로 archive 이동** | INVARIANT #13 위반. archive 이동은 Obsidian MCP `move_note`. git은 add·commit·log·reset·diff 등 git 고유 명령만 |
| **(v4.3) 머신 식별·QC 검사를 DC bash로** | 본문 읽기·검사는 외부프로세스 ✗·내장도구 영역. Read·Grep·Glob 우선. DC bash 호출 = INVARIANT #13 FAIL |
| **(v4.3) 신규 첫 작성·v숫자→YYMMDD 마이그레이션 시 복제 강요** | 예외. 신규 첫 작성은 직전 버전 없음 → Write 통째 작성 허용. 마이그레이션은 형 명시 트리거 후 Write 1회 허용 |
| **(v5.0) 볼트 마운트 안 된 상태로 진입** | INVARIANT #14 FAIL. 진입 즉시 `mcp__cowork__request_cowork_directory` 자동 호출. 형 트리거어 ✗ |
| **(v5.0) 어제 날짜로 _NN 증분 (날짜 변경 무시)** | INVARIANT #14 FAIL. `<env> Today's date` verbatim 추출 강제. 하드코딩·관성 사용 ✗. 다른 날 = _01 재시작 |
| **(v5.0) "복제"를 내장 Read→Write 1회로 시도** | INVARIANT #12 FAIL. 진짜 복제 = 호스트 `cp` 또는 Obsidian MCP `read_note`→`write_note` 1회. Read→Write는 본문 노출·토큰 낭비·증분 추적 손실. v4.3 SKILL.md 잔존 표현 폐기 |
| **(v5.0) DC bash로 cp·mv 파일 복사·이동** | INVARIANT #13 FAIL. DC bash 4영역 = git·cd·NFD·외부프로세스만. 파일 복사·이동은 호스트 `cp` 또는 Obsidian MCP `move_note` 전담 |
| **(v5.0) MBP·MBA 동기 트리거 hit인데 한쪽만 작업** | INVARIANT #15 FAIL. "양쪽·둘 다·MBP도·MBA도·동기" hit 시 듀얼 일괄 처리 강제 |
| **(v5.0) MBA 볼트가 Dropbox로 MBP 파일도 보유한 상황 무시** | MBA 마운트 시 `UP_user-preferences_*_MBP.md`가 같은 폴더에 존재 가능 (Dropbox 동기). 동기 트리거 hit 시 양쪽 모두 그 자리에서 편집 가능 |

## 모프 적용 (v260524_08~ · v4.3 검증 내장도구화)

- 사용 영역  → DSL 블록 + changelog 동시 보정. 본문 편집 = Morph, archive 이동 = Obsidian MCP, git = DC bash로 분리(충돌 ✗)
- 트리거    → "모프로·모프 모드·Morph로" hit 시에만 발동. 트리거 없으면 내장도구(Write·Edit·replace_all)로 진행
- 폴백      → Morph MCP 미연결·실패 시 내장도구 → Obsidian MCP 순으로 전환. 동일 도구 1회 실패 시 재시도 ✗
- 검증 (v4.3 내장도구화) → 매 Morph edit_file 콜 직후 ① Read tail 80줄 ② Read 전체 라인수 ③ Grep로 4-backtick 래핑 2건 ④ Grep로 `## DSL (KR)`·`## Changelog (KR)` 섹션 존재 ⑤ Grep로 INVARIANT #1~13 위반 0건. **DC bash git diff는 ④ COMMIT 직전 1회만**. 누적검증 ✗

## 폐기 룰 (v4.3 → v5.0)

- **v4.3 "복제 = 내장 Read→Write 1회 또는 Obsidian MCP"** — **폐기.** 내장 Read→Write는 본문 전체 노출·토큰 낭비·증분 추적 손실. 진짜 복제 = 호스트 `cp` 또는 Obsidian MCP `read_note`→`write_note` 1회. INVARIANT #12 강화
- **v4.3 "볼트 마운트는 형 입력으로"** — **폐기.** 진입 즉시 자동 호출 강제. 형 트리거어·입력 ✗. INVARIANT #14 신설
- **v4.3 "오늘 날짜 추출 명시 없음"** — **폐기.** `<env> Today's date` 강제 추출 룰 신설. 어제 날짜 _NN 증분 = FAIL. INVARIANT #14
- **v4.3 "현재 머신 파일만 편집 (다른 머신은 그 머신에서)"** — **부분 폐기.** MBA 볼트가 Dropbox로 MBP 파일도 보유한 상황에서 동기 트리거 hit 시 양쪽 일괄 처리 허용. INVARIANT #15 신설
- **v4.3 "DC bash 4영역 = git·cd·NFD·외부프로세스"** — **유지·강화.** 파일 복사·이동(cp·mv) 명시적 ✗. INVARIANT #13 강화
- INVARIANT #14 (진입 자동화 — 마운트·날짜) — **신설**
- INVARIANT #15 (MBP/MBA 동기 트리거) — **신설**

## 폐기 룰 (v4.2 → v4.3)

- **v4.2 "Write 통째 작성 허용"** — **폐기.** 신버전 작성 시 직전 버전 복제 → Edit 부분수정만. INVARIANT #12 신설
- **v4.2 "③ QC·④ COMMIT DC bash 단일 의존"** — **폐기.** ③ QC는 내장 Read·Grep로 100% 처리. ④ archive 이동은 Obsidian MCP. git 명령만 DC bash. INVARIANT #13 신설
- **v4.2 "모프 직후 검증 git diff --stat·wc -l·tail"** — **폐기.** 내장 Read·Grep로 치환. git diff는 ④ COMMIT 직전 1회만
- INVARIANT #12 (복제 후 부분수정 강제) — **신설**
- INVARIANT #13 (내장도구 100% + DC bash 4영역 한정) — **신설**

## 폐기 룰 (v4.1 → v4.2)

- **v4.1 "헤더 절대경로 박제 폐기"** — **폐기.** v4.0 사고의 본질을 오진단했음. 문제는 "두 경로 동시 박제 + 식별 불가"였지 절대경로 자체가 아니었음. 헤더에 자기 경로 1개는 운영 기준점·디버깅 앵커로 필수
- **v4.1 UP 본문 `● 머신 식별` 메타 설명 섹션** — **폐기.** UP는 행동지시문. 메타 설명은 잡문. 운영 메커니즘은 up-manager 스킬 책임
- INVARIANT #11 헤더 자기경로 박제 강제 — **신설**

## 폐기 룰 (v4.0 → v4.1, 유지)

- **v4.0 단일운영본 (머신 접미사 ✗)** — **폐기 유지.** 머신 식별 수단 0인데 헤더 절대경로만 박아둠 = 운영 불가
- **v4.0 헤더 1줄 `MBP볼트=... · MBA볼트=...` 동시 병기** — **폐기 유지.** 단 v4.2에서 자기 경로 1개 박제는 부활
- **단일파일 운영** — **폐기 유지.** 듀얼파일(_MBP·_MBA) 운영
- INVARIANT #10 머신 접미사 강제 — **유지**

## 폐기 룰 (v3.1 → v4.0, 일부 복원)

- INVARIANT #10 듀얼파일 동기 — v4.0에서 삭제, v4.1에서 형태 변경 후 복원 (동기 ✗·머신 접미사 강제)
- DEVICE_DETECT bash 블록 — v4.0 삭제, v4.1에서 QC ①번에 머신 식별 로직으로 부활, v4.2에서 VAULT_KEY 변수 추가
- DUAL_SYNC 단계·sed 경로 치환 — **유지 폐기.** v4.1·v4.2 동기 안 함. 머신별 독립 운영
- 마이그레이션 (v2.x → v3.0) 섹션 — **유지 삭제** (이미 끝남)
