#!/usr/bin/env python3
"""
Baibai MCP Server v3 新工具测试
覆盖: file_analyzer, prompt_engineer, code_explainer, error_analyzer,
      batch_processor, docs_generator, test_generator, refactoring_suggester,
      dependency_checker, api_doc_builder
"""

import sys
import os
import json
import tempfile
import shutil
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


# ===== file_analyzer 测试 =====

class TestFileAnalyzer:
    """测试文件分析器"""

    def test_analyze_python_file(self, tmp_path):
        """测试分析 Python 文件"""
        from tools.file_analyzer import analyze_project
        
        py_file = tmp_path / "sample.py"
        py_file.write_text('''
import os
import json

def hello(name):
    """问候函数"""
    return f"Hello, {name}!"

class Greeter:
    """打招呼类"""
    def greet(self, name):
        return hello(name)
''', encoding='utf-8')
        
        result = analyze_project(str(py_file))
        assert "total_files" in result
        assert result["total_files"] >= 1
        assert "quality_score" in result
        assert result["quality_score"] >= 0

    def test_analyze_directory(self, tmp_path):
        """测试分析目录"""
        from tools.file_analyzer import analyze_project
        
        (tmp_path / "app.py").write_text("print('hello')\n", encoding='utf-8')
        (tmp_path / "utils.py").write_text("def helper(): pass\n", encoding='utf-8')
        (tmp_path / "readme.md").write_text("# Project\n", encoding='utf-8')
        
        result = analyze_project(str(tmp_path))
        assert result["total_files"] == 3
        assert "file_types" in result
        assert ".py" in result["file_types"]

    def test_analyze_nonexistent(self):
        """测试分析不存在的路径"""
        from tools.file_analyzer import analyze_project
        
        result = analyze_project("/nonexistent/path")
        assert "error" in result

    def test_extract_dependencies(self, tmp_path):
        """测试依赖提取"""
        from tools.file_analyzer import extract_python_dependencies
        
        (tmp_path / "app.py").write_text("import flask\nfrom requests import get\n", encoding='utf-8')
        (tmp_path / "requirements.txt").write_text("flask==2.3.0\nrequests>=2.28\n", encoding='utf-8')
        
        deps = extract_python_dependencies(str(tmp_path))
        assert "flask" in deps
        assert "requests" in deps


# ===== prompt_engineer 测试 =====

class TestPromptEngineer:
    """测试提示词工程师"""

    def test_optimize_simple_prompt(self):
        """测试简单提示词优化"""
        from tools.prompt_engineer import optimize_prompt
        
        result = optimize_prompt("写一篇文章", "生成一篇关于AI的文章")
        assert "optimized" in result
        assert "score_before" in result
        assert "score_after" in result
        assert result["score_after"] >= result["score_before"]

    def test_score_prompt(self):
        """测试提示词评分"""
        from tools.prompt_engineer import score_prompt
        
        # 短提示词应该得分低
        low_score = score_prompt("写代码")
        # 详细提示词应该得分高
        high_score = score_prompt("""
你是资深工程师。
目标：编写一个函数。
格式：JSON 输出。
示例：例如 input: 5, output: 25
不要包含无关内容。
""")
        assert high_score > low_score

    def test_optimize_with_target(self):
        """测试带目标的优化"""
        from tools.prompt_engineer import optimize_prompt
        
        result = optimize_prompt(
            "分析这段代码",
            "找出代码中的性能问题"
        )
        assert "improvements" in result
        assert len(result["improvements"]) > 0


# ===== code_explainer 测试 =====

class TestCodeExplainer:
    """测试代码解释器"""

    def test_explain_python_code(self):
        """测试解释 Python 代码"""
        from tools.code_explainer import explain_code
        
        code = '''
import os
from pathlib import Path

def read_file(filepath):
    """读取文件内容"""
    return Path(filepath).read_text()

class FileReader:
    def __init__(self, path):
        self.path = path
'''
        result = explain_code(code, "python")
        assert "explanation" in result
        assert "flow_description" in result
        assert "statistics" in result
        assert result["language"] == "python"

    def test_explain_javascript(self):
        """测试解释 JavaScript 代码"""
        from tools.code_explainer import explain_code
        
        code = '''
import express from 'express';
const app = express();
function handler(req, res) { res.json({ok: true}); }
class Server { start() {} }
'''
        result = explain_code(code, "javascript")
        assert result["language"] == "javascript"
        assert "explanation" in result

    def test_language_aliases(self):
        """测试语言别名"""
        from tools.code_explainer import explain_code
        
        code = "def foo(): pass"
        for lang in ["py", "python3", "Python"]:
            result = explain_code(code, lang)
            assert result["language"] == "python"


# ===== error_analyzer 测试 =====

class TestErrorAnalyzer:
    """测试错误分析器"""

    def test_analyze_name_error(self):
        """测试 NameError 分析"""
        from tools.error_analyzer import analyze_error
        
        trace = '''Traceback (most recent call last):
  File "app.py", line 10, in main
    print(undefined_var)
NameError: name 'undefined_var' is not defined'''
        
        result = analyze_error(trace)
        assert result["error_type"] == "NameError"
        assert len(result["possible_causes"]) > 0
        assert len(result["suggestions"]) > 0

    def test_analyze_import_error(self):
        """测试 ImportError 分析"""
        from tools.error_analyzer import analyze_error
        
        trace = "ModuleNotFoundError: No module named 'flask'"
        result = analyze_error(trace)
        assert "flask" in result["error_message"] or result["error_type"] == "ImportError"

    def test_analyze_with_context(self):
        """测试带上下文的分析"""
        from tools.error_analyzer import analyze_error
        
        trace = "ConnectionError: Failed to connect to server"
        result = analyze_error(trace, context="http api")
        assert len(result["suggestions"]) > 0

    def test_analyze_unknown_error(self):
        """测试未知错误"""
        from tools.error_analyzer import analyze_error
        
        result = analyze_error("Something went wrong")
        assert result is not None
        assert "suggestions" in result


# ===== batch_processor 测试 =====

class TestBatchProcessor:
    """测试批量处理器"""

    def test_count_lines(self, tmp_path):
        """测试行数统计"""
        from tools.batch_processor import batch_process
        
        (tmp_path / "a.txt").write_text("line1\nline2\nline3\n", encoding='utf-8')
        (tmp_path / "b.txt").write_text("hello\nworld\n", encoding='utf-8')
        
        result = batch_process("*.txt", "count_lines", directory=str(tmp_path))
        assert result["success_count"] == 2
        assert result["total_files"] == 2

    def test_replace_operation(self, tmp_path):
        """测试替换操作"""
        from tools.batch_processor import batch_process
        
        f = tmp_path / "test.txt"
        f.write_text("hello world\nhello python", encoding='utf-8')
        
        result = batch_process("*.txt", "replace", 
                               directory=str(tmp_path),
                               old_text="hello", new_text="hi")
        assert result["success_count"] == 1
        
        content = f.read_text(encoding='utf-8')
        assert "hi" in content
        assert "hello" not in content

    def test_unsupported_operation(self):
        """测试不支持的操作"""
        from tools.batch_processor import batch_process
        
        result = batch_process("*.txt", "invalid_op")
        assert "error" in result

    def test_no_matching_files(self, tmp_path):
        """测试无匹配文件"""
        from tools.batch_processor import batch_process
        
        result = batch_process("*.xyz", "count_lines", directory=str(tmp_path))
        assert "error" in result or result["total_files"] == 0


# ===== docs_generator 测试 =====

class TestDocsGenerator:
    """测试文档生成器"""

    def test_generate_python_docs(self, tmp_path):
        """测试生成 Python 文件文档"""
        from tools.docs_generator import generate_docs
        
        py_file = tmp_path / "module.py"
        py_file.write_text('''
"""模块说明"""

class MyClass:
    """我的类"""
    def method(self, x):
        """方法说明"""
        return x * 2

def helper(name):
    """辅助函数"""
    return f"Hello {name}"
''', encoding='utf-8')
        
        result = generate_docs(str(py_file))
        assert "markdown" in result
        assert "MyClass" in result["markdown"]
        assert "helper" in result["markdown"]

    def test_generate_project_docs(self, tmp_path):
        """测试生成项目文档"""
        from tools.docs_generator import generate_docs
        
        (tmp_path / "app.py").write_text('"""App"""\nprint("hi")\n', encoding='utf-8')
        (tmp_path / "utils.py").write_text('"""Utils"""\ndef f(): pass\n', encoding='utf-8')
        
        result = generate_docs(str(tmp_path))
        assert result["type"] == "project"
        assert "markdown" in result

    def test_generate_nonexistent(self):
        """测试不存在的路径"""
        from tools.docs_generator import generate_docs
        
        result = generate_docs("/nonexistent")
        assert "error" in result


# ===== test_generator 测试 =====

class TestTestGenerator:
    """测试测试生成器"""

    def test_generate_pytest(self):
        """测试生成 pytest 用例"""
        from tools.test_generator import generate_tests
        
        code = '''
def add(a, b):
    return a + b

class Calculator:
    def multiply(self, x, y):
        return x * y
'''
        result = generate_tests(code, "pytest")
        assert result["test_type"] == "pytest"
        assert "tests" in result
        assert "def test_" in result["tests"]
        assert result["functions_covered"] > 0

    def test_generate_unittest(self):
        """测试生成 unittest 用例"""
        from tools.test_generator import generate_tests
        
        code = "def greet(name): return f'Hello {name}'"
        result = generate_tests(code, "unittest")
        assert result["test_type"] == "unittest"
        assert "unittest.TestCase" in result["tests"]

    def test_generate_js_tests(self):
        """测试生成 JS 测试"""
        from tools.test_generator import generate_tests
        
        code = "function add(a, b) { return a + b; } class Calc { multiply() {} }"
        result = generate_tests(code, "jest", "javascript")
        assert "jest" in result["test_type"] or result["language"] == "javascript"


# ===== refactoring_suggester 测试 =====

class TestRefactoringSuggester:
    """测试重构建议器"""

    def test_analyze_simple_file(self, tmp_path):
        """测试分析简单文件"""
        from tools.refactoring_suggester import suggest_refactoring
        
        py_file = tmp_path / "simple.py"
        py_file.write_text('''
def hello():
    print("hello")

def world():
    print("world")
''', encoding='utf-8')
        
        result = suggest_refactoring(str(py_file))
        assert "score" in result
        assert result["score"] >= 0

    def test_analyze_complex_file(self, tmp_path):
        """测试分析复杂文件（应产生更多建议）"""
        from tools.refactoring_suggester import suggest_refactoring
        
        # 生成一个较长且缺少文档的文件
        lines = []
        lines.append('def f0(a, b, c, d, e, f, g):')
        for j in range(60):
            lines.append(f'    x{j} = {j}')
        lines.append('    return x59')
        
        py_file = tmp_path / "complex.py"
        py_file.write_text('\n'.join(lines), encoding='utf-8')
        
        result = suggest_refactoring(str(py_file))
        assert "suggestions" in result
        assert len(result["suggestions"]) > 0

    def test_analyze_nonexistent(self):
        """测试不存在的路径"""
        from tools.refactoring_suggester import suggest_refactoring
        
        result = suggest_refactoring("/nonexistent")
        assert "error" in result


# ===== dependency_checker 测试 =====

class TestDependencyChecker:
    """测试依赖检查器"""

    def test_check_vulnerable_deps(self, tmp_path):
        """测试检测有漏洞的依赖"""
        from tools.dependency_checker import check_dependencies
        
        req_file = tmp_path / "requirements.txt"
        req_file.write_text(
            "flask==2.0.0\n"
            "requests==2.25.0\n"
            "pyyaml==5.4.0\n",
            encoding='utf-8'
        )
        
        result = check_dependencies(str(req_file))
        assert "vulnerabilities" in result
        assert result["score"] < 100

    def test_check_safe_deps(self, tmp_path):
        """测试安全的依赖"""
        from tools.dependency_checker import check_dependencies
        
        req_file = tmp_path / "requirements.txt"
        req_file.write_text(
            "flask==3.0.0\n"
            "requests==2.31.0\n",
            encoding='utf-8'
        )
        
        result = check_dependencies(str(req_file))
        assert result["stats"]["total_packages"] == 2

    def test_check_from_content(self):
        """测试从内容直接检查"""
        from tools.dependency_checker import check_dependencies
        
        result = check_dependencies(
            requirements_content="django==4.0.0\nnumpy==1.23.0"
        )
        assert result["stats"]["total_packages"] == 2

    def test_check_unpinned(self, tmp_path):
        """测试未锁定版本的检测"""
        from tools.dependency_checker import check_dependencies
        
        req_file = tmp_path / "requirements.txt"
        req_file.write_text("flask\nrequests\nnumpy>=1.20\n", encoding='utf-8')
        
        result = check_dependencies(str(req_file))
        assert result["stats"]["unpinned_count"] > 0


# ===== api_doc_builder 测试 =====

class TestApiDocBuilder:
    """测试 API 文档构建器"""

    def test_build_flask_api(self, tmp_path):
        """测试构建 Flask API 文档"""
        from tools.api_doc_builder import build_api_doc
        
        routes_file = tmp_path / "routes.py"
        routes_file.write_text('''
from flask import Flask
app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    return []

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return {}

@app.route('/users', methods=['POST'])
def create_user():
    return {}
''', encoding='utf-8')
        
        result = build_api_doc(str(routes_file))
        assert result["endpoints_found"] >= 2
        assert "openapi_spec" in result
        spec = result["openapi_spec"]
        assert spec["openapi"] == "3.0.3"

    def test_build_fastapi_doc(self, tmp_path):
        """测试构建 FastAPI 文档"""
        from tools.api_doc_builder import build_api_doc
        
        routes_file = tmp_path / "main.py"
        routes_file.write_text('''
from fastapi import APIRouter
router = APIRouter()

@router.get("/items")
def list_items():
    return []

@router.post("/items")
def create_item():
    return {}
''', encoding='utf-8')
        
        result = build_api_doc(str(routes_file))
        assert result["endpoints_found"] >= 2

    def test_build_express_api(self, tmp_path):
        """测试构建 Express API 文档"""
        from tools.api_doc_builder import build_api_doc
        
        routes_file = tmp_path / "routes.js"
        routes_file.write_text('''
app.get('/api/users', (req, res) => { res.json([]); });
app.post('/api/users', (req, res) => { res.json({}); });
router.delete('/api/users/:id', handler);
''', encoding='utf-8')
        
        result = build_api_doc(str(routes_file))
        assert result["endpoints_found"] >= 2

    def test_build_nonexistent(self):
        """测试不存在的路径"""
        from tools.api_doc_builder import build_api_doc
        
        result = build_api_doc("/nonexistent")
        assert "error" in result


# ===== MCP Server 集成测试 =====

class TestMcpServerV3Integration:
    """测试 MCP Server v3 集成"""

    def test_tools_registry_has_v3_tools(self):
        """测试工具注册表包含 v3 工具"""
        from mcp_server_v2 import TOOLS_REGISTRY
        
        v3_tools = [
            "file_analyzer", "prompt_engineer", "code_explainer",
            "error_analyzer", "batch_processor", "docs_generator",
            "test_generator", "refactoring_suggester", "dependency_checker",
            "api_doc_builder"
        ]
        
        for tool in v3_tools:
            assert tool in TOOLS_REGISTRY, f"工具 {tool} 未注册"
            assert "inputSchema" in TOOLS_REGISTRY[tool]

    def test_tools_count(self):
        """测试工具总数"""
        from mcp_server_v2 import TOOLS_REGISTRY
        
        # v2 有 12 个 + v3 新增 10 个 = 22 个
        assert len(TOOLS_REGISTRY) == 22


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
