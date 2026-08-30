# Baibai v{version}

## 新增功能

- MCP Server 支持，可直接接入 Claude Code、Cursor、Codex
- 12 个 MCP 工具，覆盖格式校验、内容分析、文档生成

## 安装

```bash
pip install -e ".[mcp]"
```

## 快速开始

### 1. 配置 AI 助手

在 Claude Code、Cursor 等客户端添加：

```json
{
  "mcpServers": {
    "baibai": {
      "command": "python",
      "args": ["mcp_server.py"]
    }
  }
}
```

### 2. 使用工具

```bash
# 命令行使用
baibai check-format path/to/file.md
baibai analyze path/to/dir
baibai gen-readme path/to/content

# MCP 工具调用（在 AI 助手中自动可用）
check_format(filepath="...")
classify_directory(directory="...")
md_to_html(markdown_content="...")
```

## 特性

- **格式校验**: 自动检查 Markdown 格式规范
- **内容分析**: 统计字数、章节、爽点密度
- **自动分类**: 识别剧本/小说/教程等类型
- **文档生成**: 自动生成 README
- **MCP 集成**: 支持主流 AI 助手接入

## 链接

- GitHub: https://github.com/Zeon7744/baibai
- 文档: https://github.com/Zeon7744/baibai/blob/main/README_MCP.md
