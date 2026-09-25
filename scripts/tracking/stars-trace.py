#!/usr/bin/env python3
"""Stars 增长追踪脚本 - 每日自动记录各仓库 star 数据"""

import json
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
BASE_DIR = Path('/Coze/Drive/红剑/所有对话/主对话/repo-stats')
TRACE_FILE = BASE_DIR / 'stars-trace.json'
LOG_FILE = BASE_DIR / 'stars-trace.log'

REPOS = [
    {'name': 'baibai', 'user': 'Zeon7744'},
    {'name': 'awesome-ai-short-drama', 'user': 'Zeon7744'},
    {'name': 'dev-artifacts', 'user': 'Zeon7744'},
]

def get_stars(repo: dict) -> int:
    """获取仓库 star 数"""
    url = f"https://api.github.com/repos/{repo['user']}/{repo['name']}"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json().get('stargazers_count', 0)
    except Exception as e:
        print(f"[ERROR] {repo['name']}: {e}")
        return -1

def load_trace() -> dict:
    """加载追踪记录"""
    if TRACE_FILE.exists():
        with open(TRACE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'repos': {}, 'history': []}

def save_trace(trace: dict):
    """保存追踪记录"""
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    with open(TRACE_FILE, 'w', encoding='utf-8') as f:
        json.dump(trace, f, ensure_ascii=False, indent=2)

def append_log(msg: str):
    """追加日志"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().isoformat()} {msg}\n")

def main():
    trace = load_trace()
    today = datetime.now().strftime('%Y-%m-%d')
    changes = []
    
    for repo in REPOS:
        stars = get_stars(repo)
        key = f"{repo['user']}/{repo['name']}"
        
        if stars < 0:
            continue
            
        prev = trace['repos'].get(key, 0)
        delta = stars - prev
        
        trace['repos'][key] = stars
        trace['history'].append({
            'date': today,
            'repo': key,
            'stars': stars,
            'delta': delta
        })
        
        if delta > 0:
            changes.append(f"⭐ {key} +{delta} (total: {stars})")
        elif delta < 0:
            changes.append(f"📉 {key} {delta} (total: {stars})")
    
    # 清理历史（保留最近30天）
    cutoff = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    trace['history'] = [h for h in trace['history'] if h['date'] >= cutoff]
    
    save_trace(trace)
    append_log(f"Stars check: {len(changes)} changes")
    
    if changes:
        print("=== Stars Change ===")
        for c in changes:
            print(c)
        print(f"\nSummary: {today} - {len(changes)} repos changed")
    else:
        print("No changes since last check.")
    
    return len(changes) > 0

if __name__ == '__main__':
    main()
