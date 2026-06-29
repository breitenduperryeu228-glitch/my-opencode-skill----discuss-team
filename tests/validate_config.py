#!/usr/bin/env python3
"""
validate_config.py — Validate discuss-team.config.yaml against expected schema.

Runs stdlib-only checks:
  - File exists and parses as YAML
  - Top-level keys exist
  - Required sub-keys with correct types
  - Enum-like values fall within allowed sets

Exit 0 on success, 1 on failure. Prints errors to stderr.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required.  Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


CONFIG_PATH = Path(__file__).resolve().parent.parent / "discuss-team.config.yaml"

REQUIRED_TOP_KEYS = {"discussion", "intervention", "arxiv", "roles", "output", "debug"}

REQUIRED_DISCUSSION_KEYS = {
    "max_rounds": int,
    "persona_refresh_interval": int,
    "auto_independent_thinking": bool,
    "show_round_counter": bool,
}
REQUIRED_INTERVENTION_KEYS = {
    "natural_language_enabled": bool,
    "natural_language_triggers": list,
    "slash_commands": list,
}
REQUIRED_ARXIV_KEYS = {
    "enabled": bool,
    "max_results": int,
    "download_dir": str,
    "api_base": str,
    "pdf_url_template": str,
    "request_interval_seconds": (int, float),
    "timeout_seconds": (int, float),
    "failure_strategy": str,
    "sort_by": str,
}
REQUIRED_ROLES_KEYS = {"classmate", "expert", "top_student", "grand_senior"}
REQUIRED_PER_ROLE_KEYS = {"enabled": bool, "emoji": str, "name": str}
REQUIRED_OUTPUT_KEYS = {
    "plans_dir": str,
    "filename_template": str,
    "max_slug_length": int,
    "include_todo_section": bool,
    "include_discussion_log": bool,
    "include_references_section": bool,
}
REQUIRED_DEBUG_KEYS = {
    "verbose": bool,
    "save_intermediate_state": bool,
    "log_level": str,
}

ALLOWED_FAILURE_STRATEGIES = {"use_legacy", "ask_user"}
ALLOWED_ARXIV_SORTS = {"relevance", "submittedDate", "lastUpdatedDate"}
ALLOWED_LOG_LEVELS = {"debug", "info", "warn", "error"}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)


def expect_keys(obj: dict, required: set, where: str) -> list[str]:
    errors: list[str] = []
    for key in required:
        if key not in obj:
            errors.append(f"{where}: missing required key '{key}'")
    return errors


def expect_types(obj: dict, types: dict, where: str) -> list[str]:
    errors: list[str] = []
    for key, expected in types.items():
        if key not in obj:
            continue
        if not isinstance(obj[key], expected):
            errors.append(
                f"{where}.{key}: expected type {expected}, got {type(obj[key]).__name__}"
            )
    return errors


def validate(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    # Top-level
    errors += expect_keys(config, REQUIRED_TOP_KEYS, "config")

    # discussion
    if "discussion" in config:
        d = config["discussion"]
        errors += expect_keys(d, set(REQUIRED_DISCUSSION_KEYS.keys()), "discussion")
        errors += expect_types(d, REQUIRED_DISCUSSION_KEYS, "discussion")
        if "max_rounds" in d and d["max_rounds"] <= 0:
            errors.append("discussion.max_rounds must be > 0")

    # intervention
    if "intervention" in config:
        i = config["intervention"]
        errors += expect_keys(i, set(REQUIRED_INTERVENTION_KEYS.keys()), "intervention")
        errors += expect_types(i, REQUIRED_INTERVENTION_KEYS, "intervention")
        if "natural_language_triggers" in i:
            for trigger in i["natural_language_triggers"]:
                if not isinstance(trigger, str) or not trigger.strip():
                    errors.append(f"intervention.natural_language_triggers contains invalid entry: {trigger!r}")

    # arxiv
    if "arxiv" in config:
        a = config["arxiv"]
        errors += expect_keys(a, set(REQUIRED_ARXIV_KEYS.keys()), "arxiv")
        errors += expect_types(a, REQUIRED_ARXIV_KEYS, "arxiv")
        if "failure_strategy" in a and a["failure_strategy"] not in ALLOWED_FAILURE_STRATEGIES:
            errors.append(
                f"arxiv.failure_strategy must be one of {ALLOWED_FAILURE_STRATEGIES}, got {a['failure_strategy']!r}"
            )
        if "sort_by" in a and a["sort_by"] not in ALLOWED_ARXIV_SORTS:
            errors.append(
                f"arxiv.sort_by must be one of {ALLOWED_ARXIV_SORTS}, got {a['sort_by']!r}"
            )

    # roles
    if "roles" in config:
        r = config["roles"]
        errors += expect_keys(r, REQUIRED_ROLES_KEYS, "roles")
        for role_name, role_cfg in r.items():
            if role_name not in REQUIRED_ROLES_KEYS:
                continue
            where = f"roles.{role_name}"
            errors += expect_keys(role_cfg, set(REQUIRED_PER_ROLE_KEYS.keys()), where)
            errors += expect_types(role_cfg, REQUIRED_PER_ROLE_KEYS, where)

    # output
    if "output" in config:
        o = config["output"]
        errors += expect_keys(o, set(REQUIRED_OUTPUT_KEYS.keys()), "output")
        errors += expect_types(o, REQUIRED_OUTPUT_KEYS, "output")
        if "filename_template" in o:
            for var in ("{date}", "{slug}"):
                if var not in o["filename_template"]:
                    errors.append(f"output.filename_template missing required variable {var!r}")

    # debug
    if "debug" in config:
        dbg = config["debug"]
        errors += expect_keys(dbg, set(REQUIRED_DEBUG_KEYS.keys()), "debug")
        errors += expect_types(dbg, REQUIRED_DEBUG_KEYS, "debug")
        if "log_level" in dbg and dbg["log_level"] not in ALLOWED_LOG_LEVELS:
            errors.append(
                f"debug.log_level must be one of {ALLOWED_LOG_LEVELS}, got {dbg['log_level']!r}"
            )

    return errors


def main() -> int:
    if not CONFIG_PATH.exists():
        fail(f"Config file not found: {CONFIG_PATH}")
        return 1

    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        fail(f"YAML parse error: {e}")
        return 1

    if not isinstance(config, dict):
        fail("Top-level config must be a mapping")
        return 1

    errors = validate(config)
    if errors:
        for err in errors:
            fail(err)
        print(f"\n{len(errors)} validation error(s).", file=sys.stderr)
        return 1

    print("OK: discuss-team.config.yaml passes schema validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())