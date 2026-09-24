# Baibai MCP Server Matrix

独立模块化 MCP Server 矩阵，拆分为 4 个垂直领域 Server：

## Servers

| Server | 领域 | 工具数 |
|--------|------|--------|
| `mcp_finance` | 金融数据分析 | 3 |
| `mcp_drama` | AI 短剧创作 | 3 |
| `mcp_build` | 建筑检测知识 | 3 |
| `mcp_dev` | 通用开发工具 | 3 |

## 安装

```bash
pip install mcp
# 或
npm install -g @modelcontextprotocol/server-stdio
```

## 使用

```bash
# 查看所有服务器
python src/mcp_matrix.py list

# 启动指定 server
python src/mcp_matrix.py serve finance

# 启动所有 servers (unified mode)
python src/mcp_matrix.py serve all
```

## MCP Client 配置

```json
{
  "mcpServers": {
    "baibai-finance": {
      "command": "python",
      "args": ["src/mcp_matrix.py", "serve", "finance"]
    },
    "baibai-drama": {
      "command": "python",
      "args": ["src/mcp_matrix.py", "serve", "drama"]
    }
  }
}
```
