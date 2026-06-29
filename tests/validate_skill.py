#!/usr/bin/env python3
"""
validate_skill.py — Validate SKILL.md frontmatter and structure.

Requirements:
  - YAML frontmatter delimited by '---' at top of file
  - Required keys: name, version, description, argument-hint
  - 'name' matches the directory name (kebab-case)
  - 'version' is semver-like (X.Y.Z)
  - 'description' is non-empty and < 1024 chars
  - H1 heading present after frontmatter
  - At least one '##' section

Exit 0 on success, 1 on failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required.  Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


SKILL_PATH = Path(__file__).resolve().parent.parent / "SKILL.md"
REQUIRED_KEYS = {"name", "version", "description", "argument-hint"}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?$")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)


def main() -> int:
    if not SKILL_PATH.exists():
        fail(f"SKILL.md not found at {SKILL_PATH}")
        return 1

    text = SKILL_PATH.read_text(encoding="utf-8")
    if not text.startswith("---"):
        fail("SKILL.md must start with YAML frontmatter delimited by '---'")
        return 1

    parts = text.split("---", 2)
    if len(parts) < 3:
        fail("Frontmatter is not properly closed with '---'")
        return 1

    fm_raw = parts[1].strip()
    body = parts[2].lstrip("\n")

    try:
        fm = yaml.safe_load(fm_raw)
    except yaml.YAMLError as e:
        fail(f"Frontmatter YAML parse error: {e}")
        return 1

    if not isinstance(fm, dict):
        fail("Frontmatter must be a YAML mapping")
        return 1

    errors: list[str] = []

    for key in REQUIRED_KEYS:
        if key not in fm:
            errors.append(f"missing required frontmatter key '{key}'")

    # name matches directory
    if "name" in fm:
        expected = SKILL_PATH.parent.name
        if fm["name"] != expected:
            errors.append(f"frontmatter.name ({fm['name']!r}) must match directory name ({expected!r})")

    # version semver
    if "version" in fm:
        if not isinstance(fm["version"], str) or not SEMVER_RE.match(fm["version"]):
            errors.append(f"frontmatter.version must be semver (X.Y.Z), got {fm['version']!r}")

    # description
    if "description" in fm:
        desc = fm["description"]
        if not isinstance(desc, str) or not desc.strip():
            errors.append("frontmatter.description must be a non-empty string")
        elif len(desc) >= 1024:
            errors.append(f"frontmatter.description too long ({len(desc)} >= 1024)")

    # argument-hint
    if "argument-hint" in fm and not isinstance(fm["argument-hint"], str):
        errors.append("frontmatter.argument-hint must be a string")

    # body checks
    if not re.search(r"^#\s+\S", body, re.MULTILINE):
        errors.append("body must contain at least one H1 heading")

    if not re.search(r"^##\s+\S", body, re.MULTILINE):
        errors.append("body must contain at least one H2 section")

    if errors:
        for err in errors:
            fail(err)
        print(f"\n{len(errors)} validation error(s).", file=sys.stderr)
        return 1

    print("OK: SKILL.md passes frontmatter and structure validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())