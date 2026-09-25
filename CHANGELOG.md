# Changelog

所有重要版本变更将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [v3.0.0] - 2026-09-25

### 新增
- **file_analyzer**: 项目文件结构、依赖关系、代码质量分析
- **prompt_engineer**: AI 提示词优化，评分对比与改进建议
- **code_explainer**: 代码逻辑解释，支持 Python/JS/TS 等多语言
- **error_analyzer**: 错误堆栈智能分析，匹配 12+ 种已知错误模式
- **batch_processor**: 批量文件处理（重命名/替换/统计等 12 种操作）
- **docs_generator**: 自动生成 Markdown 文档，支持 Python/JS/通用文件
- **test_generator**: 自动生成 pytest/unittest/Jest 测试用例
- **refactoring_suggester**: 代码重构建议，包含复杂度分析和安全评分
- **dependency_checker**: 依赖安全漏洞检测，覆盖 12+ 个常见 CVE
- **api_doc_builder**: 从路由代码构建 OpenAPI 3.0 规范文档

### 改进
- MCP Server 工具总数从 12 个增加到 22 个
- 版本号升级为 3.0.0
- 启动信息显示工具数量统计

### 测试
- 新增 `tests/test_new_tools.py`，覆盖全部 10 个 v3 新工具
- 测试类: TestFileAnalyzer, TestPromptEngineer, TestCodeExplainer 等
- MCP Server 集成测试验证工具注册完整性

### 文档
- README.md 全面更新，增加 v3 工具详情和示例输出
- CHANGELOG.md 记录 v3.0.0 完整变更
- .mcp.json 配置更新

---

## [v1.0.0] - 2026-09-25

### 新增
- MCP Server v2 架构重构
- 12 个核心工具实现
- Claude Code、Cursor、Codex 集成配置
- GitHub Releases 发布流程

### 优化
- README 全面重写，专业展示格式
- 添加徽章系统（Stars/Forks/License/Gitee）
- 快速开始指南完善

### 文档
- CONTRIBUTING.md 贡献指南
- CODE_OF_CONDUCT.md 行为准则
- LICENSE MIT 许可证

### 测试
- 基础测试模板框架

---

## [Unreleased]

### 计划中
- Web 界面支持
- 更多 AI 编程助手集成
- 工具市场/插件系统
