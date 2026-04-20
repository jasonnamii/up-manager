# DSL_LANG Policy — UP DSL 언어 정책

v2.1 신설 (UP v39.1~ 대응). UP DSL의 언어 정책을 명시화하여 KR↔EN 혼재·표류를 차단한다.

---

## 마스터 언어

```
DSL_LANG ::= EN
PROSE_LANG ::= KR (허용)
PROPER_NOUN ::= 원문 유지
CHANGELOG ::= KR (허용)
```

**이유:**
1. LLM 토큰 효율 — 영문 키워드가 한글 대비 토큰 1/2~1/3
2. 의미 모호성 감소 — "진실성" vs "사실성" 같은 한글 동의어 혼재 방지
3. 국제 표준 용어 — FAIL·TOP-LEVEL·CORRECTION 등은 영문이 원형
4. 호칭·고유명사만 원문 → 정체성·관계 규범 보존

---

## 영문 고정 대상 (INVARIANT)

### ① 축명 (4개)
- TRUTH (진실성)
- INDEPENDENCE (독립성)
- CURRENCY (현재성)
- BREVITY (간결성)

### ② 상태·액션 키워드
- FAIL · TOP-LEVEL FAIL
- CORRECTION (정정)
- UNKNOWN (모름)
- ASSUMPTION (추정)
- MANDATORY (강제)
- BYPASS · SKIP
- CONFLICT_RULES

### ③ DSL 변수·구조
- USER · MENTOR · ADDRESS
- FX_UNIT_CRIT · HIGH_RISK_NUMERIC
- `::=` `→` `∨` `∧` `★` `✗` `•` `①②③④`

### ④ 섹션 prefix
- §0 · §1 · §2 · §3 · §4 · §5 (영문 DSL 영역임을 시각 구분)

---

## 원문 보존 대상 (PROPER_NOUN)

### ① 호칭 값
- `"형"` (ADDRESS 값. Jason 지칭)
- `"피디님"` (ADDRESS 값. 3인칭 한정)

### ② 인명
- Jason · Choi Nam-hee
- PD-nim (영문 표기) / 김형석 (필요 시 한글 병기)
- Kim Hyung-seok

### ③ 조직명
- Ratel&Partners · Cre8orClub · KISAS Plus · KISAS Platform
- Nonuni-Teukgongdae · KISAS Holdings · K-Note

---

## 한글 허용 영역 (PROSE)

### ① Changelog
v번호별 변경 기록은 한글. 형이 직접 읽고 회상·판단.

### ② Description 하위 산문
트리거 설명·NOT 조건·가독성 중요 부분.

### ③ 사용자 지시 로그
형의 원 지시문 인용 시 한글 그대로.

---

## 전환 규칙 (KR→EN 마이그레이션)

| 단계 | 조치 |
|------|------|
| 1 | 기존 KR DSL의 축·키·값 전수 추출 |
| 2 | dsl-glossary.md 대조하여 EN 매핑 |
| 3 | 새 버전 파일 생성 (Major bump) |
| 4 | INVARIANT_GUARD 3중 검사 — 키워드·엄격도·규칙줄수 보존 확인 |
| 5 | 고유명사 원문 유지 검증 (grep로 "형" "피디님" 잔존 확인) |
| 6 | 이전 버전 _archive/ 이동 |

**절대:** KR과 EN DSL을 한 파일에 혼재 금지. 전환 진행 중인 파일은 `_draft` 접미사.

---

## INVARIANT_GUARD 연동

DSL_LANG 위반 3중 검사 (invariant-guard.md §DETECT 확장):

**① 축명 한글화 감지:**
`old_string`에 EN 축명(TRUTH·INDEPENDENCE·CURRENCY·BREVITY) 포함 + `new_string`에서 KR로 교체 → HIGH.

**② 고유명사 로마자화 감지:**
`old_string`에 "형"·"피디님" 포함 + `new_string`에서 삭제·영문 교체 → HIGH.

**③ DSL 기호 제거:**
`old_string`의 `::=`·`★`·`✗` 개수 < `new_string` → MID.

---

## Gotchas

| 함정 | 대응 |
|------|------|
| 한글 설명 편하니까 축명도 한글로 | EN 고정. 한글은 글로서리 참조용 |
| PD-nim을 Kim으로 표기 | PD-nim 우선(관계성 반영). Kim은 인명 컨텍스트만 |
| ADDRESS 값을 "hyung"으로 | FAIL. 호칭 값은 한글 원문 |
| 섹션 번호 영문화(Section 1) | §1 유지. DSL 일관성 |
| Changelog도 영문화 | 불필요. 형 가독성 우선 |
| KR→EN 전환 중 KR·EN 혼재 | FAIL. 전환 완료 후 범프 |
