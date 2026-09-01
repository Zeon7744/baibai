#!/usr/bin/env python3
"""
Markdown 转 HTML 工具
支持标题、列表、代码块、表格等常用 Markdown 语法
"""

import re
import sys
from pathlib import Path


def markdown_to_html(markdown: str) -> str:
    """将 Markdown 转换为 HTML"""
    html = markdown

    # 保护代码块（避免被其他规则处理）
    code_blocks = []

    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f"{{CODE_BLOCK_{len(code_blocks)-1}}}"

    html = re.sub(r"```[\s\S]*?```", save_code_block, html)

    # 标题
    html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^#### (.+)$", r"<h4>\1</h4>", html, flags=re.MULTILINE)

    # 粗体和斜体
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)
    html = re.sub(r"__(.+?)__", r"<strong>\1</strong>", html)
    html = re.sub(r"_(.+?)_", r"<em>\1</em>", html)

    # 行内代码
    html = re.sub(r"`(.+?)`", r"<code>\1</code>", html)

    # 链接和图片
    html = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', html)
    html = re.sub(r"!\[(.+?)\]\((.+?)\)", r'<img src="\2" alt="\1">', html)

    # 无序列表
    html = re.sub(r"^[-*] (.+)$", r"<li>\1</li>", html, flags=re.MULTILINE)
    html = re.sub(r"(<li>.*</li>\n?)+", r"<ul>\g<0></ul>", html)

    # 有序列表
    html = re.sub(r"^\d+\. (.+)$", r"<li>\1</li>", html, flags=re.MULTILINE)
    html = re.sub(r"(<li>.*</li>\n?)+", r"<ol>\g<0></ol>", html)

    # 引用
    html = re.sub(r"^> (.+)$", r"<blockquote>\1</blockquote>", html, flags=re.MULTILINE)

    # 分隔线
    html = re.sub(r"^---+$", "<hr>", html, flags=re.MULTILINE)

    # 段落（处理换行）
    lines = html.split("\n")
    result = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith(
            ("<h1", "<h2", "<h3", "<h4", "<ul", "<ol", "<li", "<blockquote", "<hr", "<pre")
        ):
            result.append(line)
        else:
            result.append(f"<p>{line}</p>")

    html = "\n".join(result)

    # 恢复代码块
    for i, code in enumerate(code_blocks):
        html = html.replace(f"{{CODE_BLOCK_{i}}}", f"<pre><code>{code[3:-3].strip()}</code></pre>")

    return html


def process_file(input_path: str, output_path: str = None):
    """处理单个文件"""
    input_file = Path(input_path)

    if output_path is None:
        output_path = input_file.with_suffix(".html")
    else:
        output_path = Path(output_path)

    with open(input_file, "r", encoding="utf-8") as f:
        markdown = f.read()

    html = markdown_to_html(markdown)

    # 包装完整 HTML 页面
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{input_file.stem}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.6;
        }}
        h1, h2, h3, h4 {{ margin-top: 1.5em; margin-bottom: 0.5em; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 16px; overflow-x: auto; border-radius: 6px; }}
        blockquote {{ border-left: 4px solid #ccc; margin: 0; padding-left: 16px; color: #666; }}
        img {{ max-width: 100%; height: auto; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #f4f4f4; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"✅ 已生成: {output_path}")
    return str(output_path)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python md2html.py <markdown文件> [输出文件]")
        print("\n示例:")
        print("  python md2html.py README.md")
        print("  python md2html.py README.md output.html")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    process_file(input_path, output_path)


if __name__ == "__main__":
    main()
