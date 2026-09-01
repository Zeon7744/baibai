#!/usr/bin/env python3
"""
CLI 增强版 - 使用 Typer 框架
"""

import sys
from pathlib import Path
from typing import Optional

try:
    import typer
    from rich.console import Console
    from rich.panel import Panel

    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    typer = None


app = typer.Typer(help="Baibai - Vibe Coding 开发工具库")
console = Console() if HAS_RICH else None


# ==================== 格式校验 ====================


@app.command()
def check_format(
    directory: str = typer.Option("...", "--dir", "-d", help="要检查的目录"),
    json_output: bool = typer.Option(False, "--json", help="输出 JSON 格式"),
):
    """检查文件或目录的格式规范"""
    sys.path.insert(0, str(Path(__file__).parent))
    from format_checker import print_report, validate_directory

    results = validate_directory(directory)

    if not results:
        console.print("[red]未找到文件[/red]") if console else print("未找到文件")
        raise typer.Exit(1)

    if json_output:
        import json

        output = [{"name": r.name, "score": r.score, "issues": r.issues} for r in results]
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print_report(results)


# ==================== 数据分析 ====================


@app.command()
def analyze(
    directory: str = typer.Option("...", "--dir", "-d", help="要分析的目录"),
    json_output: bool = typer.Option(False, "--json", help="输出 JSON 格式"),
):
    """分析目录内容统计数据"""
    sys.path.insert(0, str(Path(__file__).parent))
    from stats_analyzer import generate_stats, print_report, save_data, scan_and_analyze

    data = scan_and_analyze(directory)

    if not data.get("contents"):
        console.print("[red]未找到文件[/red]") if console else print("未找到文件")
        raise typer.Exit(1)

    stats = generate_stats(data)

    if json_output:
        import json

        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print_report(stats, data)

    save_data(data, stats)


# ==================== README 生成 ====================


@app.command()
def gen_readme(
    readme_path: str = typer.Option("...", "--readme", "-r", help="README 文件路径"),
    directory: str = typer.Option("...", "--dir", "-d", help="内容目录"),
    preview: bool = typer.Option(False, "--preview", "-p", help="仅预览不写入"),
):
    """生成或更新 README 文档"""
    sys.path.insert(0, str(Path(__file__).parent))
    from readme_gen import generate_content_section, update_readme

    new_section = generate_content_section(directory)

    if preview:
        console.print(Panel(new_section, title="预览")) if console else print(new_section)
    else:
        update_readme(readme_path, directory)
        console.print("[green]README 已更新[/green]") if console else print("README 已更新")


# ==================== Markdown 转 HTML ====================


@app.command()
def md2html(
    input_file: str = typer.Argument(..., help="输入 Markdown 文件"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="输出 HTML 文件"),
    pretty: bool = typer.Option(True, "--pretty", help="美化 HTML 输出"),
):
    """将 Markdown 文件转换为 HTML"""
    sys.path.insert(0, str(Path(__file__).parent))
    from md2html import process_file

    result = process_file(input_file, output_file)
    console.print(f"[green]已生成: {result}[/green]") if console else print(f"已生成: {result}")


# ==================== 内容分类 ====================


@app.command()
def classify(
    directory: str = typer.Option("...", "--dir", "-d", help="要分类的目录"),
    json_output: bool = typer.Option(False, "--json", help="输出 JSON 格式"),
):
    """对目录内容进行自动分类"""
    sys.path.insert(0, str(Path(__file__).parent))
    from classifier import print_classification, save_results, scan_and_classify

    results = scan_and_classify(directory)

    if not results:
        console.print("[red]未找到文件[/red]") if console else print("未找到文件")
        raise typer.Exit(1)

    if json_output:
        import json

        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_classification(results)

    save_results(results)


# ==================== 版本信息 ====================


@app.callback()
def main(version: bool = typer.Option(False, "--version", "-v", help="显示版本信息")):
    """Baibai - Vibe Coding 开发工具库"""
    if version:
        typer.echo("Baibai v1.0.0")
        raise typer.Exit()


if __name__ == "__main__":
    app()
