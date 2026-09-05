# baibai

> MCP 工具库 — 格式校验器 · 数据分析 · README 生成器 · MCP Server

[![GitHub Stars](https://img.shields.io/github/stars/Zeon7744/baibai?style=social)](https://github.com/Zeon7744/baibai)
[![Gitee stars](https://gitee.com/Zeon7744/baibai/badge/star.svg?theme=gvp)](https://gitee.com/Zeon7744/baibai)
[![GitCode stars](https://gitcode.com/Zeon7744/baibai/stars/badge)](https://gitcode.com/Zeon7744/baibai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.2.0-blue)](https://github.com/Zeon7744/baibai/releases)
[![MCP](https://img.shields.io/badge/MCP-Compatible-violet.svg)](https://modelcontextprotocol.io)

## 简介

baibai 是一个 **MCP (Model Context Protocol) 工具库**，提供实用的开发工具集，可集成到 Claude Code、Cursor、Codex 等 AI 编程助手。

## 功能特性

| 工具 | 说明 |
|------|------|
| `check-format` | 代码/文档格式校验器，支持 Markdown、JSON、YAML |
| `analyze` | 数据统计分析，生成报告 |
| `gen-readme` | README 自动生成器 |
| `md2html` | Markdown 转 HTML 页面 |
| `classify` | 内容自动分类器 |

## 快速开始

```bash
git clone https://github.com/Zeon7744/baibai.git
cd baibai
pip install -e .
```

## MCP 集成

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

## 在线演示

- [GitHub Pages](https://zeon7744.github.io/baibai/)

## 多平台镜像

| 平台 | 链接 |
|------|------|
| GitHub (主仓库) | [GitHub](https://github.com/Zeon7744/baibai) |
| Gitee | [Gitee](https://gitee.com/Zeon7744/baibai) |
| GitCode | [GitCode](https://gitcode.com/Zeon7744/baibai) |

## 赞助与支持

如果这个项目对你有帮助，欢迎赞助：

| 平台 | 链接 | 支付方式 |
|------|------|----------|
| ☕ **爱发电** | [afdian.com/@Zeon7744](https://afdian.com/@Zeon7744) | 支付宝 / 微信支付 |
| 🌍 **GitHub Sponsors** | [github.com/sponsors/Zeon7744](https://github.com/sponsors/Zeon7744) | PayPal / Stripe |

### 赞助档位

| 档位 | 价格 | 权益 |
|------|------|------|
| ☕ 请喝咖啡 | ¥18/月 | 感谢支持 + 赞助者名单 |
| 🍺 请喝啤酒 | ¥58/月 | 以上 + 优先回复 Issue |
| 🎁 项目赞助 | ¥188/月 | 以上 + 定制功能需求优先开发 |

## 相关项目

- [crypto-mlp-high-confidence](https://github.com/Zeon7744/crypto-mlp-high-confidence) — MLP 加密货币预测
- [global-investment-mlp](https://github.com/Zeon7744/global-investment-mlp) — 量化投资框架
- [awesome-ai-short-drama](https://github.com/Zeon7744/awesome-ai-short-drama) — AI 短剧资源合集
- [dev-artifacts](https://github.com/Zeon7744/dev-artifacts) — 开发工具箱

## 贡献

欢迎提交 Issue 和 Pull Request！详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

*由 [Zeon7744](https://github.com/Zeon7744) 维护 · Vibe Coding · 三平台同步*
