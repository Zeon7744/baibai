#!/usr/bin/env python3
"""发布管理脚本 - 支持 PyPI 和 GitHub Releases"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

def build_package(version: str) -> dict:
    """构建发布包"""
    print(f"正在构建版本 {version}...")
    
    # 创建 dist 目录
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    # 构建 sdist
    result = subprocess.run(
        [sys.executable, "setup.py", "sdist", "bdist_wheel"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"构建失败: {result.stderr}")
        return {"success": False, "error": result.stderr}
    
    # 列出构建的文件
    files = list(dist_dir.glob("*"))
    return {
        "success": True,
        "version": version,
        "files": [f.name for f in files],
        "path": str(dist_dir.absolute())
    }

def create_github_release(version: str, description: str) -> dict:
    """创建 GitHub Release"""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("错误: 请设置 GITHUB_TOKEN 环境变量")
        return {"success": False, "error": "Missing GITHUB_TOKEN"}
    
    # 构建 release body
    body = f"""## {version}

{description}

**发布日期**: {datetime.now().strftime('%Y-%m-%d')}

---

### 安装

\`\`\`bash
pip install baibai=={version}
\`\`\`

或从源码安装:

\`\`\`bash
git clone https://github.com/Zeon7744/baibai.git
cd baibai
git checkout v{version}
pip install -e .
\`\`\`

### 工具列表

1. \`check-format\` - 格式校验
2. \`analyze\` - 数据分析  
3. \`gen-readme\` - README生成
4. \`md2html\` - Markdown转HTML
5. \`classify\` - 内容分类
"""
    
    # 调用 GitHub API
    url = "https://api.github.com/repos/Zeon7744/baibai/releases"
    
    payload = {
        "tag_name": f"v{version}",
        "target_commitish": "main",
        "name": f"v{version}",
        "body": body,
        "draft": False,
        "prerelease": "beta" in version.lower()
    }
    
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", 
         "-H", f"Authorization: token {token}",
         "-H", "Content-Type: application/json",
         url,
         "-d", json.dumps(payload)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        return {"success": False, "error": result.stderr}
    
    try:
        response = json.loads(result.stdout)
        if "id" in response:
            return {
                "success": True,
                "release_url": response.get("html_url", ""),
                "upload_url": response.get("upload_url", "")
            }
        else:
            return {"success": False, "error": response.get("message", "Unknown error")}
    except json.JSONDecodeError:
        return {"success": False, "error": "Invalid response"}

def upload_assets(release_url: str, version: str):
    """上传发布资产"""
    token = os.getenv("GITHUB_TOKEN")
    dist_dir = Path("dist")
    
    for file in dist_dir.glob("*"):
        print(f"上传: {file.name}")
        subprocess.run([
            "curl", "-X", "POST",
            "-H", f"Authorization: token {token}",
            "-H", "Content-Type: application/zip",
            f"{release_url}?name={file.name}",
            "--data-binary", f"@{file}"
        ])

def publish_to_pypi(version: str):
    """发布到 PyPI"""
    print(f"正在发布到 PyPI...")
    
    # 使用 twine 上传
    result = subprocess.run(
        [sys.executable, "-m", "twine", "upload", "dist/*"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"发布失败: {result.stderr}")
        return {"success": False, "error": result.stderr}
    
    return {
        "success": True,
        "package_url": f"https://pypi.org/project/baibai/{version}/"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python publish.py build <version>        # 构建发布包")
        print("  python publish.py release <version> <desc>  # 创建 GitHub Release")
        print("  python publish.py pypi <version>         # 发布到 PyPI")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "build" and len(sys.argv) >= 3:
        result = build_package(sys.argv[2])
        print(json.dumps(result, indent=2))
    
    elif command == "release" and len(sys.argv) >= 4:
        result = create_github_release(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2))
    
    elif command == "pypi" and len(sys.argv) >= 3:
        result = publish_to_pypi(sys.argv[2])
        print(json.dumps(result, indent=2))
    
    else:
        print("无效命令")
        sys.exit(1)
