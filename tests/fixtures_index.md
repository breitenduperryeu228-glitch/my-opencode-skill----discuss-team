# Test fixtures & fixtures index

This file lets tests find expected fixture paths deterministically.

| Validator | Fixture / path |
|---|---|
| `validate_config.py` | `../discuss-team.config.yaml` |
| `validate_personas.py` | `../personas/{classmate,expert,top-student,grand-senior}.md` |
| `validate_skill.py` | `../SKILL.md` |

All paths are resolved relative to this file's parent (`tests/`).