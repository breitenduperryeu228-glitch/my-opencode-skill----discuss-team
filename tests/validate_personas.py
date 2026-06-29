#!/usr/bin/env python3
"""
validate_personas.py — Validate that every persona card has the required sections.

Each persona markdown file must contain (in order):
  - H1 with the persona emoji + name + "Persona 卡片"
  - ## 核心人格
  - ## 说话风格
  - ## 核心职责
  - ## 行为规约  (with subsections ### DO and ### DO NOT)
  - ## 输出模板  (at least 3 templates)
  - ## 示例对话
  - ## 启动提示
  - ## 停止条件

Exit 0 on success, 1 on failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PERSONAS_DIR = Path(__file__).resolve().parent.parent / "personas"

REQUIRED_SECTIONS = [
    "核心人格",
    "说话风格",
    "核心职责",
    "行为规约",
    "输出模板",
    "示例对话",
    "启动提示",
    "停止条件",
]

REQUIRED_BEHAVIOR_SUBSECTIONS = ["DO", "DO NOT"]
MIN_TEMPLATES = 3


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)


def check_persona(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")

    # H1 check: must start with an emoji + persona name + "Persona 卡片"
    first_line = text.splitlines()[0] if text.splitlines() else ""
    if not first_line.startswith("# "):
        errors.append(f"{path.name}: first line must be H1 ('# ...')")
    elif "Persona 卡片" not in first_line:
        errors.append(f"{path.name}: H1 must contain 'Persona 卡片'")

    # Required sections
    for section in REQUIRED_SECTIONS:
        pattern = rf"^##\s+{re.escape(section)}\s*$"
        if not re.search(pattern, text, re.MULTILINE):
            errors.append(f"{path.name}: missing section '## {section}'")

    # 行为规约 sub-check
    behavior_match = re.search(
        r"^##\s+行为规约\s*$(.*?)(?=^##\s+|\Z)", text, re.MULTILINE | re.DOTALL
    )
    if behavior_match:
        behavior_block = behavior_match.group(1)
        for sub in REQUIRED_BEHAVIOR_SUBSECTIONS:
            if not re.search(rf"^###\s+{re.escape(sub)}\b", behavior_block, re.MULTILINE):
                errors.append(f"{path.name}: 行为规约 missing subsection '### {sub}'")

    # 输出模板 count
    template_section = re.search(
        r"^##\s+输出模板\s*$(.*?)(?=^##\s+|\Z)", text, re.MULTILINE | re.DOTALL
    )
    if template_section:
        templates = re.findall(r"^###\s+模板\s+\d+", template_section.group(1), re.MULTILINE)
        if len(templates) < MIN_TEMPLATES:
            errors.append(
                f"{path.name}: 输出模板 has {len(templates)} templates, need >= {MIN_TEMPLATES}"
            )

    # Stop condition must reference "我无异议"
    if "我无异议" not in text:
        errors.append(f"{path.name}: 停止条件 must mention '我无异议' as the convergence signal")

    return errors


def main() -> int:
    if not PERSONAS_DIR.is_dir():
        fail(f"Personas directory not found: {PERSONAS_DIR}")
        return 1

    persona_files = sorted(PERSONAS_DIR.glob("*.md"))
    if not persona_files:
        fail(f"No persona files found in {PERSONAS_DIR}")
        return 1

    expected_names = {"classmate.md", "expert.md", "top-student.md", "grand-senior.md"}
    found_names = {p.name for p in persona_files}
    missing = expected_names - found_names
    if missing:
        for name in missing:
            fail(f"Missing required persona: {name}")
        return 1

    all_errors: list[str] = []
    for path in persona_files:
        all_errors += check_persona(path)

    if all_errors:
        for err in all_errors:
            fail(err)
        print(f"\n{len(all_errors)} validation error(s).", file=sys.stderr)
        return 1

    print(f"OK: all {len(persona_files)} persona cards pass schema validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())