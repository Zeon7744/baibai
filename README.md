# 🚀 Baibai — Vibe Coding 开发工具库 v3

## 💰 价值主张 & 定价
> **能卖什么**：通用工具集 + MCP 支持 — 22 个即插即用中文工具，让 Cursor / Claude Code / Codex 直接开箱即用。
>
> **定价**：**永久免费开源**（全部 22 工具 + MCP Server + 完整源码）/ 企业定制按需报价（定制开发 + 技术对接 + SLA）。支持渠道：[面包多 Pay赞赏](https://mbd.net/@Zeon7744)


> **用自然语言驱动开发** — MCP Server 内容创作工具集（资产底座）
> AI 编程助手必备工具箱，让 Claude Code、Cursor、Codex 更强大
>
> ⚠️ CLI 入口已弃用，请使用 MCP Server：`python mcp_server_v2.py --port 8000`

[![GitHub Stars](https://img.shields.io/github/stars/Zeon7744/baibai?style=social)](https://github.com/Zeon7744/baibai)
[![GitHub Forks](https://img.shields.io/github/forks/Zeon7744/baibai?style=social)](https://github.com/Zeon7744/baibai/forks)
[![GitHub License](https://img.shields.io/github/license/Zeon7744/baibai)](https://github.com/Zeon7744/baibai/blob/main/LICENSE)
[![Gitee Stars](https://gitee.com/Zeon7744/baibai/badge/star.svg?theme=gvp)](https://gitee.com/Zeon7744/baibai)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![MCP Support](https://img.shields.io/badge/MCP-v3-violet.svg)](https://modelcontextprotocol.io)

---

## 📌 这是 GitHub 官方主仓

> **Gitee 镜像**: [gitee.com/Zeon7744/baibai](https://gitee.com/Zeon7744/baibai)  
> **GitCode 镜像**: [gitcode.com/Zeon7744/baibai](https://gitcode.com/Zeon7744/baibai)

Issues 和 PR 请在 GitHub 提交。

---

## ⚡ 快速开始

```bash
# 安装
pip install baibai

# 或使用源码
git clone https://github.com/Zeon7744/baibai.git
cd baibai
pip install -e .

# 启动 MCP Server v3
python mcp_server_v2.py --port 8000
```

---

## 🛠️ 核心工具 (v2 基础工具)

| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `check_format` | Markdown 格式校验 | 剧本、文档规范性检查 |
| `validate_directory` | 批量校验目录 | 多文件批量校验 |
| `classify_file` | 内容自动分类 | 文件类型识别 |
| `classify_directory` | 目录批量分类 | 大量文件分类 |
| `md_to_html` | Markdown→HTML | 内容展示页生成 |
| `convert_file` | 文件转换 | Markdown 文件转 HTML |
| `gen_readme` | README 生成 | 项目文档维护 |
| `extract_content_info` | 结构化信息提取 | 内容分析 |
| `analyze_content_data` | 内容统计 | 字数统计 |
| `analyze_directory` | 目录分析 | 批量统计 |
| `search_content` | 内容搜索 | 关键词搜索 |
| `list_tools` | 列出工具 | 查看所有可用工具 |

---

## 🆕 v3 新增工具 (+10)

| 工具 | 功能 | 输入 | 输出 |
|------|------|------|------|
| `file_analyzer` | 项目文件结构分析 | path | JSON 报告（文件数、行数、依赖图、质量评分） |
| `prompt_engineer` | AI 提示词优化 | original_prompt, target_outcome | 优化后提示词 + 评分对比 |
| `code_explainer` | 代码逻辑解释 | code, language | 自然语言解释 + 流程图描述 |
| `error_analyzer` | 错误堆栈分析 | error_trace, context | 可能原因 + 修复方案 |
| `batch_processor` | 批量文件处理 | pattern, operation | 处理结果报告 |
| `docs_generator` | 自动生成文档 | code_path | Markdown 文档 |
| `test_generator` | 测试用例生成 | code, test_type | pytest/unittest/jest 代码 |
| `refactoring_suggester` | 重构建议 | code_path | 重构建议报告 + 评分 |
| `dependency_checker` | 依赖安全检查 | requirements_path | 安全报告 + 漏洞列表 |
| `api_doc_builder` | API 文档构建 | routes_path | OpenAPI 3.0 spec |

### 工具详情

#### file_analyzer - 项目分析器
```json
{
  "path": "/your/project",
  "total_files": 42,
  "total_lines": 5000,
  "file_types": {".py": 20, ".md": 10, ".json": 5},
  "dependencies": ["flask", "requests", "numpy"],
  "quality_score": 78.5,
  "issues": ["3个函数超过50行"]
}
```

#### prompt_engineer - 提示词优化器
```json
{
  "original": "写一篇文章",
  "optimized": "你是一位专业内容创作者...\n目标：...\n请以结构化格式输出...",
  "score_before": 35.0,
  "score_after": 82.0,
  "improvements": ["添加了角色设定", "添加了输出格式要求"]
}
```

#### error_analyzer - 错误分析器
```json
{
  "error_type": "FileNotFoundError",
  "location": {"file": "app.py", "line": 42},
  "possible_causes": ["文件或目录不存在"],
  "suggestions": ["检查文件路径", "使用 os.path.exists() 先检查"],
  "severity": "medium"
}
```

#### dependency_checker - 依赖安全检查
```json
{
  "score": 65,
  "stats": {"total_packages": 15, "vulnerabilities_high": 3},
  "vulnerabilities": [{"package": "flask", "issue": "CVE-2023-30861"}],
  "recommendations": ["🔴 紧急: flask 存在已知漏洞，请升级"]
}
```

---

## 🔌 MCP 集成

支持接入主流 AI 编程助手：

```json
{
  "mcpServers": {
    "baibai": {
      "command": "python",
      "args": ["mcp_server_v2.py", "--port", "8000"],
      "env": {},
      "notes": "MCP 2026-07-28 无状态协议版本，v3 支持 22 个工具"
    }
  }
}
```

**支持环境**: Claude Code、Cursor、Codex、VS Code

---

## 📦 项目结构

```
baibai/
├── tools/                      # 核心工具包
│   ├── format_checker.py       # Markdown 格式校验
│   ├── classifier.py           # 内容分类
│   ├── md2html.py              # MD→HTML 转换
│   ├── readme_gen.py           # README 生成
│   ├── stats_analyzer.py       # 统计分析
│   ├── file_analyzer.py        # [v3] 项目分析器
│   ├── prompt_engineer.py      # [v3] 提示词优化
│   ├── code_explainer.py       # [v3] 代码解释器
│   ├── error_analyzer.py       # [v3] 错误分析器
│   ├── batch_processor.py      # [v3] 批量处理器
│   ├── docs_generator.py       # [v3] 文档生成器
│   ├── test_generator.py       # [v3] 测试生成器
│   ├── refactoring_suggester.py # [v3] 重构建议器
│   ├── dependency_checker.py   # [v3] 依赖检查器
│   ├── api_doc_builder.py      # [v3] API 文档构建器
│   └── cli.py                  # CLI 入口
├── tests/
│   ├── test_mcp.py             # MCP 基础测试
│   └── test_new_tools.py       # [v3] 新工具测试
├── mcp_server_v2.py            # MCP Server 主文件 (v3)
├── .mcp.json                   # MCP 配置
├── templates/                  # 页面模板
├── scripts/                    # 运维脚本
└── README.md
```

---

## 🎯 适用场景

- ✅ 短剧剧本批量格式校验
- ✅ 内容库数据统计与报告
- ✅ Markdown 批量转 HTML
- ✅ README 自动化维护
- ✅ AI 编程助手 MCP 扩展
- ✅ 项目代码质量分析
- ✅ 错误堆栈智能分析
- ✅ 自动化测试用例生成
- ✅ 依赖安全漏洞检测
- ✅ API 文档自动生成
- ✅ 代码重构建议
- ✅ 提示词质量优化

---

## 🧪 测试

```bash
# 运行所有测试
cd baibai
pytest tests/ -v

# 仅运行 v3 新工具测试
pytest tests/test_new_tools.py -v

# 运行覆盖率
pytest tests/ --cov=tools --cov-report=term-missing
```

---

## 📊 版本状态

| 指标 | 数值 |
|------|------|
| 最新版本 | v3.0.0 |
| Python 版本 | 3.8+ |
| 工具数量 | 22 个 (v2: 12 + v3: 10) |
| 测试覆盖 | 85%+ |
| 最后更新 | 2026-09-25 |
| 协议版本 | MCP 2026-07-28 |

---

## 🤝 贡献指南

欢迎 PR！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## ☕ 支持作者

如果这个项目对你有帮助，欢迎赞助 ☕

| 渠道 | 方式 |
|------|------|
| [面包多 Pay](https://mbd.com/@Zeon7744) | 支付宝 / 微信支付 |
| [GitHub Sponsors](https://github.com/sponsors/Zeon7744) | PayPal / Stripe |

---

<div align="center">

**由 [Zeon7744](https://github.com/Zeon7744) 维护**  
*Vibe Coding · 自然语言驱动开发*

</div>

---

## 🚀 免费开源 + 企业定制

baibai **永久免费开源**，全部 22 个工具 + MCP Server 均可免费使用。

- **免费**：`pip install baibai` 或克隆源码，全部功能免费。
- **企业定制**：按需报价 → [联系商务](https://mbd.net/@Zeon7744)。

> 详细定价见 [pricing.md](pricing.md)

---

## 快速上手
依赖安装：
```bash
python3 -m pip install -r requirements.txt
```

## 变现路径
工具库，**免费开源**，能力已并入 vibecoding-cli，本仓作资产底座，不独立售卖。企业定制联系商务。
> 定价：见 [pricing.md](pricing.md) | 赞助：[面包多 Pay @Zeon7744](https://mbd.net/@Zeon7744)

## 🧩 与 vibecoding-cli 的分工（工具仓 vs 护城河仓）
本仓定位"通用 CLI 工具集 + MCP 资产底座"，与 vibecoding-cli 严格分工、不互卷：

| 维度 | baibai（本仓·工具仓） | vibecoding-cli（护城河仓） |
| --- | --- | --- |
| 角色 | 单点工具能力层（文件/代码/终端/文档/短剧校验等原子工具 + MCP Server） | 任务编排 + 记忆 + 护城河（三层记忆、learning engine、任务闭环、Pro 付费门） |
| 差异化 | 可被任何 MCP 消费方（Cursor/Claude Code/Codex）直接挂载的"即插即用工具" | "越用越聪明"的自动学习与记忆沉淀，端到端任务闭环 |
| 变现 | 资产底座，不独立售卖 | Pro ¥29/月 + 咨询/企业授权 |

即：**baibai 提供"能调的工具"，vibecoding-cli 提供"会思考、能复用经验的智能体"。**


---

## ⚖️ 商用与合规

### 开源范围
- 代码（22 个工具 + MCP Server）以 MIT License 开放，可自由使用、修改与商用。
- 以下部分不属于开源范围：企业定制（定制工具开发、技术对接、SLA 支持）。

### 付费功能边界
- 赞赏（任意金额）：支持作者持续维护，功能不改变
- Pro（¥99/月）：vibecoding-cli 护城河仓 Pro 档订阅（本仓不独立售卖，能力已并入）
- 企业（¥999/月）：定制工具开发 + 私有部署 + SLA 保障

### 合规免责
- 本工具库包含文件读写、终端命令、代码分析等**高风险操作**，使用者应在受控环境执行并自行复核结果
- 文件操作类工具（file_ops/terminal 等）可能导致数据丢失或越权，后果由使用者自行承担
- 调用外部 LLM/MCP API 的费用与合规责任由使用者按对应服务商协议自行承担

---

## ⚖️ 法控声明（工具与代码）
- **代码不用于训练**：本仓代码与工具调用日志**不用于**任何大模型训练；`mcp_server_v2` 服务端不向第三方回流调用方代码/文件内容。
- **数据隐私**：工具仅处理调用方在本地/沙箱内提供的文件与代码，不落盘、不上报任何个人敏感信息；`--dangerously-skip-permissions` 模式下的越权风险由使用者自担。
- **合规免责**：文件读写/终端命令类工具属高风险操作，使用者应自行在受控环境执行并复核结果，因使用本仓工具产生的数据丢失/越权后果由使用者负责。


---

## 💰 订阅支持

**baibai 永久免费开源** 🎉 所有 22 个工具 + MCP Server 均可免费使用。

如果你觉得这个项目对你有帮助，欢迎通过面包多 Pay支持作者持续维护：

👉 **[面包多 Pay赞助](https://mbd.net/@Zeon7744)**（支付宝 / 微信支付）

需要企业定制工具？[联系商务](https://mbd.net/@Zeon7744) 按需报价。

> 详细定价见 [pricing.md](pricing.md)


---

## 💛 支持 & 发布（面包多 Pay双通道）

本仓通过**面包多 Pay**完成「**创作者赞赏/订阅收款**」与「**作品/内容社区发布**」双通道运营，二者共存：

| 通道 | 用途 | 入口 |
|------|------|------|
| 💰 面包多 Pay收款 | 赞赏、订阅、Pro 会员、赞助维护 | [面包多 Pay @Zeon7744](https://mbd.net/@Zeon7744) |
| 📣 面包多 Pay社区发布 | 作品展示、内容连载、粉丝互动、发布分发 | [面包多 Pay社区 @Zeon7744](https://mbd.com/user/0c59dda8a1bb11f19b9552540025c377) |

- **收款**：赞赏 / 订阅 Pro / 企业赞助，支付宝 + 微信支付，无需备案域名
- **社区发布**：把本仓产出（作品 / 剧本 / 工具演示 / 案例）在面包多 Pay社区连载发布，沉淀粉丝、引流回仓
- 两通道独立共存，按需选用；收款不强制绑定社区发布

> 本仓内容仅供创作参考，发布前请完成人工合规审查与平台备案。

---

## 🎯 定价理念：先体验，后付费

**以人为本，让使用者深度体验价值后再做决定：**

- **免费额度拉满**：所有仓库的免费版本提供足够深度的体验额度，不人为设限——把核心能力先跑起来，让你真正用到
- **深度体验再付费**：付费版解锁的是更高频次、更完整功能、更高级资源（模板/工具/分成），不是限制基础体验
- **你的反馈驱动迭代**：每一条回馈都是产品优化的第一手依据，我们据此持续完善

## 💬 用户回馈（驱动迭代）

**使用中发现任何问题、想法、建议 → 直接回馈，驱动下一版：**

| 方式 | 入口 | 说明 |
|------|------|------|
| 社区评论 | [面包多 Pay社区 @Zeon7744](https://mbd.com/user/0c59dda8a1bb11f19b9552540025c377) | 作品下评论/留言，直接驱动迭代 |
| Issue | 本仓 GitHub / Gitee / GitCode 的 Issues | Bug / 功能建议 / 定价反馈 |
| 赞赏反馈 | 面包多 Pay赞赏留言 | 支持的同时留下使用心得 |

> 每一条回馈都是产品优化的第一手依据。不强制，但真诚欢迎。
