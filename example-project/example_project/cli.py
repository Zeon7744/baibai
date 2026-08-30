"""示例项目 CLI"""

import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def hello(name: str = typer.Option("World", "--name", "-n", help="要问候的名字")):
    """向指定名字打招呼"""
    console.print(f"[bold green]Hello, {name}![/bold green]")
    console.print(f"欢迎来到 Baibai 发布示例项目")
    console.print(f"当前版本: 1.0.0")

@app.command()
def info():
    """显示项目信息"""
    console.print("[bold]Example Project[/bold]")
    console.print(f"版本: 1.0.0")
    console.print(f"作者: Zeon7744")
    console.print(f"描述: Baibai 发布示例项目")

if __name__ == "__main__":
    app()
