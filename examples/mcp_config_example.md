# Baibai MCP Server 配置示例

## Claude Code 配置

在 `~/.claude/settings.json` 中添加：

```json
{
  "mcpServers": {
    "baibai": {
      "command": "python",
      "args": ["/path/to/baibai-workflow/mcp_server.py"]
    }
  }
}
```

或使用环境变量：

```bash
export BAIBAI_PATH="/path/to/baibai-workflow"
```

## Cursor 配置

在 `.cursor/mcp.json` 中添加：

```json
{
  "mcpServers": {
    "baibai": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "/path/to/baibai-workflow"
    }
  }
}
```

## Codex 配置

在 `~/.codex/config.toml` 中添加：

```toml
[mcp_servers.baibai]
command = "python"
args = ["mcp_server.py"]
cwd = "/path/to/baibai-workflow"
```

## 验证连接

```bash
# 测试 MCP Server 是否正常启动
python mcp_server.py &

# 检查进程
ps aux | grep mcp_server

# 停止服务
kill %1
```

## 工具调用示例

### 校验 Markdown 文件

```python
# 通过 MCP 工具调用
result = await client.call_tool("check_format", {
    "filepath": "path/to/your/file.md"
})
```

### 批量分类目录

```python
result = await client.call_tool("classify_directory", {
    "directory": "path/to/content/folder"
})
```

### 转换 Markdown 为 HTML

```python
result = await client.call_tool("md_to_html", {
    "markdown_content": "# 标题\n\n内容..."
})
```

## 故障排除

### 问题：MCP Server 无法启动

```bash
# 检查依赖
pip show mcp

# 重新安装
pip install -e ".[mcp]"
```

### 问题：工具调用失败

- 检查文件路径是否正确
- 确保文件存在且可读
- 查看服务器日志

### 问题：客户端连接超时

- 确认 MCP Server 正在运行
- 检查网络连接
- 验证配置文件路径
