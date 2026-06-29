# Quick Start

Three ways to invoke **discuss-team** in any opencode session.

## 1. Slash command

```
/discuss-team 我想做一个 AI 编程助手
/discuss-team 用 Rust 重写后端服务，值得吗？
/discuss-team React vs Vue 怎么选？
```

## 2. Natural language — Chinese

Any of these phrases activate the skill (case-insensitive):

```
讨论团 <想法>
讨论一下：<想法>
讨论团讨论：<想法>
```

Examples:

```
讨论团 我想做一个 AI 编程助手
讨论一下：用 Rust 重写后端服务
讨论团讨论：React vs Vue 怎么选
```

## 3. Natural language — English (partial support)

```
discuss-team <idea>
```

The English shorthand works for power users; the Chinese triggers are the canonical interface.

---

## What you get back

After the debate converges (or hits `max_rounds`), the skill writes a plan to:

```
.sisyphus/plans/discuss-YYYY-MM-DD-<slug>.md
```

Inside, you'll find:

- Executive summary (consensus, insights, risks, open questions)
- TODO list (Prometheus-compatible — feed to `/start-work`)
- Full discussion log (appendix)
- Reference table (papers downloaded by 大师兄)

Plus a `参考文献/` folder with PDF copies of any cited arxiv papers.

---

## Intervention

Pause / resume / interject at any time:

```
/discuss-team pause
/discuss-team resume
/discuss-team intervene
/discuss-team status
/discuss-team force-end
```

Or in plain prose: say "等等", "我有异议", "暂停", "插一句", "其实" — the skill detects these and lets you speak.