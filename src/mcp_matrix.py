#!/usr/bin/env python3
"""
baibai MCP Servers - 独立模块化 MCP Server 矩阵

拆分为以下独立 Server：
  1. mcp_finance.py   - 金融数据与分析工具
  2. mcp_drama.py     - AI短剧创作工具
  3. mcp_build.py     - 建筑检测知识库
  4. mcp_dev.py       - 通用开发工具
  5. server.py        - 统一入口，支持 --serve <module>

每个 Server 独立可发布为 npm 包。
"""

import json
import sys
from pathlib import Path
from typing import Any

# MCP SDK 兼容层 (支持 stdio 模式)
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

# ── 金融数据 MCP Server ──────────────────────────────────────
class FinanceMCPServer:
    """金融数据分析 MCP Server"""
    
    NAME = "baibai-finance"
    
    TOOLS = [
        {
            "name": "analyze_stock",
            "description": "分析股票/加密货币技术面与基本面指标",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "股票代码或加密货币符号"},
                    "interval": {"type": "string", "enum": ["1m","5m","15m","1h","4h","1d"], "default": "1d"},
                    "indicators": {"type": "array", "items": {"type": "string"}, "default": ["RSI","MACD","Bollinger"]}
                },
                "required": ["symbol"]
            }
        },
        {
            "name": "mlp_predict",
            "description": "使用 MLP 模型预测价格走势，返回置信区间",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "horizon": {"type": "integer", "default": 24, "description": "预测小时数"},
                    "confidence": {"type": "number", "default": 0.95}
                },
                "required": ["symbol"]
            }
        },
        {
            "name": "get_market_sentiment",
            "description": "获取市场情绪分析（恐惧贪婪指数、社交媒体趋势）",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "asset": {"type": "string", "default": "crypto"},
                    "source": {"type": "string", "enum": ["twitter","reddit","news"], "default": "twitter"}
                }
            }
        }
    ]
    
    async def handle_tool(self, name: str, args: dict) -> dict:
        return {"result": f"[Finance MCP] {name}({args})", "tools": len(self.TOOLS)}


# ── 短剧创作 MCP Server ──────────────────────────────────────
class DramaMCPServer:
    """AI 短剧创作 MCP Server"""
    
    NAME = "baibai-drama"
    
    TOOLS = [
        {
            "name": "generate_script",
            "description": "根据主题生成短剧剧本，支持竖屏格式适配",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "theme": {"type": "string", "description": "故事主题"},
                    "episode_count": {"type": "integer", "default": 10},
                    "platform": {"type": "string", "enum": ["douyin","kuaishou","tiktok"], "default": "douyin"},
                    "style": {"type": "string", "default": "反转爽剧"}
                },
                "required": ["theme"]
            }
        },
        {
            "name": "convert_to_short_video",
            "description": "将剧本转换为分镜脚本，适配 9:16 竖屏",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "script": {"type": "string"},
                    "duration_per_scene": {"type": "integer", "default": 15}
                },
                "required": ["script"]
            }
        },
        {
            "name": "check_compliance",
            "description": "检查剧本是否符合抖音/快手审核规则",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "platform": {"type": "string", "enum": ["douyin","kuaishou"]}
                },
                "required": ["content"]
            }
        }
    ]
    
    async def handle_tool(self, name: str, args: dict) -> dict:
        return {"result": f"[Drama MCP] {name}({args})", "tools": len(self.TOOLS)}


# ── 建筑检测 MCP Server ──────────────────────────────────────
class BuildMCPServer:
    """建筑行业检测 AI MCP Server"""
    
    NAME = "baibai-build"
    
    TOOLS = [
        {
            "name": "analyze_report",
            "description": "分析建筑检测报告，提取关键指标与建议",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "report_text": {"type": "string", "description": "检测报告文本或 PDF 路径"},
                    "report_type": {"type": "string", "enum": ["结构检测","材料检测","地基检测"], "default": "结构检测"}
                },
                "required": ["report_text"]
            }
        },
        {
            "name": "query_standard",
            "description": "查询建筑规范标准（GB/JGJ），返回条款内容",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string"},
                    "standard_type": {"type": "string", "enum": ["GB","JGJ","DB"], "default": "GB"}
                },
                "required": ["keyword"]
            }
        },
        {
            "name": "generate_checklist",
            "description": "根据项目类型生成检测项目清单",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "project_type": {"type": "string", "enum": ["住宅","商业","工业","桥梁","道路"]},
                    "region": {"type": "string", "description": "所在地区（影响地方标准）"}
                },
                "required": ["project_type"]
            }
        }
    ]
    
    async def handle_tool(self, name: str, args: dict) -> dict:
        return {"result": f"[Build MCP] {name}({args})", "tools": len(self.TOOLS)}


# ── 通用开发工具 MCP Server ────────────────────────────────
class DevMCPServer:
    """通用开发工具 MCP Server"""
    
    NAME = "baibai-dev"
    
    TOOLS = [
        {
            "name": "format_code",
            "description": "格式化代码，支持 Python/JS/TS/JSON/YAML",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "language": {"type": "string", "enum": ["python","javascript","typescript","json","yaml"]}
                },
                "required": ["code", "language"]
            }
        },
        {
            "name": "analyze_project",
            "description": "分析项目结构，生成 README 和技术文档",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "output_format": {"type": "string", "enum": ["markdown","html","json"], "default": "markdown"}
                },
                "required": ["path"]
            }
        },
        {
            "name": "generate_test",
            "description": "根据源码自动生成单元测试",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "test_framework": {"type": "string", "enum": ["pytest","unittest","jest"], "default": "pytest"}
                },
                "required": ["file_path"]
            }
        }
    ]
    
    async def handle_tool(self, name: str, args: dict) -> dict:
        return {"result": f"[Dev MCP] {name}({args})", "tools": len(self.TOOLS)}


# ── Server Registry ──────────────────────────────────────────
SERVERS = {
    "finance": FinanceMCPServer,
    "drama": DramaMCPServer,
    "build": BuildMCPServer,
    "dev": DevMCPServer,
    "all": None,  # 统一模式，注册所有 tools
}


def list_servers():
    print("\n=== Baibai MCP Server Matrix ===\n")
    for name, cls in SERVERS.items():
        if cls:
            print(f"  [{name}] {cls.NAME}")
            for tool in cls.TOOLS:
                print(f"    - {tool['name']}: {tool['description'][:50]}")
        else:
            print(f"  [*] all (unified mode)")
    print()


def get_all_tools():
    """Unified mode: combine all tools"""
    tools = []
    for name, cls in SERVERS.items():
        if cls and name != "all":
            for t in cls.TOOLS:
                t["_server"] = name
                tools.append(t)
    return tools


def run_stdio(server_name: str = "all"):
    """Run MCP server in stdio mode"""
    if not MCP_AVAILABLE:
        print("WARNING: mcp package not installed. Running in legacy mode.")
        print("Install: pip install mcp")
        # Fallback to simple JSON-RPC over stdin/stdout
        import json as _json
        tools = get_all_tools() if server_name == "all" else SERVERS[server_name].TOOLS
        response = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "tools": tools,
                "server": f"baibai-{server_name}" if server_name != "all" else "baibai-all",
                "version": "1.0.0"
            }
        }
        print(_json.dumps(response))
        return
    
    # Full MCP server
    app = Server(f"baibai-{server_name}")
    
    @app.list_tools()
    async def list_tools():
        if server_name == "all":
            tools = get_all_tools()
        else:
            tools = SERVERS[server_name].TOOLS
        return [Tool(**t) for t in tools]
    
    @app.call_tool()
    async def call_tool(name: str, args: dict):
        # Route to appropriate server
        parts = name.split("_", 1)
        prefix = parts[0]
        actual_name = parts[1] if len(parts) > 1 else name
        server_cls = next((v for k, v in SERVERS.items() if k in prefix), None)
        if server_cls:
            return [TextContent(type="text", text=json.dumps(await server_cls().handle_tool(actual_name, args), ensure_ascii=False))]
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    await app.run_stdio()


if __name__ == "__main__":
    import asyncio
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "list":
            list_servers()
        elif cmd == "serve":
            module = sys.argv[2] if len(sys.argv) > 2 else "all"
            asyncio.run(run_stdio(module))
        else:
            print(f"Unknown command: {cmd}")
            print("Usage: python server.py [list|serve <module>]")
    else:
        list_servers()
