# 讨论团 (Discuss Team)

> **4 角色 AI 讨论团** — 在你投入资源之前，让你的想法接受多角度审视。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](./CHANGELOG.md)
[![Skill Format](https://img.shields.io/badge/opencode-skill-green.svg)](./SKILL.md)
[![Docs: English](https://img.shields.io/badge/docs-English-blue.svg)](./README.md)

一个可复用的 [opencode skill](https://opencode.ai)，模拟 4 个不同 AI 角色的结构化辩论，帮你在投入工程资源之前压力测试想法。

你给一个想法 → 4 个角色从不同角度辩论 → 最终方案 + TODO 清单落到 `.sisyphus/plans/`，可直接喂给 `/start-work`。

> 📚 英文文档见 [README.md](./README.md)。本文为中文原始版本。

---

## 🎭 4 个角色

| 角色 | Emoji | 风格 | 核心武器 |
|---|---|---|---|
| **同学** | 🌱 | 苏格拉底式、好奇、假装不懂 | 连续追问"为什么"逼出隐含假设 |
| **专家** | 🎓 | 严谨、可验证、接地气 | 对比 2-3 个候选方案 + 利弊权衡 |
| **学霸** | 🧠 | 深刻、跨领域、有启发 | 补充专家盲点 + 提出独到角度 |
| **大师兄** | 📚 | arxiv 论文支撑、批判性、前沿 | 调 arxiv API、下载 PDF、按 ID 引用 |

辩论直到 **4 人全部**明确说"**我无异议**"，输出兼容 [Prometheus 工作计划](https://github.com/your-org/sisyphus) → 可直接 `/start-work`。

---

## 🚀 快速开始

### 作为 opencode skill 使用（推荐）

```bash
# 1. 克隆或软链到 opencode skills 目录
git clone https://github.com/breitenduperryeu228-glitch/discuss-team.git \
  ~/.config/opencode/skills/discuss-team

# 2. 在任何 opencode 会话中调用
/discuss-team 我想做一个 AI 编程助手
```

或自然语言触发（不需要 slash）：

```
讨论团 React vs Vue 怎么选？
讨论一下：我的产品想法是 XX
讨论团讨论：用 Rust 重写后端值得吗？
```

### 作为参考实现使用（无需 opencode）

你可以直接读 [SKILL.md](./SKILL.md) 并手动运行 4 个角色——纯 markdown，无需运行时。

完整示例见 [`examples/`](./examples/)。

---

## 📦 你将得到

讨论完成后产出**三件套**：

```
.sisyphus/plans/
├── discuss-2026-06-28-AI编程助手.md     # 主计划文件
└── 参考文献/                              # 大师兄下载的 arxiv 论文
    ├── 2401.12345.pdf
    └── 2310.54321.pdf
```

主计划文件包含：

1. **总结报告** — 共识方案、关键洞察、主要风险、开放问题
2. **TODO 清单** — Prometheus 兼容，可直接 `/start-work`
3. **完整讨论记录** — 附录，所有角色的所有发言

---

## 🎬 讨论流程

```
  ┌──────────────────────────────────────────────────────────┐
  │                  discuss-team 工作流                      │
  ├──────────────────────────────────────────────────────────┤
  │  1. 用户输入: /discuss-team <想法>                       │
  │              ↓                                           │
  │  2. 加载配置 (discuss-team.config.yaml)                  │
  │              ↓                                           │
  │  3. 生成 plan: .sisyphus/plans/{date}-{slug}.md          │
  │              ↓                                           │
  │  4. 阶段 1: 独立思考 (3 人)                              │
  │     专家 · 学霸 · 大师兄                                  │
  │              ↓                                           │
  │  5. 阶段 2: 自然辩论循环                                 │
  │     同学苏格拉底追问 → 其他三人响应                       │
  │     每 3 轮重读 persona 卡 (防 drift)                    │
  │              ↓                                           │
  │  6. 阶段 3: 收敛或超时                                   │
  │     4 人都说"我无异议" → 输出 或 超过 max_rounds → 提示用户 │
  │              ↓                                           │
  │  7. 输出: 总结 + TODO + 讨论记录                         │
  │              ↓                                           │
  │  8. 用户执行 /start-work 开始实施                        │
  └──────────────────────────────────────────────────────────┘
```

---

## 🗣️ 用户插话

### Slash 命令

| 命令 | 效果 |
|---|---|
| `/discuss-team pause` | 暂停讨论 |
| `/discuss-team resume` | 恢复讨论 |
| `/discuss-team intervene` | 插入你的意见 |
| `/discuss-team status` | 查看状态（轮次、最近 3 轮） |
| `/discuss-team force-end` | 强制收敛 |

### 自然语言触发词

以下任一关键词触发插话（暂停当前轮让你发言）：

- "等等", "等一下"
- "我有不同看法", "我有异议", "我有意见"
- "暂停", "停止", "插一句", "打断一下"
- "其实"

---

## ⚙️ 配置

所有行为由 [`discuss-team.config.yaml`](./discuss-team.config.yaml) 控制。常用配置：

```yaml
discussion:
  max_rounds: 10              # 超过此轮数提示用户
  persona_refresh_interval: 3 # 每 N 轮重读 persona 卡 (防 drift)

arxiv:
  enabled: true               # 大师兄调 arxiv API
  max_results: 3              # 每次搜索最多几篇
  failure_strategy: "use_legacy"  # 失败降级策略

intervention:
  natural_language_enabled: true
  natural_language_triggers: [...]
```

完整配置见配置文件。

---

## 📂 仓库结构

```
discuss-team/
├── SKILL.md                  # skill 定义（opencode 必需）
├── README.md                 # 英文文档
├── README.zh-CN.md           # 中文文档（本文件）
├── discuss-team.config.yaml  # 行为配置
├── LICENSE                   # MIT
├── CHANGELOG.md              # 版本历史
├── CONTRIBUTING.md           # 贡献指南
├── .gitignore
├── .editorconfig
├── personas/                 # 4 个角色卡片
│   ├── classmate.md          # 🌱 同学
│   ├── expert.md             # 🎓 专家
│   ├── top-student.md        # 🧠 学霸
│   └── grand-senior.md       # 📚 大师兄
├── templates/
│   └── plan-template.md      # 输出计划模板
├── examples/                 # 使用示例
│   ├── quick-start/
│   └── sample-discussion/    # 真实讨论记录 + 参考文献/
├── tests/                    # 校验脚本
│   ├── validate_config.py
│   ├── validate_personas.py
│   └── validate_skill.py
├── docs/                     # 扩展文档
│   ├── architecture.md
│   └── i18n/
│       └── README.zh-CN.md
└── .github/
    └── workflows/
        └── ci.yml
```

---

## 💡 使用场景

- ✅ **产品决策** — "我要不要做这个产品？"
- ✅ **技术选型** — "React vs Vue 怎么选？"
- ✅ **架构审查** — "这个微服务拆分合理吗？"
- ✅ **风险评估** — "这个上线方案有什么坑？"
- ✅ **任何开放问题** — 想要多角度审视

---

## 🛠️ 自定义

修改角色：

1. 编辑 [`personas/`](./personas/) 下的文件——都是纯 markdown。
2. 修改 `说话风格`、`核心职责`、`行为规约` 等部分。
3. 下次讨论时自动生效，无需重启。

增加第 5 个角色：

1. 按 persona 卡 schema 创建 `personas/<your-name>.md`。
2. 在 `SKILL.md` Step 2 引用它。
3. 在 `tests/validate_personas.py` 加测试。

---

## 🧪 测试与校验

```bash
# 校验配置 schema
python tests/validate_config.py

# 校验 persona 卡 (frontmatter、章节、完整性)
python tests/validate_personas.py

# 校验 SKILL.md frontmatter
python tests/validate_skill.py

# 全部跑一遍
python tests/run_all.py
```

CI 在每次 PR 上自动跑这些（见 `.github/workflows/ci.yml`）。

---

## 📜 License

[MIT](./LICENSE) — 自由使用，欢迎署名。

---

## 🙏 致谢

- [opencode](https://opencode.ai) — skill 格式与运行时
- [Sisyphus / Prometheus](https://github.com/your-org/sisyphus) — 计划兼容性
- [arxiv.org](https://arxiv.org) — 论文 API（大师兄的知识源）
- 所有角色作者 — 见 [personas/](./personas/)

---

> 📚 Read [English docs (README.md)](./README.md) for the English version.