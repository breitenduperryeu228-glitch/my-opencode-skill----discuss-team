# Contributing to discuss-team

Thanks for your interest in improving discuss-team! 🎉

This document explains how to file issues, propose changes, and submit pull requests.

---

## 🐛 Reporting Issues

When filing an issue, please include:

1. **What you did** — exact command (e.g., `/discuss-team 我想做一个 AI 编程助手`)
2. **What you expected** — what should have happened
3. **What actually happened** — paste the full discussion log
4. **Configuration** — output of `cat discuss-team.config.yaml`
5. **opencode version** — `opencode --version` if available

Use the **Bug report** issue template.

---

## 💡 Proposing Features

Open an issue with the **Feature request** template. Describe:

- The problem you want to solve
- Who benefits (and how)
- A sketch of the proposed solution
- Alternative approaches you've considered

---

## 🛠️ Submitting Pull Requests

### Setup

```bash
# Fork & clone
git clone https://github.com/<your-fork>/discuss-team.git
cd discuss-team

# (optional) Symlink for live testing
ln -s $(pwd) ~/.config/opencode/skills/discuss-team
```

### Branching

```bash
git checkout -b feat/my-improvement
# or
git checkout -b fix/persona-drift
```

### Coding conventions

- **Markdown**: Use ATX-style headings (`#`), 2-space list indent, fenced code blocks with language hints.
- **YAML**: 2-space indent, no tabs, kebab-case filenames.
- **Python (tests)**: PEP 8, type hints where reasonable, no external dependencies (stdlib only).
- **Commit messages**: Imperative mood ("Add X", not "Added X"). Reference issues with `#123`.
- **Persona cards**: Follow the existing schema in `personas/classmate.md` (核心人格 / 说话风格 / 核心职责 / 行为规约 / 输出模板 / 示例对话).

### Validation

Before pushing, run the local test suite:

```bash
python tests/run_all.py
```

All checks must pass. CI runs the same checks plus markdown lint.

### PR checklist

- [ ] I ran `python tests/run_all.py` locally and it passes.
- [ ] I added tests for new behavior (or explained why none are needed).
- [ ] I updated `CHANGELOG.md` under the "Unreleased" section.
- [ ] I updated `README.md` / `README.zh-CN.md` if user-facing.
- [ ] I did NOT introduce hardcoded paths or external network calls beyond what's already in `discuss-team.config.yaml`.

---

## 🧪 Adding a New Persona

1. Create `personas/<your-name>.md` with sections:
   - 核心人格 (core personality)
   - 说话风格 (speaking style)
   - 核心职责 (core duties)
   - 行为规约 (behavior rules — DO / DO NOT)
   - 输出模板 (output templates, 3-6)
   - 示例对话 (example dialogues)
   - 启动提示 (activation prompt)
   - 停止条件 (stop conditions)
2. Reference it from `SKILL.md` Step 2.
3. Add an entry in `discuss-team.config.yaml` under `roles:`.
4. Add a test in `tests/validate_personas.py` to assert the file exists and has all sections.

---

## 🌍 Translations

We welcome translations of README / docs into other languages.

Convention: `<basename>.<lang>.md` (e.g., `README.ja.md`, `README.es.md`).

Place translations in `docs/i18n/` and link them from `README.md`.

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the [MIT License](./LICENSE).