#!/usr/bin/env python3
"""
短剧数据分析工具
统计剧本库数据，生成分析报告
"""

import os
import re
import json
import sys
from pathlib import Path
from collections import Counter
from datetime import datetime


def analyze_drama(filepath: dict) -> dict:
    """分析单个剧本"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题
        title_match = re.search(r'#\s*《(.+?)》', content)
        title = title_match.group(1) if title_match else Path(filepath).stem
        
        # 提取集数
        episodes = re.findall(r'##\s*第(\d+)集[：:]', content)
        ep_count = len(episodes)
        
        # 提取字数
        words = len(re.sub(r'\s+', '', content))
        
        # 提取对话数量
        dialogues = re.findall(r'"([^"]+)"', content)
        dialogue_count = len(dialogues)
        
        # 提取爽点关键词频率
        shuang_keywords = ['冷笑', '怒', '杀', '废', '滚', '找死', '放肆', '你敢', '呵', '竟敢', '居然']
        shuang_count = sum(content.count(kw) for kw in shuang_keywords)
        
        # 估算阅读时间（每分钟300字）
        read_time = words // 300
        
        return {
            'title': title,
            'file': filepath,
            'episodes': ep_count,
            'words': words,
            'dialogues': dialogue_count,
            'shuang_count': shuang_count,
            'read_time': read_time
        }
    except Exception as e:
        return {
            'title': Path(filepath).stem,
            'file': filepath,
            'episodes': 0,
            'words': 0,
            'dialogues': 0,
            'shuang_count': 0,
            'read_time': 0,
            'error': str(e)
        }


def classify_genre(title: str, content: str = '') -> str:
    """根据标题和内容分类类型"""
    genre_keywords = {
        '玄幻重生': ['重生', '剑', '仙', '帝', '皇', '魂', '灵'],
        '都市异能': ['龙', '医', '神', '兵王', '战神', '总裁'],
        '都市豪门': ['豪门', '弃少', '逆袭', '少爷'],
        '悬疑推理': ['迷雾', '追凶', '案', '侦', '谜'],
        '历史穿越': ['赘婿', '大唐', '穿越', '王爷', '将军'],
        '都市甜宠': ['情缘', '替身', '前妻', '妻']
    }
    
    # 从标题判断
    for genre, keywords in genre_keywords.items():
        if any(kw in title for kw in keywords):
            return genre
    
    # 从内容判断
    for genre, keywords in genre_keywords.items():
        if content and any(kw in content for kw in keywords):
            return genre
    
    return '其他'


def scan_and_analyze(drama_dir: str) -> dict:
    """扫描并分析所有剧本"""
    drama_path = Path(drama_dir)
    
    if not drama_path.exists():
        print(f"目录不存在: {drama_dir}", file=sys.stderr)
        return {}
    
    dramas = []
    for ep_dir in drama_path.iterdir():
        if ep_dir.is_dir():
            for md_file in ep_dir.glob('*.md'):
                if '_完整剧本' in md_file.name:
                    result = analyze_drama(str(md_file))
                    result['genre'] = classify_genre(result['title'])
                    dramas.append(result)
    
    return {
        'total': len(dramas),
        'dramas': dramas,
        'generated_at': datetime.now().isoformat()
    }


def generate_stats(data: dict) -> dict:
    """生成统计数据"""
    if not data or 'dramas' not in data:
        return {}
    
    dramas = data['dramas']
    
    # 类型分布
    genre_counter = Counter(d['genre'] for d in dramas)
    
    # 集数统计
    ep_counts = [d['episodes'] for d in dramas]
    
    # 字数统计
    word_counts = [d['words'] for d in dramas]
    
    # 爽点统计
    shuang_counts = [d['shuang_count'] for d in dramas]
    
    return {
        'total_dramas': len(dramas),
        'total_episodes': sum(ep_counts),
        'total_words': sum(word_counts),
        'avg_episodes': sum(ep_counts) / len(ep_counts) if ep_counts else 0,
        'avg_words': sum(word_counts) / len(word_counts) if word_counts else 0,
        'genre_distribution': dict(genre_counter),
        'episodes_range': f"{min(ep_counts)}-{max(ep_counts)}" if ep_counts else "0-0",
        'words_range': f"{min(word_counts)//1000}k-{max(word_counts)//1000}k" if word_counts else "0k-0k",
        'top_shuang': sorted(dramas, key=lambda x: x['shuang_count'], reverse=True)[:3]
    }


def print_report(stats: dict, data: dict):
    """打印分析报告"""
    print("\n" + "="*60)
    print("📊 短剧库数据分析报告")
    print("="*60)
    print(f"生成时间: {stats.get('generated_at', 'N/A')}")
    print("-"*60)
    
    # 总体统计
    print("\n📈 总体统计")
    print(f"  剧本数量: {stats.get('total_dramas', 0)} 部")
    print(f"  总集数: {stats.get('total_episodes', 0)} 集")
    print(f"  总字数: {stats.get('total_words', 0)//10000}万字")
    print(f"  平均每部: {stats.get('avg_episodes', 0):.1f}集, {stats.get('avg_words', 0)//1000}千字")
    
    # 类型分布
    print("\n🎭 类型分布")
    for genre, count in sorted(stats.get('genre_distribution', {}).items(), key=lambda x: -x[1]):
        bar = '█' * count
        print(f"  {genre:10s}: {bar} ({count})")
    
    # 爽点排行
    print("\n🔥 爽点密度排行 (TOP 3)")
    for i, d in enumerate(stats.get('top_shuang', []), 1):
        print(f"  {i}. {d['title']} ({d['shuang_count']}次)")
    
    # 详细列表
    print("\n📋 剧本列表")
    print(f"  {'序号':<4} {'剧名':<20} {'类型':<10} {'集数':<6} {'字数':<8}")
    print("  " + "-"*50)
    for i, d in enumerate(stats.get('dramas', []), 1):
        print(f"  {i:<4} {d['title']:<20} {d.get('genre', '未知'):<10} {d['episodes']:<6} {d['words']//1000}千")
    
    print("\n" + "="*60)


def save_data(data: dict, stats: dict):
    """保存分析数据"""
    output_dir = Path('data/stats')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存原始数据
    with open(output_dir / 'drama_stats.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 保存统计数据
    with open(output_dir / 'analysis_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 数据已保存到 data/stats/")


def main():
    """主函数"""
    drama_dir = sys.argv[1] if len(sys.argv) > 1 else '../awesome-ai-short-drama/short-dramas'
    
    print(f"🔍 分析目录: {drama_dir}")
    
    # 扫描分析
    data = scan_and_analyze(drama_dir)
    
    if not data.get('dramas'):
        print("未找到剧本文件")
        sys.exit(1)
    
    # 生成统计
    stats = generate_stats(data)
    
    # 打印报告
    print_report(stats, data)
    
    # 保存数据
    save_data(data, stats)
    
    print(f"\n✅ 分析完成!")


if __name__ == '__main__':
    main()
