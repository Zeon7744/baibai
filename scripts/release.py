#!/usr/bin/env python3
"""发布管理脚本"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

def create_release(version: str, description: str = "") -> dict:
    """创建新版本发布信息"""
    release_dir = Path(f"releases/v{version}")
    release_dir.mkdir(parents=True, exist_ok=True)
    
    # 版本文件
    version_file = release_dir / "VERSION"
    version_file.write_text(version)
    
    # 发布信息
    release_info = {
        "version": version,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": description,
        "status": "beta",
        "files": []
    }
    
    # 发布说明文件
    changelog_entry = f"""## [{version}] - {datetime.now().strftime('%Y-%m-%d')}

### 新增
- {description}

### 变更
- 更新版本至 {version}

---
"""
    
    (release_dir / "CHANGELOG.md").write_text(changelog_entry)
    
    # 下载链接
    base_url = "https://github.com/Zeon7744/baibai/releases/download"
    release_info["download"] = {
        "zip": f"{base_url}/v{version}/baibai-v{version}.zip",
        "tar.gz": f"{base_url}/v{version}/baibai-v{version}.tar.gz"
    }
    
    # 保存发布信息
    info_file = release_dir / "release-info.json"
    info_file.write_text(json.dumps(release_info, indent=2, ensure_ascii=False))
    
    print(f"发布版本 {version} 已创建")
    print(f"目录: {release_dir.absolute()}")
    print(f"信息文件: {info_file.absolute()}")
    
    return release_info

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python release.py <version> [description]")
        print("示例: python release.py 1.0.0 '首次发布'")
        sys.exit(1)
    
    version = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) > 2 else ""
    create_release(version, description)
