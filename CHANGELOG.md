# up-manager Changelog

## v3.0 (2026-04-28) — DSL_LANG = KR Single-block 전환 (MAJOR)

**변경:**
- INVARIANT #1·#2: 축명·키워드 한국어 마스터 (TRUTH→진실성, RULE→규칙 등)
- INVARIANT #8: Dual-block(EN+KR) → Single-block(KR-only)
- 헤더 `## DSL (EN)` 폐지, `## DSL (KR)` 단일화
- references/dual-block-policy.md → single-block-policy.md 교체
- references/dsl-lang-policy.md, dsl-glossary.md, invariant-guard.md 갱신

**원인:** 형 명령(2026-04-28). EN-only 시스템 주입 vs LLM 한국어 컨텍스트 매칭 불일치 → 발동률 저하 의심. KR 마스터 전환으로 일관성·발동률 동시 확보.

**마이그레이션:** 기존 UP_user-preferences_v*.md의 EN 블록 + 직후 `---` 구분선 삭제 → KR 블록만 잔존 → changelog 1줄 추가.

**보존:** 파이프라인·INIT·팀싱크·세션캐시 100% 무변경.

---

# up-manager CHANGELOG

## v2.5 — 2026-04-23

**계기:** 형 요청 — 체크리스트·스태빌리티 파일 운용 중단. 파이프라인 분기·루프 제거(뺑뺑이 방지).

### 제거
- `references/checklist-sync.md` → `_archive/v2.4/` (UP_checklist.md 동기화 전량 폐기)
- `references/fast-path.md` → `_archive/v2.4/` (L1·L2 분기 폐기)
- `references/full-path.md` → `_archive/v2.4/` (L3·L4 분기 폐기)
- SCOPE_IMPACT(HIGH/MID/LOW) 판정 로직 제거
- L0/L1/L2/L3/L4 edit4_level 분기 제거
- UP_stability.md 읽기·갱신 로직 제거 (fast/full-path)
- UP_checklist.md 읽기·갱신 로직 제거 (fast/full-path)
- 풀QC 5항목(①DSL순도·②규칙보존·③참조무결·④DSL문법·⑤WRAP) → **2항목+WRAP 게이트**로 압축
- SESSION_CACHE `stability_path`·`checklist_path`·`last_stability_snapshot` 필드 제거
- INVARIANT_GUARD "세션당 BYPASS 3회 이상 → stability 파일 플래그" → 인라인 제안 1줄로 대체

### 신규
- `references/pipeline.md` — 단방향 선형 파이프라인 (①INIT → ②IG → ③EDIT → ④QC → ⑤TEAM_SYNC → ⑥REPORT)

### 업데이트
- `SKILL.md` — description에서 "체크리스트 동기" 제거. 핵심 규칙 9개 → 8개 (4/5번 통합). 판정 흐름을 단방향 선형 파이프라인으로 전면 교체. 스포크 목록에서 checklist-sync·fast-path·full-path 제거 + pipeline.md 추가. INVARIANT 마커(#1~#8) 본문 표기. version 2.4→2.5
- `references/init-protocol.md` — STEP 2에서 UP_stability.md·UP_checklist.md 경로 확정 로직 삭제. EDGE CASES에서 stability·checklist 부재 분기 삭제
- `references/session-cache.md` — CACHE_FIELDS에서 stability·checklist 관련 3필드 삭제
- `references/invariant-guard.md` — BYPASS 3회 누적 처리를 인라인 보고 제안으로 변경
- `scripts/validate.py` — REQUIRED_SPOKES에서 checklist-sync.md 제거 + pipeline.md 추가

### 설계 원칙 변경
- **단방향 선형:** 분기 없음. QC 실패 시 같은 턴 내 자동 보정 1회만 허용. 2회차 실패 = STOP
- **파일 1개만 읽기:** UP_user-preferences_v*.md + (선택) UP_team_v*.md. 부가 파일 의존 전면 제거
- **뺑뺑이 방지:** L레벨 분기·SCOPE_IMPACT·fast/full 선택·루프 복귀 경로 전부 제거

### 하위호환
- UP 본체 파일 구조 무변경 (Dual-block DSL 유지)
- TEAM_SYNC 8단계 로직 무변경 (skip 조건만 명확화)
- INVARIANT_GUARD 8축 유지 (#1~#8, 기존 ①~⑩ 흡수)
- 기존 v2.4 참조자료는 `_archive/v2.4/`에서 참조 가능

---


## v2.2 — 2026-04-21

**계기:** 팀공유 UP(`UP_team_v*.md`) 자동 동기화 요구. 개인 UP 수정 시 공통 규칙만 팀에 전파, 개인 커스텀(호칭·고유명사·PERSONAL 마커)은 제외.

### 신규 파일
- `references/team-sync.md` — TEAM_SYNC 파이프라인 8단계 + PERSONAL_FILTER 3축(HONORIFIC·PROPER_NOUN·PERSONAL_MARKER) + 역방향 INVARIANT_GUARD

### 업데이트
- `SKILL.md` — description에 팀공유 UP 관련 키워드 확장(팀공유UP, UP_team, team sync, 팀싱크, PERSONAL_FILTER). 판정 흐름에 TEAM_SYNC 단계 추가. Gotchas 3건 추가. version 2.1→2.2
- `references/init-protocol.md` — STEP 2에 `up_team_path` 확정 로직 추가. EDGE CASES에 팀 UP 부재·복수건 처리 추가
- `references/invariant-guard.md` — MECE 6축 → 7축 확장(⑦ TEAM_UP_PURITY 신설). DETECT 4중 → 5중(⑤ PERSONAL_FILTER 역방향). Gotchas 2건 추가
- `references/session-cache.md` — CACHE_FIELDS에 `up_team_path`·`up_team_version`·`last_team_sync_timestamp` 추가
- `references/fast-path.md` — 턴3 병렬 호출에 TEAM_SYNC 추가(3호출 → 4호출). 보고 포맷에 팀싱크 필드
- `references/full-path.md` — F+D+K 병렬 → F+D+K+T 병렬. T. TEAM_SYNC 섹션 신설. G단계 보고 포맷에 팀싱크 필드

### 설계 원칙
- **버전 독립:** 팀 UP 버전은 개인과 무관 범프 (개인 v39.2 ↔ 팀 v12.5 정상)
- **자동 실행(A모드):** 개인 UP 파이프라인 완료 후 자동 TEAM_SYNC. BYPASS "팀싱크 스킵" 1회 허가
- **PERSONAL_FILTER 3축:** ①HONORIFIC(호칭) ②PROPER_NOUN(개인 고유명사) ③PERSONAL_MARKER(`<!-- PERSONAL -->` 블록)
- **역방향 IG:** 팀 UP Edit 시 ⑤ PERSONAL_FILTER 검사로 개인 커스텀 역유입 차단

### 하위호환
- 팀 UP 부재 시 전면 스킵 (기존 사용자 영향 ✗)
- 개인 UP 단독 수정 시 동작 기존과 동일
- CHECKLIST_SYNC·FAST_PATH·FULL_PATH 기본 로직 무변경 (단계만 1개 추가)

---

## v2.1 — 2026-04-21

**계기:** UP v39.1 DSL 영문화 대응. DSL_LANG 정책 명시화 + KR↔EN 글로서리 추가 + INVARIANT_GUARD 확장.

### 신규 파일
- `references/dsl-lang-policy.md` — DSL 언어 정책 (DSL_LANG=EN, PROPER_NOUN 보존, CHANGELOG=KR 허용)
- `references/dsl-glossary.md` — KR↔EN 양방향 용어집 (축명·키워드·변수·섹션 매핑)

### 업데이트
- `SKILL.md` — DSL_LANG=EN 마스터 선언, 핵심 규칙 6개 표, description P1·P3 키워드 확장 (DSL_LANG, 영문DSL, DSL language policy 등), 스포크 목록 갱신
- `references/invariant-guard.md` — MECE 5축 → 6축 확장 (⑥ DSL_LANG 신설), DETECT 3중 검사 → 4중 (축명 한글화·고유명사 로마자화·DSL 기호 제거 감지)

### 하위호환
- 기존 파이프라인(FAST_PATH/FULL_PATH/CHECKLIST_SYNC) 무변경
- INVARIANT_GUARD 로직 동일, 검사 항목만 확장
- KR UP도 진단 가능 (글로서리로 역매핑)

---

## v2.0 — 2026-04-17

**계기:** skill-doctor 진단 🟠 66.4 → 🟢 목표 85+ 처방 이행.

### 구조 변경
- SKILL.md 16.6KB → 5KB 허브 + 5 스포크로 분리 (허브스포크 재설계)
- 원본 SKILL.md → `_archive/SKILL-16597B-2026-04-17.md` 보존

### 신규 파일
- `references/session-cache.md` — SESSION_CACHE 상세
- `references/init-protocol.md` — INIT STEP 0~2 + EDGE CASES
- `references/fast-path.md` — FAST_PATH L1·L2 파이프라인
- `references/full-path.md` — FULL_PATH L3·L4 파이프라인
- `references/checklist-sync.md` — CHECKLIST_SYNC 상세
- `evals/cases.json` — 회귀 방지 케이스 3종 (FAST/FULL/L0)
- `evals/README.md` — 케이스 구조 설명
- `scripts/validate.py` — 자가 점검 4종
- `CHANGELOG.md` — 본 파일

### 허브 강화
- ⛔ 절대 규칙 → INVARIANT #1~#7 마커 명시 (본질 유실 방지)
- INVARIANT #7: UP.M7.SKILL_PRECEDENCE 준수 선언 추가
- vault_dependency HARD에 outputs/ fallback 명시
- 스텔스 조항 추가 (UP 라벨·M1~M12 본문 노출 금지)
- 예시 섹션 신설 (L1·L3 2개)
- Gotchas 스캐너 감지 형식 통일
- 피드백 안내 추가

### 하위호환
- TRIGGER 조건 5종 동일
- 경로 분기 (FAST/FULL/L0) 동일
- DSL 문법 수정 규칙 동일
- INVARIANT_GUARD 로직 동일 (invariant-guard.md 무변경)

---

## v1.0 — ~2026-04-17

- 초기 버전 (단일 SKILL.md 16.6KB)
- INVARIANT_GUARD, CHECKLIST_SYNC, SESSION_CACHE, INIT, FAST_PATH, FULL_PATH 전 로직 구현
- references/invariant-guard.md 1개 스포크
