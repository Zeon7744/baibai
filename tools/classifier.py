#!/usr/bin/env python3
"""
内容分类器 - 自动识别和分类内容类型
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple


# 内容类型定义
CONTENT_TYPES = {
    '短剧剧本': {
        'keywords': ['重生', '逆袭', '总裁', '赘婿', '情缘', '豪门', '帝', '皇', '剑', '仙', '龙', '医'],
        'patterns': [r'^#\s*《.+》', r'##\s*第\d+集'],
        'description': '短剧剧本文件'
    },
    '短篇小说': {
        'keywords': ['故事', '小说', '篇', '章', '节'],
        'patterns': [r'^#\s*[^\n]+$', r'##\s*[一二三四五六七八九十]'],
        'description': '短篇小说或章节'
    },
    '教程文档': {
        'keywords': ['教程', '指南', '说明', '文档', 'howto', 'guide', 'tutorial'],
        'patterns': [r'^#\s*[^\n]*[教程指南说明文档]', r'##\s*(步骤|安装|使用|配置)'],
        'description': '教程或技术文档'
    },
    '工具脚本': {
        'keywords': ['工具', '脚本', 'check', 'analyze', 'gen', 'helper'],
        'patterns': [r'#!/usr/bin/env python', r'def main'],
        'description': '自动化脚本或工具'
    },
    '配置文件': {
        'keywords': ['config', 'settings', 'yaml', 'json', 'toml', 'ini'],
        'patterns': [r'^\s*[\{\[]', r'^\s*\w+\s*:\s*'],
        'description': '配置文件'
    },
    '其他': {
        'keywords': [],
        'patterns': [],
        'description': '未分类内容'
    }
}


def classify_content(filepath: str) -> Dict:
    """分类单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(2000)  # 只读取前2000字符
        
        filename = Path(filepath).name
        title_match = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else filename
        
        # 计算得分
        scores = {}
        for content_type, info in CONTENT_TYPES.items():
            score = 0
            
            # 关键词匹配
            for kw in info['keywords']:
                if kw.lower() in content.lower() or kw.lower() in filename.lower():
                    score += 1
            
            # 模式匹配
            for pattern in info['patterns']:
                if re.search(pattern, content, re.MULTILINE):
                    score += 2
            
            scores[content_type] = score
        
        # 选择最高分
        best_type = max(scores, key=scores.get)
        
        return {
            'file': filepath,
            'name': filename,
            'title': title,
            'type': best_type,
            'description': CONTENT_TYPES[best_type]['description'],
            'scores': scores
        }
    
    except Exception as e:
        return {
            'file': filepath,
            'name': Path(filepath).name,
            'title': '',
            'type': '其他',
            'description': f'错误: {str(e)}',
            'scores': {}
        }


def scan_and_classify(directory: str) -> List[Dict]:
    """扫描并分类目录中的所有文件"""
    dir_path = Path(directory)
    
    if not dir_path.exists():
        print(f"目录不存在: {directory}", file=sys.stderr)
        return []
    
    results = []
    for file_path in dir_path.glob("**/*"):
        if file_path.is_file() and file_path.suffix in ['.md', '.txt', '.py', '.json', '.yaml', '.yml', '.toml']:
            result = classify_content(str(file_path))
            results.append(result)
    
    return results


def print_classification(results: List[Dict]):
    """打印分类结果"""
    print("\n" + "="*60)
    print("📂 内容分类报告")
    print("="*60)
    
    # 按类型分组
    grouped = {}
    for r in results:
        type_ = r['type']
        if type_ not in grouped:
            grouped[type_] = []
        grouped[type_].append(r)
    
    # 打印每个类型
    for type_, items in grouped.items():
        print(f"\n📌 {type_} ({len(items)}个)")
        print("-"*40)
        for item in items:
            title = item['title'][:30] if item['title'] else item['name'][:30]
            print(f"  • {title}")
    
    # 统计汇总
    print("\n" + "="*60)
    print("📊 分类统计")
    print("="*60)
    for type_, items in sorted(grouped.items(), key=lambda x: -len(x[1])):
        bar = '█' * len(items)
        print(f"  {type_:12s}: {bar} ({len(items)})")
    print("="*60)


def save_results(results: List[Dict], output_path: str = "data/classification.json"):
    """保存分类结果"""
    import json
    from pathlib import Path
    
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 结果已保存: {output_path}")


def main():
    """主函数"""
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    output = sys.argv[2] if len(sys.argv) > 2 else "data/classification.json"
    
    print(f"🔍 扫描目录: {directory}")
    
    results = scan_and_classify(directory)
    
    if not results:
        print("未找到文件")
        sys.exit(1)
    
    print_classification(results)
    save_results(results, output)
    
    print(f"\n✅ 完成! 共分类 {len(results)} 个文件")


if __name__ == '__main__':
    main()
