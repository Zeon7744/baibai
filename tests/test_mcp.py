#!/usr/bin/env python3
"""
MCP Server 测试脚本
"""

import sys
from pathlib import Path

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.classifier import classify_content
from tools.format_checker import check_markdown_file
from tools.md2html import markdown_to_html


def test_format_checker():
    """测试格式校验器"""
    print("=== 测试格式校验器 ===")

    # 创建一个测试文件
    test_content = '# 测试文档\n\n## 第一章\n\n这是测试内容。\n\n- 列表项1\n- 列表项2\n\n```python\nprint("hello")\n```\n\n## 第二章\n\n更多内容...'

    test_file = Path(__file__).parent / "test_sample.md"
    test_file.write_text(test_content, encoding="utf-8")

    try:
        result = check_markdown_file(str(test_file))
        print(f"文件: {result.file_path}")
        print(f"评分: {result.score}")
        print(f"问题: {result.issues}")
        print("PASS: 格式校验器测试通过")
    except Exception as e:
        print(f"FAIL: 格式校验器测试失败: {e}")
    finally:
        test_file.unlink(missing_ok=True)


def test_classifier():
    """测试分类器"""
    print("\n=== 测试分类器 ===")

    test_content = "# 帝师无双\n\n## 第1集\n\n幂星重生回到..."

    test_file = Path(__file__).parent / "test_drama.md"
    test_file.write_text(test_content, encoding="utf-8")

    try:
        result = classify_content(str(test_file))
        print(f"文件: {result.get('file')}")
        print(f"类型: {result.get('type')}")
        print(f"置信度: {result.get('confidence')}")
        print("PASS: 分类器测试通过")
    except Exception as e:
        print(f"FAIL: 分类器测试失败: {e}")
    finally:
        test_file.unlink(missing_ok=True)


def test_md2html():
    """测试 Markdown 转 HTML"""
    print("\n=== 测试 Markdown 转 HTML ===")

    md_content = "# 测试标题\n\n## 子标题\n\n这是**粗体**和*斜体*。\n\n- 列表1\n- 列表2\n\n```python\ncode here\n```"

    try:
        html = markdown_to_html(md_content)
        assert "<h1>" in html
        assert "<strong>" in html
        assert "<em>" in html
        print("PASS: Markdown 转 HTML 测试通过")
    except Exception as e:
        print(f"FAIL: Markdown 转 HTML 测试失败: {e}")


if __name__ == "__main__":
    test_format_checker()
    test_classifier()
    test_md2html()
    print("\n=== 所有测试完成 ===")
