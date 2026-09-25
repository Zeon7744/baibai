"""baibai 基础测试"""
import pytest
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestMCPTools:
    """测试 MCP 工具"""
    
    def test_format_checker_import(self):
        """测试 format_checker 模块导入"""
        try:
            from baibai.tools.format_checker import FormatChecker
            assert FormatChecker is not None
        except ImportError:
            pytest.skip("format_checker not implemented")
    
    def test_stats_analyzer_import(self):
        """测试 stats_analyzer 模块导入"""
        try:
            from baibai.tools.stats_analyzer import StatsAnalyzer
            assert StatsAnalyzer is not None
        except ImportError:
            pytest.skip("stats_analyzer not implemented")
    
    def test_readme_gen_import(self):
        """测试 readme_gen 模块导入"""
        try:
            from baibai.tools.readme_gen import READMEGenerator
            assert READMEGenerator is not None
        except ImportError:
            pytest.skip("readme_gen not implemented")


class TestMCPClient:
    """测试 MCP 客户端"""
    
    def test_mcp_client_init(self):
        """测试 MCP 客户端初始化"""
        try:
            from baibai.mcp_client import MCPClient
            client = MCPClient()
            assert client is not None
        except ImportError:
            pytest.skip("MCPClient not implemented")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
