# SESSION_CACHE — 세션 내 재발동 가속

같은 세션에서 UP 2회 이상 수정 시, 매번 INIT부터 재실행하면 도구호출이 중복된다. 첫 발동에서 확정한 상태를 캐싱하여 2회차부터 INIT을 스킵한다.

---

## CACHE_FIELDS

| 필드 | 내용 |
|------|------|
| `up_path` | INIT에서 확정한 UP 파일 절대경로 |
| `stability_path` | UP_stability.md 절대경로 |
| `checklist_path` | UP_checklist.md 절대경로 |
| `current_version` | 현재 버전 번호 |
| `last_stability_snapshot` | 직전 수정 후 stability 상태 |
| `cache_timestamp` | 캐시 저장 시각 |

---

## LIFECYCLE

```
첫 발동 → INIT 실행 → CACHE_FIELDS 저장 (cache_timestamp 포함)
2회차↑ → CACHE_FIELDS 존재 확인 → 외부변경 감지 → 존재·미변경시 INIT 스킵, 캐시값 사용
버전 범프 완료 → current_version 갱신
```

---

## INVALIDATION

| 조건 | 동작 |
|------|------|
| 세션 종료 | 자동 소멸 (세션 컨텍스트 한정) |
| 사용자 "INIT 다시" 명시 | 캐시 무효화 후 재탐색 |
| 외부변경 감지 (mtime 신규) | 캐시 무효화 + 재로드 |

---

## 외부변경 감지

캐시 사용 전 파일 mtime 비교:
- macOS: `stat -f %m {파일경로}`
- Linux: `stat -c %Y {파일경로}`

캐시 저장 시각보다 mtime이 신규 → 캐시 무효화 + 재로드.
mtime 확인 불가 환경 → 캐시 미사용, 매번 원본 로드.

---

## Gotchas

| 함정 | 대응 |
|------|------|
| 캐시 과신 | 같은 세션 내에서만 유효. 세션 밖 UP 수정 가능성 있으면 INIT 재실행 |
| mtime 비교 생략 | 외부 수정 미감지 → 구 버전으로 Edit → 충돌. 반드시 비교 선행 |
| STEP 0 마운트 확인까지 스킵 | STEP 1·2는 스킵 가능, STEP 0은 항상 선행 |
