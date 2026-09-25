#!/usr/bin/env python3
"""
文档生成器 - 自动生成 Markdown 文档
"""

import ast
import re
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


def generate_docs(code_path: str) -> Dict[str, Any]:
    """为代码文件或目录生成 Markdown 文档"""
    p = Path(code_path).resolve()
    
    if not p.exists():
        return {"error": f"路径不存在: {code_path}"}
    
    if p.is_file():
        return _generate_file_docs(p)
    else:
        return _generate_project_docs(p)


def _generate_file_docs(file_path: Path) -> Dict[str, Any]:
    """为单个文件生成文档"""
    ext = file_path.suffix
    
    if ext == '.py':
        docs = _generate_python_file_docs(file_path)
    elif ext in ('.js', '.ts', '.jsx', '.tsx'):
        docs = _generate_js_file_docs(file_path)
    else:
        docs = _generate_generic_file_docs(file_path)
    
    return docs


def _generate_python_file_docs(file_path: Path) -> Dict[str, Any]:
    """为 Python 文件生成文档"""
    try:
        source = file_path.read_text(encoding='utf-8')
        tree = ast.parse(source)
    except Exception as e:
        return {"error": f"解析失败: {e}", "path": str(file_path)}
    
    doc_parts = []
    module_name = file_path.stem
    module_doc = ast.get_docstring(tree) or f"{module_name} 模块文档"
    
    # 标题
    doc_parts.append(f"# {module_name}\n")
    doc_parts.append(f"> {module_doc}\n")
    doc_parts.append(f"**文件**: `{file_path.name}`  \n")
    doc_parts.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    # 模块级文档
    doc_parts.append(f"\n## 概述\n")
    doc_parts.append(f"{module_doc}\n")
    
    # 类文档
    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    if classes:
        doc_parts.append(f"\n## 类\n")
        for cls in classes:
            cls_doc = ast.get_docstring(cls) or "无描述"
            doc_parts.append(f"\n### `{cls.name}`\n")
            doc_parts.append(f"{cls_doc}\n")
            
            # 方法
            methods = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
            if methods:
                doc_parts.append(f"\n**方法:**\n")
                for method in methods:
                    if method.name.startswith('_') and method.name != '__init__':
                        continue
                    args = [arg.arg for arg in method.args.args if arg.arg != 'self']
                    method_doc = ast.get_docstring(method) or "无描述"
                    args_str = ", ".join(args)
                    doc_parts.append(f"- `{method.name}({args_str})` - {method_doc}")
    
    # 函数文档
    functions = [node for node in ast.iter_child_nodes(tree) if isinstance(node, ast.FunctionDef)]
    if functions:
        doc_parts.append(f"\n## 函数\n")
        for func in functions:
            func_doc = ast.get_docstring(func) or "无描述"
            args = [arg.arg for arg in func.args.args]
            args_str = ", ".join(args)
            doc_parts.append(f"\n### `{func.name}({args_str})`\n")
            doc_parts.append(f"{func_doc}\n")
            
            # 参数表
            if args:
                doc_parts.append(f"\n| 参数 | 说明 |")
                doc_parts.append(f"|------|------|")
                for arg in args:
                    doc_parts.append(f"| `{arg}` | - |")
    
    # 常量/变量
    assigns = [node for node in ast.iter_child_nodes(tree) if isinstance(node, ast.Assign)]
    if assigns:
        doc_parts.append(f"\n## 常量/变量\n")
        for assign in assigns:
            for target in assign.targets:
                if isinstance(target, ast.Name):
                    if target.id.isupper():  # 常量
                        doc_parts.append(f"- `{target.id}`")
    
    markdown = "\n".join(doc_parts)
    
    return {
        "path": str(file_path),
        "type": "python",
        "markdown": markdown,
        "classes_count": len(classes),
        "functions_count": len(functions)
    }


def _generate_js_file_docs(file_path: Path) -> Dict[str, Any]:
    """为 JS/TS 文件生成文档"""
    try:
        source = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return {"error": f"读取失败: {e}", "path": str(file_path)}
    
    doc_parts = []
    module_name = file_path.stem
    
    doc_parts.append(f"# {module_name}\n")
    doc_parts.append(f"**文件**: `{file_path.name}`  \n")
    doc_parts.append(f"**语言**: JavaScript/TypeScript\n")
    
    # 提取函数
    functions = re.findall(r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)', source)
    if functions:
        doc_parts.append(f"\n## 函数\n")
        for name, params in functions:
            doc_parts.append(f"\n### `{name}({params})`\n")
            # 提取 JSDoc
            jsdoc_pattern = rf'/\*\*([\s\S]*?)\*/\s*(?:export\s+)?(?:async\s+)?function\s+{name}'
            jsdoc_match = re.search(jsdoc_pattern, source)
            if jsdoc_match:
                doc = jsdoc_match.group(1).strip()
                doc = re.sub(r'^\s*\*\s?', '', doc, flags=re.MULTILINE).strip()
                doc_parts.append(f"{doc}\n")
    
    # 提取类
    classes = re.findall(r'class\s+(\w+)', source)
    if classes:
        doc_parts.append(f"\n## 类\n")
        for cls in classes:
            doc_parts.append(f"- `{cls}`")
    
    # 提取导出
    exports = re.findall(r'export\s+(?:default\s+)?(?:const|let|var|function|class)\s+(\w+)', source)
    if exports:
        doc_parts.append(f"\n## 导出\n")
        for exp in exports:
            doc_parts.append(f"- `{exp}`")
    
    markdown = "\n".join(doc_parts)
    
    return {
        "path": str(file_path),
        "type": "javascript",
        "markdown": markdown
    }


def _generate_generic_file_docs(file_path: Path) -> Dict[str, Any]:
    """为通用文件生成文档"""
    try:
        source = file_path.read_text(encoding='utf-8')
    except Exception:
        source = "(二进制文件)"
    
    lines = source.split('\n')
    
    markdown = f"# {file_path.stem}\n\n"
    markdown += f"**文件**: `{file_path.name}`  \n"
    markdown += f"**大小**: {file_path.stat().st_size} bytes  \n"
    markdown += f"**行数**: {len(lines)}\n\n"
    markdown += f"## 内容预览\n\n```\n"
    markdown += "\n".join(lines[:50])
    if len(lines) > 50:
        markdown += f"\n... (省略 {len(lines) - 50} 行)"
    markdown += "\n```\n"
    
    return {
        "path": str(file_path),
        "type": "generic",
        "markdown": markdown
    }


def _generate_project_docs(dir_path: Path) -> Dict[str, Any]:
    """为项目目录生成文档"""
    doc_parts = []
    
    # 项目名
    project_name = dir_path.name
    doc_parts.append(f"# {project_name} 项目文档\n")
    doc_parts.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
    doc_parts.append(f"**路径**: `{dir_path}`\n")
    
    # 目录结构
    doc_parts.append(f"\n## 目录结构\n")
    doc_parts.append("```")
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in sorted(dirs) if not d.startswith('.') and d != '__pycache__']
        level = root.replace(str(dir_path), '').count(os.sep)
        indent = '  ' * level
        doc_parts.append(f"{indent}{os.path.basename(root)}/")
        sub_indent = '  ' * (level + 1)
        for f in sorted(files)[:20]:
            doc_parts.append(f"{sub_indent}{f}")
        if len(files) > 20:
            doc_parts.append(f"{sub_indent}... ({len(files) - 20} more files)")
    doc_parts.append("```\n")
    
    # Python 文件文档
    py_files = list(dir_path.rglob('*.py'))
    if py_files:
        doc_parts.append(f"\n## Python 模块 ({len(py_files)} 个)\n")
        for pf in sorted(py_files)[:20]:
            try:
                source = pf.read_text(encoding='utf-8')
                tree = ast.parse(source)
                doc = ast.get_docstring(tree) or ""
                rel = pf.relative_to(dir_path)
                doc_parts.append(f"- `{rel}` - {doc[:100]}")
            except Exception:
                doc_parts.append(f"- `{pf.relative_to(dir_path)}` - (解析失败)")
    
    # README 检查
    readme = dir_path / 'README.md'
    if readme.exists():
        doc_parts.append(f"\n## 项目说明\n")
        doc_parts.append(f"> 已有 README.md: `{readme}`")
    
    markdown = "\n".join(doc_parts)
    
    return {
        "path": str(dir_path),
        "type": "project",
        "markdown": markdown,
        "python_files": len(py_files),
        "total_files": sum(1 for _ in dir_path.rglob('*') if _.is_file())
    }
