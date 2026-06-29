---
name: discuss-team
version: "1.0.0"
description: >
  4 角色 AI 讨论团（同学、专家、学霸、大师兄），就用户想法展开多轮辩论讨论。
  大师兄主动检索 arxiv 论文并下载到"参考文献"目录。
  讨论结束输出对话记录 + 总结报告 + TODO 清单到 .sisyphus/plans/{name}.md，
  格式完全兼容 Prometheus 工作计划，可直接 /start-work 执行。
  触发词："/discuss-team"、"讨论团"、"讨论一下"、"讨论团讨论"。
argument-hint: "<想法描述>"
author: hope
license: MIT
---

# Discuss Team (讨论团)

A 4-AI-role discussion skill that simulates multi-perspective debate to help you refine your ideas before committing.

## What This Skill Does

You give it an idea. Four AI personas debate it from different angles:
- 🌱 **同学 (Classmate)** — Socratic, asks questions, finds logical gaps
- 🎓 **专家 (Expert)** — Rigorous, gives verifiable answers
- 🧠 **学霸 (Top Student)** — Deep knowledge, supplements expert with unique insights
- 📚 **大师兄 (Grand Senior)** — Searches arxiv, downloads PDFs, gives critical advice

They debate until all four explicitly say "我无异议" (I have no objections), then output a final plan to `.sisyphus/plans/{name}.md` that's compatible with Prometheus work plans.

## Quick Start

```bash
/discuss-team 我想做一个 AI 助手
```

Or use natural language:

```
讨论团 我想做一个 AI 助手
讨论一下：我的产品想法是 XX
```

## Activation Triggers

The skill activates when:
- **Slash command**: `/discuss-team <想法>`
- **Natural language**: "讨论团"、"讨论一下"、"讨论团讨论" + 想法描述

## Core Workflow

```
┌──────────────────────────────────────────────────────────────┐
│                  discuss-team 工作流                          │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  1. 用户输入 /discuss-team <想法>                             │
│              ↓                                                │
│  2. 加载配置文件 (discuss-team.config.yaml)                   │
│              ↓                                                │
│  3. 生成 .sisyphus/plans/{discuss-YYYY-MM-DD-slug}.md         │
│              ↓                                                │
│  4. 阶段 1: 独立思考 (3 人)                                   │
│     - 专家: 严谨分析                                          │
│     - 学霸: 补充 + 独到见解                                   │
│     - 大师兄: arxiv 检索 + 论文下载                           │
│              ↓                                                │
│  5. 阶段 2: 自然辩论循环                                      │
│     - 同学苏格拉底追问 → 其他三人回应/质疑                    │
│     - 谁有意见谁说                                            │
│     - 每 3 轮重读 persona 卡片 (防 drift)                     │
│     - 检测用户插话关键词                                      │
│              ↓                                                │
│  6. 阶段 3: 收敛或超时                                        │
│     - 4 人都说"我无异议" → 收敛                               │
│     - 超过 max_rounds → 提示用户                              │
│              ↓                                                │
│  7. 输出三件套:                                               │
│     - 总结报告 (共识/风险/洞察)                               │
│     - TODO 清单 (Prometheus 兼容)                             │
│     - 完整讨论记录 (附录)                                     │
│              ↓                                                │
│  8. 用户可执行 /start-work 开始实施                           │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## Detailed Implementation

### Step 1: Initialize Discussion

When the user invokes `/discuss-team <idea>`, execute the following:

1. **Load configuration**:
   - Read `discuss-team.config.yaml` for all parameters
   - If file is missing, use sensible defaults from the config example

2. **Generate filename**:
   ```python
   from datetime import datetime
   import re

   def generate_filename(user_idea: str) -> str:
       date = datetime.now().strftime("%Y-%m-%d")
       slug = re.sub(r'[^\w\u4e00-\u9fff]+', '-', user_idea[:30]).strip('-')
       if not slug:
           slug = f"idea-{datetime.now().strftime('%H%M%S')}"
       return f"discuss-{date}-{slug}.md"
   ```

3. **Create plan file**:
   - Path: `.sisyphus/plans/{filename}.md`
   - Use `templates/plan-template.md` as starting structure
   - Fill in `{user_idea}`, `{timestamp}`, etc.

4. **Create references directory**:
   - Path: `.sisyphus/plans/参考文献/`
   - (Will be populated by 大师兄)

5. **Initialize state**:
   - `round = 0`
   - `discussion_log = []`
   - `all_no_objection = False`

### Step 2: Load Persona Cards

Read all 4 persona cards from `personas/` directory:
- `personas/classmate.md`
- `personas/expert.md`
- `personas/top-student.md`
- `personas/grand-senior.md`

**Important**: Before each turn, if `round % persona_refresh_interval == 0`, explicitly re-read the persona card to prevent drift.

### Step 3: Phase 1 — Independent Thinking (3 Personas)

**Output format**:
```markdown
🎬 [讨论开始]
用户想法: {user_idea}
时间: {timestamp}

📋 阶段 1: 独立思考
请以下 3 位独立思考（同学不参与此阶段）：

---

🎓 专家:
[对用户想法的严谨分析，包含：
- 核心问题分解
- 现有方案对比
- 可行性评估
- 潜在风险]

---

🧠 学霸:
[在专家分析基础上的补充：
- 更深层的洞见
- 跨领域类比
- 容易被忽视的细节
- 独到观点]

---

📚 大师兄:
[前沿视角 + arxiv 论文支持：
- 调用 arxiv API 搜索相关论文
- 下载 PDF 到 参考文献/
- 引用论文支撑观点
- 指出研究趋势和空白]
```

**大师兄的 arxiv 检索流程**:

1. **构造查询**:
   - 从用户想法中提取核心关键词（3-5 个）
   - 英文翻译（如用户用中文）
   - 示例: "AI 助手" → `cat:cs.AI AND (all:"AI assistant" OR all:"conversational agent")`

2. **调用 arxiv API**:
   ```
   GET {api_base}?search_query={query}&max_results={max_results}&sortBy={sort_by}
   ```

3. **解析响应** (Atom XML):
   - 提取 paper_id, title, authors, published, summary
   - 提取 PDF URL: `{pdf_url_template}`.format(paper_id=paper_id)

4. **下载 PDF**:
   - 使用 webfetch 或 bash curl 下载
   - 保存到 `.sisyphus/plans/参考文献/{paper_id}.pdf`
   - 请求间隔 ≥ 3 秒（避免限流）

5. **失败降级**:
   - 重试 1 次
   - 仍失败 → 用知识截止内的相关论文（标注"未实时验证"）
   - 完全失败 → 明确告诉用户无法获取

**工具调用示例** (opencode webfetch):
```
webfetch(
  url="http://export.arxiv.org/api/query?search_query=cat:cs.AI+AND+all:assistant&max_results=3",
  format="text"
)
```

**PDF 下载示例** (opencode bash):
```bash
curl -L "https://arxiv.org/pdf/2401.12345.pdf" \
  -o ".sisyphus/plans/参考文献/2401.12345.pdf" \
  --max-time 30
```

### Step 4: Phase 2 — Natural Debate

**发言规则**:
- 主持人（AI 自己）每轮选择"最有意见"的角色先发言
- 其他角色可以响应/质疑/补充
- 没有固定顺序，自然辩论

**每轮格式**:
```markdown
#### Round {n}

**{role_emoji} {role_name}**: [发言内容]
```

**停止条件检测** (每轮结束后):
```python
def check_stop_conditions(round, log, config):
    # 条件 1: 4 人都说"我无异议"
    last_4_speeches = log[-4:]
    if all("我无异议" in speech for speech in last_4_speeches):
        return "consensus_reached"

    # 条件 2: 超过 max_rounds
    if round >= config['discussion']['max_rounds']:
        return "timeout"

    return "continue"
```

**超时处理**:
```markdown
⏰ [第 {max_rounds+1} 轮]
讨论已进行 {max_rounds} 轮，尚未收敛。

请用户选择：
- 输入"继续" → 继续辩论
- 输入"强行收敛" → 立即输出当前共识
- 输入"放弃" → 终止讨论
```

### Step 5: User Intervention Support

**Slash 命令** (用户输入时检测):
- `/discuss-team pause` → 暂停辩论，等待用户进一步指示
- `/discuss-team resume` → 恢复辩论
- `/discuss-team intervene` → 用户发表意见，AI 整合后继续
- `/discuss-team status` → 显示当前轮次、参与者状态、最近 3 轮
- `/discuss-team force-end` → 强制收敛，输出当前最佳方案

**自然语言关键词** (从 `intervention.natural_language_triggers` 加载):
- "等等"、"等一下"、"我有不同看法"、"我有异议" 等
- 触发后暂停当前轮，让用户发言
- 用户发言后，AI 整合意见并继续

**实现方式**:
```python
def check_user_intervention(user_input, config):
    triggers = config['intervention']['natural_language_triggers']
    for trigger in triggers:
        if trigger in user_input:
            return True
    return False
```

### Step 6: Phase 3 — Convergence Output

当停止条件满足时（无论是共识还是超时），生成最终输出：

**1. 总结报告**:
```markdown
## 📋 总结报告 (Executive Summary)

### 共识方案
[3-5 个 bullet point]

### 关键洞察
- [洞察 1]
- [洞察 2]

### 主要风险
- [风险] → 缓解: [措施]

### 开放问题
- [问题]
```

**2. TODO 清单** (Prometheus 兼容格式):
```markdown
## ✅ TODO 清单 (Action Items)

### 任务 1: [名称]
**验收标准**: [criteria]
**QA 场景**: [scenarios]
**优先级**: high/medium/low
**依赖**: [task_ids]
**工作量**: [hours]
```

**3. 完整讨论记录** (作为附录):
- 包含所有 round 的发言
- 包含阶段 1 的独立思考
- 包含用户插话记录 (如有)
- 包含超时记录 (如有)

**4. 参考文献章节**:
```markdown
## 📚 参考文献
| 论文 ID | 标题 | 相关性 | 链接 |
|---------|------|--------|------|
| 2401.12345 | [Title] | 高 | [PDF](参考文献/2401.12345.pdf) |
```

**写入文件**:
- 将所有内容按 `templates/plan-template.md` 的结构拼装
- 写入 `.sisyphus/plans/{filename}.md`
- TODO 在前，对话记录附录在后

### Step 7: Completion

**成功完成时**:
```markdown
✅ 讨论团任务完成！

📄 计划文件: .sisyphus/plans/{filename}.md
📚 参考文献: .sisyphus/plans/参考文献/ ({n} 篇论文)

🚀 下一步:
- 查看完整方案: cat .sisyphus/plans/{filename}.md
- 开始实施: /start-work
```

## Configuration

All behavior is controlled by `discuss-team.config.yaml`. Key settings:

```yaml
discussion:
  max_rounds: 10              # 超过此轮数提示用户
  persona_refresh_interval: 3 # 每 N 轮重读 persona 卡

arxiv:
  enabled: true
  max_results: 3              # 每次搜索最多几篇
  download_dir: "参考文献"   # 论文下载位置
  failure_strategy: "use_legacy"  # 失败时降级策略

intervention:
  natural_language_enabled: true
  natural_language_triggers: [...]
```

See the full config file for all options.

## Best Practices

### DO
- ✅ 让 4 个角色充分辩论，不要急于收敛
- ✅ 大师兄必须真的查 arxiv，不能只凭记忆
- ✅ 同学要多问"为什么"，逼出深层逻辑
- ✅ 每 3 轮重读 persona 卡片防 drift
- ✅ 尊重用户插话，暂停当前轮让用户发言

### DO NOT
- ❌ 让 4 个角色声音同质化
- ❌ 大师兄跳过 arxiv 检索直接"凭印象"评价
- ❌ 强行收敛（除非超时或用户要求）
- ❌ 忽略用户的插话
- ❌ 一次性生成所有内容而不迭代

## File Structure

```
~/.config/opencode/skills/discuss-team/
├── SKILL.md                           # 本文件
├── README.md                          # 用户文档
├── discuss-team.config.yaml           # 配置文件
├── personas/                          # 4 个角色卡片
│   ├── classmate.md                   # 🌱 同学
│   ├── expert.md                      # 🎓 专家
│   ├── top-student.md                 # 🧠 学霸
│   └── grand-senior.md                # 📚 大师兄
└── templates/
    └── plan-template.md               # 计划文件模板
```

## Examples

### Example 1: Product Idea
```
User: /discuss-team 我想做一个 AI 编程助手

[讨论开始... 12 轮后收敛]
✅ 输出: .sisyphus/plans/discuss-2026-06-28-AI编程助手.md
```

### Example 2: Technical Decision
```
User: 讨论团：React vs Vue for our new project

[讨论开始... 8 轮后收敛]
✅ 输出: .sisyphus/plans/discuss-2026-06-28-React-vs-Vue.md
```

## Troubleshooting

**Q: 大师兄找不到论文怎么办？**
A: 自动降级到知识截止内的论文，标注"未实时验证"。

**Q: 4 个角色声音一样？**
A: 检查 persona 卡片是否被正确加载，必要时手动重读。

**Q: 讨论卡住超过 10 轮？**
A: 自动提示用户选择"继续"或"强行收敛"。

**Q: 用户插话后上下文丢失？**
A: 插话时把用户输入显式记录到 plan 文件的"用户插话记录"章节。

## License

MIT
