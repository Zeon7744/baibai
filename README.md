# Baibai - Vibe Coding 开发工具库

> 用自然语言驱动开发 — 通用 CLI 工具集 + MCP Server

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![CLI](https://img.shields.io/badge/CLI-Ready-brightgreen.svg)](https://github.com/Zeon7744/baibai)
[![MCP](https://img.shields.io/badge/MCP-Support-violet.svg)](https://modelcontextprotocol.io)

---

## 🚀 简介

**Baibai** 是一个 **Vibe Coding 开发工具库**，提供通用的命令行工具和自动化能力。

> ⚠️ 这是**通用工具库**。短剧专用工具（格式校验器、爽点分析器等）请在 [awesome-ai-short-drama](https://github.com/Zeon7744/awesome-ai-short-drama) 查看。

核心定位：
- **通用工具库** — 格式校验、数据分析、文档生成
- **CLI 优先** — 简洁的命令行界面，适合开发者
- **MCP 支持** — 兼容 Model Context Protocol，可集成到 AI 助手
- **BYOK 模式** — 自带 API Key，工具免费使用

---

## 📦 安装

### 从源码安装（推荐）

```bash
git clone https://github.com/Zeon7744/baibai.git
cd baibai
pip install -e .
```

### 直接运行

```bash
# 无需安装，直接运行
python tools/cli.py --help
```

### 依赖

- Python 3.8+
- typer (CLI 框架)
- rich (终端美化)

---

## 🛠️ 工具集

### 1. 格式校验器 (`check-format`)

检查 Markdown 文件是否符合规范：
- 禁止字符检测
- 括号格式检查（【】）
- 标题结构验证
- 生成评分报告

```bash
baibai check-format <目录路径>
baibai check-format --json <目录>
```

### 2. 数据分析 (`analyze`)

统计分析内容库数据：
- 总字数、章节数统计
- 类型分布分析
- 排行榜生成
- JSON 报告导出

```bash
baibai analyze <目录路径>
```

### 3. README 生成器 (`gen-readme`)

根据内容库自动生成 README 文档：
- 自动提取文件信息
- 生成分类表格
- 更新现有 README

```bash
baibai gen-readme <README路径> <内容目录>
baibai gen-readme -p README.md <内容目录>  # 仅预览
```

### 4. Markdown 转 HTML (`md2html`)

将 Markdown 文件转换为美观的 HTML 页面：
- 支持标题、列表、代码块、表格
- 自动生成完整 HTML 页面
- 响应式设计

```bash
baibai md2html <输入文件> [输出文件]
```

### 5. 内容分类器 (`classify`)

自动识别和分类内容类型：
- 短剧剧本、短篇小说、教程文档
- 工具脚本、配置文件等
- 生成分类报告

```bash
baibai classify <目录路径>
```

---

## 📊 使用示例

### 示例 1：校验内容格式

```bash
cd baibai
python tools/check_format.py ../awesome-ai-short-drama/short-dramas
```

### 示例 2：分析内容库数据

```bash
python tools/stats_analyzer.py ../awesome-ai-short-drama/short-dramas
```

### 示例 3：转换 Markdown 为 HTML

```bash
python tools/md2html.py README.md
# 生成 README.html
```

---

## 🏗️ 项目结构

```
baibai/
├── tools/                  # 核心工具包
│   ├── __init__.py        # 包定义
│   ├── cli.py             # CLI 入口（基础版）
│   ├── cli_enhanced.py    # CLI 增强版（Typer + Rich）
│   ├── format_checker.py  # 格式校验器
│   ├── stats_analyzer.py  # 数据分析
│   ├── readme_gen.py      # README 生成器
│   ├── md2html.py         # Markdown 转 HTML
│   └── classifier.py      # 内容分类器
├── templates/              # 页面模板
│   ├── index.html         # 主展示页
│   └── drama.html         # 短剧详情页模板
├── examples/               # 示例项目
├── tests/                  # 测试套件
├── data/                   # 数据缓存
├── scripts/                # 辅助脚本
│   ├── release.py         # 版本发布脚本
│   └── publish.py         # PyPI/GitHub 发布
├── docs/                   # 文档
├── releases/               # 发布版本
├── example-project/        # 示例项目
├── pyproject.toml          # 项目配置
├── setup.py                # 安装脚本
├── VERSION.md              # 版本信息
├── CHANGELOG.md            # 变更日志
└── README.md               # 本文件
```

---

## 🔌 MCP 集成

Baibai 支持 Model Context Protocol (MCP)，可以集成到各种 AI 助手：

### 暴露的工具

| 工具名 | 功能 |
|--------|------|
| `baibai_format_check` | 格式校验 |
| `baibai_analyze_stats` | 数据分析 |
| `baibai_generate_readme` | README 生成 |
| `baibai_md2html` | Markdown 转 HTML |
| `baibai_classify` | 内容分类 |

### 配置 Claude Code

```json
{
  "mcpServers": {
    "baibai": {
      "command": "python",
      "args": ["-m", "tools.cli", "mcp", "serve"]
    }
  }
}
```

### 配置 Cursor

在 `.cursor/mcp.json` 中添加：

```json
{
  "mcpServers": {
    "baibai": {
      "command": "python",
      "args": ["tools/cli.py", "mcp", "serve"]
    }
  }
}
```

---

## 🚀 发布项目

Baibai 也是**项目发布地**，你可以在这里发布：

### 发布类型

| 类型 | 说明 | 位置 |
|------|------|------|
| 完整项目 | 可运行的应用/工具 | `projects/` |
| 工具脚本 | 单文件工具 | `tools/` |
| 示例代码 | 学习演示 | `examples/` |
| 试用版本 | Beta/RC 版本 | `releases/` |

---

## 🎯 扩展开发

### 添加新工具

1. 在 `tools/` 目录下创建新模块
2. 在 `cli_enhanced.py` 中注册命令
3. 在 `MCP_TOOLS` 中注册 MCP 工具

---

## 📄 许可证

MIT License - 见 [LICENSE](LICENSE) 文件

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📚 相关项目

- [dev-artifacts](https://github.com/Zeon7744/dev-artifacts) - MLP精准金融分析工具
- [awesome-ai-short-drama](https://github.com/Zeon7744/awesome-ai-short-drama) - AI 短剧创作全链路（作品 + 工具 + 资源）
- [Model Context Protocol](https://modelcontextprotocol.io) - MCP 协议规范
- [opencode](https://github.com/opencode-ai/opencode) - 开源 AI 编码助手
- [Aider](https://github.com/Aider-AI/aider) - 终端 AI 编程助手

---

*由 [Zeon7744](https://github.com/Zeon7744) 维护*  
*Vibe Coding · 自然语言驱动开发*

## 🎬 短剧项目

暂无短剧项目


---

## 🎬 短剧项目

暂无短剧项目


---

## 🎬 短剧项目

暂无短剧项目


---

## 🎬 短剧项目

暂无短剧项目


---

## 🎬 短剧项目

暂无短剧项目


---

## 🎬 短剧项目

暂无短剧项目


---

## 🎬 短剧项目

暂无短剧项目


---

## 🎬 短剧项目

暂无短剧项目


---

## 🙏 感谢赞助

暂无赞助者

---
