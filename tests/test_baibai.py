#!/usr/bin/env python3
"""
测试脚本 - 验证 baibai 工具库
"""

import sys
import os
from pathlib import Path

# 添加 tools 目录到路径（从项目根目录）
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_imports():
    """测试导入"""
    print("🧪 测试导入...")
    
    try:
        import tools
        print("  ✅ tools 包导入成功")
    except ImportError as e:
        print(f"  ❌ tools 包导入失败: {e}")
        return False
    
    try:
        from tools.format_checker import validate_directory
        print("  ✅ format_checker 导入成功")
    except ImportError as e:
        print(f"  ❌ format_checker 导入失败: {e}")
        return False
    
    try:
        from tools.stats_analyzer import scan_and_analyze
        print("  ✅ stats_analyzer 导入成功")
    except ImportError as e:
        print(f"  ❌ stats_analyzer 导入失败: {e}")
        return False
    
    try:
        from tools.readme_gen import generate_content_section
        print("  ✅ readme_gen 导入成功")
    except ImportError as e:
        print(f"  ❌ readme_gen 导入失败: {e}")
        return False
    
    return True


def test_cli():
    """测试 CLI"""
    print("\n🧪 测试 CLI...")
    
    try:
        from tools.cli import print_help
        print("  ✅ CLI 模块导入成功")
    except ImportError as e:
        print(f"  ❌ CLI 模块导入失败: {e}")
        return False
    
    return True


def main():
    """主测试函数"""
    print("="*60)
    print("Baibai 工具库测试")
    print("="*60)
    
    all_passed = True
    
    all_passed &= test_imports()
    all_passed &= test_cli()
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ 所有测试通过!")
    else:
        print("❌ 部分测试失败")
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
