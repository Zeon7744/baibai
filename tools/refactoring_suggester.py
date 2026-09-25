#!/usr/bin/env python3
"""
重构建议器 - 分析代码并提供重构建议
"""

import ast
import re
from pathlib import Path
from typing import Dict, Any, List


def suggest_refactoring(code_path: str) -> Dict[str, Any]:
    """分析代码并提供重构建议"""
    p = Path(code_path).resolve()
    
    if not p.exists():
        return {"error": f"路径不存在: {code_path}"}
    
    if p.is_file():
        return _analyze_file(p)
    else:
        return _analyze_directory(p)


def _analyze_file(file_path: Path) -> Dict[str, Any]:
    """分析单个文件"""
    ext = file_path.suffix
    
    if ext == '.py':
        return _analyze_python_file(file_path)
    else:
        return _analyze_generic_file(file_path)


def _analyze_python_file(file_path: Path) -> Dict[str, Any]:
    """分析 Python 文件"""
    try:
        source = file_path.read_text(encoding='utf-8')
        tree = ast.parse(source)
    except Exception as e:
        return {"error": f"解析失败: {e}", "path": str(file_path)}
    
    suggestions = []
    lines = source.split('\n')
    total_lines = len(lines)
    
    # 1. 文件长度检查
    if total_lines > 500:
        suggestions.append({
            "type": "file_size",
            "severity": "high",
            "message": f"文件过长 ({total_lines} 行)，建议拆分为多个模块",
            "location": "file",
            "recommendation": "将相关功能分组到不同模块，每个文件不超过 300 行"
        })
    
    # 2. 函数长度检查
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if hasattr(node, 'end_lineno') and node.end_lineno:
                func_lines = node.end_lineno - node.lineno
                
                if func_lines > 100:
                    suggestions.append({
                        "type": "long_function",
                        "severity": "high",
                        "message": f"函数 `{node.name}` 过长 ({func_lines} 行)",
                        "location": f"line {node.lineno}",
                        "recommendation": "拆分为多个小函数，每个函数不超过 50 行"
                    })
                elif func_lines > 50:
                    suggestions.append({
                        "type": "long_function",
                        "severity": "medium",
                        "message": f"函数 `{node.name}` 较长 ({func_lines} 行)",
                        "location": f"line {node.lineno}",
                        "recommendation": "考虑拆分为更小的函数"
                    })
    
    # 3. 函数参数数量
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            arg_count = len(node.args.args)
            if node.args.args and node.args.args[0].arg == 'self':
                arg_count -= 1
            
            if arg_count > 6:
                suggestions.append({
                    "type": "too_many_params",
                    "severity": "high",
                    "message": f"函数 `{node.name}` 参数过多 ({arg_count} 个)",
                    "location": f"line {node.lineno}",
                    "recommendation": "使用 dataclass 或 dict 封装参数"
                })
            elif arg_count > 4:
                suggestions.append({
                    "type": "too_many_params",
                    "severity": "medium",
                    "message": f"函数 `{node.name}` 参数较多 ({arg_count} 个)",
                    "location": f"line {node.lineno}",
                    "recommendation": "考虑合并相关参数"
                })
    
    # 4. 缺少文档字符串
    module_doc = ast.get_docstring(tree)
    if not module_doc:
        suggestions.append({
            "type": "missing_docstring",
            "severity": "low",
            "message": "模块缺少文档字符串",
            "location": "module",
            "recommendation": "在文件开头添加模块说明"
        })
    
    missing_func_docs = 0
    missing_class_docs = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not ast.get_docstring(node):
            if not node.name.startswith('_'):
                missing_func_docs += 1
        elif isinstance(node, ast.ClassDef) and not ast.get_docstring(node):
            missing_class_docs += 1
    
    if missing_func_docs > 3:
        suggestions.append({
            "type": "missing_docstring",
            "severity": "medium",
            "message": f"{missing_func_docs} 个函数缺少文档字符串",
            "location": "file",
            "recommendation": "为公共函数添加 docstring"
        })
    
    if missing_class_docs > 0:
        suggestions.append({
            "type": "missing_docstring",
            "severity": "medium",
            "message": f"{missing_class_docs} 个类缺少文档字符串",
            "location": "file",
            "recommendation": "为类添加 docstring 说明用途"
        })
    
    # 5. 重复代码检测（简化版）
    line_patterns = {}
    for i, line in enumerate(lines):
        stripped = line.strip()
        if len(stripped) > 30 and not stripped.startswith('#'):
            if stripped in line_patterns:
                line_patterns[stripped].append(i + 1)
            else:
                line_patterns[stripped] = [i + 1]
    
    duplicates = {k: v for k, v in line_patterns.items() if len(v) > 2}
    if duplicates:
        suggestions.append({
            "type": "duplicate_code",
            "severity": "medium",
            "message": f"发现 {len(duplicates)} 处重复代码",
            "location": "file",
            "recommendation": "提取重复逻辑为独立函数"
        })
    
    # 6. 硬编码值检测
    hardcoded_patterns = [
        (r'["\']https?://[^"\']+["\']', "硬编码 URL"),
        (r'["\'][a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}["\']', "硬编码邮箱"),
        (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', "硬编码 IP 地址"),
    ]
    
    for pattern, desc in hardcoded_patterns:
        if re.search(pattern, source):
            suggestions.append({
                "type": "hardcoded_value",
                "severity": "low",
                "message": f"发现{desc}",
                "location": "file",
                "recommendation": f"将{desc}提取为常量或配置文件"
            })
    
    # 7. 异常处理检查
    bare_except = len(re.findall(r'\bexcept\s*:', source))
    if bare_except > 0:
        suggestions.append({
            "type": "bare_except",
            "severity": "high",
            "message": f"发现 {bare_except} 处裸 except（会捕获所有异常）",
            "location": "file",
            "recommendation": "指定具体异常类型，如 except ValueError:"
        })
    
    # 8. 复杂度评估
    complexity = _calculate_complexity(tree)
    if complexity > 20:
        suggestions.append({
            "type": "high_complexity",
            "severity": "high",
            "message": f"代码复杂度较高 ({complexity})",
            "location": "file",
            "recommendation": "简化嵌套逻辑，减少分支数量"
        })
    
    # 按严重程度排序
    severity_order = {"high": 0, "medium": 1, "low": 2}
    suggestions.sort(key=lambda s: severity_order.get(s["severity"], 3))
    
    # 总体评分
    score = 100
    for s in suggestions:
        if s["severity"] == "high":
            score -= 10
        elif s["severity"] == "medium":
            score -= 5
        else:
            score -= 2
    score = max(0, score)
    
    return {
        "path": str(file_path),
        "total_lines": total_lines,
        "suggestions": suggestions,
        "total_suggestions": len(suggestions),
        "score": score,
        "complexity": complexity,
        "summary": _build_summary(suggestions)
    }


def _calculate_complexity(tree: ast.AST) -> int:
    """计算圈复杂度"""
    complexity = 1
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.While, ast.For)):
            complexity += 1
        elif isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1
        elif isinstance(node, ast.Try):
            complexity += 1
        elif isinstance(node, ast.ExceptHandler):
            complexity += 1
    
    return complexity


def _build_summary(suggestions: List[Dict]) -> str:
    """构建摘要"""
    if not suggestions:
        return "代码质量良好，暂无重大重构建议。"
    
    high = sum(1 for s in suggestions if s["severity"] == "high")
    medium = sum(1 for s in suggestions if s["severity"] == "medium")
    low = sum(1 for s in suggestions if s["severity"] == "low")
    
    parts = []
    if high:
        parts.append(f"{high} 个高优先级")
    if medium:
        parts.append(f"{medium} 个中优先级")
    if low:
        parts.append(f"{low} 个低优先级")
    
    return f"共 {len(suggestions)} 条建议：" + "、".join(parts)


def _analyze_generic_file(file_path: Path) -> Dict[str, Any]:
    """分析通用文件"""
    try:
        source = file_path.read_text(encoding='utf-8')
    except Exception:
        return {"error": "无法读取文件", "path": str(file_path)}
    
    lines = source.split('\n')
    suggestions = []
    
    if len(lines) > 500:
        suggestions.append({
            "type": "file_size",
            "severity": "medium",
            "message": f"文件较长 ({len(lines)} 行)",
            "location": "file",
            "recommendation": "考虑拆分文件"
        })
    
    return {
        "path": str(file_path),
        "total_lines": len(lines),
        "suggestions": suggestions,
        "total_suggestions": len(suggestions),
        "score": max(0, 100 - len(suggestions) * 5)
    }


def _analyze_directory(dir_path: Path) -> Dict[str, Any]:
    """分析目录"""
    results = []
    total_suggestions = 0
    
    py_files = list(dir_path.rglob('*.py'))
    for pf in py_files[:20]:  # 限制数量
        if any(part.startswith('.') for part in pf.parts):
            continue
        result = _analyze_python_file(pf)
        results.append({
            "file": str(pf.relative_to(dir_path)),
            "score": result.get("score", 0),
            "suggestions_count": result.get("total_suggestions", 0)
        })
        total_suggestions += result.get("total_suggestions", 0)
    
    avg_score = sum(r["score"] for r in results) / len(results) if results else 0
    
    return {
        "path": str(dir_path),
        "files_analyzed": len(results),
        "average_score": round(avg_score, 1),
        "total_suggestions": total_suggestions,
        "results": results
    }
