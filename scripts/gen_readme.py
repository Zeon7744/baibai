#!/usr/bin/env python3
"""
README 自动生成器
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
        title = title_match.group(1) if title_match else Path(filepath).stem
        
        # 提取集数
        episodes = re.findall(r'##\s*第(\d+)集[：:]', content)
        ep_count = len(episodes)
        
        # 提取字数
        words = len(re.sub(r'\s+', '', content))
        
        return {
            'title': title,
            'episodes': ep_count,
            'words': words,
            'file': filepath
        }
    except Exception as e:
        return {
            'title': Path(filepath).stem,
            'episodes': 0,
            'words': 0,
            'error': str(e)
        }


def classify_genre(title: str, content: str = '') -> str:
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


def generate_readme_section(drama_dir: str, start_index: int = 1) -> str:
    """生成 README 短剧列表部分"""
    drama_path = Path(drama_dir)
    
    if not drama_path.exists():
        return ""
    
    # 收集所有剧本
    dramas = []
    for ep_dir in drama_path.iterdir():
        if ep_dir.is_dir():
            for md_file in ep_dir.glob('*.md'):
                if '_完整剧本' in md_file.name:
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
    
    for i, d in enumerate(dramas, start_index):
        name = d['title']
        genre = d['genre']
        eps = d['episodes']
        file_link = f"[查看](short-dramas/{name}/{name}_完整剧本.md)"
        lines.append(f"| {i} | **{name}** | {genre} | {eps}集 | {file_link} |")
    
    lines.append("")
    lines.append("> 📌 剧本创作规范：标题第X集：集名 · 结尾第X集完 · 对话≤15字 · 每集≥3爽点+1甜点")
    lines.append("")
    
    return '\n'.join(lines)


def update_readme(readme_path: str, drama_dir: str):
    """更新 README 文件"""
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 生成新的短剧列表
    new_section = generate_readme_section(drama_dir)
    
    # 找到旧短剧列表位置并替换
    # 匹配从 "## 🎬 短剧剧本库" 到下一个 "##" 之前的内容
    pattern = r'(##\s*🎬\s*短剧剧本库.*?)(?=\n##\s*|$)'
    
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, new_section.strip() + '\n', content, flags=re.DOTALL)
    else:
        # 如果没有找到，追加到短剧项目部分之后
        insert_pos = content.find('## 🎬 短剧项目')
        if insert_pos > 0:
            # 找到这个部分的结尾
            next_section = content.find('\n## ', insert_pos + 1)
            if next_section > 0:
                new_content = content[:next_section] + '\n\n' + new_section + '\n' + content[next_section:]
            else:
                new_content = content + '\n\n' + new_section
        else:
            new_content = content + '\n\n' + new_section
    
    # 清理重复内容
    new_content = re.sub(r'(##\s*🎬\s*短剧项目\n-.*?\n){2,}', '', new_content, flags=re.DOTALL)
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ README 已更新: {readme_path}")


def main():
    """主函数"""
    readme_path = sys.argv[1] if len(sys.argv) > 1 else '../awesome-ai-short-drama/README.md'
    drama_dir = sys.argv[2] if len(sys.argv) > 2 else '../awesome-ai-short-drama/short-dramas'
    
    print(f"📝 生成 README 短剧列表")
    print(f"   README: {readme_path}")
    print(f"   剧本目录: {drama_dir}")
    
    # 生成并预览
    preview = generate_readme_section(drama_dir)
    print("\n预览:")
    print(preview)
    
    # 更新文件
    update_readme(readme_path, drama_dir)
    
    print(f"\n✅ 完成!")


if __name__ == '__main__':
    main()
