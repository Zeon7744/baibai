#!/usr/bin/env python3
"""
短剧格式校验器
检查剧本是否符合红果短剧平台规范
"""

import os
import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class CheckResult:
    """校验结果"""
    file_path: str
    title: str
    episodes: int
    total_words: int
    issues: List[str]
    score: int  # 0-100


def parse_drama_file(filepath: str) -> Tuple[str, List[dict]]:
    """解析短剧文件，提取集数和内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题
    title_match = re.search(r'#\s*《(.+?)》', content)
    title = title_match.group(1) if title_match else Path(filepath).stem
    
    # 提取所有集
    episodes = []
    episode_pattern = r'##\s*第(\d+)集[：:]\s*(.+?)(?=\n##\s*第|$)'
    for match in re.finditer(episode_pattern, content, re.DOTALL):
        ep_num = int(match.group(1))
        ep_content = match.group(2).strip()
        ep_name = match.group(2).strip()
        episodes.append({
            'num': ep_num,
            'name': ep_name,
            'content': ep_content
        })
    
    return title, episodes


def check_episode(ep: dict, filepath: str) -> List[str]:
    """检查单集格式"""
    issues = []
    content = ep['content']
    
    # 检查对话长度
    dialogues = re.findall(r'"([^"]+)"', content)
    for dlg in dialogues:
        if len(dlg) > 15:
            issues.append(f"对话超限 ({len(dlg)}字): {dlg[:20]}...")
            break  # 只报一次
    
    # 检查爽点（简单判断：是否有冲突、打脸、反转关键词）
    shuang_keywords = ['冷笑', '怒', '杀', '废', '滚', '找死', '放肆', '你敢', '呵', '竟敢', '居然']
    has_shuang = any(kw in content for kw in shuang_keywords)
    if not has_shuang:
        issues.append("缺少爽点关键词")
    
    # 检查字数
    word_count = len(re.sub(r'\s+', '', content))
    if word_count < 300:
        issues.append(f"字数过少 ({word_count}字)")
    
    return issues


def validate_drama(filepath: str) -> CheckResult:
    """校验整个剧本"""
    try:
        title, episodes = parse_drama_file(filepath)
        
        all_issues = []
        total_words = 0
        
        for ep in episodes:
            ep_issues = check_episode(ep, filepath)
            all_issues.extend(ep_issues)
            total_words += len(re.sub(r'\s+', '', ep['content']))
        
        # 计算分数
        score = 100
        score -= len(all_issues) * 10
        score = max(0, min(100, score))
        
        # 检查结尾标记
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        if not re.search(r'##\s*第\d+集\s*完', content):
            all_issues.append("缺少结尾标记（第X集完）")
            score -= 10
        
        # 检查禁止字眼
        if '耀' in content or '曜' in content:
            all_issues.append("包含禁止字眼：耀/曜")
            score -= 20
        
        return CheckResult(
            file_path=filepath,
            title=title,
            episodes=len(episodes),
            total_words=total_words,
            issues=all_issues,
            score=score
        )
    except Exception as e:
        return CheckResult(
            file_path=filepath,
            title=Path(filepath).stem,
            episodes=0,
            total_words=0,
            issues=[f"解析错误: {str(e)}"],
            score=0
        )


def scan_dramas(drama_dir: str) -> List[CheckResult]:
    """扫描剧本目录"""
    results = []
    drama_path = Path(drama_dir)
    
    if not drama_path.exists():
        print(f"目录不存在: {drama_dir}", file=sys.stderr)
        return results
    
    for ep_dir in drama_path.iterdir():
        if ep_dir.is_dir():
            for md_file in ep_dir.glob('*.md'):
                if '_完整剧本' in md_file.name:
                    result = validate_drama(str(md_file))
                    results.append(result)
    
    return results


def print_report(results: List[CheckResult]):
    """打印校验报告"""
    print("\n" + "="*60)
    print("📋 短剧格式校验报告")
    print("="*60)
    
    total = len(results)
    passed = sum(1 for r in results if r.score >= 80)
    warning = sum(1 for r in results if 60 <= r.score < 80)
    failed = sum(1 for r in results if r.score < 60)
    
    print(f"\n📊 统计: 共 {total} 部 | ✅通过 {passed} | ⚠️警告 {warning} | ❌失败 {failed}")
    print("-"*60)
    
    for r in results:
        status = "✅" if r.score >= 80 else "⚠️" if r.score >= 60 else "❌"
        print(f"\n{status} {r.title} ({r.episodes}集, {r.total_words}字)")
        print(f"   得分: {r.score}/100")
        
        if r.issues:
            print(f"   问题:")
            for issue in r.issues[:5]:  # 最多显示5个
                print(f"      • {issue}")
            if len(r.issues) > 5:
                print(f"      ... 还有 {len(r.issues)-5} 个问题")
    
    print("\n" + "="*60)


def main():
    """主函数"""
    # 默认扫描路径
    drama_dir = sys.argv[1] if len(sys.argv) > 1 else '../awesome-ai-short-drama/short-dramas'
    
    print(f"🔍 扫描目录: {drama_dir}")
    
    results = scan_dramas(drama_dir)
    
    if not results:
        print("未找到剧本文件")
        sys.exit(1)
    
    print_report(results)
    
    # 输出 JSON 格式供其他工具使用
    import json
    json_output = [{
        'title': r.title,
        'episodes': r.episodes,
        'words': r.total_words,
        'score': r.score,
        'issues': r.issues
    } for r in results]
    
    # 保存到数据目录
    output_dir = Path('data/stats')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / 'format_check.json', 'w', encoding='utf-8') as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 报告已保存: data/stats/format_check.json")


if __name__ == '__main__':
    main()
