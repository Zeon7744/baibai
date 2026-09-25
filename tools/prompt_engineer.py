#!/usr/bin/env python3
"""
提示词工程师 - 优化 AI 提示词
"""

import re
from typing import Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class PromptOptimizationResult:
    """提示词优化结果"""
    original: str
    optimized: str
    improvements: List[str] = field(default_factory=list)
    score_before: float = 0.0
    score_after: float = 0.0
    technique_used: List[str] = field(default_factory=list)


def score_prompt(prompt: str) -> float:
    """评估提示词质量 (0-100)"""
    score = 50.0  # 基础分
    
    # 1. 长度评估 (10分)
    length = len(prompt)
    if 50 <= length <= 2000:
        score += 10
    elif length < 20:
        score -= 5
    elif length > 5000:
        score -= 3
    
    # 2. 明确性检查 (15分)
    clarity_keywords = ['请', '需要', '应该', '必须', '确保', '生成', '创建', '分析', '解释', '列出']
    if any(kw in prompt for kw in clarity_keywords):
        score += 8
    
    # 3. 结构化检查 (15分)
    has_structure = False
    if re.search(r'^#\s', prompt, re.MULTILINE):
        has_structure = True
        score += 5
    if re.search(r'^[-*]\s', prompt, re.MULTILINE):
        has_structure = True
        score += 5
    if re.search(r'^\d+\.', prompt, re.MULTILINE):
        has_structure = True
        score += 5
    
    # 4. 上下文/约束 (15分)
    context_indicators = ['角色', '背景', '上下文', '目标', '受众', '格式', '风格', '长度']
    context_count = sum(1 for kw in context_indicators if kw in prompt)
    score += min(context_count * 3, 15)
    
    # 5. 输出格式要求 (10分)
    format_indicators = ['JSON', 'markdown', '列表', '表格', '格式', '模板', '输出']
    format_count = sum(1 for kw in format_indicators if kw.lower() in prompt.lower())
    score += min(format_count * 3, 10)
    
    # 6. 示例 (10分)
    if '示例' in prompt or '例如' in prompt or 'example' in prompt.lower():
        score += 10
    
    # 7. 负面约束 (10分)
    negative_indicators = ['不要', '禁止', '避免', '不应', '不能', '必须不']
    if any(kw in prompt for kw in negative_indicators):
        score += 10
    
    return min(100, max(0, score))


def optimize_prompt(original_prompt: str, target_outcome: str = "") -> Dict[str, Any]:
    """优化提示词"""
    improvements = []
    techniques = []
    optimized = original_prompt
    
    # 1. 添加角色设定（如果没有）
    if not any(kw in optimized.lower() for kw in ['你是', '作为', '角色', '你是一位']):
        role_suggestion = ""
        if target_outcome:
            if any(kw in target_outcome.lower() for kw in ['代码', '编程', '开发']):
                role_suggestion = "你是一位资深软件工程师，擅长编写高质量、可维护的代码。\n\n"
            elif any(kw in target_outcome.lower() for kw in ['文章', '写作', '内容']):
                role_suggestion = "你是一位专业内容创作者，擅长结构化写作和清晰表达。\n\n"
            elif any(kw in target_outcome.lower() for kw in ['分析', '数据', '报告']):
                role_suggestion = "你是一位数据分析师，擅长从数据中提取洞察并生成清晰报告。\n\n"
            else:
                role_suggestion = "你是一位经验丰富的专业顾问，擅长提供高质量的分析和解决方案。\n\n"
        
        if role_suggestion:
            optimized = role_suggestion + optimized
            improvements.append("添加了角色设定，帮助模型进入专业状态")
            techniques.append("role_assignment")
    
    # 2. 明确输出格式（如果缺失）
    format_keywords = ['json', 'markdown', '列表', '表格', '格式', '模板']
    if not any(kw in optimized.lower() for kw in format_keywords):
        optimized += "\n\n请以结构化的格式输出结果，使用清晰的标题和分段。"
        improvements.append("添加了输出格式要求")
        techniques.append("output_format")
    
    # 3. 添加目标明确性
    if target_outcome and target_outcome not in optimized:
        optimized = f"目标：{target_outcome}\n\n{optimized}"
        improvements.append("添加了明确的目标声明")
        techniques.append("goal_clarity")
    
    # 4. 添加约束条件（如果缺失）
    constraint_keywords = ['不要', '禁止', '避免', '限制', '约束']
    if not any(kw in optimized for kw in constraint_keywords):
        optimized += "\n\n注意事项：\n- 避免无关内容，保持聚焦\n- 确保内容准确、可执行"
        improvements.append("添加了约束条件")
        techniques.append("constraints")
    
    # 5. 添加示例引导（如果内容复杂且没有示例）
    if len(original_prompt) > 200 and '示例' not in optimized and '例如' not in optimized:
        improvements.append("建议：考虑添加示例输出以提高一致性")
        techniques.append("few_shot_suggestion")
    
    # 6. 检查并优化长度
    if len(optimized) > 3000:
        improvements.append("提示词较长，建议精简非核心内容")
    
    # 评分
    score_before = score_prompt(original_prompt)
    score_after = score_prompt(optimized)
    
    if not improvements:
        improvements.append("提示词质量已较好，无需大幅调整")
    
    return {
        "original": original_prompt,
        "optimized": optimized,
        "score_before": round(score_before, 1),
        "score_after": round(score_after, 1),
        "improvements": improvements,
        "techniques_used": techniques
    }
