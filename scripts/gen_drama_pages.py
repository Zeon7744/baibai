#!/usr/bin/env python3
"""
短剧详情页生成器
为每部短剧生成独立的展示页面
"""

import os
import re
import json
import sys
from pathlib import Path
from datetime import datetime


def hex_to_rgb(hex_color: str) -> tuple:
    """转换十六进制颜色为RGB元组"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def extract_drama_info(filepath: str) -> dict:
    """从剧本文件提取完整信息"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题
        title_match = re.search(r'#\s*《(.+?)》', content)
        title = title_match.group(1) if title_match else Path(filepath).stem.replace('_完整剧本', '')
        
        # 提取角色表
        characters = []
        char_pattern = r'\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|'
        for match in re.finditer(char_pattern, content):
            characters.append({
                'name': match.group(1),
                'role': match.group(2),
                'tags': match.group(3)
            })
        
        # 提取所有集数
        episodes = []
        ep_pattern = r'##\s*第(\d+)集[：:]\s*(.+?)(?=\n##\s*第|$)'
        for match in re.finditer(ep_pattern, content, re.DOTALL):
            ep_num = int(match.group(1))
            ep_content = match.group(2).strip()
            lines = ep_content.split('\n')
            ep_title = lines[0].strip() if lines else ''
            words = len(re.sub(r'\s+', '', ep_content))
            shuang_keywords = ['冷笑', '怒', '杀', '废', '滚', '找死', '放肆', '你敢', '呵', '竟敢', '居然']
            shuang_count = sum(1 for kw in shuang_keywords if kw in ep_content)
            
            episodes.append({
                'num': ep_num,
                'title': ep_title,
                'words': words,
                'shuang_count': shuang_count
            })
        
        total_words = len(re.sub(r'\s+', '', content))
        dialogues = re.findall(r'"([^"]+)"', content)
        total_shuang = sum(ep['shuang_count'] for ep in episodes)
        
        return {
            'title': title,
            'characters': characters,
            'episodes': episodes,
            'total_episodes': len(episodes),
            'total_words': total_words,
            'dialogue_count': len(dialogues),
            'total_shuang': total_shuang,
            'shuang_density': round(total_shuang / len(episodes), 1) if episodes else 0,
            'file': filepath
        }
    except Exception as e:
        return {
            'title': Path(filepath).stem,
            'characters': [],
            'episodes': [],
            'total_episodes': 0,
            'total_words': 0,
            'dialogue_count': 0,
            'total_shuang': 0,
            'shuang_density': 0,
            'error': str(e)
        }


def classify_genre(title: str) -> tuple:
    """分类类型，返回类型名和颜色"""
    genre_map = {
        '玄幻重生': ('xuanhuan', '#a855f7'),
        '都市异能': ('dushi', '#3b82f6'),
        '都市豪门': ('haomen', '#f59e0b'),
        '悬疑推理': ('xuanyi', '#ef4444'),
        '历史穿越': ('lishi', '#22c55e'),
        '都市甜宠': ('tianchong', '#ec4899')
    }
    
    for genre, (key, color) in genre_map.items():
        if any(kw in title for kw in genre.replace('玄幻重生', '').replace('都市', '')):
            return genre, key, color
    
    if any(kw in title for kw in ['重生', '剑', '仙', '帝', '皇', '魂']):
        return '玄幻重生', 'xuanhuan', '#a855f7'
    if any(kw in title for kw in ['龙', '医', '神', '兵王', '战神', '总裁']):
        return '都市异能', 'dushi', '#3b82f6'
    if any(kw in title for kw in ['豪门', '弃少', '逆袭', '少爷']):
        return '都市豪门', 'haomen', '#f59e0b'
    if any(kw in title for kw in ['迷雾', '追凶', '案', '侦', '谜']):
        return '悬疑推理', 'xuanyi', '#ef4444'
    if any(kw in title for kw in ['赘婿', '大唐', '穿越', '王爷']):
        return '历史穿越', 'lishi', '#22c55e'
    if any(kw in title for kw in ['情缘', '替身', '前妻', '妻']):
        return '都市甜宠', 'tianchong', '#ec4899'
    
    return '其他', 'other', '#64748b'


def generate_drama_page(info: dict, output_path: str):
    """生成单部短剧的展示页"""
    title = info['title']
    genre, genre_key, color = classify_genre(title)
    r, g, b = hex_to_rgb(color)
    
    # 生成角色表格 HTML
    chars_html = ''
    for char in info['characters'][:5]:
        chars_html += f'''
            <tr>
                <td><strong>{char['name']}</strong></td>
                <td>{char['role']}</td>
                <td>{char['tags']}</td>
            </tr>'''
    
    # 生成集数列表 HTML
    eps_html = ''
    for ep in info['episodes'][:10]:
        eps_html += f'''
            <tr>
                <td>第{ep['num']}集</td>
                <td>{ep['title'][:30]}{'...' if len(ep['title']) > 30 else ''}</td>
                <td>{ep['words']}字</td>
                <td>{ep['shuang_count']}次</td>
            </tr>'''
    
    if len(info['episodes']) > 10:
        eps_html += f'<tr><td colspan="4" style="text-align:center;color:var(--text-muted)">... 还有 {len(info["episodes"])-10} 集 ...</td></tr>'
    
    # 生成爽点分布条形图
    shuang_bars = ''
    max_shuang = max((ep['shuang_count'] for ep in info['episodes']), default=1)
    for ep in info['episodes'][:15]:
        width = int(ep['shuang_count'] / max_shuang * 100) if max_shuang > 0 else 0
        shuang_bars += f'''
            <div class="shuang-bar">
                <span class="bar-label">第{ep['num']}集</span>
                <div class="bar-track">
                    <div class="bar-fill" style="width:{width}%;background:{color}"></div>
                </div>
                <span class="bar-value">{ep['shuang_count']}</span>
            </div>'''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Baibai 短剧库</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{
            --primary: {color};
            --bg: #0f172a;
            --bg-card: #1e293b;
            --bg-hover: #334155;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --border: #334155;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 40px 20px; }}
        .back-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: var(--text-muted);
            text-decoration: none;
            margin-bottom: 30px;
            transition: color 0.2s;
        }}
        .back-link:hover {{ color: var(--primary); }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .genre-tag {{
            display: inline-block;
            padding: 6px 16px;
            background: rgba({r}, {g}, {b}, 0.2);
            color: {color};
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 16px;
        }}
        h1 {{
            font-size: 36px;
            font-weight: 800;
            margin-bottom: 12px;
        }}
        .stats-row {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 40px;
        }}
        .stat-item {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 28px;
            font-weight: 800;
            color: {color};
        }}
        .stat-label {{
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 4px;
        }}
        .section {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
        }}
        h2 {{
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        th {{
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }}
        tr:hover {{ background: var(--bg-hover); }}
        .shuang-chart {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .shuang-bar {{
            display: grid;
            grid-template-columns: 60px 1fr 40px;
            align-items: center;
            gap: 12px;
        }}
        .bar-label {{ font-size: 12px; color: var(--text-muted); }}
        .bar-track {{
            height: 8px;
            background: var(--border);
            border-radius: 4px;
            overflow: hidden;
        }}
        .bar-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s;
        }}
        .bar-value {{ font-size: 12px; color: var(--text-muted); text-align: right; }}
        .read-btn {{
            display: inline-block;
            padding: 12px 24px;
            background: {color};
            color: white;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: opacity 0.2s;
        }}
        .read-btn:hover {{ opacity: 0.9; }}
        @media (max-width: 600px) {{
            .stats-row {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-link">← 返回短剧库</a>
        
        <div class="header">
            <span class="genre-tag">{genre}</span>
            <h1>{title}</h1>
        </div>
        
        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-value">{info['total_episodes']}</div>
                <div class="stat-label">集数</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{info['total_words']//1000}k</div>
                <div class="stat-label">字数</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{info['total_shuang']}</div>
                <div class="stat-label">爽点</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{info['shuang_density']}</div>
                <div class="stat-label">爽点/集</div>
            </div>
        </div>
        
        {f'''
        <div class="section">
            <h2>👥 主要角色</h2>
            <table>
                <thead>
                    <tr><th>角色</th><th>身份</th><th>标签</th></tr>
                </thead>
                <tbody>
                    {chars_html}
                </tbody>
            </table>
        </div>
        ''' if info['characters'] else ''}
        
        <div class="section">
            <h2>🔥 爽点密度分布</h2>
            <div class="shuang-chart">
                {shuang_bars}
            </div>
        </div>
        
        <div class="section">
            <h2>📖 剧集列表</h2>
            <table>
                <thead>
                    <tr><th>集数</th><th>标题</th><th>字数</th><th>爽点</th></tr>
                </thead>
                <tbody>
                    {eps_html}
                </tbody>
            </table>
        </div>
        
        <div style="text-align: center; margin-top: 40px;">
            <a href="https://github.com/Zeon7744/awesome-ai-short-drama/tree/main/short-dramas/{{ title }}" class="read-btn" target="_blank">查看完整剧本</a>
        </div>
    </div>
</body>
</html>'''
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_path


def main():
    """主函数"""
    drama_dir = sys.argv[1] if len(sys.argv) > 1 else '../awesome-ai-short-drama/short-dramas'
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'pages/dramas'
    
    drama_path = Path(drama_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"🎬 生成短剧详情页")
    print(f"   源目录: {drama_dir}")
    print(f"   输出目录: {output_dir}")
    print("-" * 50)
    
    count = 0
    for ep_dir in drama_path.iterdir():
        if ep_dir.is_dir():
            for md_file in ep_dir.glob('*_完整剧本.md'):
                info = extract_drama_info(str(md_file))
                if info.get('error'):
                    print(f"❌ {info['title']}: {info['error']}")
                    continue
                
                output_file = output_path / f"{info['title']}.html"
                generate_drama_page(info, str(output_file))
                print(f"✅ {info['title']} ({info['total_episodes']}集, {info['total_shuang']}爽点)")
                count += 1
    
    print("-" * 50)
    print(f"完成！共生成 {count} 个页面")


if __name__ == '__main__':
    main()
