# Baibai - Vibe Coding 开发工具库

> 用自然语言驱动开发 — 通用 CLI 工具集

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![CLI](https://img.shields.io/badge/CLI-Ready-brightgreen.svg)](https://github.com/Zeon7744/baibai)
[![MCP](https://img.shields.io/badge/MCP-Support-violet.svg)](https://modelcontextprotocol.io)

---

## 🚀 简介

**Baibai** 是一个 **Vibe Coding 开发工具库**，提供通用的命令行工具和自动化能力。

核心定位：
- **通用工具库** — 格式校验、数据分析、文档生成
- **CLI 优先** — 简洁的命令行界面，适合开发者
- **MCP 支持** — 兼容 Model Context Protocol，可集成到 AI 助手
- **BYOK 模式** — 自带 API Key，工具免费使用

### 第一个应用场景：短剧创作

Baibai 的第一个成功场景是短剧创作工具链，但这不是唯一场景。工具设计为通用可扩展架构。

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

### 1. 格式校验器 (`format check`)

检查 Markdown 文件是否符合规范：
- 禁止字符检测（如：耀、曜）
- 括号格式检查（【】）
- 标题结构验证
- 生成评分报告

```bash
# 基本用法
baibai format check <目录路径>

# 示例
baibai format check ../awesome-ai-short-drama/short-dramas
```

### 2. 数据分析 (`stats analyze`)

统计分析内容库数据：
- 总字数、章节数统计
- 类型分布分析
- 排行榜生成
- JSON 报告导出

```bash
# 基本用法
baibai stats analyze <目录路径>

# 示例
baibai stats analyze ../awesome-ai-short-drama/short-dramas
```

### 3. README 生成器 (`readme generate`)

根据内容库自动生成 README 文档：
- 自动提取文件信息
- 生成分类表格
- 更新现有 README

```bash
# 基本用法
baibai readme generate <README路径> <内容目录>

# 示例
baibai readme generate README.md ../awesome-ai-short-drama/short-dramas
```

### 4. MCP 服务器 (`mcp serve`)

启动 MCP 服务器，将 baibai 工具暴露给 AI 助手：

```bash
baibai mcp serve
```

暴露的工具：
- `baibai_format_check` — 格式校验
- `baibai_analyze_stats` — 数据分析
- `baibai_generate_readme` — README 生成

---

## 📊 使用示例

### 示例 1：校验短剧剧本格式

```bash
# 进入 baibai 目录
cd baibai

# 校验短剧库
python tools/format_checker.py ../awesome-ai-short-drama/short-dramas
```

输出示例：
```
============================================================
📋 格式校验报告
============================================================

📊 统计: 共 8 个文件 | ✅通过 6 | ⚠️警告 2 | ❌失败 0
------------------------------------------------------------

✅ 剑魂重生
   得分: 95/100 | 内容: 30项, 45000字符
   
✅ 帝师无双
   得分: 85/100 | 内容: 10项, 42000字符
...
```

### 示例 2：分析内容库数据

```bash
python tools/stats_analyzer.py ../awesome-ai-short-drama/short-dramas
```

输出示例：
```
============================================================
📊 内容数据分析报告
============================================================

📈 总体统计
  内容数量: 8 个
  总字数: 6万字
  总章节: 120 章
  
📂 类型分布
  短剧剧本: ████████ (8)
...
```

### 示例 3：生成 README

```bash
python tools/readme_gen.py README.md ../awesome-ai-short-drama/short-dramas
```

---

## 🏗️ 项目结构

```
baibai/
├── tools/                  # 工具库
│   ├── __init__.py        # 包定义
│   ├── cli.py             # CLI 入口
│   ├── format_checker.py  # 格式校验器
│   ├── stats_analyzer.py  # 数据分析
│   └── readme_gen.py      # README 生成器
├── templates/              # 页面模板
│   ├── index.html         # 主展示页
│   └── drama.html         # 短剧详情页模板
├── examples/               # 示例项目
├── data/                   # 数据缓存
│   └── stats/             # 统计数据
├── scripts/                # 遗留脚本（兼容）
├── docs/                   # 文档
├── pyproject.toml          # 项目配置
└── README.md               # 本文件
```

---

## 🔌 MCP 集成

Baibai 支持 Model Context Protocol (MCP)，可以集成到各种 AI 助手：

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

## 🎯 扩展开发

### 添加新工具

1. 在 `tools/` 目录下创建新模块
2. 在 `cli.py` 中注册命令
3. 在 `MCP_TOOLS` 中注册 MCP 工具

示例：

```python
# tools/new_tool.py
def new_feature(directory: str) -> dict:
    # 实现功能
    return {"status": "ok"}

# cli.py 中注册
@app.command()
def new_command(directory: str = Option(...)):
    result = new_feature(directory)
    print(result)
```

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

- [awesome-ai-short-drama](https://github.com/Zeon7744/awesome-ai-short-drama) - AI 短剧资源库
- [Model Context Protocol](https://modelcontextprotocol.io) - MCP 协议规范

---

*由 [Zeon7744](https://github.com/Zeon7744) 维护*  
*Vibe Coding · 自然语言驱动开发*

## 🎬 短剧项目

暂无短剧项目


---

## 🙏 感谢赞助

暂无赞助者

---
