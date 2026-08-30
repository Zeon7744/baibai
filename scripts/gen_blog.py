#!/usr/bin/env python3
"""
创作日志生成器
根据数据统计生成创作日志页面
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def generate_blog_page(stats_file: str, output_file: str):
    """生成创作日志页面"""
    
    # 读取统计数据
    with open(stats_file, 'r', encoding='utf-8') as f:
        stats = json.load(f)
    
    dramas = stats.get('dramas', [])
    
    # 生成剧集列表 HTML
    episodes_html = ''
    for i, d in enumerate(dramas, 1):
        genre_class = {
            '玄幻重生': 'xuanhuan',
            '都市异能': 'dushi',
            '都市豪门': 'haomen',
            '悬疑推理': 'xuanyi',
            '历史穿越': 'lishi',
            '都市甜宠': 'tianchong'
        }.get(d.get('genre', '其他'), 'other')
        
        episodes_html += f'''
            <tr>
                <td>{i}</td>
                <td><strong>{d['title']}</strong></td>
                <td><span class="genre-tag genre-{genre_class}">{d.get('genre', '其他')}</span></td>
                <td>{d['episodes']}集</td>
                <td>{d['words']//1000}k字</td>
                <td>{d['shuang_count']}次</td>
            </tr>'''
    
    # 生成类型分布 HTML
    genre_dist = stats.get('genre_distribution', {})
    genre_bars = ''
    for genre, count in sorted(genre_dist.items(), key=lambda x: -x[1]):
        bar_width = int(count / len(dramas) * 100)
        genre_bars += f'''
            <div class="genre-bar">
                <span class="genre-name">{genre}</span>
                <div class="bar-track">
                    <div class="bar-fill" style="width:{bar_width}%"></div>
                </div>
                <span class="genre-count">{count}部</span>
            </div>'''
    
    # 生成日志条目
    log_entries = ''
    for i, d in enumerate(dramas, 1):
        read_time = d.get('read_time', d['words'] // 300)
        log_entries += f'''
        <div class="log-entry">
            <div class="log-date">作品 {i}</div>
            <div class="log-content">
                <h3>{d['title']}</h3>
                <p>{d.get('genre', '其他')} · {d['episodes']}集 · {d['words']//1000}千字 · 爽点密度 {d['shuang_count']/max(d['episodes'],1):.1f}/集</p>
            </div>
        </div>'''
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>创作日志 - Baibai</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{
            --primary: #6366f1;
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
        h1 {{
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 8px;
        }}
        .subtitle {{
            color: var(--text-muted);
            margin-bottom: 40px;
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
        }}
        table {{ width: 100%; border-collapse: collapse; }}
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
        .genre-tag {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }}
        .genre-xuanhuan {{ background: rgba(168,85,247,0.2); color: #a855f7; }}
        .genre-dushi {{ background: rgba(59,130,246,0.2); color: #3b82f6; }}
        .genre-haomen {{ background: rgba(245,158,11,0.2); color: #f59e0b; }}
        .genre-xuanyi {{ background: rgba(239,68,68,0.2); color: #ef4444; }}
        .genre-lishi {{ background: rgba(34,197,94,0.2); color: #22c55e; }}
        .genre-tianchong {{ background: rgba(236,72,153,0.2); color: #ec4899; }}
        .genre-other {{ background: rgba(100,116,139,0.2); color: #64748b; }}
        .genre-bar {{
            display: grid;
            grid-template-columns: 100px 1fr 60px;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }}
        .genre-name {{ font-size: 14px; }}
        .bar-track {{
            height: 8px;
            background: var(--border);
            border-radius: 4px;
            overflow: hidden;
        }}
        .bar-fill {{
            height: 100%;
            background: var(--primary);
            border-radius: 4px;
        }}
        .genre-count {{ font-size: 14px; color: var(--text-muted); text-align: right; }}
        .log-entry {{
            display: grid;
            grid-template-columns: 100px 1fr;
            gap: 20px;
            padding: 20px 0;
            border-bottom: 1px solid var(--border);
        }}
        .log-entry:last-child {{ border-bottom: none; }}
        .log-date {{
            font-size: 14px;
            color: var(--text-muted);
            padding-top: 4px;
        }}
        .log-content h3 {{
            font-size: 18px;
            margin-bottom: 8px;
        }}
        .log-content p {{
            font-size: 14px;
            color: var(--text-muted);
        }}
        @media (max-width: 600px) {{
            .genre-bar {{ grid-template-columns: 80px 1fr 50px; }}
            .log-entry {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-link">← 返回首页</a>
        
        <h1>📝 创作日志</h1>
        <p class="subtitle">记录每一部作品的创作历程</p>
        
        <div class="section">
            <h2>📊 作品总览</h2>
            <table>
                <thead>
                    <tr><th>#</th><th>剧名</th><th>类型</th><th>集数</th><th>字数</th><th>爽点</th></tr>
                </thead>
                <tbody>
                    {episodes_html}
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>🎭 类型分布</h2>
            <div>
                {genre_bars}
            </div>
        </div>
        
        <div class="section">
            <h2>📖 创作历程</h2>
            <div>
                {log_entries}
            </div>
        </div>
    </div>
</body>
</html>'''
    
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_file


def main():
    """主函数"""
    stats_file = sys.argv[1] if len(sys.argv) > 1 else '../baibai-workflow/data/stats/drama_stats.json'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'pages/blog/index.html'
    
    if not Path(stats_file).exists():
        print(f"❌ 统计文件不存在: {stats_file}")
        sys.exit(1)
    
    output = generate_blog_page(stats_file, output_file)
    print(f"✅ 创作日志已生成: {output}")


if __name__ == '__main__':
    main()
