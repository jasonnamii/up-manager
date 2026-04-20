# DSL Glossary — KR ↔ EN 용어집

v2.1 신설. UP DSL v39.1~ 영문화 대응. KR↔EN 양방향 매핑.

---

## 축명 (Axes)

| KR | EN | 의미 |
|----|-----|------|
| 진실성 | TRUTH | 근거 기반 발언 |
| 독립성 | INDEPENDENCE | 검증된 근거 기반 입장 유지 |
| 현재성 | CURRENCY | 최신성 점검 |
| 간결성 | BREVITY | 즉시 실행·최소 질문 |
| 사용자 컨텍스트 | USER_CONTEXT | 최우선 정체성·관계 규범 |
| 충돌 규칙 | CONFLICT_RULES | 축간 우선순위 결정 |

---

## 상태·판정 키워드

| KR | EN | 의미 |
|----|-----|------|
| 실패 | FAIL | 규칙 위반 |
| 최상위 실패 | TOP-LEVEL FAIL | 절대 회피 대상 |
| 정정 | CORRECTION | 오류 발견 시 즉시 수정 선언 |
| 모름 | UNKNOWN | 근거 없음 선언 |
| 추정 | ASSUMPTION | 정보 부족 시 제한 실행 |
| 강제 | MANDATORY | 예외 없음 |
| 우회 | BYPASS | 사용자 명시 허가 |
| 스킵 | SKIP | 해당 단계 생략 |
| 경고 | WARN | MID 등급 |
| 통과 | PASS | 검증 성공 |

---

## DSL 변수·구조

| KR | EN | 의미 |
|----|-----|------|
| 사용자 | USER | 형(Jason) |
| 멘토 | MENTOR | 피디님 |
| 호칭 | ADDRESS | 고정 호명 규칙 |
| 고위험 수치 | HIGH_RISK_NUMERIC | 돈·환율·지분·계약 등 |
| 환율·단위 긴급 | FX_UNIT_CRIT | 최상위 FAIL 수치 축 |
| 응답 전 판정 | pre-response judgment | 3분기 분기 |
| 왕복 역산 | round-trip (A→B→A) | FX 검증 기법 |
| 2차 경로 대조 | 2nd_path_crosscheck | Python+독립계산 |

---

## 조건·연산자

| KR | EN | 의미 |
|----|-----|------|
| 또는 | ∨ (OR) | 논리합 |
| 그리고 | ∧ (AND) | 논리곱 |
| 최대 1 | MAX 1 | 상한 |
| ≥ / ≤ | ≥ / ≤ | 비교 |
| 정의 | `::=` | DSL 할당 |
| 도출 | `→` | 결과 도출 |
| 금지 | `✗` | 위반 표지 |
| 강조 | `★` | 최우선 표지 |

---

## 섹션 매핑 (v38.1 KR ↔ v39.1 EN)

| v38.1 (KR) | v39.1 (EN) |
|------------|-----------|
| 0. 사용자 컨텍스트 | §0 USER_CONTEXT |
| 1. 진실성 | §1 TRUTH |
| 2. 독립성 | §2 INDEPENDENCE |
| 3. 현재성 | §3 CURRENCY |
| 4. 간결성 | §4 BREVITY |
| 5. 충돌 규칙 | §5 CONFLICT_RULES |

---

## 원문 보존 (NOT translated)

| 원문 | 비고 |
|------|------|
| 형 | ADDRESS 값. Jason 지칭. 절대 번역 금지 |
| 피디님 | ADDRESS 값. MENTOR 3인칭 지칭 |
| 라텔앤드파트너즈 | 조직명. 필요 시 Ratel&Partners 영문 병기 |
| Cre8orClub · KISAS Plus · KISAS Platform | 조직명 원문 그대로 |
| 노느니특공대 / Nonuni-Teukgongdae | KR 원문 우선, EN은 참조용 |
| KISAS홀딩스(가칭) / KISAS Holdings (tentative) | 괄호 주석 포함 번역 |
| 케이노트 / K-Note | 양방 병용 |

---

## 호칭 규칙 (번역 금지 핵심)

```
ADDRESS ::=
  Jason → "형"        # 2인칭 대화. EN으로도 "형" 유지
  PD-nim → "피디님"   # 3인칭 전용. EN으로도 "피디님" 유지
  세션 첫 응답 ∨ 식별 모호 → FORCE "형"
```

USER를 "피디님"으로 호명 = **TOP-LEVEL FAIL** (정체성 규범 위반, 한·영 공통).

---

## 사용 예

**KR v38.1:**
```
• USER ::= Jason(최남희, 형) | 라텔앤드파트너즈·Cre8orClub... | ★대화 상대★
• FX_UNIT_CRIT ::= {환율·통화변환·단위변환·자릿수·0갯수} = 최상위 FAIL
• 오류감지 → [정정] + 파생전수추적
```

**EN v39.1 (변환):**
```
• USER ::= Jason (Choi Nam-hee, "형") | CEO of Ratel&Partners · Cre8orClub... | ★conversation partner★
• FX_UNIT_CRIT ::= {FX · currency_conversion · unit_conversion · digit_count · zero_count} = TOP-LEVEL FAIL
• error_detected → [CORRECTION] + trace_all_derivatives
```

**보존 요소:** `::=` · `★` · `FX_UNIT_CRIT` · `"형"` · `Jason`
**변환 요소:** 축명 · 키워드 · 조건식
