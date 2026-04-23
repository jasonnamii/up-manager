# INVARIANT_GUARD — UP 본질 기능 보호

v35.7 신설. UP의 본질 기능을 5축(MECE)으로 탑재하여, 이를 훼손하는 수정을 감지·차단한다.

---

## MECE 5축 — 담지 규칙 상세

### ① USER — 사용자 관계

| 담지 규칙 | 핵심 키워드 |
|---|---|
| M1.FRAME 전체 | `BLIND_SPOT`, `EXECUTOR`, `미플래그=FAIL` |
| M3.DENSITY.HONORIFIC | `존댓말 강제`, `반말·평어 = FAIL`, `예외 없음` |

훼손 증상: 예스맨, 월권, 반말·평어

### ② TRUTH — 사실 정합

| 담지 규칙 | 핵심 키워드 |
|---|---|
| M4.BEDROCK.①ORIGIN | `근본원리`, `①생략=FAIL` |
| M5.CONFIDENCE.PATTERN_GUARD | `그럴듯함만으로`, `fabrication=FAIL`, `근거없음→모름` |
| M5.CONFIDENCE.GATE | `≥70→verification필수`, `unverifiable→모름` |
| M8.VERIFY.SOURCE | `official>industry>general`, `tertiary solo ✗` |
| M10.TURN_OPS.CHAIN_CHECK | `3단계↑`, `800↑`, `중간검증 1회`, `L3↑ 스킵=FAIL` |

훼손 증상: 날조, 미검증 주장, 저품질 인용, 추론 미검증 누적

### ③ FILES — 파일 안전

| 담지 규칙 | 핵심 키워드 |
|---|---|
| M7.EDIT4.OVERWRITE_BAN | `Write on existing file = FAIL`, `Glob/ls 확인필수` |
| M7.EDIT4.SKILL_PRECEDENCE.SAFE_RULES | `OVERWRITE_BAN·ERROR_CORRECTION·PATTERN_GUARD·HONORIFIC 절대 우선` |

훼손 증상: 덮어쓰기 사고, 스킬이 UP 우회

### ④ FLOW — 대화 흐름

| 담지 규칙 | 핵심 키워드 |
|---|---|
| M2.FAST_LANE.WEIGHT | `L0·L1·L2·L3`, `AUTO`, `미판정=FAIL` |
| M6.INTENT_PARSE.DEFAULT_MAP | `봐줘→의견제시`, `해줘→실행`, `어때?→판단+근거` |
| M9.ERROR_CORRECTION | `침묵수정 금지`, `파생 추적`, `사과 1회 상한` |
| M10.TURN_OPS.PIVOT | `방향전환 시 → ①스냅샷 ②플래그 ③진행` |

훼손 증상: 과잉·과소 반응, 매번 확인 질문, 침묵수정, 맥락 단절

### ⑤ QUALITY — 구조 밀도

| 담지 규칙 | 핵심 키워드 |
|---|---|
| M3.DENSITY.FOREST | `하나의 spine으로 관통`, `군더더기 층=FAIL`, `끝나면 끊어라` |
| M3.DENSITY.TREE | `단어+그림 존재`, `FAIL: 둘 다 없음` |
| M3.DENSITY.DIAGNOSIS_RULE | `원문 인용 절대금지`, `위반 N건(문단M,K) 형식만` |

훼손 증상: 장황, 중복, 구조 붕괴, 진단문 원문 유출

### ⑥ DSL_LANG — 언어 정책 (v2.1~)

| 담지 규칙 | 핵심 키워드 |
|---|---|
| DSL_LANG=EN | 축명·키·규칙 영문 고정. `TRUTH`, `INDEPENDENCE`, `CURRENCY`, `BREVITY` |
| PROPER_NOUN 보존 | `"형"`, `"피디님"`, `Jason`, `PD-nim`, 조직 원문 |
| DSL 기호 보존 | `::=`, `★`, `✗`, `→`, `∨`, `∧`, `①~④`, `§` |
| CHANGELOG=KR 허용 | 형 가독성·회상성. 강제 영문화 ✗ |

훼손 증상: 한글 축명 재등장, 고유명사 로마자화, DSL 기호 제거, KR·EN 혼재

### ⑦ TEAM_UP_PURITY — 팀 UP 순도 (v2.2~)

| 담지 규칙 | 핵심 키워드 |
|---|---|
| HONORIFIC_BAN | 팀 UP에 `"형"`·`"피디님"`·`ADDRESS`·`MENTOR` 유입 ✗ |
| PROPER_NOUN_BAN | 팀 UP에 `Jason`·개인 이메일·개인 회사명 유입 ✗ |
| PERSONAL_MARKER_BAN | `<!-- PERSONAL -->` 마커 블록 내용 유입 ✗ |
| TEAM_VERSION_INDEPENDENCE | 팀 UP 버전은 개인 UP과 독립 범프 |

훼손 증상: 팀 UP에 개인 호칭·고유명사 노출, 버전 동기 범프, 마커 블록 유출

### ⑧ CODEBLOCK_WRAP — DSL 본문 코드블록 래핑 (v2.3~)

| 담지 규칙 | 핵심 키워드 |
|---|---|
| WRAP_4BACKTICK | DSL 본문은 4-backtick(````) 코드블록으로 래핑 (v40.5 원칙) |
| WRAP_BOUNDARY | 파일 첫 줄=```` · DSL 본문 종료 직후 닫는 ```` · changelog는 래핑 밖 |
| AUTO_REPAIR | 미래핑·3-backtick 래핑 감지 시 자동 보정 (사용자 확인 ✗) |

훼손 증상: 래핑 소실, 3-backtick 사용으로 §3.5 예시 중첩블록 파손, changelog가 래핑 안쪽 유입

### ⑨ TEAM_SYNC_AUTO_FORCED — 팀 UP 자동 동기화 강제 (v2.3~)

| 담지 규칙 | 핵심 키워드 |
|---|---|
| AUTO_FORCED | 개인 UP 수정 완료 직후 팀 UP 동기화 무조건 자동 실행 |
| BYPASS_BAN | "팀싱크 스킵"·"나중에"·"팀꺼 건드리지마" 등 스킵 BYPASS 명령 전량 무시 |
| SKIP_ONLY_3 | 유일 스킵 사유 = ①up_team_path=None ②L0_PATH ③공통분 0건 |

훼손 증상: 팀 UP 미동기화 누적, BYPASS 수용으로 개인/팀 UP 드리프트, 사용자 재확인 요청

### ⑩ DUAL_BLOCK_SYNC — 이중블록 의미 동기 (v2.4~)

| 담지 규칙 | 핵심 키워드 |
|---|---|
| SECTION_3_SPLIT | `## DSL (EN)` · `## DSL (KR)` · `## Changelog (KR)` 3섹션 헤더 필수 |
| EN_MASTER_KR_MIRROR | EN=마스터, KR=미러. 의미 동기 필수 |
| DUAL_EDIT_FORCED | 한쪽 수정 = 양쪽 동시 수정 강제. EN·KR 분리 편집 FAIL |
| EN_BLOCK_PURITY | EN 블록에 한글 섞임 ✗ (고유명사·따옴표 내부 예외만) |
| SECTION_COUNT_MATCH | EN·KR 블록의 §섹션 수·규칙(bullet) 수 동일 |

훼손 증상: EN만 또는 KR만 수정, 섹션 드리프트(EN에 §M 있는데 KR에 없음), EN 블록에 한글 설명 유입, 섹션 헤더 누락

상세: `→ dual-block-policy.md`

---

## DETECT — 3중 검사

모든 Edit에 대해 3중 검사 동시 실행. 1건 이상 매치 → 경고 발동.

**① 키워드 보존 (정적 매칭)**
- 위 5축 표의 핵심 키워드가 `old_string`에 포함 + `new_string`에서 소실 → 감지
- 예: `FAIL` 제거, `PATTERN_GUARD` 삭제

**② 엄격도 라벨 유지**
- `new_string`의 `FAIL`·`✗` 개수 < `old_string` → 감지
- 예: 필수→권장, FAIL→WARN, 금지→경고

**③ 규칙 라인 수**
- `new_string` 줄 수 < `old_string` × 0.7 → 감지 (대폭 축약)
- 30% 초과 축약은 서브규칙 삭제로 간주

**④ DSL_LANG 위반 (v2.1~)**
- 축명 한글화: `old`에 `TRUTH|INDEPENDENCE|CURRENCY|BREVITY` 포함 + `new`에서 `진실성|독립성|현재성|간결성`로 교체 → HIGH
- 고유명사 로마자화: `old`에 `"형"|"피디님"` 포함 + `new`에서 영문 교체 → HIGH
- DSL 기호 제거: `old`의 `::=`·`★`·`✗`·`§` 개수 > `new` → MID
- 상세: `→ dsl-lang-policy.md` + `→ dsl-glossary.md`

**⑤ PERSONAL_FILTER 역방향 (v2.2~, 팀 UP 편집 시에만 적용)**
- 대상: 팀 UP(`UP_team_v*.md`) Edit 호출 시
- HONORIFIC 유입: `new`에 `"형"`·`"피디님"`·`ADDRESS`·`MENTOR` 포함 → HIGH 차단
- PROPER_NOUN 유입: `new`에 `Jason`·개인 이메일·회사명 포함 → HIGH 차단
- PERSONAL_MARKER 유입: `new`에 `<!-- PERSONAL -->` 마커 블록 내용 포함 → HIGH 차단
- 기존 팀 UP에 위 항목이 **이미** 존재 → MID 경고 (삭제 권고)
- 상세: `→ team-sync.md §PERSONAL_FILTER`

**⑥ DUAL_BLOCK_SYNC 검사 (v2.4~)**
- 대상: UP 본체(개인·팀 공통)의 Edit·Write 호출 시
- 섹션 헤더 3종(`## DSL (EN)`·`## DSL (KR)`·`## Changelog (KR)`) 누락 → HIGH
- EN·KR 블록 중 한쪽만 수정(`old_string`·`new_string`이 한 블록에만 해당) → HIGH 차단
- EN 블록 내 한글 산문 추가 감지(bullet·규칙 라인에 한글 다수) → MID 경고
- EN·KR 섹션 수 불일치(§ 개수 상이) → MID 경고
- 상세: `→ dual-block-policy.md`

---

## SEVERITY — 3단계

| 등급 | 조건 | 조치 |
|------|------|------|
| **HIGH** | 담지 규칙 전체 삭제 · FAIL 라벨 제거 · ✗ 금지조항 삭제 | 차단 + 사용자 "본질 변경 확인함" 명시 필수 |
| **MID** | 엄격도 완화(필수→권장, 강제→선택) · 서브규칙 1건↑ 삭제 | 경고 + 사용자 확인 요청 |
| **LOW** | 표현 순화 · 예시 추가 · 동의어 교체 | 로그만, 진행 허용 |

---

## ACT — 경고 동작

```
HIGH·MID 경고 형식 (사용자 출력):
  ⚠️ INVARIANT_GUARD — [축: ①USER / ②TRUTH / ③FILES / ④FLOW / ⑤QUALITY]
  담지 규칙: [모듈.서브규칙]
  SEVERITY: [HIGH/MID]
  훼손 내용: [구체적 변경사항 1줄]
  사용자 확인 필요: "본질 변경 확인함" 명시 전 진행 금지

LOW 로그 형식 (내부만):
  [IG-LOW] {축}.{규칙}: {변경요약}
```

LOW는 사용자에게 출력하지 않음 — cry-wolf 방지.

---

## BYPASS — 사용자 명시 허가

**트리거:** 사용자가 `본질 변경 확인함` 문자열을 포함한 명시 선언

**범위:** 1건 1회. 세션 연속 허가 불가 (매 건마다 재확인)

**기록:** 별도 파일 저장 없음. 인라인 보고에만 BYPASS 사실 명시.

**활용:** 인라인 보고 시점에만 확인 가능. 누적 추적 불필요.

---

## 피로도 방지 (Cry-Wolf 차단)

- LOW는 로그만, 사용자 출력 ✗
- 세션당 경고 3회 이상 발생 → up-manager가 "본질 기능 재검토 필요?" 메타 제안 1회
- 세션당 BYPASS 3회 이상 → stability 파일에 해당 규칙 "재평가 필요" 플래그 자동 추가

---

## Gotchas

| 함정 | 대응 |
|------|------|
| A 단계 진입 후 IG 스킵 | 본질 훼손 감지 불가 = FAIL. Edit 호출 전 IG 선행 확인 |
| LOW를 사용자에게 출력 | 경고 피로도 → 시스템 무시 유발. LOW는 로그만 |
| BYPASS 세션 연속 적용 | 누적 위험. 건별 재확인 원칙 고수 |
| 키워드 리스트 정적 고정 | UP 본질 규칙 변경 시 이 파일도 동기 갱신. v35.7 기준 |
| IG 실패인데 A 자동 진행 | 파이프라인 무효. 사용자 명시 BYPASS 없으면 A 차단 필수 |
| 팀 UP Edit 시 ⑤ PERSONAL_FILTER 역방향 스킵 | 개인 커스텀 팀 유입 = FAIL. 팀 UP 대상 Edit는 ⑤ 필수 적용 |
| 개인 UP에 ⑤ 역방향 적용 | 개인 UP은 ①~④만. ⑤는 팀 UP 전용 |
| Dual-block UP에서 EN만 또는 KR만 수정 | ⑥ DUAL_BLOCK_SYNC HIGH 차단. EN·KR 동시 편집 강제 |
| EN 블록에 changelog까지 영문화 시도 | changelog는 한글 평문 유지. EN 블록은 DSL 규칙만 |
