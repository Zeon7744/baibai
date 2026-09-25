#!/usr/bin/env python3
"""
测试生成器 - 自动生成 pytest/unittest 测试用例
"""

import ast
import re
from typing import Dict, Any, List, Optional


def generate_tests(code: str, test_type: str = "pytest", language: str = "python") -> Dict[str, Any]:
    """根据代码生成测试用例"""
    test_type = test_type.lower().strip()
    if test_type not in ("pytest", "unittest"):
        test_type = "pytest"
    
    if language.lower() in ("python", "py", "python3"):
        return _generate_python_tests(code, test_type)
    elif language.lower() in ("javascript", "js", "typescript", "ts"):
        return _generate_js_tests(code, test_type)
    else:
        return _generate_generic_tests(code, test_type, language)


def _generate_python_tests(code: str, test_type: str) -> Dict[str, Any]:
    """生成 Python 测试"""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"error": f"代码语法错误: {e}", "tests": ""}
    
    functions = []
    classes = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            defaults = [None] * (len(args) - len(node.args.defaults)) + \
                       [ast.unparse(d) for d in node.args.defaults]
            functions.append({
                "name": node.name,
                "args": list(zip(args, defaults)),
                "returns": hasattr(node, 'returns') and node.returns is not None,
                "docstring": ast.get_docstring(node) or ""
            })
        elif isinstance(node, ast.ClassDef):
            methods = [n for n in node.body if isinstance(n, ast.FunctionDef) 
                       and not n.name.startswith('_')]
            if methods:
                classes.append({
                    "name": node.name,
                    "methods": [{"name": m.name, "args": [a.arg for a in m.args.args if a.arg != 'self']}
                               for m in methods]
                })
    
    if test_type == "pytest":
        tests = _build_pytest(functions, classes)
    else:
        tests = _build_unittest(functions, classes)
    
    return {
        "test_type": test_type,
        "language": "python",
        "tests": tests,
        "functions_covered": len(functions),
        "classes_covered": len(classes)
    }


def _build_pytest(functions: List[Dict], classes: List[Dict]) -> str:
    """构建 pytest 测试代码"""
    lines = [
        '"""自动生成的 pytest 测试用例"""',
        '',
        'import pytest',
        '# from your_module import ...  # 替换为实际导入路径',
        '',
        ''
    ]
    
    # 函数测试
    for func in functions:
        if func["name"].startswith('_'):
            continue
        fname = func["name"]
        lines.append(f"class Test{fname.title().replace('_', '')}:")
        lines.append(f'    """测试 {fname} 函数"""')
        lines.append('')
        
        # 正常用例
        args = func["args"]
        if args:
            args_str = ", ".join([f"{a}={d}" if d else f"{a}=None" for a, d in args[:3]])
        else:
            args_str = ""
        
        lines.append(f"    def test_{fname}_normal(self):")
        lines.append(f'        """测试正常情况"""')
        lines.append(f"        result = {fname}({args_str})")
        lines.append(f"        assert result is not None")
        lines.append('')
        
        # 边界用例
        lines.append(f"    def test_{fname}_edge_case(self):")
        lines.append(f'        """测试边界情况"""')
        if args:
            empty_args = ", ".join([f"{a}=None" if d else f"{a}=None" for a, d in args[:3]])
            lines.append(f"        result = {fname}({empty_args})")
            lines.append(f"        # TODO: 根据实际逻辑添加断言")
        else:
            lines.append(f"        result = {fname}()")
            lines.append(f"        assert result is not None")
        lines.append('')
        
        # 异常用例
        lines.append(f"    def test_{fname}_error_handling(self):")
        lines.append(f'        """测试异常情况"""')
        lines.append(f"        with pytest.raises(Exception):")
        if args:
            bad_args = ", ".join([f'{a}="invalid"' for a, d in args[:2]])
            lines.append(f"            {fname}({bad_args})")
        else:
            lines.append(f"            {fname}()")
        lines.append('')
        lines.append('')
    
    # 类测试
    for cls in classes:
        cname = cls["name"]
        lines.append(f"class Test{cname}:")
        lines.append(f'    """测试 {cname} 类"""')
        lines.append('')
        lines.append(f"    @pytest.fixture")
        lines.append(f"    def instance(self):")
        lines.append(f"        return {cname}()")
        lines.append('')
        
        for method in cls["methods"]:
            mname = method["name"]
            margs = method["args"]
            args_str = ", ".join([f'"{a}"' for a in margs[:3]])
            lines.append(f"    def test_{mname}(self, instance):")
            lines.append(f'        """测试 {mname} 方法"""')
            lines.append(f"        result = instance.{mname}({args_str})")
            lines.append(f"        assert result is not None")
            lines.append('')
        lines.append('')
    
    return "\n".join(lines)


def _build_unittest(functions: List[Dict], classes: List[Dict]) -> str:
    """构建 unittest 测试代码"""
    lines = [
        '"""自动生成的 unittest 测试用例"""',
        '',
        'import unittest',
        '# from your_module import ...  # 替换为实际导入路径',
        '',
        ''
    ]
    
    for func in functions:
        if func["name"].startswith('_'):
            continue
        fname = func["name"]
        lines.append(f"class Test{fname.title().replace('_', '')}(unittest.TestCase):")
        lines.append(f'    """测试 {fname} 函数"""')
        lines.append('')
        
        args = func["args"]
        args_str = ", ".join([f"{a}=None" for a, d in args[:3]]) if args else ""
        
        lines.append(f"    def test_{fname}_normal(self):")
        lines.append(f'        """测试正常情况"""')
        lines.append(f"        result = {fname}({args_str})")
        lines.append(f"        self.assertIsNotNone(result)")
        lines.append('')
        
        lines.append(f"    def test_{fname}_edge_case(self):")
        lines.append(f'        """测试边界情况"""')
        lines.append(f"        result = {fname}({args_str})")
        lines.append(f"        # TODO: 添加具体断言")
        lines.append('')
        lines.append('')
    
    for cls in classes:
        cname = cls["name"]
        lines.append(f"class Test{cname}(unittest.TestCase):")
        lines.append(f'    """测试 {cname} 类"""')
        lines.append('')
        lines.append(f"    def setUp(self):")
        lines.append(f"        self.instance = {cname}()")
        lines.append('')
        
        for method in cls["methods"]:
            mname = method["name"]
            margs = method["args"]
            args_str = ", ".join([f'"{a}"' for a in margs[:3]])
            lines.append(f"    def test_{mname}(self):")
            lines.append(f'        """测试 {mname} 方法"""')
            lines.append(f"        result = self.instance.{mname}({args_str})")
            lines.append(f"        self.assertIsNotNone(result)")
            lines.append('')
        lines.append('')
    
    lines.append("")
    lines.append('if __name__ == "__main__":')
    lines.append("    unittest.main()")
    
    return "\n".join(lines)


def _generate_js_tests(code: str, test_type: str) -> Dict[str, Any]:
    """生成 JavaScript 测试 (Jest)"""
    functions = re.findall(r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)', code)
    classes = re.findall(r'(?:export\s+)?class\s+(\w+)', code)
    
    lines = [
        "// 自动生成的 Jest 测试用例",
        "// import { ... } from './your_module';  // 替换为实际导入",
        ""
    ]
    
    for name, params in functions:
        lines.append(f"describe('{name}', () => {{")
        lines.append(f"  test('should execute normally', () => {{")
        lines.append(f"    const result = {name}();")
        lines.append(f"    expect(result).toBeDefined();")
        lines.append(f"  }});")
        lines.append("")
        lines.append(f"  test('should handle edge cases', () => {{")
        lines.append(f"    // TODO: 添加边界情况测试")
        lines.append(f"  }});")
        lines.append(f"}});")
        lines.append("")
    
    for cls in classes:
        lines.append(f"describe('{cls}', () => {{")
        lines.append(f"  let instance;")
        lines.append(f"  beforeEach(() => {{")
        lines.append(f"    instance = new {cls}();")
        lines.append(f"  }});")
        lines.append("")
        lines.append(f"  test('should be created', () => {{")
        lines.append(f"    expect(instance).toBeDefined();")
        lines.append(f"    expect(instance).toBeInstanceOf({cls});")
        lines.append(f"  }});")
        lines.append(f"}});")
        lines.append("")
    
    return {
        "test_type": "jest",
        "language": "javascript",
        "tests": "\n".join(lines),
        "functions_covered": len(functions),
        "classes_covered": len(classes)
    }


def _generate_generic_tests(code: str, test_type: str, language: str) -> Dict[str, Any]:
    """生成通用测试模板"""
    lines = [
        f"# {language} 测试用例模板",
        f"# 自动生成，请根据实际逻辑完善",
        "",
        "# 测试场景:",
        "# 1. 正常输入",
        "# 2. 边界值输入", 
        "# 3. 异常输入",
        "# 4. 空值/None 输入",
        ""
    ]
    
    return {
        "test_type": test_type,
        "language": language,
        "tests": "\n".join(lines),
        "functions_covered": 0,
        "classes_covered": 0,
        "note": "通用模板，需要手动补充具体测试"
    }
