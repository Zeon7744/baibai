# 变更日志

所有重要的版本变更将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.1.0] - 2026-08-31

### 新增
- **MCP Server 支持** - 将 baibai 工具包装为 MCP 协议服务
- 新增 12 个 MCP 工具：
  - `check_format` - 校验 Markdown 格式
  - `validate_directory` - 批量校验目录
  - `classify_file` - 分类单个文件
  - `classify_directory` - 批量分类目录
  - `md_to_html` - Markdown 转 HTML
  - `convert_file` - 文件转换
  - `gen_readme` - 生成 README
  - `extract_content_info` - 提取内容信息
  - `analyze_content_data` - 分析单文件数据
  - `analyze_directory` - 分析目录统计数据
  - `search_content` - 搜索内容
  - `list_tools` - 列出所有工具
- 支持 Claude Code、Cursor、Codex 等 AI 助手接入
- 添加 `.mcp.json` 配置文件
- 添加 MCP 配置示例文档

### 改进
- 更新 README.md 添加 MCP 集成说明
- 完善安装和使用文档

---

## [1.0.0] - 2026-08-30

### 新增
- 工具库重构为通用 Vibe Coding 工具集
- 新增 7 个核心工具模块：
  - `cli.py` - 基础 CLI 入口
  - `cli_enhanced.py` - Typer + Rich 增强版 CLI
  - `format_checker.py` - Markdown 格式校验器
  - `stats_analyzer.py` - 数据分析工具
  - `readme_gen.py` - README 自动生成器
  - `md2html.py` - Markdown 转 HTML
  - `classifier.py` - 内容自动分类器
- 支持 pip 安装 (`pip install -e .`)
- GitHub Actions CI 测试
- Pages 展示页重构

### 变更
- 项目定位从短剧工具库 → 通用开发工具库
- 目录结构调整：`scripts/` → `tools/`
- 添加 `pyproject.toml` 标准化配置

### 删除
- 移除短剧专属脚本（迁移至 awesome-ai-short-drama）

---

## [0.x.x] - 早期版本

### 功能
- 短剧剧本格式检查
- 字数统计分析
- README 自动生成

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.1.0 | 2026-08-31 | MCP Server 支持 |
| 1.0.0 | 2026-08-30 | 首次通用化工具库发布 |
| 0.3.0 | 2026-08-29 | 短剧工具优化 |
| 0.2.0 | 2026-08-28 | 初始版本 |
