# Quality Gate (Moderator 检查清单)

discuss-team v2.0 的质量门禁机制，确保讨论收敛时不草率。

## Gate 触发时机

每 Phase 结束自动触发：
- **Gate 1**: Phase 1 独立思考 → Phase 2 自然辩论
- **Gate 2**: Phase 2 自然辩论 → Phase 3 收敛输出

## Gate 检查清单 (3 项)

### 1. HMW 问题 (核心问题是否清晰)

**问题**: 核心问题是否能 restate 为 "How Might We..." 形式？

**通过标准**:
- 包含明确的动词 + 对象 + 约束
- 避免"如何做好 X"这种空泛表述
- 示例: ✅ "我们如何帮助用户在 5 分钟内做出 MVP 决策？"  
         ❌ "我们如何做 AI？"

**不通过时动作**:
```
Moderator: 卡在 [HMW 问题不清晰]。需要 [同学] 补充: "这个想法到底要解决啥问题？"
```

### 2. 独立论据 (推荐方向是否有支撑)

**问题**: 推荐方向是否有 ≥ 2 个独立论据？

**通过标准**:
- 至少 2 个**不同来源**的论据（不是同源重复）
- 来源可以是：专家经验 / 学术论文 / 用户场景 / 跨领域类比
- 不接受"我觉得"作为唯一论据

**不通过时动作**:
```
Moderator: 卡在 [推荐方向缺乏独立论据]。需要 [专家] 补充: "请给出第 2 个独立论据来源。"
```

### 3. 可验证 TODO (每项是否可执行)

**问题**: 每个 TODO 是否含可执行命令？

**通过标准**:
- 每个 TODO 含 "验收标准" 字段
- 至少 1 个验收项含**可执行命令**（grep / wc / bun test / pytest / curl 等）
- 避免"功能更好"这种主观表述

**不通过时动作**:
```
Moderator: 卡在 [TODO 任务 N 不可验证]。需要 [专家] 补充: "请给出可执行的验证命令。"
```

## Moderator 输出模板

### 通过时

```markdown
✅ Phase N 质量检验通过：
- HMW 问题: ✅ 清晰
- 独立论据: ✅ ≥ 2 个
- 可验证 TODO: ✅ 全部可执行

进入 Phase N+1。
```

### 不通过时

```markdown
⚠️ Phase N 质量检验未通过：
- HMW 问题: ✅ 清晰
- 独立论据: ❌ 仅 1 个独立论据
- 可验证 TODO: ✅ 全部可执行

🔧 卡点: [推荐方向缺乏独立论据]
🎯 需要: [专家] 补充第 2 个独立论据来源
⏰ 已失败次数: N/3
```

## 失败次数管理

```python
gate_failure_count = 0
MAX_GATE_FAILURES = 3

def on_gate_failure():
    global gate_failure_count
    gate_failure_count += 1
    if gate_failure_count >= MAX_GATE_FAILURES:
        trigger_timeout_protocol()
    else:
        assign_specific_persona_to_fix()
```

## 超时协议 (3 次失败后)

```markdown
🚨 **Phase N 质量检验连续 3 次失败**

讨论陷入循环，无法收敛。

请用户选择：
- 输入 "继续" → 继续辩论（重置失败计数）
- 输入 "强行收敛" → 接受当前最佳方案，标注已知问题
- 输入 "放弃" → 终止讨论，无 plan 输出
```

## 强制指派规则

Gate 失败时，moderator 指派**特定角色**补充，不允许转嫁：

| 失败类型 | 指派角色 | 指派理由 |
|---|---|---|
| HMW 不清晰 | 🌱 同学 | 同学本职是追问和澄清 |
| 论据不足 | 🎓 专家 | 专家本职是严谨分析 |
| TODO 不可验证 | 🎓 专家 | 专家本负责可执行性 |

被指派角色必须**直接回应**，不允许说"让其他人来回答"。

## 与停止条件的关系

```
Phase 2 进行中
  ↓
每轮结束 → Quality Gate 检查
  ↓
Gate 通过 + 4 人都无异议 → Phase 3
Gate 通过 + 超过 max_rounds → 提示用户
Gate 失败 < 3 次 → 指派补充
Gate 失败 ≥ 3 次 → 超时协议
```