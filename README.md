# Baibai - Vibe Coding 开发仓库

> 代码 · 程序 · 工作流 — 用自然语言驱动开发

## 项目简介

Baibai 是一个 **Vibe Coding 开发仓库**，整合了应用开发、工具构建和工作流自动化的完整能力。

核心定位：
- **代码仓库** — 存放 Vibe Coding 相关的工具代码和模板
- **应用开发** — 提供基于 AI 的编程环境和 IDE
- **开发工具** — 编剧工坊等创作工具，支持一键发布到三平台
- **工作流自动化** — 配置自动同步、CI/CD、赞助管理等开发工作流

---

## 🎬 短剧创作工具

### 编剧工坊

[![](https://img.shields.io/badge/在线使用-点击打开-6366f1?style=for-the-badge)](https://zeon7744.github.io/baibai/)

编剧工坊是一款专业的短剧剧本创作工具，支持：
- **要素生成** — 从零创作，输入故事要素自动生成完整剧本
- **小说改编** — 上传小说文本，自动改编为短剧格式
- **格式校验** — 符合红果短剧平台规范（≤15字对话、≥3爽点/集）
- **一键发布** — 创作完成后直接推送至 GitHub/Gitee/爱发电

---

## 🛠️ 工具链

### 脚本工具

| 工具 | 说明 | 使用方式 |
|------|------|---------|
| `check_format.py` | 短剧格式校验器 | 检查剧本是否符合平台规范 |
| `stats_analyzer.py` | 数据统计分析 | 统计剧本库数据，生成分析报告 |
| `gen_readme.py` | README 自动生成 | 根据剧本库内容自动生成 README 短剧列表 |

### 使用示例

```bash
# 格式校验
python scripts/check_format.py ../awesome-ai-short-drama/short-dramas

# 数据分析
python scripts/stats_analyzer.py ../awesome-ai-short-drama/short-dramas

# 生成 README
python scripts/gen_readme.py ../awesome-ai-short-drama/short-dramas
```

---

## 🎬 短剧剧本库

本仓库收录 **8部完整短剧剧本**，符合红果短剧平台规范（≤15字对话、≥3爽点/集）。详见 [awesome-ai-short-drama](https://github.com/Zeon7744/awesome-ai-short-drama)。

| 序号 | 剧名 | 类型 | 集数 |
|------|------|------|------|
| 1 | **剑魂重生** | 玄幻重生 | 30集 |
| 2 | **帝师无双** | 玄幻重生 | 10集 |
| 3 | **总裁的替身前妻** | 都市异能 | 10集 |
| 4 | **暗夜追凶** | 悬疑推理 | 10集 |
| 5 | **江城情缘** | 都市甜宠 | 30集 |
| 6 | **狂少逆袭** | 都市豪门 | 10集 |
| 7 | **神医赘婿** | 都市异能 | 10集 |
| 8 | **龙皇归来** | 玄幻重生 | 10集 |

> 📌 剧本创作规范：标题第X集：集名 · 结尾第X集完 · 对话≤15字 · 每集≥3爽点+1甜点

---

## 🎬 短剧项目

暂无短剧项目


---

## 🙏 感谢赞助

- [爱发电赞助列表](https://ifdian.net/a/Zeon7744)

---

## 三平台联动

```
GitHub (国际) ↔ Gitee (国内) ↔ 爱发电 (赞助变现)
```

| 平台 | 地址 |
|------|------|
| GitHub | https://github.com/Zeon7744/baibai |
| Gitee | https://gitee.com/Zeon7744/baibai |
| 爱发电 | https://ifdian.net/a/Zeon7744 |
| 编剧工坊 | https://zeon7744.github.io/baibai/ |
| 展示页 | https://zeon7744.github.io/baibai-pages/ |

---

## 内容结构

```
baibai/
├── README.md                    # 项目介绍
├── 编剧工坊.html                # 短剧创作工具（GitHub Pages）
├── pages/                       # GitHub Pages 展示页
│   └── index.html              # 主展示页
├── docs/                        # 详细文档
├── scripts/                     # 工具脚本
│   ├── check_format.py         # 格式校验器
│   ├── stats_analyzer.py       # 数据分析
│   └── gen_readme.py           # README 生成
├── data/stats/                  # 统计数据缓存
└── .github/workflows/           # 自动化工作流
    ├── update-content.yml      # 内容自动更新
    ├── publish-pages.yml       # GitHub Pages 发布
    └── sync-to-gitee.yml       # Gitee 同步
```

---

## 快速开始

### 克隆仓库

```bash
git clone https://github.com/Zeon7744/baibai.git
cd baibai
```

### 使用编剧工坊

1. 访问 [编剧工坊](https://zeon7744.github.io/baibai/)
2. 选择创作模式：
   - **要素生成**：输入故事要素，自动生成剧本
   - **小说改编**：上传小说文本，自动改编为短剧格式
3. 导出剧本文件
4. 提交到仓库，自动同步

### 本地运行

```bash
# 直接打开 HTML 文件
open 编剧工坊.html
```

---

## 短剧创作规范

### 格式要求
- ✅ 标题：第X集：集名
- ✅ 结尾：第X集完
- ✅ 对话：≤15字/句
- ✅ 每集：≥500字，≥3爽点+1甜点
- ❌ 禁止：耀/曜、【】括号

### 发布流程
1. 使用编剧工坊创作剧本
2. 运行格式校验：`python scripts/check_format.py`
3. 运行数据分析：`python scripts/stats_analyzer.py`
4. 提交到 [awesome-ai-short-drama](https://github.com/Zeon7744/awesome-ai-short-drama) 仓库

---

## 详细文档

- [功能特性](./docs/FEATURES.md)
- [工作流说明](./docs/WORKFLOW.md)
- [安装配置](./docs/SETUP.md)
- [三平台联动](./docs/PLATFORMS.md)
- [编剧工坊融合指南](./docs/SCREENWRITING_INTEGRATION.md)

---

*由 [红剑](https://github.com/Zeon7744) 维护*  
*Vibe Coding · 自然语言驱动开发*
