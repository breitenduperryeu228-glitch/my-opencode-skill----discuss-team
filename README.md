# discuss-team

> **4-AI-role debate skill** — refine your idea before committing by exposing it to 4 different critical perspectives.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](./CHANGELOG.md)
[![Skill Format](https://img.shields.io/badge/opencode-skill-green.svg)](./SKILL.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![Docs: 中文](https://img.shields.io/badge/docs-中文-red.svg)](./README.zh-CN.md)

A reusable [opencode skill](https://opencode.ai) that simulates a 4-AI-role structured debate to help you stress-test ideas before you commit engineering resources to them.

You give it an idea → 4 personas debate it from different angles → final plan + TODO list lands in `.sisyphus/plans/`, ready to feed into `/start-work`.

---

## 🎭 The Four Personas

| Persona | Emoji | Style | Core Weapon |
|---|---|---|---|
| **Classmate (同学)** | 🌱 | Socratic, naive, curious | Asks "why" until hidden assumptions surface |
| **Expert (专家)** | 🎓 | Rigorous, verifiable, grounded | Compares 2-3 candidate solutions with trade-offs |
| **Top Student (学霸)** | 🧠 | Deep, cross-domain, insightful | Supplements Expert with angles no one else thought of |
| **Grand Senior (大师兄)** | 📚 | arxiv-grounded, critical, frontier-aware | Hits arxiv API, downloads PDFs, cites papers by ID |

They debate until **all four** explicitly say "**我无异议**" (I have no objections), then output a plan compatible with [Prometheus work plans](https://github.com/your-org/sisyphus) → directly executable via `/start-work`.

---

## 🚀 Quick Start

### As an opencode skill (recommended)

```bash
# 1. Clone or symlink into your opencode skills directory
git clone https://github.com/breitenduperryeu228-glitch/discuss-team.git \
  ~/.config/opencode/skills/discuss-team

# 2. Invoke in any opencode session
/discuss-team 我想做一个 AI 编程助手
```

Or in natural language (no slash):

```
讨论团 React vs Vue 怎么选？
讨论一下：我的产品想法是 XX
讨论团讨论：用 Rust 重写后端值得吗？
```

### As a reference implementation (no opencode)

You can read [SKILL.md](./SKILL.md) and run the personas manually — it's all markdown, no runtime required.

See [`examples/`](./examples/) for a complete walkthrough.

---

## 📦 What You Get

After a discussion completes, you get **three artifacts**:

```
.sisyphus/plans/
├── discuss-2026-06-28-AI编程助手.md     # main plan file
└── 参考文献/                              # arxiv PDFs downloaded by 大师兄
    ├── 2401.12345.pdf
    └── 2310.54321.pdf
```

The plan file contains:

1. **Executive summary** — consensus, key insights, risks, open questions
2. **TODO list** — Prometheus-compatible, ready for `/start-work`
3. **Full discussion log** — appendix with every persona's speech

---

## 🎬 Discussion Workflow

```
  ┌──────────────────────────────────────────────────────────┐
  │                  discuss-team 工作流                      │
  ├──────────────────────────────────────────────────────────┤
  │  1. User input: /discuss-team <idea>                     │
  │              ↓                                           │
  │  2. Load config (discuss-team.config.yaml)              │
  │              ↓                                           │
  │  3. Generate plan file: .sisyphus/plans/{date}-{slug}.md │
  │              ↓                                           │
  │  4. Phase 1 — Independent thinking (3 personas)          │
  │     Expert · Top Student · Grand Senior                  │
  │              ↓                                           │
  │  5. Phase 2 — Natural debate loop                        │
  │     Classmate's Socratic questions → others respond      │
  │     Refresh persona cards every 3 rounds (anti-drift)    │
  │              ↓                                           │
  │  6. Phase 3 — Convergence or timeout                     │
  │     4 "我无异议" → output OR max_rounds → user prompt    │
  │              ↓                                           │
  │  7. Output: summary + TODOs + discussion log            │
  │              ↓                                           │
  │  8. User runs /start-work to execute                     │
  └──────────────────────────────────────────────────────────┘
```

---

## 🗣️ User Intervention

### Slash commands

| Command | Effect |
|---|---|
| `/discuss-team pause` | Pause debate |
| `/discuss-team resume` | Resume debate |
| `/discuss-team intervene` | Insert your opinion |
| `/discuss-team status` | Show current state (round, last 3 speeches) |
| `/discuss-team force-end` | Force convergence |

### Natural-language triggers

Any of these pause the current round and let you speak:

- "等等", "等一下"
- "我有不同看法", "我有异议", "我有意见"
- "暂停", "停止", "插一句", "打断一下"
- "其实"

---

## ⚙️ Configuration

All behavior is controlled by [`discuss-team.config.yaml`](./discuss-team.config.yaml). Key knobs:

```yaml
discussion:
  max_rounds: 10              # prompt user after this many rounds
  persona_refresh_interval: 3 # re-read persona cards every N rounds (anti-drift)

arxiv:
  enabled: true               # 大师兄 hits arxiv API
  max_results: 3              # cap papers per search
  failure_strategy: "use_legacy"  # fallback when API fails

intervention:
  natural_language_enabled: true
  natural_language_triggers: [...]
```

See the full config file for all options.

---

## 📂 Repository Layout

```
discuss-team/
├── SKILL.md                  # skill definition (opencode required)
├── README.md                 # this file (English)
├── README.zh-CN.md           # 中文文档
├── discuss-team.config.yaml  # behavior config
├── LICENSE                   # MIT
├── CHANGELOG.md              # version history
├── CONTRIBUTING.md           # how to contribute
├── .gitignore
├── .editorconfig
├── personas/                 # 4 persona cards
│   ├── classmate.md          # 🌱 同学
│   ├── expert.md             # 🎓 专家
│   ├── top-student.md        # 🧠 学霸
│   └── grand-senior.md       # 📚 大师兄
├── templates/
│   └── plan-template.md      # output plan template
├── examples/                 # usage examples
│   ├── quick-start/
│   └── sample-discussion/    # real discussion transcript + 参考文献/
├── tests/                    # validation scripts
│   ├── validate_config.py
│   ├── validate_personas.py
│   └── validate_skill.py
├── docs/                     # extended docs
│   ├── architecture.md
│   └── i18n/
│       └── README.zh-CN.md
└── .github/
    └── workflows/
        └── ci.yml
```

---

## 💡 Use Cases

- **Product decisions** — "Should I build this product?"
- **Tech selection** — "React vs Vue for our new project?"
- **Architecture review** — "Is this microservices split sensible?"
- **Risk assessment** — "What could go wrong with this launch?"
- **Any open question** that benefits from multi-perspective scrutiny

---

## 🛠️ Customization

To tweak personas:

1. Edit files in [`personas/`](./personas/) — each is plain markdown.
2. Tweak `discuss-style`, `core duties`, `behavior rules`.
3. Changes apply on the next discussion (no restart).

To add a 5th persona:

1. Create `personas/<your-name>.md` following the persona card schema.
2. Reference it from `SKILL.md` Step 2.
3. Add tests in `tests/validate_personas.py`.

---

## 🧪 Testing & Validation

```bash
# Validate config schema
python tests/validate_config.py

# Validate persona cards (frontmatter, sections, completeness)
python tests/validate_personas.py

# Validate SKILL.md frontmatter
python tests/validate_skill.py

# Run all
python tests/run_all.py
```

CI runs these on every PR via `.github/workflows/ci.yml`.

---

## 📜 License

[MIT](./LICENSE) — use freely, attribution appreciated.

---

## 🙏 Acknowledgments

- [opencode](https://opencode.ai) — skill format & runtime
- [Sisyphus / Prometheus](https://github.com/your-org/sisyphus) — plan compatibility
- [arxiv.org](https://arxiv.org) — paper API (大师兄's knowledge source)
- All persona authors — see [personas/](./personas/)

---

> 📚 Read the [中文文档 (README.zh-CN.md)](./README.zh-CN.md) for the original Chinese documentation.