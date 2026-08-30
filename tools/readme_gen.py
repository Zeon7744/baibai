#!/usr/bin/env python3
"""
README 生成器 - 根据内容库自动生成 README 文档
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime


def extract_info(filepath: str) -> dict:
    """从内容文件提取信息"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题
        title_match = re.search(r'^#\s*(.+?)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else Path(filepath).stem
        
        # 提取章节数
        sections = re.findall(r'^##\s+.+$', content, re.MULTILINE)
        section_count = len(sections)
        
        # 提取字数
        words = len(re.sub(r'\s+', '', content))
        
        return {
            'title': title,
            'sections': section_count,
            'words': words,
            'file': filepath
        }
    except Exception as e:
        return {
            'title': Path(filepath).stem,
            'sections': 0,
            'words': 0,
            'error': str(e)
        }


def classify_content(title: str, content: str = '') -> str:
    """分类内容类型"""
    type_map = {
        '短剧剧本': ['重生', '逆袭', '总裁', '赘婿', '情缘', '豪门', '帝', '皇'],
        '短篇小说': ['故事', '小说', '篇'],
        '教程文档': ['教程', '指南', '说明', '文档'],
        '工具脚本': ['工具', '脚本', 'check', 'analyze']
    }
    
    combined = f"{title} {content}"
    
    for content_type, keywords in type_map.items():
        if any(kw in combined for kw in keywords):
            return content_type
    
    return '其他'


def generate_content_section(content_dir: str) -> str:
    """生成内容列表部分"""
    content_path = Path(content_dir)
    
    if not content_path.exists():
        return ""
    
    # 收集所有内容
    contents = []
    for md_file in content_path.glob("**/*.md"):
        if md_file.is_file():
            info = extract_info(str(md_file))
            info['type'] = classify_content(info['title'])
            contents.append(info)
    
    # 按标题排序
    contents.sort(key=lambda x: x['title'])
    
    # 生成表格
    lines = []
    lines.append("## 📚 内容库")
    lines.append("")
    lines.append(f"本仓库收录 **{len(contents)} 个内容文件**，涵盖短剧剧本、短篇小说、教程文档等。")
    lines.append("")
    lines.append("| 序号 | 名称 | 类型 | 章节 | 字数 |")
    lines.append("|------|------|------|------|------|")
    
    for i, c in enumerate(contents, 1):
        name = c['title'][:20] if c['title'] else c['file'].split('/')[-1][:20]
        type_ = c['type']
        sections = c['sections']
        words = f"{c['words']//1000}千" if c['words'] >= 1000 else f"{c['words']}"
        lines.append(f"| {i} | **{name}** | {type_} | {sections} | {words} |")
    
    lines.append("")
    return '\n'.join(lines)


def update_readme(readme_path: str, content_dir: str):
    """更新 README 文件"""
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 生成新的内容列表
    new_section = generate_content_section(content_dir)
    
    # 找到旧内容列表位置并替换
    pattern = r'(##\s*📚\s*内容库.*?)(?=\n##\s*|$)'
    
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, new_section.strip() + '\n', content, flags=re.DOTALL)
    else:
        # 如果没有找到，追加到项目简介之后
        insert_pos = content.find("## 🛠️ 工具链")
        if insert_pos > 0:
            new_content = content[:insert_pos] + new_section + '\n' + content[insert_pos:]
        else:
            new_content = content + '\n\n' + new_section
    
    # 清理重复内容
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ README 已更新: {readme_path}")


def main():
    """主函数"""
    readme_path = sys.argv[1] if len(sys.argv) > 1 else "README.md"
    content_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    print(f"📝 生成 README 内容列表")
    print(f"   README: {readme_path}")
    print(f"   内容目录: {content_dir}")
    
    # 生成并预览
    preview = generate_content_section(content_dir)
    print("\n预览:")
    print(preview)
    
    # 更新文件
    update_readme(readme_path, content_dir)
    
    print(f"\n✅ 完成!")


if __name__ == '__main__':
    main()
