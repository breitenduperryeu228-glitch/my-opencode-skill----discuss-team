# Discuss Team (讨论团)

> 4 角色 AI 讨论团 — 让你的想法在决策前接受多角度审视

## 🎯 这是什么？

**讨论团** 是一个 opencode skill，模拟 4 个不同视角的 AI 角色就你的想法进行多轮辩论讨论。

你给一个想法 → 4 个角色开始辩论 → 最终输出可执行的方案 + TODO 清单。

## 🎭 4 个角色

| 角色 | 特点 | 职责 |
|------|------|------|
| 🌱 **同学** | 苏格拉底式追问 | 揪逻辑漏洞，问"为什么" |
| 🎓 **专家** | 严谨、可验证 | 给完整答案，讲给同学听 |
| 🧠 **学霸** | 知识渊博 | 补充专家，提出独到见解 |
| 📚 **大师兄** | 紧跟前沿 | 查 arxiv 论文，给批判性建议 |

## 🚀 快速开始

### 方式 1: Slash 命令
```
/discuss-team 我想做一个 AI 助手
```

### 方式 2: 自然语言
```
讨论团 我想做一个 AI 助手
讨论一下：我的产品想法是 XX
讨论团讨论：React vs Vue
```

## 📦 产出

讨论结束后，会在 `.sisyphus/plans/` 目录生成：

```
.sisyphus/plans/
├── discuss-2026-06-28-AI助手.md    # 主计划文件
└── 参考文献/                        # 大师兄下载的 arxiv 论文
    ├── 2401.12345.pdf
    └── 2310.54321.pdf
```

主计划文件包含：
1. **总结报告** - 共识方案、关键洞察、主要风险
2. **TODO 清单** - 兼容 Prometheus 格式，可直接 `/start-work`
3. **完整讨论记录** - 4 个角色的所有发言（作为附录）

## 🎬 讨论流程

```
1. 你提出想法
   ↓
2. 阶段 1: 独立思考（专家/学霸/大师兄）
   ↓
3. 阶段 2: 自然辩论（同学苏格拉底追问 → 循环辩论）
   ↓
4. 停止条件：
   - 4 人都说"我无异议" → 收敛
   - 超过 10 轮 → 提示你选择
   ↓
5. 输出三件套
```

## 🗣️ 用户插话

### Slash 命令
- `/discuss-team pause` — 暂停讨论
- `/discuss-team resume` — 恢复讨论
- `/discuss-team intervene` — 你要插话
- `/discuss-team status` — 查看当前状态
- `/discuss-team force-end` — 强制收敛

### 自然语言关键词
说这些词会触发插话：
- "等等"、"等一下"
- "我有不同看法"、"我有异议"
- "暂停"、"插一句"、"打断一下"
- "其实"

## ⚙️ 配置

所有行为由 `discuss-team.config.yaml` 控制。常用配置：

```yaml
discussion:
  max_rounds: 10              # 超过此轮数提示你
  persona_refresh_interval: 3 # 每 N 轮重读角色卡（防 drift）

arxiv:
  enabled: true
  max_results: 3              # 每次搜索最多几篇论文
  download_dir: "参考文献"

intervention:
  natural_language_enabled: true
  natural_language_triggers: [...]
```

完整配置见 [discuss-team.config.yaml](./discuss-team.config.yaml)

## 📂 目录结构

```
discuss-team/
├── SKILL.md                  # 主文件（opencode skill 必需）
├── README.md                 # 本文件
├── discuss-team.config.yaml  # 配置文件
├── personas/                 # 4 个角色的 prompt 卡片
│   ├── classmate.md
│   ├── expert.md
│   ├── top-student.md
│   └── grand-senior.md
└── templates/
    └── plan-template.md      # 计划文件模板
```

## 💡 使用场景

- ✅ **产品决策** — "我要不要做这个产品？"
- ✅ **技术选型** — "用 React 还是 Vue？"
- ✅ **方案设计** — "这个架构怎么设计？"
- ✅ **风险评估** — "这个想法有什么坑？"
- ✅ **任何开放问题** — 想要多角度审视

## ❓ FAQ

### Q1: 大师兄找不到论文怎么办？
A: 会自动降级到知识截止内的相关论文，并在文中标注"未实时验证"。

### Q2: 4 个角色声音听起来一样？
A: 检查 `personas/` 目录的 4 个角色卡片是否正确加载。如果还是一样，可以手动重新读 persona 文件。

### Q3: 讨论卡住超过 10 轮怎么办？
A: 系统会提示你选择"继续"或"强行收敛"。

### Q4: 我能中途改想法吗？
A: 可以！用 `/discuss-team intervene` 或说"我有不同看法"，系统会暂停当前轮让你发言。

### Q5: 生成的 plan 能直接用吗？
A: 可以！TODO 清单完全兼容 Prometheus 格式，可以直接 `/start-work` 开始实施。

### Q6: 论文下载失败会怎样？
A: 不会中断讨论，只是参考文献会少几篇。大师兄会改用知识截止内的论文。

## 🔧 进阶：自定义角色

如果你想修改 4 个角色的人格或行为：

1. 编辑 `personas/{role}.md` 文件
2. 修改 `讨论风格`、`核心职责`、`行为规约` 等部分
3. 下次讨论时自动生效

## 📜 License

MIT
