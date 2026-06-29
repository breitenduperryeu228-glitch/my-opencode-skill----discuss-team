# Architecture

This document explains how **discuss-team** is structured internally.

## Layer diagram

```
┌──────────────────────────────────────────────────────────────┐
│  opencode runtime                                            │
│  ┌────────────────────────┐                                  │
│  │ SKILL.md (frontmatter) │  ← declares slash command + hint │
│  └──────────┬─────────────┘                                  │
│             │ loads                                          │
│  ┌──────────▼──────────────────────┐                         │
│  │ discuss-team.config.yaml        │  ← behavior knobs       │
│  └──────────┬──────────────────────┘                         │
│             │ configures                                     │
│  ┌──────────▼─────────┐  ┌────────────────┐                  │
│  │ personas/*.md (×4) │  │ templates/     │                  │
│  │                    │  │ plan-template  │                  │
│  └──────────┬─────────┘  └────────┬───────┘                  │
│             │                      │                          │
│  ┌──────────▼──────────────────────▼────────┐                │
│  │ Runtime: orchestrates 3 phases            │                │
│  │  Phase 1 — Independent thinking           │                │
│  │  Phase 2 — Natural debate loop            │                │
│  │  Phase 3 — Convergence output             │                │
│  └──────────┬───────────────────────────────┘                │
│             │ writes                                         │
│  ┌──────────▼──────────────────────┐                         │
│  │ .sisyphus/plans/                  │                        │
│  │   discuss-{date}-{slug}.md       │                        │
│  │   参考文献/*.pdf                 │                        │
│  └──────────────────────────────────┘                         │
└──────────────────────────────────────────────────────────────┘
```

## Key design decisions

### 1. Persona cards are pure markdown

Each persona is a standalone markdown file. The runtime reads them as prompts. This means:

- **No code coupling** — editing a persona doesn't require rebuilding anything.
- **Version-controlled** — diff-able, review-able, revert-able.
- **Multi-lingual** — write personas in any language; the model picks up the style.

### 2. Single config file

`discuss-team.config.yaml` carries all behavior knobs. Defaults are sensible; advanced users can tune everything from `max_rounds` to `arxiv.api_base`.

### 3. Output is Prometheus-compatible

Plan files include a TODO section that matches Prometheus's work plan schema. After `/discuss-team`, you can pipe the result directly into `/start-work`.

### 4. Anti-drift: periodic persona refresh

Every `persona_refresh_interval` rounds (default 3), the runtime re-reads persona cards. This prevents the model from drifting into a generic "expert voice" and losing persona distinctiveness.

### 5. arxiv API with graceful degradation

大师兄 hits `http://export.arxiv.org/api/query`. On failure:
- Retry once.
- On second failure → fall back to model knowledge (marked "未实时验证").
- On total failure → explicitly tell the user no papers were downloaded.

The failure strategy is configurable (`use_legacy` vs `ask_user`).

### 6. Natural-language intervention

The skill detects Chinese intervention phrases (`等等`, `我有异议`, `暂停`, `插一句`, etc.) inside any user message and pauses the current round. This avoids the rigidity of pure slash-command interaction.

## File-by-file responsibility

| File | Role |
|---|---|
| `SKILL.md` | Skill manifest (frontmatter) + step-by-step runtime instructions for the LLM |
| `README.md` | English documentation |
| `README.zh-CN.md` | Chinese documentation (original) |
| `discuss-team.config.yaml` | Behavior configuration |
| `personas/classmate.md` | 🌱 Socratic-question persona |
| `personas/expert.md` | 🎓 Rigorous-verifiable persona |
| `personas/top-student.md` | 🧠 Cross-domain insight persona |
| `personas/grand-senior.md` | 📚 arxiv-grounded persona |
| `templates/plan-template.md` | Skeleton for output plan |
| `examples/` | Worked examples & invocation guides |
| `tests/` | Schema & structural validators |
| `.github/workflows/ci.yml` | CI for validators + markdown + YAML lint |
| `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md` | Open-source hygiene |

## Extension points

- **Add a 5th persona** — drop a markdown file in `personas/`, register in config + SKILL.md.
- **Different language** — translate persona cards; the skill works in any language the model supports.
- **Different domain** — e.g. legal debate team: edit persona cards to reflect legal roles (junior associate, partner, etc.).
- **Non-arxiv knowledge source** — fork `grand-senior.md` and replace arxiv API call with a different retrieval tool (PubMed, SSRN, etc.).

## Future ideas

- Pluggable output schemas (Jira tickets, GitHub issues, Linear).
- Async parallel personas in Phase 1 (currently sequential for transparency).
- Web UI for non-opencode users.
- Persona consistency scoring metric.