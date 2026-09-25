#!/bin/bash
# 对比分析脚本 - 版本对比与效果评估

set -e

REPO_DIR="${1:-.}"
OUTPUT_DIR="${2:-./analysis}"

mkdir -p "$OUTPUT_DIR"

echo "=== 仓库健康分析 ===" > "$OUTPUT_DIR/report.md"
echo "" >> "$OUTPUT_DIR/report.md"
echo "- 仓库: $REPO_DIR" >> "$OUTPUT_DIR/report.md"
echo "- 分析时间: $(date)" >> "$OUTPUT_DIR/report.md"
echo "" >> "$OUTPUT_DIR/report.md"

# 统计信息
echo "## 版本统计" >> "$OUTPUT_DIR/report.md"
echo "" >> "$OUTPUT_DIR/report.md"
echo "| 指标 | 数值 |" >> "$OUTPUT_DIR/report.md"
echo "|------|------|" >> "$OUTPUT_DIR/report.md"
echo "| 总提交数 | $(git -C "$REPO_DIR" rev-list --all --count) |" >> "$OUTPUT_DIR/report.md"
echo "| 分支数 | $(git -C "$REPO_DIR" branch --list | wc -l) |" >> "$OUTPUT_DIR/report.md"
echo "| 标签数 | $(git -C "$REPO_DIR" tag --list | wc -l) |" >> "$OUTPUT_DIR/report.md"
echo "| 最近提交 | $(git -C "$REPO_DIR" log -1 --format="%ai") |" >> "$OUTPUT_DIR/report.md"
echo "" >> "$OUTPUT_DIR/report.md"

# 贡献者统计
echo "## 贡献者统计" >> "$OUTPUT_DIR/report.md"
echo "" >> "$OUTPUT_DIR/report.md"
git -C "$REPO_DIR" shortlog -sn --all >> "$OUTPUT_DIR/report.md"
echo "" >> "$OUTPUT_DIR/report.md"

# 文件变更统计
echo "## 最近7天文件变更" >> "$OUTPUT_DIR/report.md"
echo "" >> "$OUTPUT_DIR/report.md"
git -C "$REPO_DIR" log --since="7 days ago" --stat --oneline >> "$OUTPUT_DIR/report.md"
echo "" >> "$OUTPUT_DIR/report.md"

echo "分析报告已保存至: $OUTPUT_DIR/report.md"
