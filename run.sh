#!/usr/bin/env bash
# baibai 一键启动 MCP Server
set -euo pipefail
cd "$(dirname "$0")"
python3 mcp_server.py
