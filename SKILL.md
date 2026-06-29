---
name: discuss-team
version: "2.0.0"
description: >
  4-AI-role debate to refine ideas. USE FOR: ideate / stress-test plans / multi-perspective brainstorm. standard=one-pager, full=plan+TODOs.
argument-hint: "<想法描述>"
author: hope
license: MIT
---

# Discuss Team (讨论团)

A 4-AI-role discussion skill that simulates multi-perspective debate to refine ideas before commitment.

**Roles**: 🌱 Classmate (Socratic) · 🎓 Expert (rigorous) · 🧠 Top Student (deep insights) · 📚 Grand Senior (arxiv research)

## Quick Start

```bash
/discuss-team 我想做一个 AI 助手
讨论团：React vs Vue for our new project
```

## Core Workflow

```
用户输入 → 加载 persona → Phase 1 独立思考 → Phase 2 自然辩论
         → Quality Gate (3 项检查) → Phase 3 收敛输出 → plan 文件
```

## Modes (二档，no lite)

| Mode | 角色 | 轮数 | arxiv | 输出 | 适用场景 |
|---|---|---|---|---|---|
| **standard** | 4 | 4-6 | 0-2 篇 (摘要) | one-pager | 日常决策 |
| **full** | 4 | 8-12 | 3-5 篇 (含 PDF) | 完整 plan + TODO | 重要项目 |

**首次启动会询问模式**：
```
💬 检测到你想讨论: "{user_idea}"

请选择讨论深度（输入档位名 / 直接回车默认 full）：
- "standard" — 快速决策，one-pager 输出（4-6 轮，2 篇 arxiv 摘要）
- "full"     — 深入论证，完整 plan + TODO（8-12 轮，3-5 篇 arxiv 含 PDF）
- "skip"     — 使用配置文件中的 mode 字段（默认 full）
```
用户回答后写入状态机，后续轮次不再询问。

## Quality Gate (每 Phase 结束)

Moderator 自动检查 3 项：
1. **HMW 问题**: 核心问题是否能 restate 为 "How Might We..."？
2. **独立论据**: 推荐方向是否有 ≥ 2 个独立来源论据？
3. **可验证 TODO**: 每项 TODO 是否含可执行命令？

**Gate 通过** → 进入下一 Phase。  
**Gate 失败** → moderator 输出"卡点 + 需要 + 指派角色"（如 `需要 专家 补充第 2 个独立论据`）。  
**连续 3 次失败** → 触发超时协议，提示用户"继续 / 强行收敛 / 放弃"。

详见 `references/quality-gate.md`。

## arXiv 三协议降级

- **协议 A (实时)**: API 成功 → 引用真实论文
- **协议 B (legacy)**: API 失败 → 用截止知识，每篇标注 ⚠️ 未实时验证
- **协议 C (放弃)**: 完全失败 → plan 文件显式声明"本讨论无学术依据支持"

详见 `references/arxiv-protocol.md`。

## User Intervention (用户插话)

触发关键词：`等等` / `我有异议` / `我有不同看法` / `等一下` 等（详见 `discuss-team.config.yaml`）。

**协议**：
1. 用户输入触发关键词 → 暂停当前轮
2. 用户原文写入 plan 文件 `## 用户插话记录` 章节（保留时间戳 + 轮次）
3. AI 回应必须**逐条引用**用户意见（避免选择性忽略）
4. 关键词列表可在 `discuss-team.config.yaml` 中配置

**示例**：
```markdown
### 用户插话记录

#### 插话 #1 (Round 3)
- **用户**: "等等，这个 arxiv 论文我没读过，怎么知道是不是真的？"
- **AI 响应**: "你提到的'arxiv 论文真实性'问题——我会按以下方式回应：
  1. 论文 ID 必须来自实时 arxiv API 响应（不可编造）
  2. API 失败时会显式标注'⚠️ 未实时验证'
  3. 你可在 https://arxiv.org/abs/{paper_id} 直接核验
  ..."
```

## Output Format

**standard** 输出 one-pager：
- 核心问题（HMW）
- 推荐方向
- 关键假设
- MVP 范围（做/不做）
- 风险

**full** 输出 Prometheus 兼容 plan：
- 总结报告 (共识方案 / 洞察 / 风险)
- TODO 清单（每项含**可执行命令 + QA 场景**）
- 完整讨论记录（附录）
- 参考文献章节

**TODO 硬约束**（v2.0 新增）：
每个 TODO 必须含：
1. **验收标准**: ≥ 1 项含可执行命令（`grep`/`wc`/`bun test`/`pytest`/`curl` 等）
2. **QA 场景**: ≥ 1 项含具体验证步骤（含命令和期望输出）
3. **优先级**: `high` / `medium` / `low`
4. **依赖**: 前置任务 ID
5. **工作量**: 预估小时数

**示例**:
```
### 任务 1: 实现用户登录
**验收标准**:
- [ ] `bun test src/auth/login.test.ts → PASS (3 tests, 0 failures)`
- [ ] `wc -l src/auth/login.ts ≥ 50`

**QA 场景**:
- 场景 1: 输入错误密码 → 期望返回 401
- 场景 2: 输入正确密码 → 期望返回 JWT token

**优先级**: high
**依赖**: 无
**工作量**: 4h
```

## File References (折叠到 references/)

详细步骤见 `references/` 子目录：

- `references/phases.md` — divergent → convergent 流程图
- `references/personas.md` — 4 角色完整 prompt + 重读 prompt
- `references/arxiv-protocol.md` — arxiv 三协议伪代码
- `references/quality-gate.md` — moderator 检查清单

详细 persona 提示词见 `personas/` 子目录。

## Activation Triggers

- **Slash**: `/discuss-team <idea>`
- **Natural**: "讨论团"、"讨论一下"、"讨论团讨论" + 想法

## Best Practices

- ✅ 4 角色充分辩论，不急于收敛
- ✅ 大师兄必须真查 arxiv，不能凭印象
- ✅ 同学多问"为什么"，逼出深层逻辑
- ✅ 每 3 轮重读 persona 卡防 drift
- ❌ 不要强行收敛（除非超时或用户要求）
- ❌ 不要忽略用户插话
- ❌ 不要跳过 quality gate

## Troubleshooting

**Q: arxiv 检索失败？**
A: 自动降级到协议 B，每篇标注"未实时验证"；完全失败走协议 C，plan 文件显式声明。

**Q: 4 角色声音同质化？**
A: 检查 persona 是否正确加载；每 3 轮重读；moderator gate 强制差异化。

**Q: 讨论卡住超过 max_rounds？**
A: 自动提示用户"继续 / 强行收敛 / 放弃"。

**Q: 用户插话后上下文丢失？**
A: 显式写入 plan 文件"用户插话记录"章节，AI 必须逐条引用回应。

## License

MIT