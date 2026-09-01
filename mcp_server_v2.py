#!/usr/bin/env python3
"""
Baibai MCP Server v2 - MCP 2026-07-28 无状态协议实现

核心特性:
1. 无状态模式 - 不需要 initialize 握手，每个请求独立处理
2. MRTR 多轮次请求 - 支持 InputRequiredResult 用户确认场景
3. HTTP Streamable 传输 - 标准 HTTP POST/GET 端点
4. Header 路由 - 使用 Mcp-Method 和 Mcp-Name 头进行路由

支持的协议版本: 2026-07-28
"""

import json
import sys
import uuid
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time

# 导入 baibai 工具
sys.path.insert(0, str(Path(__file__).parent))
try:
    from tools.format_checker import check_markdown_file, scan_files, validate_directory
    from tools.classifier import classify_content, scan_and_classify
    from tools.md2html import markdown_to_html, process_file
    from tools.readme_gen import extract_info, generate_content_section, update_readme
    from tools.stats_analyzer import analyze_content, scan_and_analyze, generate_stats
    TOOLS_AVAILABLE = True
except ImportError as e:
    TOOLS_AVAILABLE = False
    print(f"警告: 工具导入失败: {e}")

# MCP 2026 协议常量
MCP_PROTOCOL_VERSION = "2026-07-28"
MCP_CONTENT_TYPE_JSON = "application/json"
MCP_CONTENT_TYPE_EVENT_STREAM = "text/event-stream"
MCP_HEADER_METHOD = "Mcp-Method"
MCP_HEADER_NAME = "Mcp-Name"
MCP_HEADER_VERSION = "Mcp-Protocol-Version"
MCP_HEADER_SESSION_ID = "Mcp-Session-Id"

# 支持的 RPC 方法
SUPPORTED_METHODS = {
    "server/discover": "能力发现（替代 initialize）",
    "tools/list": "列出可用工具",
    "tools/call": "调用工具",
    "resources/list": "列出资源（预留）",
    "prompts/list": "列出提示模板（预留）",
}

# 工具定义（与 baibai 工具对应）
TOOLS_REGISTRY = {
    "check_format": {
        "name": "check_format",
        "description": "校验 Markdown 文件格式，检查标题、禁止字符、括号等",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "要校验的 Markdown 文件路径"}
            },
            "required": ["filepath"]
        }
    },
    "validate_directory": {
        "name": "validate_directory",
        "description": "批量校验目录下所有 Markdown 文件",
        "inputSchema": {
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "目录路径"}
            },
            "required": ["directory"]
        }
    },
    "classify_file": {
        "name": "classify_file",
        "description": "自动识别和分类单个文件的内容类型",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "要分类的文件路径"}
            },
            "required": ["filepath"]
        }
    },
    "classify_directory": {
        "name": "classify_directory",
        "description": "批量分类目录下所有文件",
        "inputSchema": {
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "目录路径"}
            },
            "required": ["directory"]
        }
    },
    "md_to_html": {
        "name": "md_to_html",
        "description": "将 Markdown 内容转换为 HTML",
        "inputSchema": {
            "type": "object",
            "properties": {
                "markdown_content": {"type": "string", "description": "Markdown 文本内容"}
            },
            "required": ["markdown_content"]
        }
    },
    "convert_file": {
        "name": "convert_file",
        "description": "转换 Markdown 文件为 HTML",
        "inputSchema": {
            "type": "object",
            "properties": {
                "input_path": {"type": "string", "description": "输入文件路径"},
                "output_path": {"type": "string", "description": "输出文件路径（可选）"}
            },
            "required": ["input_path"]
        }
    },
    "gen_readme": {
        "name": "gen_readme",
        "description": "根据内容库自动生成 README 文档",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content_dir": {"type": "string", "description": "内容目录路径"},
                "readme_path": {"type": "string", "description": "README 文件路径"}
            },
            "required": ["content_dir"]
        }
    },
    "extract_content_info": {
        "name": "extract_content_info",
        "description": "从内容文件提取结构化信息",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "文件路径"}
            },
            "required": ["filepath"]
        }
    },
    "analyze_content_data": {
        "name": "analyze_content_data",
        "description": "分析单个内容文件的统计数据",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "文件路径"}
            },
            "required": ["filepath"]
        }
    },
    "analyze_directory": {
        "name": "analyze_directory",
        "description": "分析目录下所有内容文件，生成统计数据",
        "inputSchema": {
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "目录路径"}
            },
            "required": ["directory"]
        }
    },
    "search_content": {
        "name": "search_content",
        "description": "在目录下搜索包含关键词的内容",
        "inputSchema": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string", "description": "搜索关键词"},
                "directory": {"type": "string", "description": "搜索目录"}
            },
            "required": ["keyword"]
        }
    },
    "list_tools": {
        "name": "list_tools",
        "description": "列出所有可用的 baibai 工具",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
}

# MRTR 状态存储（用于处理需要用户确认的多轮请求）
mrtr_state = {}


def create_json_rpc_response(request_id: Any, result: Any = None, error: Dict = None) -> Dict:
    """创建 JSON-RPC 2.0 响应"""
    response = {
        "jsonrpc": "2.0",
        "id": request_id,
    }
    if error:
        response["error"] = error
    else:
        response["result"] = result
    return response


def create_notification(method: str, params: Dict = None) -> Dict:
    """创建 JSON-RPC 通知（无 id）"""
    notification = {
        "jsonrpc": "2.0",
        "method": method,
    }
    if params:
        notification["params"] = params
    return notification


class McpRequestHandler(BaseHTTPRequestHandler):
    """MCP HTTP 请求处理器 - 无状态实现"""
    
    # 服务器信息
    server_name = "baibai-mcp-server"
    server_version = "1.0.0"
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.log_date_time_string()}] {format % args}")
    
    def send_json_response(self, status_code: int, data: Dict, extra_headers: Dict = None):
        """发送 JSON 响应"""
        self.send_response(status_code)
        self.send_header("Content-Type", MCP_CONTENT_TYPE_JSON)
        self.send_header("Access-Control-Allow-Origin", "*")
        if extra_headers:
            for key, value in extra_headers.items():
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def send_event_stream_response(self):
        """发送 SSE 流响应头"""
        self.send_response(200)
        self.send_header("Content-Type", MCP_CONTENT_TYPE_EVENT_STREAM)
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
    
    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", f"{MCP_HEADER_METHOD}, {MCP_HEADER_NAME}, {MCP_HEADER_VERSION}, Content-Type")
        self.end_headers()
    
    def do_GET(self):
        """处理 GET 请求 - 用于 SSE 监听端点"""
        parsed = urlparse(self.path)
        
        # 健康检查
        if parsed.path == "/health":
            self.send_json_response(200, {
                "status": "healthy",
                "server": self.server_name,
                "version": self.server_version,
                "protocol": MCP_PROTOCOL_VERSION,
                "features": ["stateless", "mrtr", "streamable-http"]
            })
            return
        
        # MCP 端点 - 返回 405 表示不支持 SSE 流（无状态模式）
        if parsed.path == "/mcp":
            self.send_response(405)
            self.send_header("Allow", "POST")
            self.send_header("Content-Type", MCP_CONTENT_TYPE_JSON)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32000,
                    "message": "Stateless mode: GET not supported for /mcp endpoint. Use POST instead."
                }
            }).encode('utf-8'))
            return
        
        # 默认返回 404
        self.send_json_response(404, {
            "error": "Not found",
            "path": parsed.path
        })
    
    def do_POST(self):
        """处理 POST 请求 - 主要 MCP 请求处理"""
        parsed = urlparse(self.path)
        
        if parsed.path != "/mcp":
            self.send_json_response(404, {"error": "Not found"})
            return
        
        # 读取请求体
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self.send_json_response(400, {
                "jsonrpc": "2.0",
                "error": {"code": -32700, "message": "Invalid Request: empty body"}
            })
            return
        
        try:
            body = self.rfile.read(content_length)
            request_data = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError as e:
            self.send_json_response(400, {
                "jsonrpc": "2.0",
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            })
            return
        
        # 解析请求头
        method = self.headers.get(MCP_HEADER_METHOD) or request_data.get("method")
        tool_name = self.headers.get(MCP_HEADER_NAME) or request_data.get("params", {}).get("name") if request_data.get("params") else None
        client_version = self.headers.get(MCP_HEADER_VERSION, MCP_PROTOCOL_VERSION)
        request_id = request_data.get("id")
        
        # 验证协议版本
        if request_data.get("params", {}).get("_meta", {}).get("protocolVersion"):
            client_version = request_data["params"]["_meta"]["protocolVersion"]
        
        # 路由处理
        if method == "server/discover":
            result = self.handle_discover(request_data, client_version)
        elif method == "tools/list":
            result = self.handle_tools_list(request_data)
        elif method == "tools/call":
            result = self.handle_tools_call(request_data, tool_name)
        elif method == "notifications/initialized":
            # 客户端通知（无状态模式下可忽略）
            result = create_json_rpc_response(request_id, {})
        else:
            result = create_json_rpc_response(request_id, error={
                "code": -32601,
                "message": f"Method not found: {method}"
            })
        
        # 添加 _meta 信息
        if result.get("result"):
            result["result"]["_meta"] = {
                "serverInfo": {
                    "name": self.server_name,
                    "version": self.server_version
                },
                "protocolVersion": MCP_PROTOCOL_VERSION
            }
        
        # 发送响应
        self.send_json_response(200, result)
    
    def handle_discover(self, request: Dict, client_version: str) -> Dict:
        """处理 server/discover 请求 - 替代旧的 initialize"""
        request_id = request.get("id")
        
        # 检查客户端版本兼容性
        supported_versions = [MCP_PROTOCOL_VERSION, "2025-11-25"]
        if client_version not in supported_versions:
            return create_json_rpc_response(request_id, error={
                "code": -32606,
                "message": f"Unsupported protocol version: {client_version}. Supported: {', '.join(supported_versions)}"
            })
        
        # 返回服务器能力
        return create_json_rpc_response(request_id, {
            "protocolVersion": MCP_PROTOCOL_VERSION,
            "capabilities": {
                "tools": {
                    "listChanged": True
                },
                "logging": {},
                "elicitation": {}  # 支持 MRTR  elicitation
            },
            "serverInfo": {
                "name": self.server_name,
                "version": self.server_version
            },
            "instructions": "这是一个无状态 MCP 服务器，支持 MRTR 多轮次请求。每次请求都是独立的。"
        })
    
    def handle_tools_list(self, request: Dict) -> Dict:
        """处理 tools/list 请求"""
        request_id = request.get("id")
        
        return create_json_rpc_response(request_id, {
            "tools": list(TOOLS_REGISTRY.values())
        })
    
    def handle_tools_call(self, request: Dict, tool_name: Optional[str] = None) -> Dict:
        """处理 tools/call 请求 - 支持 MRTR"""
        request_id = request.get("id")
        params = request.get("params", {})
        
        # 确定工具名称
        target_tool = tool_name or params.get("name")
        arguments = params.get("arguments", {})
        progress_token = params.get("_meta", {}).get("progressToken")
        
        if not target_tool:
            return create_json_rpc_response(request_id, error={
                "code": -32602,
                "message": "Missing required parameter: name"
            })
        
        if target_tool not in TOOLS_REGISTRY:
            return create_json_rpc_response(request_id, error={
                "code": -32601,
                "message": f"Tool not found: {target_tool}"
            })
        
        # 检查是否需要用户确认（MRTR）
        if self._needs_confirmation(target_tool, arguments):
            # 返回 InputRequiredResult
            return create_json_rpc_response(request_id, {
                "content": [{
                    "type": "text",
                    "text": f"工具 '{target_tool}' 需要您的确认才能执行。"
                }],
                "isError": False,
                "_meta": {
                    "inputRequired": {
                        "requestId": str(uuid.uuid4()),
                        "message": f"确认是否执行 {target_tool}？",
                        "fields": self._get_confirmation_fields(target_tool),
                        "expiresAt": int(time.time()) + 300  # 5分钟过期
                    }
                }
            })
        
        # 执行工具
        try:
            result_text = self._execute_tool(target_tool, arguments)
            return create_json_rpc_response(request_id, {
                "content": [{
                    "type": "text",
                    "text": result_text
                }],
                "isError": False
            })
        except Exception as e:
            return create_json_rpc_response(request_id, error={
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            })
    
    def _needs_confirmation(self, tool_name: str, arguments: Dict) -> bool:
        """检查工具是否需要用户确认"""
        # 定义需要确认的工具
        require_confirm = {
            "gen_readme": "生成 README 将覆盖现有文件",
            "convert_file": "转换文件将创建新文件",
            "validate_directory": "批量校验将处理目录下所有文件"
        }
        return tool_name in require_confirm
    
    def _get_confirmation_fields(self, tool_name: str) -> List[Dict]:
        """获取确认字段"""
        return [
            {
                "name": "confirm",
                "type": "boolean",
                "description": "确认执行此操作",
                "required": True
            },
            {
                "name": "reason",
                "type": "string",
                "description": "执行原因（可选）"
            }
        ]
    
    def _execute_tool(self, tool_name: str, arguments: Dict) -> str:
        """执行工具函数"""
        if not TOOLS_AVAILABLE:
            raise ImportError("工具模块未导入")
        
        if tool_name == "check_format":
            result = check_markdown_file(arguments.get("filepath", ""))
            return json.dumps({
                "file": result.file_path,
                "name": result.name,
                "items": result.items,
                "total_chars": result.total_chars,
                "issues": result.issues,
                "score": result.score,
                "status": "pass" if result.score >= 80 else "fail"
            }, ensure_ascii=False, indent=2)
        
        elif tool_name == "validate_directory":
            results = validate_directory(arguments.get("directory", "."))
            summary = {
                "total_files": len(results),
                "passed": sum(1 for r in results if r.score >= 80),
                "failed": sum(1 for r in results if r.score < 80),
                "results": [
                    {
                        "file": r.file_path,
                        "score": r.score,
                        "issues": r.issues
                    }
                    for r in results
                ]
            }
            return json.dumps(summary, ensure_ascii=False, indent=2)
        
        elif tool_name == "classify_file":
            result = classify_content(arguments.get("filepath", ""))
            return json.dumps(result, ensure_ascii=False, indent=2)
        
        elif tool_name == "classify_directory":
            results = scan_and_classify(arguments.get("directory", "."))
            return json.dumps(results, ensure_ascii=False, indent=2)
        
        elif tool_name == "md_to_html":
            html = markdown_to_html(arguments.get("markdown_content", ""))
            return html
        
        elif tool_name == "convert_file":
            output = process_file(
                arguments.get("input_path", ""),
                arguments.get("output_path")
            )
            return json.dumps({"success": True, "output": output}, ensure_ascii=False)
        
        elif tool_name == "gen_readme":
            update_readme(
                arguments.get("readme_path", "README.md"),
                arguments.get("content_dir", ".")
            )
            return json.dumps({
                "success": True,
                "readme": arguments.get("readme_path", "README.md"),
                "message": "README.md 已生成"
            }, ensure_ascii=False)
        
        elif tool_name == "extract_content_info":
            info = extract_info(arguments.get("filepath", ""))
            return json.dumps(info, ensure_ascii=False, indent=2)
        
        elif tool_name == "analyze_content_data":
            data = analyze_content(arguments.get("filepath", ""))
            return json.dumps(data, ensure_ascii=False, indent=2)
        
        elif tool_name == "analyze_directory":
            data = scan_and_analyze(arguments.get("directory", "."))
            stats = generate_stats(data)
            return json.dumps({"data": data, "stats": stats}, ensure_ascii=False, indent=2)
        
        elif tool_name == "search_content":
            matches = []
            search_path = Path(arguments.get("directory", "."))
            keyword = arguments.get("keyword", "")
            
            for md_file in search_path.glob("**/*.md"):
                if md_file.is_file():
                    try:
                        content = md_file.read_text(encoding="utf-8")
                        if keyword.lower() in content.lower():
                            matches.append({
                                "file": str(md_file),
                                "keyword": keyword
                            })
                    except:
                        pass
            
            return json.dumps({
                "keyword": keyword,
                "matches": matches,
                "count": len(matches)
            }, ensure_ascii=False, indent=2)
        
        elif tool_name == "list_tools":
            return json.dumps(list(TOOLS_REGISTRY.values()), ensure_ascii=False, indent=2)
        
        else:
            raise ValueError(f"Unknown tool: {tool_name}")


def create_cors_middleware(handler_class):
    """创建 CORS 中间件"""
    class CORSMcpHandler(handler_class):
        def do_GET(self):
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", f"{MCP_HEADER_METHOD}, {MCP_HEADER_NAME}, {MCP_HEADER_VERSION}, Content-Type")
            super().do_GET()
        
        def do_POST(self):
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", f"{MCP_HEADER_METHOD}, {MCP_HEADER_NAME}, {MCP_HEADER_VERSION}, Content-Type")
            super().do_POST()
        
        def do_OPTIONS(self):
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", f"{MCP_HEADER_METHOD}, {MCP_HEADER_NAME}, {MCP_HEADER_VERSION}, Content-Type")
            self.end_headers()
    return CORSMcpHandler


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """运行 MCP 服务器"""
    handler = create_cors_middleware(McpRequestHandler)
    server = HTTPServer((host, port), handler)
    
    print(f"\n{'='*60}")
    print(f"Baibai MCP Server v2 (MCP 2026-07-28)")
    print(f"{'='*60}")
    print(f"协议模式: 无状态 (Stateless)")
    print(f"端点: http://{host}:{port}/mcp")
    print(f"健康检查: http://{host}:{port}/health")
    print(f"{'='*60}\n")
    print(f"🚀 服务器启动中...")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
        server.server_close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Baibai MCP Server v2")
    parser.add_argument("--host", default="0.0.0.0", help="绑定地址")
    parser.add_argument("--port", type=int, default=8000, help="绑定端口")
    args = parser.parse_args()
    
    run_server(args.host, args.port)
