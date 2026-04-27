# DSL Language Policy (v3.0~)

## 정책

**DSL_LANG ::= KR** (한국어 마스터, 영문 블록 폐지)

## 변경 이력

- v1.x ~ v2.x: EN master + KR mirror (Dual-block)
- v3.0~: KR master only (Single-block)

## 한국어 강제 대상

| 항목 | 예시 |
|---|---|
| 축명 | 진실성·독립성·통화성·간결성 |
| 키워드 | 정정·미상·가정·FAIL·통화단위 위반·규칙충돌 |
| 룰 키 | TRIGGER → 트리거·발동조건 / RULE → 규칙 / CHECK → 점검·검사 / SCOPE → 범위 / GUARD → 가드·차단 |
| 섹션명 | INFRA → 인프라 / PROTOCOL → 프로토콜 / VOICE → 표현 / DECISION → 의사결정 |

## 영문 허용 예외

- 정규식 본문 (`[0-9]+\s*(...)`)
- 업계 표준 (BEP·KPI·MECE·MVP·API 등)
- 고유명사 (Jason·Choi Nam-hee·회사명)
- MCP 도구명·파일 경로 (mcp__cowork__request_cowork_directory)
- 스킬명 (trigger-skill·up-manager 등)
- 기호 (::=·★·✗·→·∨·∧·①~④·•)

## 자가합리화 차단

- "관용 표현이라 영문 OK" → FAIL
- "이번엔 예외" → FAIL
- "키 이름은 영문이 명료" → FAIL (글로서리 한국어 치환 강제)

## 검증

`grep -E "TRIGGER|RULE|CHECK|GUARD|SCOPE_OUT" UP_*.md | grep -v 정규식` hit ≥1 = INVARIANT #2 위반 (예외 제외).
