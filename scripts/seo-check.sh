#!/bin/bash
# 自动提热脚本 - SEO 优化与推广

set -e

REPO_DIR="${1:-.}"
PLATFORM="${2:-github}"

echo "=== 提热机制启动 ==="
echo "仓库: $REPO_DIR"
echo "平台: $PLATFORM"
echo ""

# 1. README 关键词检查
echo "## 1. README 关键词检查"
if grep -q "AI短剧\|短剧剧本\|MCP" "$REPO_DIR/README.md" 2>/dev/null; then
    echo "✅ 核心关键词已包含"
else
    echo "⚠️ 建议添加核心关键词: AI短剧、短剧剧本、MCP Server"
fi

# 2. 标签检查
echo ""
echo "## 2. 仓库标签检查"
TAGS=$(gh repo view "$(basename $REPO_DIR)" --json topicTopics 2>/dev/null | python3 -c "import sys,json; print(','.join([t['name'] for t in json.load(sys.stdin).get('topicTopics',{}).get('topics',[])]))" 2>/dev/null || echo "")
echo "当前标签: $TAGS"

# 3. 描述检查
echo ""
echo "## 3. 仓库描述检查"
DESC=$(gh repo view "$(basename $REPO_DIR)" --json description 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('description',''))" 2>/dev/null || echo "")
if [ -n "$DESC" ] && [ ${#DESC} -gt 20 ]; then
    echo "✅ 描述长度: ${#DESC} 字符"
else
    echo "⚠️ 建议完善仓库描述（至少20字符）"
fi

# 4. 三平台同步检查
echo ""
echo "## 4. 三平台同步检查"
for remote in origin gitee; do
    if git -C "$REPO_DIR" remote get-url "$remote" &>/dev/null; then
        echo "✅ $remote 已配置"
    else
        echo "⚠️ $remote 未配置"
    fi
done

# 5. CI/CD 状态检查
echo ""
echo "## 5. CI/CD 状态检查"
WORKFLOWS=$(ls "$REPO_DIR/.github/workflows/" 2>/dev/null | wc -l)
echo "工作流数量: $WORKFLOWS"

echo ""
echo "=== 提热检查完成 ==="
