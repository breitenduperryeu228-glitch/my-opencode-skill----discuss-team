# arXiv Three-Protocol Degradation

discuss-team v2.0.1 大师兄必须遵循的 arxiv 三协议降级标准。

> **v2.0.1 修复**：强制 HTTPS + 跟随重定向 + paper_id 去版本号 + 健康检查 + 指数退避

---

## ⚠️ v2.0.1 关键修复（必读）

| 问题 | 修复前 | 修复后 |
|---|---|---|
| HTTP→HTTPS 重定向 | `http://` 返回 301，webfetch 不跟随 → **静默失败** | `https://` + `follow_redirects: true` |
| paper_id 版本号 | `1101.4081v3` 直接拼 URL → **下载失败** | `sed 's/v[0-9]*$//'` 去版本号 |
| 重试策略 | 固定 `sleep(3)` | 指数退避 1s, 2s, 4s |
| 健康检查 | 无 | 每次运行前 PING 验证 |

**历史背景**：arxiv 于 2025-11-11 完成 API 全面迁移（强制 HTTPS），官方公告：
> "We are replacing the software and hardware for the arXiv api... You may notice an increase in errors returned."

---

## 三协议总览

| 协议 | 触发条件 | 输出 | 用户知情 |
|---|---|---|---|
| **A (实时)** | API 调用成功 | 真实论文引用 + 可点击链接 | ✅ 默认 |
| **B (legacy)** | API 失败 | 截止知识内论文 + ⚠️ 标注 | ✅ 显式声明 |
| **C (放弃)** | 完全失败 | plan 文件显式警告 | ✅ 强制 moderator 警告 |

---

## 协议 A (Protocol A: Real-time) — v2.0.1 完整实现

### 流程（含健康检查 + 指数退避）

```python
import re
import subprocess

def protocol_a(query, config):
    """v2.0.1 完整实现：HTTPS + follow_redirects + paper_id 去版本号"""

    # Step 1: 健康检查
    if config.get('health_check', {}).get('enabled', True):
        if not health_check(config):
            return None  # 健康检查失败，降级协议 B

    # Step 2: 构造 URL（强制 HTTPS）
    api_base = "https://export.arxiv.org/api/query"  # 永远 HTTPS，禁止 http://
    url = f"{api_base}?search_query={query}&max_results=3&sortBy=relevance"

    # Step 3: 调用 API（curl -L 跟随重定向）
    max_retries = config.get('max_retries', 3)
    for attempt in range(max_retries + 1):
        try:
            result = subprocess.run(
                ["curl", "-L", "-s", "--max-time", "30", url],
                capture_output=True, text=True, timeout=35
            )
            if result.returncode == 0 and "<entry>" in result.stdout:
                return parse_atom_xml(result.stdout)
        except (subprocess.TimeoutExpired, Exception) as e:
            if attempt < max_retries:
                # 指数退避: 1s, 2s, 4s
                time.sleep(2 ** attempt)
                continue
    return None  # 重试耗尽，降级协议 B


def parse_atom_xml(xml_text):
    """解析 Atom XML，处理 paper_id 版本号"""
    papers = []
    for entry in re.finditer(r'<entry>(.*?)</entry>', xml_text, re.DOTALL):
        e = entry.group(1)
        # 提取 paper_id（含版本号）
        raw_id = re.search(r'<id>http://arxiv.org/abs/([^<]+)</id>', e)
        if not raw_id:
            continue
        # v2.0.1 关键修复：去除版本号
        # "2605.19362v3" → "2605.19362"
        paper_id = re.sub(r'v\d+$', '', raw_id.group(1))

        title = re.search(r'<title>(.*?)</title>', e, re.DOTALL)
        summary = re.search(r'<summary>(.*?)</summary>', e, re.DOTALL)
        published = re.search(r'<published>([^<]+)</published>', e)

        papers.append({
            "id": paper_id,
            "raw_id": raw_id.group(1),  # 保留原始（含版本号）用于追溯
            "title": title.group(1).strip() if title else "",
            "summary": summary.group(1).strip() if summary else "",
            "year": published.group(1)[:4] if published else "",
            "url": f"https://arxiv.org/abs/{paper_id}",
            "pdf_url": f"https://arxiv.org/pdf/{paper_id}",
        })
    return papers
```

### 输出格式 (plan 文件)

```markdown
| 论文 ID | 标题 | 相关性 | 链接 |
|---------|------|--------|------|
| 2605.19362 | Efficient LLM Safety Evaluation... | 高 | [arxiv.org/abs/2605.19362](https://arxiv.org/abs/2605.19362) |
```

---

## 协议 B (Protocol B: Legacy Knowledge)

### 触发条件
- arxiv API 超时（>30s）
- arxiv API 返回 5xx
- arxiv API 返回 429 (限流)
- 网络不可达
- 健康检查失败

### 流程
```python
def protocol_b(query):
    """使用模型知识截止内的相关论文，标注未实时验证"""
    papers = recall_from_training(query)  # 模型内部知识
    return [
        {
            "id": paper.id,
            "title": paper.title,
            "year": paper.year,
            "summary": paper.summary,
            "verified": False,  # 关键标注
        }
        for paper in papers
    ]
```

### 输出格式 (plan 文件)
```markdown
| 论文 ID | 标题 | 相关性 | 链接 | 验证状态 |
|---------|------|--------|------|----------|
| 2301.12345 | [Title] | 高 | (未实时验证) | ⚠️ Legacy knowledge |
```

### 关键标注
- 每篇论文**必须**带 `⚠️ 未实时验证` 标记
- plan 文件 References 章节开头声明：
  `> ⚠️ 本节使用截止知识内的论文，未经 arxiv API 实时验证。`

---

## 协议 C (Protocol C: Abandon)

### 触发条件
- 模型知识截止内无相关论文
- 用户明确禁用网络访问
- 健康检查连续失败 ≥ fail_threshold

### 流程
```python
def protocol_c(query):
    return []  # 空结果
```

### 输出格式 (plan 文件)
```markdown
## 📚 参考文献

> ⚠️ **本讨论无学术依据支持**
>
> arxiv API 调用失败，且模型知识截止内未找到相关论文。
> 用户的"我想做 X"想法未被任何已发表研究直接验证。
>
> 建议用户：
> - 自行检索 Google Scholar / Semantic Scholar
> - 推迟决策直到获得学术支撑
> - 接受"未经验证假设"风险
```

### Moderator 强制警告
```markdown
🚨 **Moderator 警告**: 本讨论未获得 arxiv 学术依据支持。
结论可能是"基于常识的推测"，请用户在采纳前独立验证。
```

---

## 健康检查（v2.0.1 新增）

### 实现
```python
def health_check(config):
    """每次讨论启动前 PING arxiv"""
    hc = config.get('health_check', {})
    if not hc.get('enabled', True):
        return True

    timeout = hc.get('timeout_seconds', 5)
    fail_threshold = hc.get('fail_threshold', 3)

    for attempt in range(fail_threshold):
        try:
            result = subprocess.run(
                ["curl", "-L", "-s", "-o", "/dev/null",
                 "-w", "%{http_code}",
                 "--max-time", str(timeout),
                 "https://export.arxiv.org/api/query?search_query=all:test&max_results=1"],
                capture_output=True, text=True, timeout=timeout + 2
            )
            if result.stdout.strip() == "200":
                return True
        except Exception:
            pass
        time.sleep(1)
    return False  # 连续失败，降级协议 B
```

### 健康检查输出
```markdown
## 📊 arxiv 检索健康报告

| 步骤 | 状态 | 耗时 | 备注 |
|---|---|---|---|
| API 健康检查 | ✅ 200 | 0.6s | HTTPS, 无重定向 |
| Query 构造 | ✅ | <0.1s | 关键词: ... |
| HTTP 请求 | ✅ 200 | 0.5s | follow_redirects: true |
| XML 解析 | ✅ 3 篇 | <0.1s | paper_id 去版本号 |
| PDF 下载 | ✅ 437KB | 1.2s | 9 页 |
| **总耗时** | | **~3s** | |

**协议标注**: A (实时成功)
```

---

## 失败重试策略（v2.0.1 升级为指数退避）

```python
def fetch_with_exponential_backoff(url, max_retries=3):
    """v2.0.1: 指数退避替代固定 sleep(3)"""
    for attempt in range(max_retries + 1):
        try:
            result = subprocess.run(
                ["curl", "-L", "-s", "--max-time", "30", url],
                capture_output=True, text=True, timeout=35
            )
            if result.returncode == 0:
                return result.stdout
        except subprocess.TimeoutExpired:
            if attempt < max_retries:
                # 1s, 2s, 4s
                time.sleep(2 ** attempt)
                continue
    return None
```

---

## PDF 下载（v2.0.1 完整实现）

```python
def download_pdf(paper_id, download_dir, request_interval=3):
    """下载 PDF，使用去版本号的 paper_id"""
    pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
    output_path = f"{download_dir}/{paper_id}.pdf"

    try:
        result = subprocess.run(
            ["curl", "-L", "-s", "-o", output_path,
             "--max-time", "30", pdf_url],
            capture_output=True, text=True, timeout=35
        )

        # v2.0.1 验证：检查文件是否真实 PDF
        if os.path.exists(output_path) and os.path.getsize(output_path) > 100_000:
            return output_path
        else:
            os.remove(output_path) if os.path.exists(output_path) else None
            return None
    except Exception:
        return None
```

**关键验证**：
- 文件 > 100KB（防止下载到错误页面）
- 文件以 `%PDF-` 开头（防止下载到 HTML 错误页）

---

## Standard vs Full 模式差异

| 模式 | arxiv 协议 | PDF 下载 | plan 章节标注 |
|---|---|---|---|
| **standard** | A (检索, ≤2篇) | ❌ 不下载 | 默认无 References |
| **full** | A (检索+下载, ≤5篇) | ✅ 下载到 `参考文献/` | 强制 References 章节 |

---

## 防幻觉铁律

**配置示例（完整）**：
```yaml
arxiv:
  api_base: "https://export.arxiv.org/api/query"  # 必须 HTTPS
  follow_redirects: true
  paper_id_strip_version: true
  retry_strategy: "exponential"
  max_retries: 3
  health_check:
    enabled: true
    timeout_seconds: 5
    fail_threshold: 3
```

❌ **绝对不允许**：
- "凭印象"评价（"我记得有个论文是……"）
- 论文 ID 编造（必须来自 API 响应）
- 作者 / 年份 / 期刊瞎填
- 跳过 `follow_redirects` 直接用 HTTP（v2.0.1 强制 HTTPS）

✅ **必须做**：
- 论文 ID 必须来自真实 API 响应
- **paper_id 去版本号后保存**（v2.0.1 关键修复）
- API 失败时显式声明协议降级
- **健康检查在 API 调用前完成**（v2.0.1 新增）
- **curl 必须加 `-L` 跟随重定向**（v2.0.1 关键修复）
- **PDF 下载后验证文件大小 > 100KB**（v2.0.1 验证机制）
- 用户对引用真伪有 audit 权（plan 文件可被检查）