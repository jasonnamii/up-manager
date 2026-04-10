# UP 매니저

**사용자 설정 (UP) 통합 관리 파이프라인.**

> 🇺🇸 [English README](./README.md)

## 사전 요구사항

- **Obsidian Vault** — 머신별 Cowork 가이드라인 참조용 Vault 경로
- **Desktop Commander MCP** — Vault 파일 읽기/쓰기 필요
- **Claude Cowork 또는 Claude Code** 환경

## 목적

up-manager는 모든 사용자 설정 관리를 위한 통합 인터페이스를 제공합니다. UP의 전체 생명주기를 처리합니다: DSL 편집, 버전 범프, 경로 업데이트, QC 검증, 안정도 추적, 전파, 보고. 영어 전용 마스터 (v29.0+).

## 사용 시점 및 방법

설정을 추가, 수정, 관리하려고 할 때 발동하세요. L1/L2 빠른 편집은 FAST_PATH로 단일턴 처리. 더 큰 변경은 전체 파이프라인 거침.

## 사용 예시

| 상황 | 프롬프트 | 결과 |
|---|---|---|
| 빠른 편집 | `"출력 형식 설정 추가. L1."` | FAST_PATH: 파싱→검증→버전 범프→경로 업데이트→QC→보고 (1턴) |
| 대규모 재구성 | `"워크플로우 설정 재구성."` | 전체 파이프라인: 편집→검증→범프→경로→안정도→전파→보고 |
| 배치 업데이트 | `"생태계 전역 5개 설정 업데이트."` | 모두 파싱→검증→단일 버전 범프→QC→영향 보고 |

## 핵심 기능

- 인간 읽기 가능한 설정 문법을 통한 DSL 편집
- 자동 시맨틱 버전 범프 (v29.0+)
- 경로 관리: 모든 참조 자동 업데이트
- 역호환성을 위한 QC 검증
- 의존 시스템 간 안정도 추적
- 모든 의존 스킬로의 생태계 전파
- L1/L2 단일턴 편집용 FAST_PATH

## 연관 스킬

- **[git-sync](https://github.com/jasonnamii/git-sync)** — 버전 범프된 설정을 GitHub로 커밋
- **[session-briefing](https://github.com/jasonnamii/session-briefing)** — 연속성을 위해 설정 변경 기록
## 설치

```bash
git clone https://github.com/jasonnamii/up-manager.git ~/.claude/skills/up-manager
```

## 업데이트

```bash
cd ~/.claude/skills/up-manager && git pull
```

`~/.claude/skills/`에 배치된 스킬은 Claude Code 및 Cowork 세션에서 자동으로 사용할 수 있습니다.

## Cowork 스킬 생태계

25개 이상의 커스텀 스킬 중 하나입니다. 전체 카탈로그: [github.com/jasonnamii/cowork-skills](https://github.com/jasonnamii/cowork-skills)

## 라이선스

MIT 라이선스 — 자유롭게 사용, 수정, 공유하세요.
