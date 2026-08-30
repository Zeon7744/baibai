#!/usr/bin/env python3
"""
数据分析工具 - 统计内容数据，生成分析报告
"""

import os
import re
import json
import sys
from pathlib import Path
from collections import Counter
from datetime import datetime


def analyze_content(filepath: str) -> dict:
    """分析单个内容文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        name = Path(filepath).stem
        
        # 提取标题
        title_match = re.search(r'#\s*(.+?)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else name
        
        # 提取章节数
        sections = re.findall(r'^##\s+.+$', content, re.MULTILINE)
        section_count = len(sections)
        
        # 提取字数
        words = len(re.sub(r'\s+', '', content))
        
        # 提取对话数量
        dialogues = re.findall(r'"([^"]+)"', content)
        dialogue_count = len(dialogues)
        
        # 估算阅读时间（每分钟300字）
        read_time = words // 300
        
        return {
            'name': name,
            'title': title,
            'sections': section_count,
            'words': words,
            'dialogues': dialogue_count,
            'read_time': read_time
        }
    except Exception as e:
        return {
            'name': Path(filepath).stem,
            'title': '',
            'sections': 0,
            'words': 0,
            'dialogues': 0,
            'read_time': 0,
            'error': str(e)
        }


def classify_content(title: str, content: str = '') -> str:
    """分类内容类型"""
    type_keywords = {
        '短剧剧本': ['重生', '逆袭', '总裁', '赘婿', '情缘', '豪门', '帝', '皇'],
        '短篇小说': ['故事', '小说', '篇'],
        '教程文档': ['教程', '指南', '说明', '文档'],
        '工具脚本': ['工具', '脚本', 'check', 'analyze']
    }
    
    combined = f"{title} {content}"
    
    for content_type, keywords in type_keywords.items():
        if any(kw in combined for kw in keywords):
            return content_type
    
    return '其他'


def scan_and_analyze(content_dir: str) -> dict:
    """扫描并分析所有内容文件"""
    content_path = Path(content_dir)
    
    if not content_path.exists():
        print(f"目录不存在: {content_dir}", file=sys.stderr)
        return {}
    
    contents = []
    for md_file in content_path.glob("**/*.md"):
        if md_file.is_file():
            result = analyze_content(str(md_file))
            result['type'] = classify_content(result['title'], '')
            contents.append(result)
    
    return {
        'total': len(contents),
        'contents': contents,
        'generated_at': datetime.now().isoformat()
    }


def generate_stats(data: dict) -> dict:
    """生成统计数据"""
    if not data or 'contents' not in data:
        return {}
    
    contents = data['contents']
    
    # 类型分布
    type_counter = Counter(c['type'] for c in contents)
    
    # 字数统计
    word_counts = [c['words'] for c in contents]
    
    # 章节统计
    section_counts = [c['sections'] for c in contents]
    
    return {
        'total_items': len(contents),
        'total_words': sum(word_counts),
        'total_sections': sum(section_counts),
        'avg_words': sum(word_counts) / len(word_counts) if word_counts else 0,
        'avg_sections': sum(section_counts) / len(section_counts) if section_counts else 0,
        'type_distribution': dict(type_counter),
        'words_range': f"{min(word_counts)//1000}k-{max(word_counts)//1000}k" if word_counts else "0k-0k",
        'top_by_words': sorted(contents, key=lambda x: x['words'], reverse=True)[:3]
    }


def print_report(stats: dict, data: dict):
    """打印分析报告"""
    print("\n" + "="*60)
    print("📊 内容数据分析报告")
    print("="*60)
    print(f"生成时间: {stats.get('generated_at', 'N/A')}")
    print("-"*60)
    
    # 总体统计
    print("\n📈 总体统计")
    print(f"  内容数量: {stats.get('total_items', 0)} 个")
    print(f"  总字数: {stats.get('total_words', 0)//10000}万字")
    print(f"  总章节: {stats.get('total_sections', 0)} 章")
    print(f"  平均字数: {stats.get('avg_words', 0)//1000}千字")
    
    # 类型分布
    print("\n📂 类型分布")
    for content_type, count in sorted(stats.get('type_distribution', {}).items(), key=lambda x: -x[1]):
        bar = '█' * count
        print(f"  {content_type:12s}: {bar} ({count})")
    
    # 字数排行
    print("\n📝 字数排行 (TOP 3)")
    for i, c in enumerate(stats.get('top_by_words', []), 1):
        print(f"  {i}. {c['title'] or c['name']} ({c['words']//1000}字)")
    
    # 详细列表
    print("\n📋 内容列表")
    print(f"  {'序号':<4} {'名称':<20} {'类型':<10} {'字数':<8}")
    print("  " + "-"*45)
    for i, c in enumerate(stats.get('contents', []), 1):
        title = (c.get('title') or c['name'])[:18]
        print(f"  {i:<4} {title:<20} {c.get('type', '未知'):<10} {c['words']//1000}千")
    
    print("\n" + "="*60)


def save_data(data: dict, stats: dict):
    """保存分析数据"""
    output_dir = Path("data/stats")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / 'content_stats.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    with open(output_dir / 'analysis_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 数据已保存到 data/stats/")


def main():
    """主函数"""
    content_dir = sys.argv[1] if len(sys.argv) > 1 else "../awesome-ai-short-drama/short-dramas"
    
    print(f"🔍 分析目录: {content_dir}")
    
    data = scan_and_analyze(content_dir)
    
    if not data.get('contents'):
        print("未找到内容文件")
        sys.exit(1)
    
    stats = generate_stats(data)
    print_report(stats, data)
    save_data(data, stats)
    
    print(f"\n✅ 分析完成!")


if __name__ == '__main__':
    main()
