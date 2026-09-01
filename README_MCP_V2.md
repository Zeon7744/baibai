# Baibai MCP Server v2

MCP 2026-07-28 无状态协议实现

## 特性

1. **无状态模式** - 不需要 initialize 握手，每个请求独立处理
2. **MRTR 多轮次请求** - 支持 InputRequiredResult 用户确认场景
3. **HTTP Streamable 传输** - 标准 HTTP POST/GET 端点
4. **Header 路由** - 使用 Mcp-Method 和 Mcp-Name 头进行路由

## 启动

```bash
python mcp_server_v2.py --port 8000
```

## API

### Discover
```http
POST /mcp
Mcp-Method: server/discover
Mcp-Name: baibai-mcp
```

### Tools List
```http
POST /mcp
Mcp-Method: tools/list
Mcp-Name: baibai-mcp
```

### Tools Call
```http
POST /mcp
Mcp-Method: tools/call
Mcp-Name: baibai-mcp

{
  "name": "check_format",
  "arguments": {
    "filepath": "/path/to/file.md"
  }
}
```

## 工具列表

- `check_format` - Markdown格式校验
- `validate_directory` - 批量校验目录
- `classify_file` - 文件分类
- `md_to_html` - Markdown转HTML
- `gen_readme` - 生成README
- `analyze_content` - 内容分析
- `search_content` - 内容搜索
- `list_tools` - 列出工具
