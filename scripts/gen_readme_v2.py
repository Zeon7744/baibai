#!/usr/bin/env python3
"""
README 自动生成器 - 修复版
根据剧本库内容自动生成 README 短剧列表部分
"""

import os
import re
import sys
from pathlib import Path


def extract_info(filepath: str) -> dict:
    """从剧本文件提取信息"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题
        title_match = re.search(r'#\s*《(.+?)》', content)
        title = title_match.group(1) if title_match else Path(filepath).stem.replace('_完整剧本', '')
        
        # 提取集数
        episodes = re.findall(r'##\s*第(\d+)集[：:]', content)
        ep_count = len(episodes)
        
        # 提取字数
        words = len(re.sub(r'\s+', '', content))
        
        # 提取目录路径（相对路径）
        rel_path = filepath.replace(os.getcwd() + '/', '')
        dir_name = Path(filepath).parent.name
        file_name = Path(filepath).name
        
        return {
            'title': title,
            'episodes': ep_count,
            'words': words,
            'dir': dir_name,
            'file': file_name,
            'rel_path': f"short-dramas/{dir_name}/{file_name}"
        }
    except Exception as e:
        return {
            'title': Path(filepath).stem.replace('_完整剧本', ''),
            'episodes': 0,
            'words': 0,
            'rel_path': '',
            'error': str(e)
        }


def classify_genre(title: str) -> str:
    """分类类型"""
    genre_map = {
        '玄幻重生': ['重生', '剑', '仙', '帝', '皇', '魂', '灵'],
        '都市异能': ['龙', '医', '神', '兵王', '战神', '总裁'],
        '都市豪门': ['豪门', '弃少', '逆袭', '少爷'],
        '悬疑推理': ['迷雾', '追凶', '案', '侦', '谜'],
        '历史穿越': ['赘婿', '大唐', '穿越', '王爷', '将军'],
        '都市甜宠': ['情缘', '替身', '前妻', '妻']
    }
    
    for genre, keywords in genre_map.items():
        if any(kw in title for kw in keywords):
            return genre
    
    return '其他'


def generate_readme_section(drama_dir: str) -> str:
    """生成 README 短剧列表部分"""
    drama_path = Path(drama_dir)
    
    if not drama_path.exists():
        return ""
    
    # 收集所有剧本
    dramas = []
    for ep_dir in drama_path.iterdir():
        if ep_dir.is_dir():
            for md_file in ep_dir.glob('*_完整剧本.md'):
                info = extract_info(str(md_file))
                info['genre'] = classify_genre(info['title'])
                dramas.append(info)
    
    # 按标题排序
    dramas.sort(key=lambda x: x['title'])
    
    # 生成表格
    lines = []
    lines.append("## 🎬 短剧剧本库")
    lines.append("")
    lines.append(f"本仓库收录 **{len(dramas)}部完整短剧剧本**，符合红果短剧平台规范（≤15字对话、≥3爽点/集）。详见 [short-dramas/](short-dramas/)。")
    lines.append("")
    lines.append("| 序号 | 剧名 | 类型 | 集数 | 剧本文件 |")
    lines.append("|------|------|------|------|---------|")
    
    for i, d in enumerate(dramas, 1):
        name = d['title']
        genre = d['genre']
        eps = d['episodes']
        file_link = f"[查看]({d['rel_path']})"
        lines.append(f"| {i} | **{name}** | {genre} | {eps}集 | {file_link} |")
    
    lines.append("")
    lines.append("> 📌 剧本创作规范：标题第X集：集名 · 结尾第X集完 · 对话≤15字 · 每集≥3爽点+1甜点")
    lines.append("")
    
    return '\n'.join(lines)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python gen_readme.py <drama_dir>")
        sys.exit(1)
    
    drama_dir = sys.argv[1]
    
    # 生成并输出
    section = generate_readme_section(drama_dir)
    print(section)


if __name__ == '__main__':
    main()
