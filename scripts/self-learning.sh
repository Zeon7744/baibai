#!/bin/bash
# 数字员工自学习 - 反馈分析与自动优化

set -e

REPO_DIR="${1:-.}"
LOG_FILE="${2:-./logs/self-learning.log}"

mkdir -p "$(dirname "$LOG_FILE")"

echo "[$(date)] === 数字员工自学习启动 ===" >> "$LOG_FILE"

# 1. Issue 分析
echo "[*] 分析近期 Issue..."
RECENT_ISSUES=$(gh issue list --repo "$(basename $REPO_DIR)" --state all --limit 10 2>/dev/null || echo "")
if [ -n "$RECENT_ISSUES" ]; then
    echo "✅ 发现近期 Issue" >> "$LOG_FILE"
    echo "$RECENT_ISSUES" >> "$LOG_FILE"
else
    echo "⚠️ 无近期 Issue" >> "$LOG_FILE"
fi

# 2. PR 分析
echo "[*] 分析近期 PR..."
RECENT_PRS=$(gh pr list --repo "$(basename $REPO_DIR)" --state all --limit 10 2>/dev/null || echo "")
if [ -n "$RECENT_PRS" ]; then
    echo "✅ 发现近期 PR" >> "$LOG_FILE"
    echo "$RECENT_PRS" >> "$LOG_FILE"
fi

# 3. Star 增长趋势
echo "[*] 检查 Star 增长..."
STATS=$(curl -s "https://api.github.com/repos/$(echo $REPO_DIR | sed 's|.*/||')/$(basename $REPO_DIR)" 2>/dev/null || echo '{}')
STARS=$(echo "$STATS" | python3 -c "import sys,json; print(json.load(sys.stdin).get('stargazers_count', 0))" 2>/dev/null || echo "0")
echo "当前 Stars: $STARS" >> "$LOG_FILE"

# 4. 自动优化建议
echo "[*] 生成优化建议..."
SUGGESTIONS=""

# 检查 README 完整性
if ! grep -q "安装\|Usage\|使用" "$REPO_DIR/README.md" 2>/dev/null; then
    SUGGESTIONS="$SUGGESTIONS\n- 建议添加安装说明章节"
fi

if ! grep -q "三平台\|Gitee\|GitHub" "$REPO_DIR/README.md" 2>/dev/null; then
    SUGGESTIONS="$SUGGESTIONS\n- 建议添加多平台同步说明"
fi

if [ -n "$SUGGESTIONS" ]; then
    echo "优化建议:" >> "$LOG_FILE"
    echo -e "$SUGGESTIONS" >> "$LOG_FILE"
else
    echo "✅ README 结构完整" >> "$LOG_FILE"
fi

echo "[$(date)] === 数字员工自学习完成 ===" >> "$LOG_FILE"

echo "学习日志已保存: $LOG_FILE"
