# 功能特性

## 1. 代码仓库

### 核心代码
- **Vibe Coding 引擎** — 自然语言到代码的转换逻辑
- **项目模板** — React/Next.js/Express/纯 HTML 等模板
- **配置文件** — `.vibe/config.json` 工作流配置

### 工具脚本
- 代码生成器
- 项目初始化器
- 格式化工具

---

## 2. 程序开发

### 开发窗（Web IDE）
- **Monaco Editor** — 专业代码编辑器
- **实时预览** — iframe 内嵌即时查看
- **文件树导航** — 可视化文件浏览
- **终端输出** — 日志与错误展示

### AI 助手
- 代码生成（自然语言描述 → 可运行代码）
- 代码解释（理解现有代码）
- Bug 修复建议
- 架构优化推荐

---

## 3. 工作流自动化

### 自动化能力
- **Git 同步** — GitHub ↔ Gitee 自动镜像
- **赞助管理** — 爱发电赞助者名单自动更新
- **CI/CD** — 测试、构建、部署流程

### 工作流配置
```yaml
# .github/workflows/sync-to-gitee.yml
name: Sync to Gitee
on:
  push:
    branches: [main, master]
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Sync to Gitee
        env:
          GITEE_TOKEN: ${{ secrets.GITEE_TOKEN }}
        run: |
          git remote add gitee https://${{ secrets.GITEE_USER }}:${GITEE_TOKEN}@gitee.com/${{ secrets.GITEE_USER }}/baibai.git
          git push gitee --all --force
```

---

## 4. 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| 前端框架 | Next.js 16 | 应用壳 |
| UI 库 | React 19 + TypeScript | 组件开发 |
| 样式 | TailwindCSS | 原子化样式 |
| 编辑器 | Monaco Editor | 代码编辑 |
| 状态管理 | Zustand | 客户端状态 |
| 后端框架 | FastAPI | Python API |
| AI 服务 | OpenRouter / Anthropic / OpenAI | LLM 调用 |

---

## 5. 使用场景

- [x] 快速原型开发
- [x] 个人工具/小程序
- [x] 学习 AI 辅助编程
- [x] 非程序员构建网页
- [ ] 团队协作开发（规划中）

---

*详见 [工作流说明](./WORKFLOW.md)*
