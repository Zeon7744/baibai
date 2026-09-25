#!/bin/bash
# 迭代运维脚本 - 自动化CI/CD流程

set -e

REPO_DIR="${1:-.}"
LOG_FILE="${REPO_DIR}/.logs/ci-cd.log"

mkdir -p "$(dirname "$LOG_FILE")"

echo "[$(date)] === 迭代运维启动 ===" >> "$LOG_FILE"

# 1. 代码检查
echo "[*] 运行代码检查..."
if [ -f "$REPO_DIR/pyproject.toml" ]; then
    python -m ruff check "$REPO_DIR/tools" || echo "⚠️ 代码检查发现需修复项"
fi

# 2. 测试运行
echo "[*] 运行测试..."
if [ -d "$REPO_DIR/tests" ]; then
    python -m pytest "$REPO_DIR/tests" -v --tb=short 2>&1 | tail -20 || echo "⚠️ 部分测试未通过"
fi

# 3. 同步检查
echo "[*] 检查多平台同步状态..."
for remote in origin gitee; do
    if git -C "$REPO_DIR" remote get-url "$remote" &>/dev/null; then
        LAST_SYNC=$(git -C "$REPO_DIR" log --format="%ai" -1 "$remote/main" 2>/dev/null || echo "未知")
        echo "✅ $remote: $LAST_SYNC" >> "$LOG_FILE"
    fi
done

# 4. 生成变更日志
echo "[*] 生成变更日志..."
git -C "$REPO_DIR" log --oneline -10 >> "$LOG_FILE"

echo "[$(date)] === 迭代运维完成 ===" >> "$LOG_FILE"
