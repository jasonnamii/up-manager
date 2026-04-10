# up-manager

> 🇰🇷 [한국어 README](./README.ko.md)

**User Preferences (UP) management pipeline.**

## Prerequisites

- **Obsidian Vault** — vault path referenced for machine-specific Cowork guidelines
- **Desktop Commander MCP** — required for vault file reads/writes
- **Claude Cowork or Claude Code** environment

## Goal

up-manager provides a unified interface for managing all User Preferences settings. It handles the entire UP lifecycle: DSL editing, version bumping, path updates, QC validation, stability tracking, propagation, and reporting. English-only master (v29.0+).

## When & How to Use

Trigger to add, modify, or manage preferences. L1/L2 quick edits use FAST_PATH for single-turn processing. Larger changes go through full pipeline.

## Use Cases

| Scenario | Prompt | What Happens |
|---|---|---|
| Quick edit | `"Add output format preference. L1."` | FAST_PATH: parse→validate→bump version→update paths→QC→report (1 turn) |
| Major restructure | `"Reorganize workflow preferences."` | Full pipeline: edit→validate→bump→paths→stability→propagate→report |
| Batch updates | `"Update 5 preferences across ecosystem."` | Parse all→validate→single version bump→QC→impact report |

## Key Features

- DSL editing with human-readable preference syntax
- Automatic semantic version bumping (v29.0+)
- Path management: auto-updates all references
- QC validation for backward compatibility
- Stability tracking across dependent systems
- Ecosystem propagation to all dependent skills
- FAST_PATH for L1/L2 single-turn edits

## Works With

- **[git-sync](https://github.com/jasonnamii/git-sync)** — commits version-bumped preferences to GitHub
- **[session-briefing](https://github.com/jasonnamii/session-briefing)** — records preference changes for continuity

## Installation

```bash
git clone https://github.com/jasonnamii/up-manager.git ~/.claude/skills/up-manager
```

## Update

```bash
cd ~/.claude/skills/up-manager && git pull
```

Skills placed in `~/.claude/skills/` are automatically available in Claude Code and Cowork sessions.

## Part of Cowork Skills

This is one of 25+ custom skills. See the full catalog: [github.com/jasonnamii/cowork-skills](https://github.com/jasonnamii/cowork-skills)

## License

MIT License — feel free to use, modify, and share.
