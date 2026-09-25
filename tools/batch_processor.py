#!/usr/bin/env python3
"""
批量处理器 - 批量处理文件
"""

import os
import re
import json
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional


SUPPORTED_OPERATIONS = {
    "rename": "重命名文件",
    "move": "移动文件到目标目录",
    "copy": "复制文件到目标目录",
    "replace": "替换文件内容中的文本",
    "prefix": "添加文件名前缀",
    "suffix": "添加文件名后缀",
    "lowercase": "文件名转为小写",
    "uppercase": "文件名转为大写",
    "add_line": "在文件开头/结尾添加文本行",
    "remove_lines": "删除包含特定文本的行",
    "count_lines": "统计文件行数",
    "find_replace": "批量查找替换内容",
}


def batch_process(pattern: str, operation: str, files: List[str] = None,
                  directory: str = ".", **kwargs) -> Dict[str, Any]:
    """批量处理文件"""
    
    if operation not in SUPPORTED_OPERATIONS:
        return {
            "error": f"不支持的操作: {operation}",
            "supported": list(SUPPORTED_OPERATIONS.keys())
        }
    
    # 获取文件列表
    target_files = []
    if files:
        target_files = [Path(f) for f in files if Path(f).exists()]
    elif directory:
        p = Path(directory)
        if p.is_dir():
            target_files = list(p.glob(pattern)) if '*' in pattern or '?' in pattern else list(p.rglob(pattern))
    
    if not target_files:
        return {
            "error": "没有匹配的文件",
            "pattern": pattern,
            "directory": directory,
            "files_provided": len(files) if files else 0
        }
    
    results = []
    success_count = 0
    error_count = 0
    
    for file_path in target_files:
        try:
            result = _execute_operation(file_path, operation, **kwargs)
            results.append({
                "file": str(file_path),
                "status": "success",
                "result": result
            })
            success_count += 1
        except Exception as e:
            results.append({
                "file": str(file_path),
                "status": "error",
                "error": str(e)
            })
            error_count += 1
    
    return {
        "operation": operation,
        "pattern": pattern,
        "total_files": len(target_files),
        "success_count": success_count,
        "error_count": error_count,
        "results": results
    }


def _execute_operation(file_path: Path, operation: str, **kwargs) -> Any:
    """执行具体操作"""
    
    if operation == "rename":
        new_name = kwargs.get("new_name", "")
        if not new_name:
            raise ValueError("缺少 new_name 参数")
        new_path = file_path.parent / new_name
        file_path.rename(new_path)
        return {"new_path": str(new_path)}
    
    elif operation == "move":
        target_dir = kwargs.get("target_dir", "")
        if not target_dir:
            raise ValueError("缺少 target_dir 参数")
        dest = Path(target_dir)
        dest.mkdir(parents=True, exist_ok=True)
        new_path = dest / file_path.name
        shutil.move(str(file_path), str(new_path))
        return {"new_path": str(new_path)}
    
    elif operation == "copy":
        target_dir = kwargs.get("target_dir", "")
        if not target_dir:
            raise ValueError("缺少 target_dir 参数")
        dest = Path(target_dir)
        dest.mkdir(parents=True, exist_ok=True)
        new_path = dest / file_path.name
        shutil.copy2(str(file_path), str(new_path))
        return {"new_path": str(new_path)}
    
    elif operation == "replace":
        old_text = kwargs.get("old_text", "")
        new_text = kwargs.get("new_text", "")
        if not old_text:
            raise ValueError("缺少 old_text 参数")
        content = file_path.read_text(encoding='utf-8')
        new_content = content.replace(old_text, new_text)
        file_path.write_text(new_content, encoding='utf-8')
        count = content.count(old_text)
        return {"replacements": count}
    
    elif operation == "prefix":
        prefix = kwargs.get("prefix", "")
        if not prefix:
            raise ValueError("缺少 prefix 参数")
        new_name = prefix + file_path.name
        new_path = file_path.parent / new_name
        file_path.rename(new_path)
        return {"new_name": new_name}
    
    elif operation == "suffix":
        suffix = kwargs.get("suffix", "")
        if not suffix:
            raise ValueError("缺少 suffix 参数")
        stem = file_path.stem
        ext = file_path.suffix
        new_name = f"{stem}{suffix}{ext}"
        new_path = file_path.parent / new_name
        file_path.rename(new_path)
        return {"new_name": new_name}
    
    elif operation == "lowercase":
        new_name = file_path.name.lower()
        if new_name != file_path.name:
            new_path = file_path.parent / new_name
            file_path.rename(new_path)
            return {"new_name": new_name}
        return {"new_name": file_path.name, "changed": False}
    
    elif operation == "uppercase":
        new_name = file_path.name.upper()
        if new_name != file_path.name:
            new_path = file_path.parent / new_name
            file_path.rename(new_path)
            return {"new_name": new_name}
        return {"new_name": file_path.name, "changed": False}
    
    elif operation == "add_line":
        text = kwargs.get("text", "")
        position = kwargs.get("position", "end")  # "start" or "end"
        if not text:
            raise ValueError("缺少 text 参数")
        content = file_path.read_text(encoding='utf-8')
        if position == "start":
            new_content = text + "\n" + content
        else:
            new_content = content.rstrip('\n') + "\n" + text + "\n"
        file_path.write_text(new_content, encoding='utf-8')
        return {"position": position}
    
    elif operation == "remove_lines":
        pattern_text = kwargs.get("pattern", "")
        if not pattern_text:
            raise ValueError("缺少 pattern 参数")
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        original_count = len(lines)
        filtered = [l for l in lines if pattern_text not in l]
        removed = original_count - len(filtered)
        file_path.write_text('\n'.join(filtered), encoding='utf-8')
        return {"removed_lines": removed}
    
    elif operation == "count_lines":
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        return {
            "total_lines": len(lines),
            "non_empty_lines": sum(1 for l in lines if l.strip()),
            "characters": len(content)
        }
    
    elif operation == "find_replace":
        search = kwargs.get("search", "")
        replace = kwargs.get("replace", "")
        use_regex = kwargs.get("use_regex", False)
        if not search:
            raise ValueError("缺少 search 参数")
        
        content = file_path.read_text(encoding='utf-8')
        if use_regex:
            new_content, count = re.subn(search, replace, content)
        else:
            count = content.count(search)
            new_content = content.replace(search, replace)
        
        file_path.write_text(new_content, encoding='utf-8')
        return {"replacements": count}
    
    else:
        raise ValueError(f"未实现的操作: {operation}")
