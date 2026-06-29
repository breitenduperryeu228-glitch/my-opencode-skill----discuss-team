# Phases (Phases Flow)

discuss-team v2.0 的 3 阶段流程图，遵循 divergent → convergent 哲学。

## Phase 1: Independent Thinking (独立思考)

```
用户输入想法 → 加载 4 persona → 3 个分析者并行思考
                ├─ 专家: 严谨分析
                ├─ 学霸: 补充 + 独到洞见
                └─ 大师兄: arxiv 检索
同学不参与此阶段（避免前置锚定）
```

### 退出条件 (Gate 1)
- 3 个分析者输出完成
- 大师兄 arxiv 检索已尝试（不论协议 A/B/C）

## Phase 2: Natural Debate (自然辩论)

```
Round 1: 同学发起苏格拉底追问 → 其他 3 人响应
Round 2-N: 谁有意见谁说 → 自然辩论
每 3 轮: 强制重读 persona 卡（防 drift）
每轮结束: Quality Gate 检查
```

### 退出条件 (Gate 2)
- 条件 1: 4 人都说"我无异议" → 进入 Phase 3
- 条件 2: 超过 max_rounds → 提示用户
- 条件 3: Quality Gate 失败 3 次 → 触发超时
- 条件 4: 用户主动 force-end → 强制收敛

## Phase 3: Convergence Output (收敛输出)

```
停止条件满足 → 生成最终输出:
  1. 总结报告 (共识 / 洞察 / 风险)
  2. TODO 清单 (Prometheus 兼容，每项含可执行命令)
  3. 完整讨论记录 (附录)
  4. 参考文献章节 (含 arxiv 协议标注)

→ 写入 .sisyphus/plans/{date-slug}.md
```

## Quality Gate 检查清单

每 Phase 结束自动触发：

1. **HMW 问题**: 核心问题是否 restate 为 "How Might We..."？
2. **独立论据**: 推荐方向是否有 ≥ 2 个独立论据？
3. **可验证 TODO**: 每项 TODO 是否含可执行命令？

详见 `quality-gate.md`。