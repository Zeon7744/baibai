#!/usr/bin/env python3
"""Baibai 安装脚本 — MCP 资产底座，CLI 入口已弃用"""

from setuptools import setup, find_packages
import os

# 读取版本
version_file = os.path.join(os.path.dirname(__file__), "VERSION.md")
if os.path.exists(version_file):
    with open("VERSION.md", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("- **主版本**:"):
                version = line.split(":")[-1].strip()
                break
        else:
            version = "1.0.0"
else:
    version = "1.0.0"

# 读取长描述
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="baibai",
    version=version,
    description="Vibe Coding 开发工具库 — MCP Server 内容创作工具集（资产底座）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zeon7744",
    author_email="zeon7744@gmail.com",
    url="https://github.com/Zeon7744/baibai",
    packages=find_packages(where="."),
    package_dir={"": "."},
    include_package_data=True,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
    ],
    keywords=[
        "vibe-coding",
        "mcp",
        "ai",
        "assistant",
        "markdown",
        "analysis",
        "tools",
    ],
    project_urls={
        "Homepage": "https://github.com/Zeon7744/baibai",
        "Documentation": "https://github.com/Zeon7744/baibai#readme",
        "Repository": "https://github.com/Zeon7744/baibai.git",
        "Issues": "https://github.com/Zeon7744/baibai/issues",
        "Changelog": "https://github.com/Zeon7744/baibai/blob/main/CHANGELOG.md",
    },
)
