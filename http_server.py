#!/usr/bin/env python3
"""
Baibai MCP HTTP Server - 独立的 HTTP 服务入口
支持多种部署方式：
- 单进程 HTTP 服务器（默认）
- gunicorn/uwsgi WSGI 服务器
- Docker 部署
"""

import os
import sys
from pathlib import Path
from http.server import HTTPServer
import threading
import signal
import json

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

# 导入 MCP 服务器核心
from mcp_server_v2 import run_server, McpRequestHandler, MCP_PROTOCOL_VERSION, SUPPORTED_METHODS


def print_banner():
    """打印启动横幅"""
    banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                    Baibai MCP Server v2                      ║
║              MCP Protocol Version: {MCP_PROTOCOL_VERSION}               ║
╠══════════════════════════════════════════════════════════════╣
║  Features:                                                  ║
║    ✓ Stateless Operation (No initialize handshake)          ║
║    ✓ MRTR Multi-Round-Trip Requests                         ║
║    ✓ HTTP Streamable Transport                               ║
║    ✓ Header-Based Routing (Mcp-Method, Mcp-Name)            ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_endpoints(port: int):
    """打印可用端点"""
    print("\n📍 Available Endpoints:")
    print(f"   POST   http://localhost:{port}/mcp          - MCP RPC endpoint")
    print(f"   GET    http://localhost:{port}/health       - Health check")
    print(f"   GET    http://localhost:{port}/info         - Server info")
    print(f"   POST   http://localhost:{port}/tools/list   - List tools (shortcut)")
    print()


def print_example_requests(port: int):
    """打印示例请求"""
    print("💡 Example Requests:")
    print()
    print("1. Discover server capabilities:")
    print(f'   curl -X POST http://localhost:{port}/mcp \\')
    print(f"      -H 'Mcp-Method: server/discover' \\")
    print(f"      -H 'Content-Type: application/json' \\")
    print(f'      -d \'{{"jsonrpc":"2.0","id":1,"method":"server/discover"}}\'')
    print()
    print("2. List available tools:")
    print(f'   curl -X POST http://localhost:{port}/mcp \\')
    print(f"      -H 'Mcp-Method: tools/list' \\")
    print(f"      -H 'Content-Type: application/json' \\")
    print(f'      -d \'{{"jsonrpc":"2.0","id":2,"method":"tools/list"}}\'')
    print()
    print("3. Call a tool:")
    print(f'   curl -X POST http://localhost:{port}/mcp \\')
    print(f"      -H 'Mcp-Method: tools/call' \\")
    print(f"      -H 'Mcp-Name: check_format' \\")
    print(f"      -H 'Content-Type: application/json' \\")
    print(f'      -d \'{{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{{"name":"check_format","arguments":{{"filepath":"/path/to/file.md"}}}}}}\'')
    print()


def health_check():
    """健康检查端点"""
    from mcp_server_v2 import McpRequestHandler
    handler = McpRequestHandler.__new__(McpRequestHandler)
    handler.server_name = "baibai-mcp-server"
    handler.server_version = "1.0.0"
    return {
        "status": "healthy",
        "server": handler.server_name,
        "version": handler.server_version,
        "protocol": MCP_PROTOCOL_VERSION,
        "features": ["stateless", "mrtr", "streamable-http"],
        "tools": list(SUPPORTED_METHODS.keys())
    }


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Baibai MCP HTTP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python http_server.py                          # Start on default port 8000
  python http_server.py --port 8080              # Start on port 8080
  python http_server.py --host 127.0.0.1         # Bind to localhost only
  python http_server.py --demo                   # Show demo mode with example requests
        """
    )
    parser.add_argument("--host", default="0.0.0.0", help="Bind to host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Bind to port (default: 8000)")
    parser.add_argument("--demo", action="store_true", help="Show demo mode with example requests")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon (background)")
    
    args = parser.parse_args()
    
    # 打印横幅
    print_banner()
    print_endpoints(args.port)
    
    # Demo 模式
    if args.demo:
        print_example_requests(args.port)
        print("💡 These examples demonstrate the new stateless MCP protocol.")
        print()
    
    # 配置信号处理
    def signal_handler(sig, frame):
        print("\n\n👋 Shutting down gracefully...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 启动服务器
    print(f"🚀 Starting server on {args.host}:{args.port}...")
    
    if args.daemon:
        # 后台模式
        pid = os.fork()
        if pid > 0:
            print(f"✅ Server started in background with PID {pid}")
            sys.exit(0)
    
    try:
        run_server(args.host, args.port)
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
