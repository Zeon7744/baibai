#!/usr/bin/env python3
"""
依赖检查器 - 检查依赖安全性
"""

import re
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


# 已知有安全问题的包版本（简化数据库）
KNOWN_VULNERABILITIES = {
    "requests": {"fixed_version": "2.31.0", "issue": "CVE-2023-32681 - 代理泄露认证信息"},
    "urllib3": {"fixed_version": "2.0.4", "issue": "CVE-2023-43804 - Cookie 信息泄露"},
    "flask": {"fixed_version": "2.3.3", "issue": "CVE-2023-30861 - 会话固定"},
    "django": {"fixed_version": "4.2.5", "issue": "CVE-2023-41164 - XSS 漏洞"},
    "pillow": {"fixed_version": "10.0.1", "issue": "CVE-2023-44271 - 资源耗尽"},
    "numpy": {"fixed_version": "1.24.0", "issue": "潜在的缓冲区溢出"},
    "pyyaml": {"fixed_version": "6.0.1", "issue": "CVE-2022-1467 - 任意代码执行"},
    "jinja2": {"fixed_version": "3.1.3", "issue": "CVE-2024-22195 - XSS 漏洞"},
    "cryptography": {"fixed_version": "41.0.0", "issue": "CVE-2023-38325 - 证书验证绕过"},
    "setuptools": {"fixed_version": "65.5.1", "issue": "CVE-2022-40897 - ReDoS"},
    "werkzeug": {"fixed_version": "2.3.7", "issue": "CVE-2023-46136 - 资源耗尽"},
    "certifi": {"fixed_version": "2023.7.22", "issue": "CVE-2023-37920 - 根证书撤销"},
}

# 废弃/不推荐的包
DEPRECATED_PACKAGES = {
    "distribute": "已被 setuptools 取代",
    "pycrypto": "已被 pycryptodome 取代",
    "flask-compress-old": "使用 flask-compress",
    "requirements-parser": "考虑使用 pip-tools",
}


def parse_requirements(content: str) -> List[Dict[str, Any]]:
    """解析 requirements.txt 内容"""
    packages = []
    
    for line in content.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('-'):
            continue
        
        # 处理各种格式: pkg==1.0, pkg>=1.0, pkg~=1.0, pkg, -r other.txt
        if line.startswith('-r ') or line.startswith('--requirement'):
            continue
        
        # 提取包名和版本
        match = re.match(r'^([a-zA-Z0-9_-]+(?:\[[a-z]+\])?)\s*([><=~!]+\s*[\d.]+(?:\s*,\s*[><=~!]+\s*[\d.]+)?)?', line)
        if match:
            pkg_name = match.group(1).split('[')[0].strip().lower()
            version_spec = match.group(2) or ""
            
            # 提取精确版本
            exact_version = None
            version_match = re.search(r'==\s*([\d.]+)', version_spec)
            if version_match:
                exact_version = version_match.group(1)
            
            packages.append({
                "name": pkg_name,
                "version_spec": version_spec.strip(),
                "exact_version": exact_version,
                "pinned": "==" in version_spec,
                "raw": line
            })
    
    return packages


def check_vulnerabilities(packages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """检查已知漏洞"""
    vulnerabilities = []
    
    for pkg in packages:
        name = pkg["name"]
        version = pkg.get("exact_version")
        
        if name in KNOWN_VULNERABILITIES:
            vuln_info = KNOWN_VULNERABILITIES[name]
            fixed = vuln_info["fixed_version"]
            
            # 简单版本比较
            is_vulnerable = True
            if version:
                try:
                    v_parts = [int(x) for x in version.split('.')]
                    f_parts = [int(x) for x in fixed.split('.')]
                    # 补齐
                    while len(v_parts) < len(f_parts):
                        v_parts.append(0)
                    while len(f_parts) < len(v_parts):
                        f_parts.append(0)
                    is_vulnerable = v_parts < f_parts
                except Exception:
                    is_vulnerable = True  # 无法比较时假设存在风险
            
            if is_vulnerable:
                vulnerabilities.append({
                    "package": name,
                    "current_version": version or "未指定",
                    "fixed_version": fixed,
                    "issue": vuln_info["issue"],
                    "severity": "high",
                    "action": f"升级到 {name}>={fixed}"
                })
            else:
                vulnerabilities.append({
                    "package": name,
                    "current_version": version or "未指定",
                    "fixed_version": fixed,
                    "issue": vuln_info["issue"],
                    "severity": "resolved",
                    "action": "已修复"
                })
    
    return vulnerabilities


def check_deprecated(packages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """检查废弃包"""
    deprecated = []
    
    for pkg in packages:
        if pkg["name"] in DEPRECATED_PACKAGES:
            deprecated.append({
                "package": pkg["name"],
                "reason": DEPRECATED_PACKAGES[pkg["name"]],
                "action": f"替换为推荐的替代包"
            })
    
    return deprecated


def check_pinning(packages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """检查版本锁定情况"""
    unpinned = []
    
    for pkg in packages:
        if not pkg["pinned"]:
            unpinned.append({
                "package": pkg["name"],
                "version_spec": pkg["version_spec"] or "无版本限制",
                "risk": "未锁定版本可能导致不同环境安装不同版本",
                "action": f"使用 == 锁定版本: {pkg['name']}==<version>"
            })
    
    return unpinned


def check_dependencies(requirements_path: str = None, requirements_content: str = None) -> Dict[str, Any]:
    """主检查函数"""
    
    content = ""
    source = ""
    
    if requirements_content:
        content = requirements_content
        source = "direct input"
    elif requirements_path:
        p = Path(requirements_path)
        if p.is_file():
            try:
                content = p.read_text(encoding='utf-8')
                source = str(p)
            except Exception as e:
                return {"error": f"读取文件失败: {e}"}
        elif p.is_dir():
            # 尝试常见文件名
            for fname in ['requirements.txt', 'requirements-dev.txt', 'Pipfile', 'pyproject.toml']:
                candidate = p / fname
                if candidate.exists():
                    try:
                        content = candidate.read_text(encoding='utf-8')
                        source = str(candidate)
                        break
                    except Exception:
                        pass
            if not content:
                return {"error": f"目录下未找到依赖文件: {requirements_path}"}
        else:
            return {"error": f"路径不存在: {requirements_path}"}
    else:
        return {"error": "请提供 requirements 文件路径或内容"}
    
    # 解析 requirements
    packages = parse_requirements(content)
    
    if not packages:
        return {
            "source": source,
            "packages_found": 0,
            "message": "未解析到有效的包依赖"
        }
    
    # 执行检查
    vulnerabilities = check_vulnerabilities(packages)
    deprecated = check_deprecated(packages)
    pinning_issues = check_pinning(packages)
    
    # 安全评分
    score = 100
    for v in vulnerabilities:
        if v["severity"] == "high":
            score -= 15
        elif v["severity"] == "resolved":
            pass  # 已修复不扣分
    for d in deprecated:
        score -= 10
    for p in pinning_issues[:5]:  # 只扣前5个
        score -= 2
    score = max(0, score)
    
    # 统计
    stats = {
        "total_packages": len(packages),
        "pinned_count": sum(1 for p in packages if p["pinned"]),
        "unpinned_count": sum(1 for p in packages if not p["pinned"]),
        "vulnerabilities_high": sum(1 for v in vulnerabilities if v["severity"] == "high"),
        "vulnerabilities_resolved": sum(1 for v in vulnerabilities if v["severity"] == "resolved"),
        "deprecated_count": len(deprecated),
        "pinning_issues": len(pinning_issues)
    }
    
    return {
        "source": source,
        "score": score,
        "stats": stats,
        "packages": [{"name": p["name"], "version": p["exact_version"] or p["version_spec"] or "latest"} 
                     for p in packages],
        "vulnerabilities": [v for v in vulnerabilities if v["severity"] == "high"],
        "deprecated": deprecated,
        "pinning_issues": pinning_issues,
        "recommendations": _build_recommendations(vulnerabilities, deprecated, pinning_issues)
    }


def _build_recommendations(vulns: List, deprecated: List, pinning: List) -> List[str]:
    """构建建议"""
    recs = []
    
    if vulns:
        high = [v for v in vulns if v["severity"] == "high"]
        if high:
            names = ", ".join(v["package"] for v in high[:5])
            recs.append(f"🔴 紧急: 以下包存在已知漏洞，请立即升级: {names}")
    
    if deprecated:
        names = ", ".join(d["package"] for d in deprecated[:5])
        recs.append(f"🟡 建议: 以下包已废弃，请替换: {names}")
    
    if pinning:
        recs.append(f"🟢 改善: 建议锁定 {len(pinning)} 个未固定版本的依赖，确保构建可重复")
    
    if not recs:
        recs.append("✅ 依赖状况良好，无需立即处理")
    
    return recs
