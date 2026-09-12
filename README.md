# baibai

> MCP 工具库 — 格式校验器 · 数据分析 · README 生成器 · TTS

[![GitHub Stars](https://img.shields.io/github/stars/Zeon7744/baibai?style=social)](https://github.com/Zeon7744/baibai)
[![Gitee stars](https://gitee.com/Zeon7744/baibai/badge/star.svg?theme=gvp)](https://gitee.com/Zeon7744/baibai)
[![GitCode stars](https://gitcode.com/Zeon7744/baibai/stars/badge)](https://gitcode.com/Zeon7744/baibai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.2.0-blue)](https://github.com/Zeon7744/baibai/releases/tag/v1.2.0)
[![MCP](https://img.shields.io/badge/MCP-Compatible-violet.svg)](https://modelcontextprotocol.io)

## 简介

baibai 是一个 **MCP (Model Context Protocol) 工具库**，提供实用的开发工具集，可集成到 Claude Code、Cursor、Codex 等 AI 编程助手。

## 工具列表

| 工具 | 说明 | 用法 |
|------|------|------|
| `check-format` | 代码/文档格式校验器，支持 Markdown、JSON、YAML | `python -m tools.check_format <path>` |
| `analyze` | 数据统计分析，生成报告 | `python -m tools.analyze <path>` |
| `gen-readme` | README 自动生成器 | `python -m tools.gen_readme` |
| `md2html` | Markdown 转 HTML 页面 | `python -m tools.md2html <input> <output>` |
| `classify` | 内容自动分类器 | `python -m tools.classify <text>` |
| `tts` | 文本转语音 (Coqui TTS) | `python -m tools.tts "文本"` |
| `summarize` | 文本摘要生成 | `python -m tools.summarize <path>` |
| `translate` | 多语言翻译 | `python -m tools.translate <text>` |

## 快速开始

### 方式一：pip 安装（推荐）

```bash
# 从 GitHub Releases 安装（预编译 wheel）
pip install https://github.com/Zeon7744/baibai/releases/download/v1.2.0/baibai-1.2.0-py3-none-any.whl

# 或从源码安装
pip install https://github.com/Zeon7744/baibai/releases/download/v1.2.0/baibai-1.2.0.tar.gz
```

### 方式二：源码安装

```bash
git clone https://github.com/Zeon7744/baibai.git
cd baibai
pip install -e .
```

### 方式三：直接 Git 安装

```bash
pip install git+https://github.com/Zeon7744/baibai.git@v1.2.0
```

## MCP 集成

将以下内容添加到 Claude Code / Cursor 的 MCP 配置中：

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

## 变更日志

- [CHANGELOG.md](CHANGELOG.md) — 版本历史与更新记录

## 多平台镜像

| 平台 | 链接 |
|------|------|
| GitHub (主仓库) | [GitHub](https://github.com/Zeon7744/baibai) |
| Gitee | [Gitee](https://gitee.com/Zeon7744/baibai) |
| GitCode | [GitCode](https://gitcode.com/Zeon7744/baibai) |

## 赞助与支持

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

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)

---

*由 [Zeon7744](https://github.com/Zeon7744) 维护 · MCP ToolKit · Vibe Coding · 三平台同步*

## 🎬 短剧项目

暂无短剧项目


---

## 🎬 短剧项目

暂无短剧项目


---

## 🙏 感谢赞助

暂无赞助者

---
