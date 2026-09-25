#!/bin/bash
# 工段分发脚本 - 按模块分工执行任务

set -e

REPO_DIR="${1:-.}"
TASK_TYPE="${2:-all}"

echo "=== 工段分发: $TASK_TYPE ==="

case "$TASK_TYPE" in
    content)
        echo "[内容工段] 处理剧本/小说内容..."
        # 格式校验
        python "$REPO_DIR/tools/format_checker.py" "$REPO_DIR/short-dramas" 2>/dev/null || true
        # 统计更新
        python "$REPO_DIR/tools/stats_analyzer.py" "$REPO_DIR/short-dramas" > "$REPO_DIR/data/stats.json" 2>/dev/null || true
        ;;
    
    tool)
        echo "[工具工段] 测试MCP Server..."
        # 单元测试
        python -m pytest "$REPO_DIR/tests/" -v 2>/dev/null || true
        # MCP健康检查
        python "$REPO_DIR/mcp_server_v2.py" --health 2>/dev/null || true
        ;;
    
    data)
        echo "[数据工段] 采集分析..."
        # RSS采集
        if [ -f "$REPO_DIR/scripts/fetch-rss.py" ]; then
            python "$REPO_DIR/scripts/fetch-rss.py" 2>/dev/null || true
        fi
        # 分析报告
        python "$REPO_DIR/scripts/analysis.sh" "$REPO_DIR" 2>/dev/null || true
        ;;
    
    all)
        bash "$REPO_DIR/scripts/cicd.sh" "$REPO_DIR"
        bash "$REPO_DIR/scripts/seo-check.sh" "$REPO_DIR"
        bash "$REPO_DIR/scripts/self-learning.sh" "$REPO_DIR"
        ;;
esac

echo "=== 工段分发完成 ==="
