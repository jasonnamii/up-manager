# INIT — 파이프라인 착수 전 필수

스킬 발동 직후, 본격 수정 전에 **볼트 마운트를 확인**하고 **파일경로를 확정**한다. SESSION_CACHE 존재 시 STEP 1~2 스킵(STEP 0은 항상 선행).

---

## STEP 0 — 마운트 확인 (최우선, 항상 선행)

```
Agent-Ops/ 디렉토리 접근 가능? (ls 또는 glob 1회로 확인)
  → YES: STEP 1 진행
  → NO (마운트 미확인):
     `mcp__cowork__request_cowork_directory` 도구 호출로 사용자에게 볼트 마운트 요청
     → 마운트 성공 → STEP 1 진행
     → 사용자 거부·실패 → STOP + 보고 (파일 접근 불가로 파이프라인 진행 불가)

RULE: 마운트 미확인 상태에서 STEP 1 진입 ✗. 파일 탐색 실패 루프 방지.
```

### FALLBACK (vault_dependency: HARD 대체)

STEP 0 실패 시 기본은 STOP. 단, 사용자가 "outputs 폴백" 명시 시:
- `/sessions/{session}/mnt/outputs/` 에 Draft UP 파일 생성 후 진행
- 경고 표시: "⚠️ 볼트 미마운트 — outputs/로 폴백. 사용자가 수동으로 볼트에 반영 필요"
- 전파·체크리스트 동기화는 스킵, 보고에 "미반영 항목" 명시

---

## STEP 1 — 캐시 확인

```
SESSION_CACHE.up_path 존재?
  → YES: INIT 스킵, 캐시값 사용 → 경로 분기로 직행
  → NO: STEP 2 진행
```

---

## STEP 2 — 파일경로 확정

```
Agent-Ops/ 디렉토리를 탐색 → UP_user-preferences_v*.md 파일명 확정
  → 동시에 UP_stability.md, UP_checklist.md 경로도 확정
  → SESSION_CACHE에 저장

RULE: 이후 파이프라인 전체에서 확정 경로를 재사용. 재탐색 ✗
```

---

## EDGE CASES

| 케이스 | 대응 |
|--------|------|
| Agent-Ops/ 디렉토리 존재, UP_user-preferences_v*.md 0건 | STOP + 보고 "UP 본체 없음. 파일명 확인 요청" |
| UP_user-preferences_v*.md 2건+ 발견 | 버전 번호 최고값 1개 선택 + 보고 "복수 버전 감지: [목록]" |
| UP_stability.md 부재 | 경고 1줄 후 진행, S단계에서 "stability 파일 부재" 로그 |
| UP_checklist.md 부재 | 경고 1줄 후 진행, K단계 자동 스킵 (임의 생성 ✗) |
| 사용자 빈 입력 | STOP + "수정 내용을 명시해주세요" 1줄 |
| 사용자가 볼트 외부 파일 경로 제시 | STOP + "UP 본체는 Agent-Ops/ 하위만 대상" 안내 |

---

## Gotchas

| 함정 | 대응 |
|------|------|
| 마운트 미확인 직행 | Agent-Ops/ 접근 불가 상태에서 STEP 1 진입 시 탐색 실패·글롭 0건 루프. STEP 0 필수 |
| INIT 스킵 (첫 발동) | 경로 확정 건너뛰면 파일 탐색 루프. SESSION_CACHE 있을 때만 스킵 허용 |
| 복수 버전 자동 선택 | 경고 없이 최고값 선택 시 사용자 혼란. 보고 1줄 필수 |
| stability·checklist 파일 임의 생성 | 파일 부재는 사용자 환경 신호. 임의 생성 = UP 관할 외 |
