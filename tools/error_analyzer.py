#!/usr/bin/env python3
"""
错误分析器 - 分析错误堆栈，给出修复建议
"""

import re
from typing import Dict, Any, List, Optional


# 常见错误模式库
ERROR_PATTERNS = {
    # Python 错误
    "NameError": {
        "pattern": r"NameError:\s*name\s+'(\w+)'\s+is not defined",
        "cause": "使用了未定义的变量或函数名",
        "solutions": [
            "检查变量名拼写是否正确",
            "确认变量在使用前已定义",
            "检查是否在正确的变量作用域内"
        ]
    },
    "TypeError": {
        "pattern": r"TypeError:\s*(.+)",
        "cause": "类型不匹配或操作不支持该类型",
        "solutions": [
            "检查函数参数类型是否正确",
            "使用类型转换 (str(), int(), float() 等)",
            "添加类型检查或 isinstance() 验证"
        ]
    },
    "ValueError": {
        "pattern": r"ValueError:\s*(.+)",
        "cause": "传入的值不在有效范围内",
        "solutions": [
            "检查输入值的格式和范围",
            "添加输入验证",
            "查看函数文档了解合法值"
        ]
    },
    "IndexError": {
        "pattern": r"IndexError:\s*(.+)",
        "cause": "列表/数组索引超出范围",
        "solutions": [
            "检查索引值是否在范围内 (0 到 len-1)",
            "使用 len() 检查长度后再访问",
            "考虑使用 try-except 或安全访问模式"
        ]
    },
    "KeyError": {
        "pattern": r"KeyError:\s*(.+)",
        "cause": "字典中不存在指定的键",
        "solutions": [
            "使用 dict.get(key, default) 安全访问",
            "先用 'key in dict' 检查键是否存在",
            "检查键名拼写"
        ]
    },
    "FileNotFoundError": {
        "pattern": r"FileNotFoundError:\s*(.+)",
        "cause": "文件或目录不存在",
        "solutions": [
            "检查文件路径是否正确",
            "使用 os.path.exists() 先检查",
            "确认工作目录正确 (os.getcwd())",
            "使用绝对路径而非相对路径"
        ]
    },
    "ImportError": {
        "pattern": r"(?:Import|ModuleNotFoundError):\s*(?:No module named '(\w+)'|.+)",
        "cause": "模块未安装或路径不正确",
        "solutions": [
            "使用 pip install 安装缺失模块",
            "检查虚拟环境是否激活",
            "确认 sys.path 包含模块路径"
        ]
    },
    "AttributeError": {
        "pattern": r"AttributeError:\s*(.+)",
        "cause": "对象没有该属性或方法",
        "solutions": [
            "检查对象类型是否正确",
            "确认方法/属性名拼写",
            "使用 hasattr() 检查属性是否存在"
        ]
    },
    "PermissionError": {
        "pattern": r"PermissionError:\s*(.+)",
        "cause": "没有权限执行该操作",
        "solutions": [
            "检查文件/目录权限 (chmod/chown)",
            "以管理员/root 身份运行",
            "确认目标路径可写"
        ]
    },
    "ConnectionError": {
        "pattern": r"(?:Connection|ConnectionRefused|ConnectionReset)Error:\s*(.+)",
        "cause": "网络连接失败",
        "solutions": [
            "检查目标服务是否运行",
            "验证主机地址和端口",
            "检查防火墙设置",
            "添加重试机制"
        ]
    },
    "JSONDecodeError": {
        "pattern": r"json\.decoder\.JSONDecodeError:\s*(.+)",
        "cause": "JSON 格式解析失败",
        "solutions": [
            "检查 JSON 字符串格式是否正确",
            "使用 json.loads() 前先验证",
            "检查引号类型（JSON 要求双引号）",
            "去除多余的逗号或缺少的括号"
        ]
    },
    "SyntaxError": {
        "pattern": r"SyntaxError:\s*(.+)",
        "cause": "代码语法错误",
        "solutions": [
            "检查括号是否匹配",
            "确认缩进正确（混用空格和Tab会导致错误）",
            "检查字符串引号是否闭合",
            "查看错误行号附近的代码"
        ]
    },
    # JavaScript/Node.js 错误
    "ReferenceError": {
        "pattern": r"ReferenceError:\s*(.+)\s+is not defined",
        "cause": "JS 变量未定义",
        "solutions": [
            "检查变量声明 (let/const/var)",
            "确认变量在正确的作用域内",
            "检查脚本加载顺序"
        ]
    },
    "TypeError_JS": {
        "pattern": r"TypeError:\s+Cannot read propert.+of (?:null|undefined)",
        "cause": "访问了 null/undefined 的属性",
        "solutions": [
            "使用可选链 (?.) 安全访问",
            "添加 null 检查",
            "使用默认值"
        ]
    },
}


def parse_error_trace(error_trace: str) -> Dict[str, Any]:
    """解析错误堆栈"""
    result = {
        "error_type": None,
        "error_message": None,
        "file": None,
        "line_number": None,
        "function_name": None,
        "stack_trace": [],
        "raw_trace": error_trace
    }
    
    lines = error_trace.strip().split('\n')
    
    # 提取错误类型和消息（通常在最后一行）
    for line in reversed(lines):
        line = line.strip()
        # Python 格式: ExceptionType: message
        match = re.match(r'^(\w+Error|\w+Exception|\w+Warning):\s*(.*)', line)
        if match:
            result["error_type"] = match.group(1)
            result["error_message"] = match.group(2)
            break
        # JS 格式: ErrorType: message
        match = re.match(r'^(\w+Error):\s*(.*)', line)
        if match:
            result["error_type"] = match.group(1)
            result["error_message"] = match.group(2)
            break
    
    # 提取文件/行号信息
    file_pattern = r'File\s+"([^"]+)",\s+line\s+(\d+)'
    for line in lines:
        match = re.search(file_pattern, line)
        if match:
            result["file"] = match.group(1)
            result["line_number"] = int(match.group(2))
            # 尝试提取函数名
            func_match = re.search(r'in\s+(\w+)', line)
            if func_match:
                result["function_name"] = func_match.group(1)
            break
    
    # 收集堆栈帧
    frame_pattern = r'File\s+"([^"]+)",\s+line\s+(\d+),?\s*(?:in\s+(\w+))?'
    for line in lines:
        match = re.search(frame_pattern, line)
        if match:
            result["stack_trace"].append({
                "file": match.group(1),
                "line": int(match.group(2)),
                "function": match.group(3)
            })
    
    return result


def match_error_patterns(error_trace: str, error_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """匹配错误模式库"""
    matches = []
    
    for name, pattern_info in ERROR_PATTERNS.items():
        if re.search(pattern_info["pattern"], error_trace, re.IGNORECASE | re.DOTALL):
            matches.append({
                "error_name": name,
                "cause": pattern_info["cause"],
                "solutions": pattern_info["solutions"],
                "confidence": "high" if error_type and error_type in name else "medium"
            })
    
    return matches


def analyze_error(error_trace: str, context: str = "") -> Dict[str, Any]:
    """分析错误堆栈，给出修复建议"""
    # 解析堆栈
    parsed = parse_error_trace(error_trace)
    
    # 匹配已知错误模式
    matches = match_error_patterns(error_trace, parsed.get("error_type"))
    
    # 综合建议
    suggestions = []
    possible_causes = []
    
    if matches:
        for match in matches:
            possible_causes.append(match["cause"])
            suggestions.extend(match["solutions"])
    else:
        # 通用建议
        if parsed.get("error_type"):
            possible_causes.append(f"发生了 {parsed['error_type']} 错误")
        else:
            possible_causes.append("发生了未知错误")
        
        suggestions.extend([
            "仔细检查错误信息中的文件路径和行号",
            "检查最近的代码变更",
            "查看相关文档和社区讨论"
        ])
    
    # 上下文相关建议
    if context:
        if 'http' in context.lower() or 'api' in context.lower():
            suggestions.append("检查网络请求的 URL、方法和参数")
            suggestions.append("验证响应状态码和返回内容")
        if 'database' in context.lower() or 'sql' in context.lower():
            suggestions.append("检查数据库连接配置")
            suggestions.append("验证 SQL 语法和表结构")
        if 'file' in context.lower() or 'path' in context.lower():
            suggestions.append("使用 os.path.abspath() 确认实际路径")
            suggestions.append("检查文件编码是否为 UTF-8")
    
    # 去重
    suggestions = list(dict.fromkeys(suggestions))
    possible_causes = list(dict.fromkeys(possible_causes))
    
    return {
        "error_type": parsed.get("error_type"),
        "error_message": parsed.get("error_message"),
        "location": {
            "file": parsed.get("file"),
            "line": parsed.get("line_number"),
            "function": parsed.get("function_name")
        },
        "stack_frames": len(parsed.get("stack_trace", [])),
        "possible_causes": possible_causes,
        "suggestions": suggestions,
        "matched_patterns": len(matches),
        "severity": _assess_severity(parsed.get("error_type", ""))
    }


def _assess_severity(error_type: str) -> str:
    """评估错误严重程度"""
    critical = ["MemoryError", "SystemExit", "KeyboardInterrupt", "OOMError"]
    high = ["ConnectionError", "PermissionError", "AuthenticationError"]
    medium = ["TypeError", "ValueError", "KeyError", "IndexError", "FileNotFoundError"]
    low = ["Warning", "DeprecationWarning", "UserWarning"]
    
    if error_type in critical:
        return "critical"
    elif error_type in high:
        return "high"
    elif error_type in medium:
        return "medium"
    elif error_type in low:
        return "low"
    else:
        return "unknown"
