# baibai 模块结构

## 目录
```
baibai/
├── mcp_server.py    # MCP Server（22 工具，FastMCP 或裸 JSON-RPC 降级）
├── http_server.py   # HTTP 服务
├── tools/           # 22 个工具实现（格式校验/目录/分类/MD→HTML 等）
├── billing.py       # 收款层：NoopGateway + MbdGateway + PAYWALL_RULES + check_access
└── docs/
```

## 数据流
1. 客户端 → MCP 协议 → `mcp_server.py` 接收 `tools/call`
2. 每次调用前走 `billing.check_access('free','tool_call')` 门控
3. 30 次/天超限 → 402 + 企业定制/赞赏链接（面包多 Pay https://mbd.com/@Zeon7744）

## 门控模型
- `PAYWALL_RULES`: free=30 次/天, enterprise=不限（定制报价）
