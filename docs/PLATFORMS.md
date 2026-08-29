# 三平台联动配置指南

## 平台架构

```
GitHub (国际) ↔ Gitee (国内) ↔ 爱发电 (赞助变现)
```

| 平台 | 定位 | 地址 |
|------|------|------|
| GitHub | 主仓库（国际） | https://github.com/Zeon7744/baibai |
| Gitee | 镜像同步（国内） | https://gitee.com/Zeon7744/baibai |
| 爱发电 | 赞助变现 | https://ifdian.net/a/Zeon7744 |

---

## 自动同步配置

### 1. Gitee 同步

工作流文件：`.github/workflows/sync-to-gitee.yml`

触发条件：
- 推送到 main/master 分支
- 手动触发（workflow_dispatch）

执行流程：
```
GitHub push → Checkout → Sync to Gitee → Force Push
```

### 2. 爱发电赞助名单更新

工作流文件：`.github/workflows/afdian-sponsors.yml`

触发条件：
- 每天 UTC 09:00（北京时间 17:00）
- 手动触发

执行流程：
```
Cron → Fetch Sponsors → Parse → Update README → Commit → Push
```

---

## Secrets 配置

在 GitHub 仓库设置中添加以下 Secrets：

| Secret 名称 | 值 | 用途 |
|-------------|-----|------|
| `AFDIAN_TOKEN` | `WTcfMbUpkvFdACswPruY3ySxG87KJ45e` | 爱发电 API 认证 |
| `GITEE_TOKEN` | `03be1ea3a7dbd34d1a7669426ea133d8` | Gitee API Token |
| `GITEE_USER` | `Zeon7744` | Gitee 用户名 |

### 设置步骤

1. 打开 GitHub 仓库
2. Settings → Secrets and variables → Actions
3. 点击 "New repository secret"
4. 逐个添加上述三个 Secret

---

## Gitee 仓库创建

### 步骤

1. 打开 https://gitee.com/Zeon7744/baibai
2. 点击 **创建项目**
3. 选择 **空项目**
4. 勾选 **初始化仓库**
5. 点击 **创建项目**

创建后，GitHub Actions 会自动推送代码。

---

## 更新 README

当有赞助者加入时，GitHub Actions 会自动更新 README 中的感谢名单。

更新范围：
- 前 20 名赞助者
- 显示昵称和主页链接
- 格式：`- [昵称](链接)`

---

## 维护说明

### 每月检查项

- [ ] Gitee 同步是否正常
- [ ] 爱发电名单是否更新
- [ ] Secrets 是否过期

### 手动触发工作流

在 GitHub Actions 页面点击 "Run workflow" 即可手动执行。

---

## 其他项目联动

本项目与以下项目共享同一套三平台联动配置：

- `awesome-ai-short-drama` — AI短剧资源清单
- 本仓库 `baibai` — Vibe Coding开发仓库

共用 Secrets，统一维护。

---

*详见 [README.md](../README.md)*
