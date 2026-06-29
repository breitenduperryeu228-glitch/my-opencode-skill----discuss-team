#!/usr/bin/env python3
"""
run_all.py — Run all validation scripts in this directory.

Exits 0 only if every validator passes.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
VALIDATORS = [
    "validate_config.py",
    "validate_personas.py",
    "validate_skill.py",
]


def main() -> int:
    failures = 0
    for name in VALIDATORS:
        script = TESTS_DIR / name
        print(f"\n=== {name} ===")
        result = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(TESTS_DIR.parent),
        )
        if result.returncode != 0:
            failures += 1

    print()
    if failures == 0:
        print(f"PASS: all {len(VALIDATORS)} validators succeeded.")
        return 0
    print(f"FAIL: {failures}/{len(VALIDATORS)} validators failed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())