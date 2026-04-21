# TEAM_SYNC — 팀공유 UP 동기화

개인 UP 수정 후 같은 폴더의 팀공유 UP에 공통 규칙을 전파. 개인 커스텀(호칭·고유명사·PERSONAL 마커 블록)은 제외.

**트리거:** 개인 UP 수정 파이프라인 완료 직후 **자동 실행**(기본 A모드). BYPASS: 사용자 "팀싱크 스킵" 명시 시 1회 허가.

---

## TARGET

```
개인: Agent-Ops/UP_user-preferences_v{N}.md
팀:   Agent-Ops/UP_team_v{M}.md   (같은 폴더, 버전 독립)
```

파일 부재 시 경고 1줄 후 스킵 (임의 생성 ✗).

---

## PERSONAL_FILTER — 개인 커스텀 판정 (3축)

팀 UP에 유입 ✗. 개인 UP 수정 내용이 아래 3축 중 하나라도 해당하면 팀 동기화 대상에서 제외.

| 축 | 기준 | 예시 |
|----|------|------|
| **① HONORIFIC** | 호칭 관련 블록(`ADDRESS`, `형`, `피디님`, `MENTOR`, 2인칭·3인칭 호칭 규칙) | `ADDRESS ::= "형"`, `MENTOR = 피디님(3인칭 전용)` |
| **② PROPER_NOUN** | 개인 고유명사(`Jason`, `형`, `피디님`, 회사명, 프로젝트명, 개인 이메일·경로) | `USER = Jason(형)`, `jasoncnh@gmail.com` |
| **③ PERSONAL_MARKER** | `<!-- PERSONAL -->` ~ `<!-- /PERSONAL -->` 섹션 전체 | 마커 사이의 모든 라인 |

**판정 순서:** ③ 마커 우선(명시적) → ① 호칭 → ② 고유명사. 하나라도 매치 = 팀 UP 유입 차단.

**역방향 검사(팀 UP 오염 차단):** 팀 UP에 개인 커스텀 3축 항목이 기존재하거나 신규 유입 시 HIGH 경고 발동.

---

## PIPE

```
개인 UP 수정 완료(FAST/FULL 파이프라인 G단계 보고 완료 후)
  → STEP 1: 팀 UP 경로 확인 (SESSION_CACHE.up_team_path, 없으면 Agent-Ops/ glob)
  → STEP 2: 개인 UP diff 산출 (이번 수정의 Before/After)
  → STEP 3: PERSONAL_FILTER 적용 → 공통 변경분만 추출
  → STEP 4: 팀 UP INVARIANT_GUARD (역방향 — 개인 커스텀 유입 차단)
  → STEP 5: 팀 UP Edit (같은 규칙·같은 위치, Write 금지)
  → STEP 6: 팀 UP 버전 범프 (독립 버전, Minor)
  → STEP 7: 팀 UP QC (grep old 텍스트 잔존 확인)
  → STEP 8: TEAM_SYNC 보고 (Before/After 3열 + 제외된 개인 커스텀 목록)
```

---

## STEP 3 — 공통 변경분 추출

```
공통분 = (개인 UP diff) − (PERSONAL_FILTER 매치 블록)

추출 규칙:
  ① DSL 축·키·규칙 영문 고정 블록 → 공통(동기화)
  ② 본질 기능(TRUTH·INDEPENDENCE·CURRENCY·BREVITY 등 축 규칙) → 공통
  ③ FAIL·✗ 금지조항 → 공통
  ④ CHANGELOG 행 → 공통(한글 허용)
  ⑤ HONORIFIC·PROPER_NOUN·PERSONAL_MARKER 블록 → 제외

제외 로그: 팀싱크 보고에 "제외: [블록명] (사유: ①/②/③)" 형식 기록
```

---

## STEP 4 — 역방향 INVARIANT_GUARD

팀 UP 편집 전, 개인 커스텀 3축 항목이 `new_string`에 포함되는지 검사.

| 감지 | 등급 | 조치 |
|------|------|------|
| `new_string`에 `"형"`·`"피디님"`·`Jason`·회사명 포함 | **HIGH** | 차단 + 재추출 |
| `new_string`에 `ADDRESS`·`MENTOR`·개인 이메일 포함 | **HIGH** | 차단 + 재추출 |
| `new_string`이 PERSONAL 마커 내부 내용 포함 | **HIGH** | 차단 + 재추출 |
| 기존 팀 UP에 위 항목이 **이미** 존재 | **MID** | 경고 + 사용자 컨펌(삭제 권고) |

HIGH = 컨펌 없이 자동 차단. STEP 3로 복귀 후 재필터링.

---

## STEP 5 — 팀 UP Edit 규칙

```
- Write.덮어쓰기 ✗ → Edit only (개인 UP과 동일 원칙)
- 같은 규칙은 같은 위치에. 위치 불일치 감지 시 구조 정합성 QC → FAIL
- 팀 UP 고유 섹션(팀 전용 규칙)은 불변. 개인 diff가 팀 고유 섹션을 건드리면 STOP + 보고
```

---

## STEP 6 — 팀 UP 버전 범프

```
독립 버전: 개인 UP 버전과 무관
Minor(내용 동기화): v{M}.x → v{M}.x+1
Major(구조 재편): v{M}.x → v{M+1}.0 (드물게, 공통 축 신설·삭제 시)

파일명 rename + 코드블록 헤더 `# UP team vX.X` 갱신 + CHANGELOG 행 추가
CHANGELOG 행 포맷: "v{버전} | §{섹션} {변경요약 1줄} | from 개인 v{N}"
```

---

## STEP 7 — QC (2항목)

| # | 항목 |
|---|------|
| ① | `grep` old 텍스트 잔존 0건 |
| ② | PERSONAL_FILTER 3축 항목 0건 (최종 확인) |

✗ 이 2항목만. 추가·변형 금지. FAIL 시 STEP 3 복귀.

---

## STEP 8 — 보고 포맷

```
[TEAM_SYNC]
개인 v{old}→v{new}  →  팀 v{old}→v{new}
공통 변경분: [항목 수]건 동기화
제외(개인 커스텀): [목록 또는 "없음"]
  - ①HONORIFIC: [블록명 또는 "없음"]
  - ②PROPER_NOUN: [블록명 또는 "없음"]
  - ③PERSONAL_MARKER: [블록명 또는 "없음"]
QC: ①✓ ②✓
IG 역방향: [통과 또는 경고 내용]

SAVE: 인라인만. 파일 저장 ✗.
```

---

## EDGE CASES

| 케이스 | 대응 |
|--------|------|
| 팀 UP 파일 부재 (`UP_team_v*.md` 0건) | 경고 1줄 후 전면 스킵. "팀공유 UP 없음 — 동기화 스킵" |
| 팀 UP 2건+ 발견 | 버전 최고값 1개 선택 + 보고 "복수 팀 버전 감지" |
| 이번 수정이 전부 개인 커스텀(공통분 0건) | "동기화 대상 없음. 팀 UP 무변경" 1줄 보고 후 종료 |
| 개인 UP과 팀 UP 구조 불일치 (섹션명 상이) | STOP + 보고 "구조 정합성 실패. 수동 확인 요청" |
| 팀 UP이 읽기전용(권한) | STOP + 보고 "팀 UP 쓰기권한 없음" |
| BYPASS "팀싱크 스킵" 명시 | STEP 1부터 스킵, 개인 UP 보고만 |
| L0_PATH(QC 교정만) | TEAM_SYNC 전면 스킵 (의미 변경 없음) |

---

## SESSION_CACHE 확장

| 신규 필드 | 내용 |
|----------|------|
| `up_team_path` | 팀 UP 파일 절대경로 |
| `up_team_version` | 현재 팀 UP 버전 |
| `last_team_sync_timestamp` | 직전 TEAM_SYNC 실행 시각 |

INIT STEP 2에서 개인 UP과 동시 탐색·저장. 캐시 LIFECYCLE은 개인 UP과 동일.

---

## Gotchas

| 함정 | 대응 |
|------|------|
| PERSONAL_FILTER 누락 | 호칭·고유명사 팀 유입 = FAIL. 3축 전수 검사 필수 |
| 개인 UP diff 대신 전체 덮어쓰기 | 팀 고유 섹션 소실. diff 기반만 허용 |
| 팀 UP 버전을 개인 UP과 동일하게 범프 | 독립 버전 원칙 위반. 개인 v39.2 ↔ 팀 v12.5 같은 형태 정상 |
| PERSONAL 마커 누락한 개인 블록 | 마커 없으면 ①·② 축으로 차단. 새 개인 블록 추가 시 마커 동시 추가 권장 |
| 역방향 IG 스킵 | 기존 팀 UP 오염 미감지. STEP 4 필수 |
| CHANGELOG까지 개인 정보 유입 | 개인 UP CHANGELOG에 호칭·고유명사 있으면 팀으로 복사 ✗. 요약만 재작성 |
| L0에서 TEAM_SYNC 실행 | 불필요한 도구 호출. L0_PATH는 전면 스킵 |
