# Baibai 发布指南

本文档说明如何在 Baibai 发布项目、应用和测试版本。

---

## 发布类型

| 类型 | 说明 | 位置 | 状态 |
|------|------|------|------|
| **完整项目** | 可运行的应用/工具 | `projects/` | Stable |
| **工具脚本** | 单文件工具 | `tools/` | Stable |
| **示例代码** | 学习演示 | `examples/` | Beta |
| **试用版本** | Beta/RC 版本 | `releases/` | Beta |

---

## 发布流程

### 1. 准备发布内容

```bash
# 创建版本目录
mkdir -p releases/v1.0.0

# 复制发布文件
cp -r tools/ releases/v1.0.0/
cp -r templates/ releases/v1.0.0/
cp README.md releases/v1.0.0/
```

### 2. 创建版本信息

```bash
# 使用发布脚本
python scripts/release.py 1.0.0 "首次通用化工具库发布"
```

### 3. 更新版本文件

编辑根目录的 `VERSION.md`：

```markdown
## 当前版本
- **主版本**: 1.0.0
- **发布日期**: 2026-08-30
- **状态**: Beta
```

### 4. 更新变更日志

编辑 `CHANGELOG.md`，添加新版本条目：

```markdown
## [1.0.0] - 2026-08-30

### 新增
- 首次通用化工具库发布
- 7 个核心工具模块
- MCP 协议支持
- pip 安装支持
```

### 5. 提交推送

```bash
git add .
git commit -m "release: v1.0.0"
git tag v1.0.0
git push origin main --tags
```

---

## GitHub Releases

### 创建 Release

1. 访问 https://github.com/Zeon7744/baibai/releases/new
2. 选择 Tag: `v1.0.0`
3. 填写 Release title 和 Description
4. 上传构建产物（可选）
5. 点击 Publish release

### 发布说明模板

使用 `.github/release-template.md` 作为模板。

---

## PyPI 发布

### 安装 twine

```bash
pip install twine
```

### 构建发布包

```bash
python setup.py sdist bdist_wheel
```

### 上传到 PyPI

```bash
twine upload dist/*
```

或使用测试 PyPI：

```bash
twine upload --repository testpypi dist/*
```

---

## 发布检查清单

- [ ] 版本号正确（SEMVER）
- [ ] CHANGELOG.md 已更新
- [ ] VERSION.md 已更新
- [ ] 测试通过 (`pytest`)
- [ ] 文档已更新
- [ ] GitHub Release 已创建
- [ ] PyPI 包已上传（如适用）

---

## 快速参考

### 常用命令

```bash
# 查看版本
cat VERSION.md

# 创建发布
python scripts/release.py <version> <description>

# 构建发布包
python setup.py sdist bdist_wheel

# 上传到 PyPI
twine upload dist/*

# 创建 GitHub Release
# 访问 https://github.com/Zeon7744/baibai/releases/new
```

### 版本命名规则

- `1.0.0` - 正式稳定版
- `1.1.0` - 新功能（向后兼容）
- `1.0.1` - Bug 修复
- `1.0.0-beta.1` - Beta 测试版
- `1.0.0-rc.1` - 候选发布版

---

## 示例项目

查看 `example-project/` 了解完整的发布项目结构。
