#!/usr/bin/env python3
"""
代码解释器 - 解释代码逻辑
"""

import ast
import re
from typing import Dict, Any, List, Optional


def _extract_python_info(code: str) -> Dict[str, Any]:
    """解析 Python 代码提取结构信息"""
    info = {
        "imports": [],
        "classes": [],
        "functions": [],
        "main_logic": [],
        "variables": []
    }
    
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        info["error"] = f"语法错误: {e}"
        return info
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                info["imports"].append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                info["imports"].append(node.module)
        elif isinstance(node, ast.ClassDef):
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            info["classes"].append({
                "name": node.name,
                "methods": methods,
                "docstring": ast.get_docstring(node) or ""
            })
        elif isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            info["functions"].append({
                "name": node.name,
                "args": args,
                "docstring": ast.get_docstring(node) or "",
                "line": node.lineno
            })
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    info["variables"].append(target.id)
    
    return info


def _extract_js_info(code: str) -> Dict[str, Any]:
    """解析 JavaScript/TypeScript 代码提取结构信息"""
    info = {
        "imports": [],
        "functions": [],
        "classes": [],
        "variables": []
    }
    
    # 提取 import
    import_patterns = re.findall(r'(?:import|require)\s*[({]([^}]+)[)}]', code)
    info["imports"] = import_patterns[:10]
    
    # 提取函数
    func_patterns = re.findall(r'(?:function|const|let|var)\s+(\w+)\s*(?:=.*?(?:=>|function)|\([^)]*\)\s*\{)', code)
    info["functions"] = [{"name": f, "type": "function"} for f in func_patterns[:20]]
    
    # 提取类
    class_patterns = re.findall(r'class\s+(\w+)', code)
    info["classes"] = [{"name": c} for c in class_patterns[:10]]
    
    # 提取变量
    var_patterns = re.findall(r'(?:const|let|var)\s+(\w+)\s*=', code)
    info["variables"] = var_patterns[:20]
    
    return info


def _build_flow_description(info: Dict[str, Any], language: str) -> str:
    """构建流程图描述"""
    flow_lines = []
    flow_lines.append("```")
    flow_lines.append("流程图:")
    flow_lines.append("")
    
    step = 1
    
    if info.get("imports"):
        flow_lines.append(f"  [{step}] 导入依赖模块")
        step += 1
    
    if info.get("classes"):
        for cls in info["classes"]:
            flow_lines.append(f"  [{step}] 定义类: {cls['name']}")
            step += 1
    
    if info.get("functions"):
        for func in info["functions"][:5]:  # 限制数量
            name = func if isinstance(func, str) else func.get("name", "unknown")
            flow_lines.append(f"  [{step}] 定义函数: {name}")
            step += 1
    
    flow_lines.append(f"  [{step}] 执行主逻辑")
    step += 1
    flow_lines.append(f"  [{step}] 返回结果/输出")
    flow_lines.append("```")
    
    return "\n".join(flow_lines)


def _build_explanation(info: Dict[str, Any], language: str) -> str:
    """构建自然语言解释"""
    parts = []
    
    # 概述
    parts.append(f"## 概述\n")
    parts.append(f"这是一段 {language} 代码。")
    
    # 依赖
    if info.get("imports"):
        parts.append(f"\n## 依赖模块\n")
        parts.append(f"代码导入了以下模块: {', '.join(info['imports'][:10])}")
    
    # 类
    if info.get("classes"):
        parts.append(f"\n## 类定义\n")
        for cls in info["classes"]:
            name = cls['name']
            doc = cls.get('docstring', '')
            methods = cls.get('methods', [])
            parts.append(f"- **{name}**: {doc or '无文档说明'}")
            if methods:
                parts.append(f"  方法: {', '.join(methods[:8])}")
    
    # 函数
    if info.get("functions"):
        parts.append(f"\n## 函数/方法\n")
        for func in info["functions"][:10]:
            if isinstance(func, str):
                parts.append(f"- `{func}()`")
            else:
                name = func.get("name", "unknown")
                args = func.get("args", [])
                doc = func.get("docstring", "")
                args_str = f"({', '.join(args[:5])})" if args else "()"
                desc = f" - {doc}" if doc else ""
                parts.append(f"- `{name}{args_str}`{desc}")
    
    # 变量
    if info.get("variables"):
        parts.append(f"\n## 主要变量\n")
        unique_vars = list(set(info["variables"]))[:10]
        parts.append(f"`{', '.join(unique_vars)}`")
    
    return "\n".join(parts)


def explain_code(code: str, language: str = "python") -> Dict[str, Any]:
    """解释代码逻辑"""
    language = language.lower().strip()
    
    # 语言别名映射
    lang_map = {
        "py": "python", "python3": "python",
        "js": "javascript", "ts": "typescript",
        "tsx": "typescript", "jsx": "javascript",
        "rb": "ruby", "rs": "rust",
        "cs": "csharp", "c#": "csharp",
        "cpp": "cpp", "c++": "cpp",
    }
    language = lang_map.get(language, language)
    
    # 根据语言提取信息
    if language == "python":
        info = _extract_python_info(code)
    elif language in ("javascript", "typescript"):
        info = _extract_js_info(code)
    else:
        # 通用提取
        info = {
            "imports": re.findall(r'(?:import|include|require|use)\s+[<"]?([^>";\n]+)', code)[:10],
            "functions": re.findall(r'(?:function|def|func|fn)\s+(\w+)', code)[:20],
            "classes": re.findall(r'class\s+(\w+)', code)[:10],
            "variables": []
        }
    
    # 构建解释
    explanation = _build_explanation(info, language)
    flow = _build_flow_description(info, language)
    
    # 代码统计
    lines = code.strip().split('\n')
    stats = {
        "total_lines": len(lines),
        "code_lines": sum(1 for l in lines if l.strip() and not l.strip().startswith('#') and not l.strip().startswith('//')),
        "comment_lines": sum(1 for l in lines if l.strip().startswith('#') or l.strip().startswith('//')),
        "blank_lines": sum(1 for l in lines if not l.strip())
    }
    
    return {
        "language": language,
        "explanation": explanation,
        "flow_description": flow,
        "statistics": stats,
        "structure": info
    }
