#!/usr/bin/env python3
"""
Baibai CLI - Vibe Coding 开发工具集

快速开始:
  baibai --help
  baibai format check <剧本目录>
  baibai stats analyze <剧本目录>
  baibai readme generate <README路径> <剧本目录>

MCP 模式:
  baibai mcp serve
"""

import sys
from pathlib import Path
from typing import Optional

# 尝试导入 Typer，如果没有则 fallback
try:
    from typer import Typer, Option
    import typer
    HAS_TYPER = True
except ImportError:
    HAS_TYPER = False


# ==================== 工具函数 ====================

def get_drama_dir(default: str = "../awesome-ai-short-drama/short-dramas") -> str:
    """获取剧本目录"""
    return default


def check_format(drama_dir: str) -> dict:
    """格式校验"""
    sys.path.insert(0, str(Path(__file__).parent))
    from format_checker import validate_drama, scan_dramas, print_report
    
    results = scan_dramas(drama_dir)
    if not results:
        print("未找到剧本文件")
        return {"status": "error", "message": "No dramas found"}
    
    print_report(results)
    
    # 保存 JSON 报告
    import json
    from pathlib import Path
    output_dir = Path("data/stats")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    json_output = [{
        'title': r.title,
        'episodes': r.episodes,
        'words': r.total_words,
        'score': r.score,
        'issues': r.issues
    } for r in results]
    
    with open(output_dir / 'format_check.json', 'w', encoding='utf-8') as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)
    
    return {"status": "ok", "count": len(results)}


def analyze_stats(drama_dir: str) -> dict:
    """数据分析"""
    sys.path.insert(0, str(Path(__file__).parent))
    from stats_analyzer import scan_and_analyze, generate_stats, print_report, save_data
    
    data = scan_and_analyze(drama_dir)
    if not data.get('dramas'):
        print("未找到剧本文件")
        return {"status": "error", "message": "No dramas found"}
    
    stats = generate_stats(data)
    print_report(stats, data)
    save_data(data, stats)
    
    return {"status": "ok", "stats": stats}


def generate_readme(readme_path: str, drama_dir: str) -> dict:
    """生成 README"""
    sys.path.insert(0, str(Path(__file__).parent))
    from readme_gen import update_readme
    
    update_readme(readme_path, drama_dir)
    return {"status": "ok"}


# ==================== MCP Server ====================

MCP_TOOLS = [
    {
        "name": "baibai_format_check",
        "description": "检查剧本文件格式是否符合规范",
        "inputSchema": {
            "type": "object",
            "properties": {
                "drama_dir": {"type": "string", "description": "剧本目录路径"}
            },
            "required": ["drama_dir"]
        }
    },
    {
        "name": "baibai_analyze_stats",
        "description": "分析剧本库统计数据",
        "inputSchema": {
            "type": "object",
            "properties": {
                "drama_dir": {"type": "string", "description": "剧本目录路径"}
            },
            "required": ["drama_dir"]
        }
    },
    {
        "name": "baibai_generate_readme",
        "description": "自动生成 README 文档",
        "inputSchema": {
            "type": "object",
            "properties": {
                "readme_path": {"type": "string", "description": "README 文件路径"},
                "drama_dir": {"type": "string", "description": "剧本目录路径"}
            },
            "required": ["readme_path", "drama_dir"]
        }
    }
]


def mcp_list_tools():
    """MCP: 列出可用工具"""
    return {"tools": MCP_TOOLS}


def mcp_call_tool(name: str, arguments: dict):
    """MCP: 调用工具"""
    if name == "baibai_format_check":
        result = check_format(arguments.get("drama_dir", "../awesome-ai-short-drama/short-dramas"))
        return {"content": [{"type": "text", "text": f"格式校验完成: {len(result.get('results', []))} 部剧本"}]}
    
    elif name == "baibai_analyze_stats":
        result = analyze_stats(arguments.get("drama_dir", "../awesome-ai-short-drama/short-dramas"))
        return {"content": [{"type": "text", "text": f"统计分析完成，共 {result.get('stats', {}).get('total_dramas', 0)} 部剧本"}]}
    
    elif name == "baibai_generate_readme":
        generate_readme(arguments.get("readme_path"), arguments.get("drama_dir"))
        return {"content": [{"type": "text", "text": "README 已生成"}]}
    
    else:
        return {"error": f"Unknown tool: {name}"}


# ==================== 主入口 ====================

def main(args=None):
    """CLI 主入口"""
    if args is None:
        args = sys.argv[1:]
    
    if not args or args[0] in ["--help", "-h"]:
        print_help()
        return 0
    
    command = args[0]
    
    if command == "format" and args[1] == "check":
        drama_dir = args[2] if len(args) > 2 else get_drama_dir()
        check_format(drama_dir)
        return 0
    
    elif command == "stats" and args[1] == "analyze":
        drama_dir = args[2] if len(args) > 2 else get_drama_dir()
        analyze_stats(drama_dir)
        return 0
    
    elif command == "readme" and args[1] == "generate":
        readme_path = args[2] if len(args) > 2 else "../awesome-ai-short-drama/README.md"
        drama_dir = args[3] if len(args) > 3 else get_drama_dir()
        generate_readme(readme_path, drama_dir)
        return 0
    
    elif command == "mcp" and args[1] == "serve":
        print("MCP Server started (stdin/stdout mode)")
        print("Press Ctrl+C to exit")
        # 这里应该实现完整的 MCP 服务器逻辑
        return 0
    
    else:
        print_help()
        return 1


def print_help():
    """打印帮助信息"""
    help_text = """
Baibai - Vibe Coding 开发工具集

Usage:
  baibai <command> [options]

Commands:
  format check <dir>     检查剧本格式规范
  stats analyze <dir>    分析剧本统计数据
  readme generate <r> <d> 生成 README 文档
  mcp serve              启动 MCP 服务器

Options:
  --version              显示版本
  --help                 显示帮助

Examples:
  baibai format check ../awesome-ai-short-drama/short-dramas
  baibai stats analyze ../awesome-ai-short-drama/short-dramas
  baibai readme generate README.md ../awesome-ai-short-drama/short-dramas
"""
    print(help_text)


if __name__ == "__main__":
    sys.exit(main())
