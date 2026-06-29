# Changelog

All notable changes to **discuss-team** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-28

### Added
- Initial public release of discuss-team skill.
- 4 personas (classmate, expert, top-student, grand-senior) with full prompt cards.
- `discuss-team.config.yaml` with discussion / arxiv / intervention / output / debug sections.
- Plan output template (`templates/plan-template.md`) compatible with Prometheus work plans.
- Slash command (`/discuss-team`) and natural-language triggers ("讨论团", "讨论一下").
- User intervention via `/discuss-team {pause|resume|intervene|status|force-end}` and natural-language triggers.
- arxiv API integration for 大师兄 with failure-degradation strategy (`use_legacy`).
- English README (`README.md`) + Chinese README (`README.zh-CN.md`).
- Validation test suite (`tests/validate_*.py`).
- GitHub Actions CI (`.github/workflows/ci.yml`).

### Notes
- This is the first tagged release. Configuration schema may evolve in 1.x but persona cards are stable.
- License: MIT.