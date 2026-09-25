#!/usr/bin/env python3
"""
数字员工自学习体系 - 分析仓库表现并生成优化建议
包含：Stars分析、Issue反馈、PR质量、内容优化
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import requests

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
BASE_DIR = Path('/Coze/Drive/红剑/所有对话/主对话/repo-stats')
LOG_FILE = BASE_DIR / 'self-learning.log'

REPOS = [
    {'name': 'baibai', 'user': 'Zeon7744'},
    {'name': 'awesome-ai-short-drama', 'user': 'Zeon7744'},
    {'name': 'dev-artifacts', 'user': 'Zeon7744'},
]

def log(msg: str):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().isoformat()} {msg}\n")

def api_request(url: str, headers: dict = None) -> dict | None:
    """API 请求封装"""
    default_headers = {'Authorization': f'token {GITHUB_TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
    if headers:
        default_headers.update(headers)
    try:
        r = requests.get(url, headers=default_headers, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log(f"API Error: {url} - {e}")
        return None

def analyze_repo(repo: dict) -> dict:
    """分析单个仓库"""
    result = {'name': repo['name'], 'issues': [], 'prs': [], 'analysis': {}}
    
    # 获取仓库信息
    repo_url = f"https://api.github.com/repos/{repo['user']}/{repo['name']}"
    repo_data = api_request(repo_url)
    if not repo_data:
        return result
    
    result['analysis'] = {
        'stars': repo_data.get('stargazers_count', 0),
        'forks': repo_data.get('forks_count', 0),
        'open_issues': repo_data.get('open_issues_count', 0),
        'watchers': repo_data.get('subscribers_count', 0),
        'language': repo_data.get('language', 'Unknown'),
        'description': repo_data.get('description', ''),
        'updated_at': repo_data.get('pushed_at', ''),
    }
    
    # 分析近期 Issue
    issues = api_request(f"{repo_url}/issues?state=open&per_page=10")
    if issues:
        result['issues'] = [
            {'number': i['number'], 'title': i['title'], 'labels': [l['name'] for l in i.get('labels', [])], 'created': i['created_at'][:10]}
            for i in issues
        ]
    
    # 分析近期 PR
    prs = api_request(f"{repo_url}/pulls?state=all&per_page=10")
    if prs:
        result['pr_analysis'] = []
        for pr in prs:
            stats = api_request(f"{repo_url}/pulls/{pr['number']}")
            if stats and 'additions' in stats and 'deletions' in stats:
                result['pr_analysis'].append({
                    'number': pr['number'],
                    'title': pr['title'],
                    'status': 'merged' if pr['merged_at'] else 'open' if pr['state'] == 'open' else 'closed',
                    'commits': pr.get('commits', 0),
                    'added': stats.get('additions', 0),
                    'deleted': stats.get('deletions', 0),
                })
    
    return result

def generate_insights(repo: dict) -> list:
    """生成优化建议"""
    insights = []
    a = repo['analysis']
    
    # Stars 建议
    if a['stars'] < 5:
        insights.append({
            'type': 'promotion',
            'priority': 'high',
            'message': f"⭐ Stars 较少 ({a['stars']})，建议：1)添加更多中文内容 2)在短剧社区分享 3)优化 README 可见性"
        })
    
    # Issue 反馈建议
    if repo['issues']:
        has_question = any('question' in i['labels'] or '?' in i['title'] for i in repo['issues'])
        if has_question:
            insights.append({
                'type': 'engagement',
                'priority': 'medium',
                'message': f"有 {len(repo['issues'])} 个待处理 Issue，请及时回复以活跃仓库氛围"
            })
    
    # 更新频率建议
    if a['updated_at']:
        days_since = (datetime.now() - datetime.fromisoformat(a['updated_at'].replace('Z', '+00:00'))).days
        if days_since > 30:
            insights.append({
                'type': 'activity',
                'priority': 'low',
                'message': f"仓库 {days_since} 天未更新，建议添加新内容提升活跃度"
            })
    
    # PR 建议
    if repo.get('pr_analysis'):
        merged = [p for p in repo['pr_analysis'] if p['status'] == 'merged']
        if merged:
            insights.append({
                'type': 'contribution',
                'priority': 'medium',
                'message': f"已有 {len(merged)} 个已合并 PR，考虑添加 CONTRIBUTING.md 吸引更多贡献者"
            })
    
    return insights

def main():
    """主执行函数"""
    all_results = []
    all_insights = []
    
    for repo in REPOS:
        result = analyze_repo(repo)
        insights = generate_insights(result)
        result['insights'] = insights
        all_results.append(result)
        all_insights.extend(insights)
        
        log(f"Analyzed {repo['name']}: {result['analysis'].get('stars', 0)} stars, {len(insights)} insights")
    
    # 生成报告
    report = {
        'timestamp': datetime.now().isoformat(),
        'repos': all_results,
        'summary': {
            'total_repos': len(REPOS),
            'total_issues': sum(len(r['issues']) for r in all_results),
            'total_insights': len(all_insights),
            'high_priority': len([i for i in all_insights if i['priority'] == 'high']),
        }
    }
    
    # 保存报告
    report_file = BASE_DIR / f'self-learning-report-{datetime.now().strftime("%Y%m%d")}.json'
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 输出摘要
    print("=== 数字员工自学习报告 ===")
    print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"分析仓库: {len(REPOS)} 个")
    print(f"总 Issue 数: {report['summary']['total_issues']}")
    print(f"建议数量: {report['summary']['total_insights']} (高优先级: {report['summary']['high_priority']})")
    print()
    
    for repo in all_results:
        print(f"\n📊 {repo['name']}:")
        a = repo['analysis']
        print(f"  ⭐ {a['stars']} stars | 🍴 {a['forks']} forks | 📝 {a['open_issues']} issues")
        if repo['insights']:
            for ins in repo['insights']:
                icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(ins['priority'], '⚪')
                print(f"  {icon} [{ins['type']}] {ins['message']}")
    
    # 保存报告路径到文件
    with open(BASE_DIR / 'latest-report.txt', 'w', encoding='utf-8') as f:
        f.write(str(report_file))
    
    print(f"\n完整报告已保存: {report_file}")
    
    return all_insights

if __name__ == '__main__':
    insights = main()
    sys.exit(0 if len(insights) == 0 else 1)  # 有建议时返回非零
