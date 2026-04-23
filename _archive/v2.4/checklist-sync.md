# CHECKLIST_SYNC — UP 체크리스트 동기화

UP 본체(엔진) 수정 후 UP_checklist.md(계기판)와 정합성 유지. stale 체크리스트는 계기판이 엔진을 잘못 반영하는 역효과를 낸다.

---

## TARGET

```
Agent-Ops/UP_checklist.md
```

파일 부재 시 경고 후 스킵 (임의 생성 ✗).

---

## SCOPE_IMPACT (수정이 체크리스트에 주는 영향)

| 등급 | 대상 | 조치 |
|------|------|------|
| **HIGH** | TOP5 조항(존댓말·hedge·판단먼저·확신도·덮어쓰기), T1 규칙, 모듈 신설/삭제, 우선순위 체계 변경 | 반드시 갱신 |
| **MID** | FULL15 조항(spine·500자·출처태그·logic tag·인과·의도디폴트·EDIT4·정정·모드게이트), T2·T3 규칙 수정 | 갱신 제안 + 컨펌 |
| **LOW** | 표현 순화, changelog만 추가, 문구 다듬기 | 스킵 (frontmatter `source:` 버전만 자동 갱신) |

---

## ACT — 동기화 동작

| 등급 | 동작 |
|------|------|
| HIGH | 영향 항목 Before/After 제시 → 컨펌 후 Edit → 체크리스트 `updated` 갱신 |
| MID | 영향 항목 After 1줄씩 제시 → 컨펌 후 Edit → 체크리스트 `updated` 갱신 |
| LOW | Edit로 frontmatter `source: UP_user-preferences_v{new}.md` 1줄만 자동 갱신 |

---

## DETECT — 영향 판정 로직

```
UP 수정 대상의 모듈명·라인·키워드를 체크리스트 TOP5/FULL15 항목과 대조
  → 대조 매치 + 규칙 의미 변경 = HIGH·MID 분기
  → 대조 매치 0 또는 표현 다듬기만 = LOW
```

**판정 주의:** TOP5·FULL15 키워드 매치만으로 HIGH 단정 ✗. **규칙 의미 변경 여부**가 판정 기준. 표현만 다듬었으면 LOW.

---

## SKIP 조건

- **L0_PATH** (QC교정만, 의미 변경 없음) — 체크리스트 영향 없음으로 전면 스킵
- **사용자 "체크리스트 스킵" 명시** — 1회 허가 BYPASS

---

## Gotchas

| 함정 | 대응 |
|------|------|
| 체크리스트 파일 임의 생성 | 파일 부재는 사용자 환경 신호. `Agent-Ops/UP_checklist.md` 부재 시 경고 후 스킵 |
| HIGH·MID 스킵 = FAIL | stale 방치는 계기판 오작동 유발. LOW도 frontmatter source 갱신은 필수 |
| 키워드 매치만으로 HIGH 단정 | 의미 변경 여부 판정 필수. 표현 다듬기는 LOW |
| L0에서 K단계 실행 | 불필요한 도구 호출. L0_PATH는 K단계도 스킵 |
