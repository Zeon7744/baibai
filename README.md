# 🚀 Baibai — Vibe Coding 开发工具库 v3

> **用自然语言驱动开发** — 通用 CLI 工具集 + MCP Server  
> AI 编程助手必备工具箱，让 Claude Code、Cursor、Codex 更强大

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
| [爱发电](https://afdian.com/@Zeon7744) | 支付宝 / 微信支付 |
| [GitHub Sponsors](https://github.com/sponsors/Zeon7744) | PayPal / Stripe |

---

<div align="center">

**由 [Zeon7744](https://github.com/Zeon7744) 维护**  
*Vibe Coding · 自然语言驱动开发*

</div>
