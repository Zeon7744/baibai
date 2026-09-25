#!/bin/bash
# 作品上传布局生成器

set -e

REPO_DIR="${1:-.}"
OUTPUT_DIR="${2:-./pages}"

mkdir -p "$OUTPUT_DIR"

# 提取仓库信息
REPO_NAME=$(basename "$REPO_DIR")
REPO_DESC=$(grep -m1 "^>" "$REPO_DIR/README.md" 2>/dev/null | sed 's/^> //' || echo "暂无描述")
STARS=$(curl -s "https://api.github.com/repos/Zeon7744/$REPO_NAME" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('stargazers_count',0))" || echo "0")
FORKS=$(curl -s "https://api.github.com/repos/Zeon7744/$REPO_NAME" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('forks_count',0))" || echo "0")
COMMITS=$(git -C "$REPO_DIR" rev-list --all --count 2>/dev/null || echo "0")
ISSUES=$(curl -s "https://api.github.com/repos/Zeon7744/$REPO_NAME" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin).get('open_issues_count',0))" || echo "0")
LAST_UPDATE=$(date +%Y-%m-%d)

# 生成内容块
CONTENT_BLOCKS=""
for dir in "$REPO_DIR"/short-dramas "$REPO_DIR"/short-stories "$REPO_DIR"/tools; do
    if [ -d "$dir" ]; then
        NAME=$(basename "$dir")
        COUNT=$(ls "$dir" 2>/dev/null | wc -l)
        CONTENT_BLOCKS="$CONTENT_BLOCKS
        <div class='content-card'>
            <h3>$NAME</h3>
            <p>$COUNT 个项目</p>
            <div class='meta'>自动更新</div>
        </div>"
    fi
done

# 渲染HTML
sed \
    -e "s/{{REPO_NAME}}/$REPO_NAME/g" \
    -e "s/{{REPO_DESCRIPTION}}/$REPO_DESC/g" \
    -e "s/{{STARS}}/$STARS/g" \
    -e "s/{{FORKS}}/$FORKS/g" \
    -e "s/{{COMMITS}}/$COMMITS/g" \
    -e "s/{{ISSUES}}/$ISSUES/g" \
    -e "s|{{GITEE_REPO}}|Zeon7744/$REPO_NAME|g" \
    -e "s|{{GITHUB_REPO}}|Zeon7744/$REPO_NAME|g" \
    -e "s|{{GITCODE_REPO}}|Zeon7744/$REPO_NAME|g" \
    -e "s/{{LAST_UPDATE}}/$LAST_UPDATE/g" \
    -e "s|{{CONTENT_BLOCKS}}|$CONTENT_BLOCKS|g" \
    "$REPO_DIR/templates/repo-showcase.html" > "$OUTPUT_DIR/index.html"

echo "✅ 页面已生成: $OUTPUT_DIR/index.html"
