#!/usr/bin/env python3
"""
文件分析器 - 分析项目文件结构、依赖关系、代码质量
"""

import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class FileAnalyzerResult:
    """文件分析结果"""
    path: str
    total_files: int = 0
    total_lines: int = 0
    file_types: Dict[str, int] = field(default_factory=dict)
    largest_files: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    quality_score: float = 0.0
    issues: List[str] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)


def analyze_file_structure(path: str) -> Dict[str, int]:
    """分析文件类型分布"""
    file_types = {}
    p = Path(path)
    
    if p.is_file():
        ext = p.suffix or '.no_ext'
        file_types[ext] = 1
        return file_types
    
    for root, dirs, files in os.walk(p):
        # 跳过隐藏目录和常见非源码目录
        dirs[:] = [d for d in dirs if not d.startswith('.') 
                   and d not in ('__pycache__', 'node_modules', 'venv', '.git')]
        
        for f in files:
            if f.startswith('.'):
                continue
            ext = Path(f).suffix or '.no_ext'
            file_types[ext] = file_types.get(ext, 0) + 1
    
    return dict(sorted(file_types.items(), key=lambda x: -x[1]))


def count_lines(path: str) -> int:
    """统计代码行数"""
    p = Path(path)
    total = 0
    
    if p.is_file():
        try:
            total = sum(1 for _ in open(p, encoding='utf-8', errors='ignore'))
        except Exception:
            pass
        return total
    
    for root, dirs, files in os.walk(p):
        dirs[:] = [d for d in dirs if not d.startswith('.') 
                   and d not in ('__pycache__', 'node_modules', 'venv', '.git')]
        for f in files:
            fp = Path(root) / f
            try:
                total += sum(1 for _ in open(fp, encoding='utf-8', errors='ignore'))
            except Exception:
                pass
    
    return total


def extract_python_dependencies(path: str) -> List[str]:
    """提取 Python 项目的依赖（import 语句）"""
    deps = set()
    p = Path(path)
    
    # 先尝试读取 requirements.txt
    req_file = p / 'requirements.txt' if p.is_dir() else p.parent / 'requirements.txt'
    if req_file.exists():
        try:
            content = req_file.read_text(encoding='utf-8')
            for line in content.strip().split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    pkg = re.split(r'[>=<~!]', line)[0].strip()
                    if pkg:
                        deps.add(pkg)
        except Exception:
            pass
    
    # 分析 Python 文件的 import 语句
    search_path = p if p.is_dir() else p.parent
    for py_file in search_path.rglob('*.py'):
        if any(part.startswith('.') for part in py_file.parts):
            continue
        try:
            tree = ast.parse(py_file.read_text(encoding='utf-8'))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        top_level = alias.name.split('.')[0]
                        deps.add(top_level)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        top_level = node.module.split('.')[0]
                        deps.add(top_level)
        except Exception:
            pass
    
    # 过滤标准库模块
    stdlib = {
        'os', 'sys', 're', 'json', 'math', 'time', 'datetime', 'collections',
        'itertools', 'functools', 'pathlib', 'typing', 'dataclasses', 'abc',
        'io', 'hashlib', 'uuid', 'logging', 'unittest', 'ast', 'subprocess',
        'threading', 'multiprocessing', 'asyncio', 'http', 'urllib', 'socket',
        'sqlite3', 'csv', 'xml', 'html', 'email', 'tempfile', 'shutil', 'glob',
        'random', 'string', 'struct', 'copy', 'pprint', 'enum', 'contextlib',
        'textwrap', 'warnings', 'traceback', 'inspect', 'importlib', 'base64',
        'pickle', 'marshal', 'dbm', 'gzip', 'bz2', 'lzma', 'zipfile', 'tarfile'
    }
    deps = {d for d in deps if d not in stdlib and not d.startswith('_')}
    
    return sorted(deps)


def analyze_code_quality(path: str) -> Dict[str, Any]:
    """简单的代码质量分析"""
    p = Path(path)
    issues = []
    score = 100.0
    
    py_files = []
    if p.is_file() and p.suffix == '.py':
        py_files = [p]
    elif p.is_dir():
        py_files = [f for f in p.rglob('*.py') 
                    if not any(part.startswith('.') for part in f.parts)]
    
    total_functions = 0
    total_classes = 0
    long_functions = 0
    missing_docstrings = 0
    
    for py_file in py_files:
        try:
            content = py_file.read_text(encoding='utf-8')
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    total_functions += 1
                    # 检查函数长度
                    if hasattr(node, 'end_lineno') and node.end_lineno:
                        func_lines = node.end_lineno - node.lineno
                        if func_lines > 50:
                            long_functions += 1
                    # 检查 docstring
                    if not ast.get_docstring(node):
                        missing_docstrings += 1
                        
                elif isinstance(node, ast.ClassDef):
                    total_classes += 1
                    if not ast.get_docstring(node):
                        missing_docstrings += 1
                        
        except Exception as e:
            issues.append(f"解析失败: {py_file} - {e}")
            score -= 5
    
    # 计算扣分
    if total_functions > 0:
        long_ratio = long_functions / total_functions
        if long_ratio > 0.3:
            score -= 15
            issues.append(f"超过30%的函数超过50行 ({long_functions}/{total_functions})")
        elif long_ratio > 0.1:
            score -= 8
            issues.append(f"超过10%的函数超过50行 ({long_functions}/{total_functions})")
    
    if total_functions + total_classes > 0:
        docstring_ratio = missing_docstrings / (total_functions + total_classes)
        if docstring_ratio > 0.5:
            score -= 15
            issues.append(f"超过50%的函数/类缺少文档字符串 ({missing_docstrings})")
        elif docstring_ratio > 0.2:
            score -= 8
            issues.append(f"超过20%的函数/类缺少文档字符串 ({missing_docstrings})")
    
    # 检查过长文件
    for py_file in py_files[:20]:  # 限制检查数量
        try:
            lines = sum(1 for _ in open(py_file, encoding='utf-8', errors='ignore'))
            if lines > 500:
                score -= 2
                issues.append(f"文件过长: {py_file.name} ({lines}行)")
        except Exception:
            pass
    
    score = max(0, score)
    
    return {
        "score": round(score, 1),
        "total_functions": total_functions,
        "total_classes": total_classes,
        "long_functions": long_functions,
        "missing_docstrings": missing_docstrings,
        "issues": issues
    }


def get_largest_files(path: str, limit: int = 10) -> List[Dict[str, Any]]:
    """获取最大的文件"""
    p = Path(path)
    files = []
    
    if p.is_file():
        return [{"path": str(p), "size": p.stat().st_size, "lines": count_lines(str(p))}]
    
    for root, dirs, filenames in os.walk(p):
        dirs[:] = [d for d in dirs if not d.startswith('.') 
                   and d not in ('__pycache__', 'node_modules', 'venv', '.git')]
        for f in filenames:
            fp = Path(root) / f
            try:
                stat = fp.stat()
                files.append({
                    "path": str(fp),
                    "size": stat.st_size,
                    "lines": 0  # 延迟计算
                })
            except Exception:
                pass
    
    files.sort(key=lambda x: -x['size'])
    return files[:limit]


def analyze_project(path: str) -> Dict[str, Any]:
    """主分析函数 - 分析项目文件结构、依赖关系、代码质量"""
    p = Path(path).resolve()
    
    if not p.exists():
        return {"error": f"路径不存在: {path}", "path": path}
    
    # 文件类型分布
    file_types = analyze_file_structure(str(p))
    total_files = sum(file_types.values())
    
    # 代码行数
    total_lines = count_lines(str(p))
    
    # 依赖分析
    dependencies = extract_python_dependencies(str(p))
    
    # 代码质量
    quality = analyze_code_quality(str(p))
    
    # 最大文件
    largest = get_largest_files(str(p))
    
    return {
        "path": str(p),
        "total_files": total_files,
        "total_lines": total_lines,
        "file_types": file_types,
        "dependencies": dependencies,
        "quality_score": quality["score"],
        "quality_details": quality,
        "largest_files": largest,
        "issues": quality["issues"]
    }
