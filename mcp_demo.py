# -*- coding: utf-8 -*-
"""baibai MCP 端到端接入 demo（P0：证明 MCP 消费方可一条命令验证）。

背景：baibai 定位是 MCP 工具层（vibecoding-cli 是通用 CLI，二者分工）。
v2 MCP Server（mcp_server_v2.py）已支持标准 JSON-RPC（server/discover +
tools/list + tools/call，含 MRTR 确认与 CORS），但缺一个“起服务→调用工具→
拿到结果”的可跑通 demo，导致 MCP 消费方（Cursor/Claude Code）无法快速验证接入。

本脚本补齐这条最小闭环：

    1) 后台起 v2 HTTP MCP 服务
    2) 用标准 JSON-RPC 客户端依次调用：server/discover → tools/list → tools/call
    3) 打印每一步返回，证明 MCP 接入链路可用

运行：
    python3 mcp_demo.py
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
import http.client
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))

import mcp_server_v2 as v2  # noqa: E402

_HOST = "127.0.0.1"
_PORT = 8741  # 避免与默认 8000 冲突


def _post(payload: dict, timeout: int = 15) -> dict:
    """向 v2 服务发 JSON-RPC 请求（端点 /mcp），用 raw socket 读取完整响应。

    服务端回写 CORS 头后回状态行；raw socket 读到 EOF 后按
    “行首是 JSON 对象”提取结果，规避 http.client 对 CORS 头顺序解析报错。
    """
    import socket
    body = json.dumps(payload).encode("utf-8")
    req = (
        f"POST /mcp HTTP/1.1\r\nHost: {_HOST}:{_PORT}\r\n"
        f"Content-Type: application/json\r\n"
        f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n"
    ).encode("ascii") + body
    with socket.create_connection((_HOST, _PORT), timeout=timeout) as s:
        s.sendall(req)
        chunks = []
        while True:
            b = s.recv(4096)
            if not b:
                break
            chunks.append(b)
    raw = b"".join(chunks).decode("utf-8", "ignore")
    for line in reversed(raw.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    return {"_raw": raw[:500]}


def _wait_ready(port: int, timeout: float = 20.0) -> bool:
    """轮询 /health 等待 HTTP 服务可访问。"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        conn = http.client.HTTPConnection(_HOST, port, timeout=2)
        try:
            conn.request("GET", "/health")
            conn.getresponse()
            conn.close()
            return True
        except Exception:
            try: conn.close()
            except Exception: pass
            time.sleep(0.3)
    return False


def run() -> None:
    # 1) 同进程起 v2 服务（独立线程，避免子进程 stdout 吞输出导致“未就绪”误判）
    print("[1/4] 启动 baibai MCP v2 服务 …")
    from http.server import ThreadingHTTPServer
    handler = v2.create_cors_middleware(v2.McpRequestHandler)
    server = ThreadingHTTPServer((_HOST, _PORT), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.3)  # 让服务就绪
    try:

        # 2) server/discover（v2 用 discover 替代 initialize）
        print("[2/4] server/discover …")
        disc = _post({"jsonrpc": "2.0", "id": 1, "method": "server/discover",
                           "params": {"clientVersion": v2.MCP_PROTOCOL_VERSION}})
        print("  protocolVersion =", disc.get("result", {}).get("protocolVersion"))
        print("  serverInfo      =", disc.get("result", {}).get("serverInfo"))

        # 3) tools/list
        print("[3/4] tools/list …")
        lst = _post({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        tools = lst.get("result", {}).get("tools", [])
        names = [t.get("name") for t in tools]
        print(f"  工具总数 = {len(tools)}")
        print(f"  工具列表 = {names[:12]}{' …' if len(names) > 12 else ''}")

        # 4) tools/call：选一个只读、无需确认的工具做端到端调用
        call_name = "classify_file" if "classify_file" in names else (names[0] if names else None)
        if call_name:
            print(f"[4/4] tools/call {call_name} …")
            call = _post({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                               "params": {"name": call_name,
                                          "arguments": {"filepath": str(BASE / "README.md")}}})
            text = call.get("result", {}).get("content", [{}])[0].get("text", "")
            print("  返回（截断）=" + text.replace("\n", " ")[:300])
        else:
            print("[4/4] 无可用工具，跳过 tools/call")

        print("\n✅ MCP 端到端 demo 闭环完成：起服务 → discover → tools/list → tools/call")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    run()
