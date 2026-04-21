# up-manager CHANGELOG

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
