# Baibai MCP Server

将 Vibe Coding 工具包装为 MCP 协议兼容服务，支持 AI 助手接入。

## 支持的 AI 助手

- Claude Code
- Cursor
- Codex
- 其他 MCP 兼容客户端

## 快速开始

### 1. 安装 MCP Server

```bash
pip install -e ".[mcp]"
```

### 2. 配置客户端

在 Claude Code、Cursor 等客户端的配置中添加：

```json
{
  "mcpServers": {
    "baibai": {
      "command": "python",
      "args": ["-m", "mcp_server"]
    }
  }
}
```

或使用 `.mcp.json` 文件：

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

## 可用工具

| 工具名 | 描述 | 参数 |
|--------|------|------|
| `check_format` | 校验 Markdown 文件格式 | filepath |
| `validate_directory` | 批量校验目录下所有文件 | directory |
| `classify_file` | 自动识别单个文件类型 | filepath |
| `classify_directory` | 批量分类目录下所有文件 | directory |
| `md_to_html` | Markdown 转 HTML | markdown_content |
| `convert_file` | 转换 Markdown 文件为 HTML | input_path, output_path |
| `gen_readme` | 自动生成 README 文档 | content_dir, readme_path |
| `extract_content_info` | 提取内容结构化信息 | filepath |
| `analyze_content_data` | 分析单文件统计数据 | filepath |
| `analyze_directory` | 分析目录统计数据 | directory |
| `search_content` | 搜索包含关键词的内容 | keyword, directory |
| `list_tools` | 列出所有可用工具 | - |

## 使用示例

### Claude Code

在 Claude Code 中，工具会自动列出并可供调用。

### 命令行测试

```bash
# 启动 MCP Server（会保持运行）
python mcp_server.py

# 或在另一个终端测试
python -c "from mcp_server import create_mcp_server; s = create_mcp_server(); print('Ready')"
```

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev,mcp]"

# 运行测试
pytest tests/test_mcp.py -v
```

## 架构

```
baibai/
├── mcp_server.py       # MCP Server 主入口
├── tools/              # 原有工具库
│   ├── format_checker.py
│   ├── classifier.py
│   ├── md2html.py
│   ├── readme_gen.py
│   └── stats_analyzer.py
├── tests/
│   └── test_mcp.py
├── .mcp.json          # MCP 配置示例
└── pyproject.toml     # 项目配置
```

## 注意事项

- MCP Server 需要 Python 3.8+ 和 mcp>=1.0.0
- 工具返回 JSON 格式结果
- 支持相对路径和绝对路径
