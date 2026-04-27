# Single-block Policy (v3.0~)

## 구조

UP 파일 = 2섹션 단일 블록.

```
## DSL (KR)              ← 마스터 (시스템 설정 붙여넣기 대상)

````
# UP v??? — YYYY-MM-DD
SECTION: 인프라
[블록명]
RULE ::= ...
...
````

---

## Changelog (KR)         ← 변경 이력 (한글)

PREV_CHANGELOG: ...
v??? | TYPE(요약) — 형 명령(YYYY-MM-DD).
원인: ...
변경: ...
영향: ...
보존: ...
PERSONAL_FILTER: ...
```

## v2.x → v3.0 마이그레이션

| 항목 | v2.x (Dual) | v3.0 (Single) |
|---|---|---|
| 블록 수 | 2 (EN master + KR mirror) | 1 (KR master) |
| 시스템 설정 붙여넣기 | EN 블록 | KR 블록 |
| 헤더 | `## DSL (EN)` + `## DSL (KR)` | `## DSL (KR)` |
| 동기화 부담 | EN·KR 양쪽 동시 편집 | KR 단일 |
| 영문 키워드 | TRIGGER·RULE·CHECK·SCOPE_OUT 영문 키 | 한국어 치환 (트리거·규칙·점검·범위제외) |

## 단일 블록 강제 룰

1. EN 블록 헤더(`## DSL (EN)`) 등장 = INVARIANT #8 위반 → 즉시 삭제
2. EN 블록 직후 `---` 구분선도 함께 삭제
3. KR 블록 안 영문 키워드 잔존 시 → glossary 역방향 매핑 적용
4. 코드 블록 래핑은 4-backtick 유지

## 예외 (영문 허용)

- 정규식 패턴 (`[0-9]+\s*(...)`) — 정규식 자체는 영문/특수문자 본질
- 코드명·기술 용어 (BEP·KPI·MECE·MVP·API 등 업계 표준)
- 고유명사 (Jason·Choi Nam-hee 등)
- 파일 경로·MCP 도구명 (mcp__cowork__request_cowork_directory)

## 점검

- `grep -c "## DSL (EN)" UP_*.md` = 0 확인
- `grep -c "## DSL (KR)" UP_*.md` = 1 확인
- `grep -c "## Changelog (KR)" UP_*.md` = 1 확인
