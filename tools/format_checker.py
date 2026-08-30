#!/usr/bin/env python3
"""
格式校验器 - 检查内容格式是否符合规范
"""

import os
import re
import sys
import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class CheckResult:
    """校验结果"""
    file_path: str
    name: str
    items: int
    total_chars: int
    issues: List[str]
    score: int  # 0-100


def check_markdown_file(filepath: str) -> CheckResult:
    """校验 Markdown 文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        name = Path(filepath).stem
        issues = []
        
        # 检查标题格式
        titles = re.findall(r'^#\s+(.+)$', content, re.MULTILINE)
        if not titles:
            issues.append("缺少一级标题")
        
        # 检查禁止字符
        forbidden = ['耀', '曜']
        for char in forbidden:
            if char in content:
                issues.append(f"包含禁止字符: '{char}'")
        
        # 检查括号格式
        if '【' in content or '】' in content:
            issues.append("包含禁止括号 【】")
        
        # 计算统计
        items = len(re.findall(r'^##\s+', content, re.MULTILINE))
        total_chars = len(content)
        
        # 计算分数
        score = 100
        score -= len(issues) * 15
        score = max(0, min(100, score))
        
        return CheckResult(
            file_path=filepath,
            name=name,
            items=items,
            total_chars=total_chars,
            issues=issues,
            score=score
        )
    except Exception as e:
        return CheckResult(
            file_path=filepath,
            name=Path(filepath).stem,
            items=0,
            total_chars=0,
            issues=[f"解析错误: {str(e)}"],
            score=0
        )


def scan_files(directory: str, pattern: str = "*.md") -> List[str]:
    """扫描目录中的文件"""
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"目录不存在: {directory}", file=sys.stderr)
        return []
    
    files = []
    for md_file in dir_path.glob(f"**/{pattern}"):
        files.append(str(md_file))
    
    return files


def validate_directory(directory: str) -> List[CheckResult]:
    """校验整个目录"""
    files = scan_files(directory)
    results = []
    
    for filepath in files:
        result = check_markdown_file(filepath)
        results.append(result)
    
    return results


def print_report(results: List[CheckResult]):
    """打印校验报告"""
    print("\n" + "="*60)
    print("📋 格式校验报告")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for r in results if r.score >= 80)
    warning = sum(1 for r in results if 60 <= r.score < 80)
    failed = sum(1 for r in results if r.score < 60)
    
    print(f"\n📊 统计: 共 {total} 个文件 | ✅通过 {passed} | ⚠️警告 {warning} | ❌失败 {failed}")
    print("-"*60)
    
    for r in results:
        status = "✅" if r.score >= 80 else "⚠️" if r.score >= 60 else "❌"
        print(f"\n{status} {r.name}")
        print(f"   得分: {r.score}/100 | 内容: {r.items}项, {r.total_chars}字符")
        
        if r.issues:
            print(f"   问题:")
            for issue in r.issues[:5]:
                print(f"      • {issue}")
            if len(r.issues) > 5:
                print(f"      ... 还有 {len(r.issues)-5} 个问题")
    
    print("\n" + "="*60)


def main():
    """主函数"""
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    
    print(f"🔍 扫描目录: {directory}")
    
    results = validate_directory(directory)
    
    if not results:
        print("未找到文件")
        sys.exit(1)
    
    print_report(results)
    
    # 保存 JSON 报告
    output_dir = Path("data/stats")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    json_output = [{
        'name': r.name,
        'items': r.items,
        'chars': r.total_chars,
        'score': r.score,
        'issues': r.issues
    } for r in results]
    
    with open(output_dir / 'format_check.json', 'w', encoding='utf-8') as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 报告已保存: data/stats/format_check.json")


if __name__ == '__main__':
    main()
