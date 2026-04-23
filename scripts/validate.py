#!/usr/bin/env python3
"""
up-manager self-check validator.

4종 자가 점검:
  ① SKILL.md 크기 ≤ 6KB
  ② references/ 스포크 5개+ 존재
  ③ INVARIANT 마커 6개+ 존재
  ④ evals/cases.json 구문 유효

사용:
  python scripts/validate.py ./
  python scripts/validate.py /path/to/up-manager/

출력:
  JSON {"status": "PASS|FAIL", "checks": [...], "errors": [...]}
"""

import json
import sys
import re
from pathlib import Path


HUB_SIZE_LIMIT = 8 * 1024  # 8KB (skill_scanner 10KB 대비 여유)
REQUIRED_SPOKES = [
    "invariant-guard.md",
    "session-cache.md",
    "init-protocol.md",
    "pipeline.md",
]
INVARIANT_MIN = 6


def check_hub_size(skill_dir: Path) -> dict:
    hub = skill_dir / "SKILL.md"
    if not hub.exists():
        return {"name": "hub_size", "status": "FAIL", "evidence": "SKILL.md 부재"}
    size = hub.stat().st_size
    if size <= HUB_SIZE_LIMIT:
        return {"name": "hub_size", "status": "PASS",
                "evidence": f"{size}B / {HUB_SIZE_LIMIT}B"}
    return {"name": "hub_size", "status": "FAIL",
            "evidence": f"{size}B > {HUB_SIZE_LIMIT}B (한계 초과)"}


def check_spokes(skill_dir: Path) -> dict:
    refs_dir = skill_dir / "references"
    if not refs_dir.exists():
        return {"name": "spokes", "status": "FAIL", "evidence": "references/ 부재"}
    existing = {f.name for f in refs_dir.iterdir() if f.is_file()}
    missing = [s for s in REQUIRED_SPOKES if s not in existing]
    if not missing:
        return {"name": "spokes", "status": "PASS",
                "evidence": f"{len(REQUIRED_SPOKES)}개 스포크 모두 존재"}
    return {"name": "spokes", "status": "FAIL",
            "evidence": f"누락: {missing}"}


def check_invariants(skill_dir: Path) -> dict:
    hub = skill_dir / "SKILL.md"
    if not hub.exists():
        return {"name": "invariants", "status": "FAIL", "evidence": "SKILL.md 부재"}
    text = hub.read_text(encoding="utf-8")
    markers = re.findall(r"INVARIANT\s*#\d+", text)
    if len(markers) >= INVARIANT_MIN:
        return {"name": "invariants", "status": "PASS",
                "evidence": f"INVARIANT 마커 {len(markers)}개 (최소 {INVARIANT_MIN}개)"}
    return {"name": "invariants", "status": "FAIL",
            "evidence": f"INVARIANT 마커 {len(markers)}개 < {INVARIANT_MIN}개"}


def check_evals(skill_dir: Path) -> dict:
    cases_file = skill_dir / "evals" / "cases.json"
    if not cases_file.exists():
        return {"name": "evals", "status": "FAIL", "evidence": "evals/cases.json 부재"}
    try:
        data = json.loads(cases_file.read_text(encoding="utf-8"))
        cases = data.get("cases", [])
        if not cases:
            return {"name": "evals", "status": "FAIL",
                    "evidence": "cases 배열 비어있음"}
        required_keys = {"case_id", "category", "input", "expected"}  # edit4_level 제거 v2.5~
        for c in cases:
            missing = required_keys - set(c.keys())
            if missing:
                return {"name": "evals", "status": "FAIL",
                        "evidence": f"case {c.get('case_id', '?')} 필드 누락: {missing}"}
        return {"name": "evals", "status": "PASS",
                "evidence": f"케이스 {len(cases)}건 모두 유효"}
    except json.JSONDecodeError as e:
        return {"name": "evals", "status": "FAIL",
                "evidence": f"JSON 구문 오류: {e}"}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "FAIL",
                          "errors": ["usage: validate.py <skill_dir>"]}))
        sys.exit(1)
    skill_dir = Path(sys.argv[1]).resolve()
    if not skill_dir.is_dir():
        print(json.dumps({"status": "FAIL",
                          "errors": [f"not a directory: {skill_dir}"]}))
        sys.exit(1)

    checks = [
        check_hub_size(skill_dir),
        check_spokes(skill_dir),
        check_invariants(skill_dir),
        check_evals(skill_dir),
    ]
    fails = [c for c in checks if c["status"] == "FAIL"]
    status = "PASS" if not fails else "FAIL"
    errors = [f"{c['name']}: {c['evidence']}" for c in fails]

    result = {
        "status": status,
        "target": str(skill_dir),
        "checks": checks,
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
