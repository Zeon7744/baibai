#!/usr/bin/env python3
"""
Baibai MCP Server - 将 Vibe Coding 工具包装为 MCP 协议兼容服务

支持 AI 助手：
- Claude Code
- Cursor
- Codex
- 其他 MCP 兼容客户端
"""

import json
import sys
from pathlib import Path
from typing import Any

# 尝试导入 MCP SDK
try:
    from mcp.server.fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("警告: mcp 包未安装，请运行: pip install mcp")

# 导入 baibai 工具
sys.path.insert(0, str(Path(__file__).parent))
from tools.format_checker import check_markdown_file, scan_files, validate_directory
from tools.classifier import classify_content, scan_and_classify
from tools.md2html import markdown_to_html, process_file
from tools.readme_gen import extract_info, generate_content_section, update_readme
from tools.stats_analyzer import analyze_content, scan_and_analyze, generate_stats


def create_mcp_server() -> "FastMCP":
    """创建 MCP 服务器实例"""
    mcp = FastMCP("baibai")
    
    # 注册工具
    register_tools(mcp)
    
    return mcp


def register_tools(mcp: "FastMCP") -> None:
    """注册所有 baibai 工具"""
    
    # 1. 格式校验工具
    @mcp.tool()
    def check_format(filepath: str) -> str:
        """校验 Markdown 文件格式，检查标题、禁止字符、括号等
        
        Args:
            filepath: 要校验的 Markdown 文件路径
        """
        try:
            result = check_markdown_file(filepath)
            return json.dumps({
                "file": result.file_path,
                "name": result.name,
                "items": result.items,
                "total_chars": result.total_chars,
                "issues": result.issues,
                "score": result.score,
                "status": "pass" if result.score >= 80 else "fail"
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.tool()
    def validate_directory(directory: str) -> str:
        """批量校验目录下所有 Markdown 文件
        
        Args:
            directory: 目录路径
        """
        try:
            results = validate_directory(directory)
            summary = {
                "total_files": len(results),
                "passed": sum(1 for r in results if r.score >= 80),
                "failed": sum(1 for r in results if r.score < 80),
                "results": [
                    {
                        "file": r.file_path,
                        "score": r.score,
                        "issues": r.issues
                    }
                    for r in results
                ]
            }
            return json.dumps(summary, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    # 2. 内容分类工具
    @mcp.tool()
    def classify_file(filepath: str) -> str:
        """自动识别和分类内容类型
        
        Args:
            filepath: 要分类的文件路径
        """
        try:
            result = classify_content(filepath)
            return json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.tool()
    def classify_directory(directory: str) -> str:
        """批量分类目录下所有文件
        
        Args:
            directory: 目录路径
        """
        try:
            results = scan_and_classify(directory)
            return json.dumps(results, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    # 3. Markdown 转 HTML 工具
    @mcp.tool()
    def md_to_html(markdown_content: str) -> str:
        """将 Markdown 内容转换为 HTML
        
        Args:
            markdown_content: Markdown 文本内容
        """
        try:
            html = markdown_to_html(markdown_content)
            return html
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.tool()
    def convert_file(input_path: str, output_path: str = None) -> str:
        """转换 Markdown 文件为 HTML
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径（可选，默认同目录生成 .html）
        """
        try:
            output = process_file(input_path, output_path)
            return json.dumps({
                "success": True,
                "output": output
            }, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    # 4. README 生成工具
    @mcp.tool()
    def gen_readme(content_dir: str, readme_path: str = "README.md") -> str:
        """根据内容库自动生成 README 文档
        
        Args:
            content_dir: 内容目录路径
            readme_path: README 文件路径（默认当前目录 README.md）
        """
        try:
            update_readme(readme_path, content_dir)
            return json.dumps({
                "success": True,
                "readme": readme_path,
                "message": "README.md 已生成"
            }, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.tool()
    def extract_content_info(filepath: str) -> str:
        """从内容文件提取结构化信息（标题、章节、字数）
        
        Args:
            filepath: 文件路径
        """
        try:
            info = extract_info(filepath)
            return json.dumps(info, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    # 5. 数据分析工具
    @mcp.tool()
    def analyze_content_data(filepath: str) -> str:
        """分析单个内容文件的统计数据
        
        Args:
            filepath: 文件路径
        """
        try:
            data = analyze_content(filepath)
            return json.dumps(data, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    @mcp.tool()
    def analyze_directory(directory: str) -> str:
        """分析目录下所有内容文件，生成统计数据
        
        Args:
            directory: 目录路径
        """
        try:
            data = scan_and_analyze(directory)
            stats = generate_stats(data)
            return json.dumps({
                "data": data,
                "stats": stats
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    # 6. 内容搜索工具
    @mcp.tool()
    def search_content(keyword: str, directory: str = ".") -> str:
        """在目录下搜索包含关键词的内容
        
        Args:
            keyword: 搜索关键词
            directory: 搜索目录（默认当前目录）
        """
        try:
            matches = []
            search_path = Path(directory)
            
            for md_file in search_path.glob("**/*.md"):
                if md_file.is_file():
                    try:
                        content = md_file.read_text(encoding="utf-8")
                        if keyword.lower() in content.lower():
                            matches.append({
                                "file": str(md_file),
                                "keyword": keyword
                            })
                    except:
                        pass
            
            return json.dumps({
                "keyword": keyword,
                "matches": matches,
                "count": len(matches)
            }, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)
    
    # 7. 工具列表工具
    @mcp.tool()
    def list_tools() -> str:
        """列出所有可用的 baibai 工具
        
        返回工具列表及其描述
        """
        tools = [
            {
                "name": "check_format",
                "description": "校验 Markdown 文件格式",
                "args": ["filepath"]
            },
            {
                "name": "validate_directory",
                "description": "批量校验目录下所有 Markdown 文件",
                "args": ["directory"]
            },
            {
                "name": "classify_file",
                "description": "自动识别和分类单个文件",
                "args": ["filepath"]
            },
            {
                "name": "classify_directory",
                "description": "批量分类目录下所有文件",
                "args": ["directory"]
            },
            {
                "name": "md_to_html",
                "description": "将 Markdown 内容转换为 HTML",
                "args": ["markdown_content"]
            },
            {
                "name": "convert_file",
                "description": "转换 Markdown 文件为 HTML",
                "args": ["input_path", "output_path"]
            },
            {
                "name": "gen_readme",
                "description": "根据内容库自动生成 README",
                "args": ["content_dir", "readme_path"]
            },
            {
                "name": "extract_content_info",
                "description": "从内容文件提取结构化信息",
                "args": ["filepath"]
            },
            {
                "name": "analyze_content_data",
                "description": "分析单个内容文件的统计数据",
                "args": ["filepath"]
            },
            {
                "name": "analyze_directory",
                "description": "分析目录下所有内容文件",
                "args": ["directory"]
            },
            {
                "name": "search_content",
                "description": "在目录下搜索包含关键词的内容",
                "args": ["keyword", "directory"]
            },
            {
                "name": "list_tools",
                "description": "列出所有可用的 baibai 工具",
                "args": []
            }
        ]
        return json.dumps(tools, ensure_ascii=False, indent=2)


def run_server():
    """运行 MCP 服务器"""
    if not MCP_AVAILABLE:
        print("错误: mcp 包未安装")
        print("请运行: pip install mcp")
        sys.exit(1)
    
    server = create_mcp_server()
    server.run()


if __name__ == "__main__":
    run_server()
