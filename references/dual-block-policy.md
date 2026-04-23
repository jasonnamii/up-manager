# Dual-block DSL Policy (v2.4~)

UP 본문을 **영문 DSL(master)** + **한글 DSL(mirror)** + **한글 Changelog** 3섹션으로 분리. 영문 블록 단독 복사 가능, LLM 파싱 최적, 형 가독성 보존.

---

## 1. 구조 규격

```
## DSL (EN)
````
# UP v{version} — Lite+
# Priority: USER > TRUTH > INDEPENDENCE > OUTPUT

## §0. USER
- ...영문 규칙...

## §M. MOUNT_GATE
- ...

...
````

---

## DSL (KR)
````
# UP v{version} — Lite+
# Priority: USER > TRUTH > INDEPENDENCE > OUTPUT

## §0. USER
- ...한글 규칙...

...
````

---

## Changelog (KR)

v{version} | ...변경 이력 평문...
v{prev} | ...
```

**요건:**
- 3섹션 헤더(`## DSL (EN)` / `## DSL (KR)` / `## Changelog (KR)`) 명시
- 각 DSL 블록은 4-backtick(````) 래핑 독립
- 섹션 사이 `---` 구분선 필수
- 고유명사(형·피디님·Jason 등)는 EN 블록에서도 원문 보존

---

## 2. 편집 프로토콜

**한쪽만 수정 = FAIL.** EN·KR 두 블록을 동시에 편집. 의미 동기 드리프트 차단이 본 정책의 목적.

```
수정 요청 입력
  → ① 변경 의미 추출 (KR 기준 자연어)
  → ② EN 블록 수정 (축명·키·규칙 영문)
  → ③ KR 블록 수정 (동일 의미, 한글 번역)
  → ④ DUAL_BLOCK_SYNC 검증: 섹션 수·규칙 수·의미 동기 확인
  → ⑤ 한쪽만 수정된 경우 STOP + 미동기 항목 보고
```

---

## 3. 영문 변환 원칙 (EN 블록)

| 축 | KR | EN |
|----|----|----|
| 축명 | USER·TRUTH·INDEPENDENCE·OUTPUT | 원형 유지 (이미 EN) |
| 신설 축명 | 진실성·독립성·간결성 | TRUTH·INDEPENDENCE·BREVITY |
| 키워드 | 오류·불확실·검산·필수 | CORRECTION·UNKNOWN·VERIFICATION·REQUIRED |
| 섹션명 | `§M. MOUNT_GATE` | 원형 유지 (이미 EN) |
| 규칙 본문 | "문서·파일 작업 시 마운트 선행" | "On document/file work, pre-mount required" |
| 예시 | "순열 → 순서대로 뽑는 경우" | "permutation → ordered selection case" |
| 고유명사 | 형·피디님·Jason | **원문 보존** (Hyung·PDnim으로 로마자화 ✗) |
| 기호 | `::=` `★` `✗` `→` `∨` `∧` | 원형 유지 |

---

## 4. DUAL_BLOCK_SYNC 가드 (INVARIANT_GUARD ⑩)

**검사 항목:**
1. 섹션 헤더 3종(`## DSL (EN)`·`## DSL (KR)`·`## Changelog (KR)`) 모두 존재
2. EN·KR 두 DSL 블록 모두 4-backtick 래핑
3. EN·KR 섹션 수 동일 (§0·§M·§1·§2·§3·§3.1·§3.5·§4 등)
4. 각 섹션의 규칙(bullet) 수 동일
5. 고유명사(형·피디님 등)는 EN 블록에서도 원문
6. EN 블록에 한글 섞임 없음 (단 고유명사·한국어 예시 따옴표 내부 예외)

**위반 감지 시:**
- 자동 보정 가능(섹션 헤더 누락·래핑 누락) → 조용히 복구
- 의미 드리프트(규칙 수 불일치·번역 누락) → STOP + 보고

---

## 5. 마이그레이션 (단일블록 → Dual-block)

기존 단일 KR 블록 UP → Dual-block 전환 1회 수행:

```
① 현 UP 파일 읽기 → KR DSL 추출
② EN 버전 초안 작성 (축명·키워드 영문화, 산문 번역)
③ 새 UP 파일 작성: DSL (EN) → DSL (KR) → Changelog 순
④ DUAL_BLOCK_SYNC 검증
⑤ 버전 Minor 범프 + changelog에 "Dual-block 전환" 명시
```

**주의:** 기존 changelog는 전부 한글 평문으로 보존. changelog는 EN 블록 대상 아님.

---

## 6. 팀 UP 이관 규칙

팀 UP(`UP_team_v*.md`)도 Dual-block 구조 동일 적용. PERSONAL_FILTER 3축 통과 후 EN·KR 양쪽 동시 이관.

- 개인 UP EN 블록 → 팀 UP EN 블록 (2인칭 치환: 형 → user)
- 개인 UP KR 블록 → 팀 UP KR 블록 (2인칭 치환: 형 → 사용자)

---

## Gotchas

| 함정 | 대응 |
|------|------|
| EN만 수정하고 KR 방치 | DUAL_BLOCK_SYNC FAIL. 양쪽 동시 편집 강제 |
| KR만 수정하고 EN 방치 | 동일. 마스터는 EN이지만 편집 시점 동기 필수 |
| EN 블록에 한글 설명 섞임 | EN 블록은 순수 영문. 한글 예시 필요시 KR 블록에만 |
| 섹션 헤더 생략 | `## DSL (EN)` 등 3섹션 헤더 명시 필수. 생략 시 블록 경계 모호 |
| 4-backtick 래핑 누락 | CODEBLOCK_WRAP 가드가 자동 보정. EN·KR 두 블록 모두 대상 |
| changelog까지 영문화 | 불필요. Changelog는 한글 평문 유지 (형 가독성·토큰 효율) |
| 고유명사 로마자화(형→Hyung) | 호칭 정체성 FAIL. EN 블록에서도 원문 |
| 기존 단일블록 UP을 Dual 전환 없이 계속 수정 | §5 마이그레이션 1회 수행 후 이후 편집 재개 |
