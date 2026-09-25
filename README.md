# 🚀 Baibai — Vibe Coding 开发工具库

> **用自然语言驱动开发** — 通用 CLI 工具集 + MCP Server  
> AI 编程助手必备工具箱，让 Claude Code、Cursor、Codex 更强大

[![GitHub Stars](https://img.shields.io/github/stars/Zeon7744/baibai?style=social)](https://github.com/Zeon7744/baibai)
[![GitHub Forks](https://img.shields.io/github/forks/Zeon7744/baibai?style=social)](https://github.com/Zeon7744/baibai/forks)
[![GitHub License](https://img.shields.io/github/license/Zeon7744/baibai)](https://github.com/Zeon7744/baibai/blob/main/LICENSE)
[![Gitee Stars](https://gitee.com/Zeon7744/baibai/badge/star.svg?theme=gvp)](https://gitee.com/Zeon7744/baibai)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![MCP Support](https://img.shields.io/badge/MCP-Support-violet.svg)](https://modelcontextprotocol.io)

---

## 📌 这是 GitHub 官方主仓

> **Gitee 镜像**: [gitee.com/Zeon7744/baibai](https://gitee.com/Zeon7744/baibai)  
> **GitCode 镜像**: [gitcode.com/Zeon7744/baibai](https://gitcode.com/Zeon7744/baibai)

Issues 和 PR 请在 GitHub 提交。

---

## ⚡ 快速开始

```bash
# 安装
pip install baibai

# 或使用源码
git clone https://github.com/Zeon7744/baibai.git
cd baibai
pip install -e .

# 验证 MCP 服务
python mcp_server_v2.py --health
```

---

## 🛠️ 核心工具

| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `format_checker` | Markdown 格式校验 | 剧本、文档规范性检查 |
| `stats_analyzer` | 内容统计分析 | 字数统计、类型分布 |
| `readme_gen` | README 自动生成 | 项目文档维护 |
| `md2html` | Markdown→HTML | 内容展示页生成 |
| `classifier` | 内容自动分类 | 文件类型识别 |

---

## 🔌 MCP 集成

支持接入主流 AI 编程助手：

```json
{
  "mcpServers": {
    "baibai": {
      "command": "python",
      "args": ["-m", "tools.cli", "mcp", "serve"]
    }
  }
}
```

**支持环境**: Claude Code、Cursor、Codex、VS Code

---

## 📦 项目结构

```
baibai/
├── tools/              # 核心工具包
│   ├── cli.py          # CLI 入口
│   ├── format_checker.py
│   ├── stats_analyzer.py
│   └── ...
├── templates/          # 页面模板
├── tests/             # 测试套件
├── scripts/           # 运维脚本
└── README.md
```

---

## 🎯 适用场景

- ✅ 短剧剧本批量格式校验
- ✅ 内容库数据统计与报告
- ✅ Markdown 批量转 HTML
- ✅ README 自动化维护
- ✅ AI 编程助手 MCP 扩展

---

## 📊 版本状态

| 指标 | 数值 |
|------|------|
| 最新版本 | v1.0.0 |
| Python 版本 | 3.8+ |
| 测试覆盖 | 85%+ |
| 最后更新 | 2026-09-25 |

---

## 🤝 贡献指南

欢迎 PR！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## ☕ 支持作者

如果这个项目对你有帮助，欢迎赞助 ☕

| 渠道 | 方式 |
|------|------|
| [爱发电](https://afdian.com/@Zeon7744) | 支付宝 / 微信支付 |
| [GitHub Sponsors](https://github.com/sponsors/Zeon7744) | PayPal / Stripe |

---

<div align="center">

**由 [Zeon7744](https://github.com/Zeon7744) 维护**  
*Vibe Coding · 自然语言驱动开发*

</div>
