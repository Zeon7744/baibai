# 安装配置

## 环境要求

- Node.js 18+
- Python 3.10+
- npm / pnpm
- OpenRouter API Key 或 Anthropic API Key

---

## 前端配置

### 1. 克隆仓库

```bash
git clone https://github.com/Zeon7744/baibai.git
cd baibai/webapp
```

### 2. 安装依赖

```bash
npm install
# 或使用 pnpm
pnpm install
```

### 3. 配置环境变量

```bash
# webapp/.env.local
OPEN_ROUTER_API_KEY=your_key_here
# 或
ANTHROPIC_API_KEY=your_key_here
```

### 4. 启动开发服务器

```bash
npm run dev
# 访问 http://localhost:3000
```

---

## 后端配置

### 1. 进入后端目录

```bash
cd ../server
```

### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# server/.env.local
OPEN_ROUTER_API_KEY=your_key_here
# 或
ANTHROPIC_API_KEY=your_key_here
```

### 4. 启动后端服务

```bash
python main.py
# 访问 http://localhost:8000
```

---

## 环境变量详解

### OpenRouter（推荐）

支持多模型，按量计费：
- Claude 3 Opus
- GPT-4 Turbo
- Gemini Pro

### Anthropic

直接调用 Claude API：
- 更稳定
- 但成本较高

### 本地模型（可选）

支持 Ollama 等本地部署模型：
```bash
# .env.local
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

---

## 运行测试

```bash
# 前端测试
cd webapp
npm test

# 后端测试
cd server
pytest
```

---

## 生产部署

### 前端构建

```bash
cd webapp
npm run build
# 产物在 webapp/.next/
```

### 后端生产运行

```bash
cd server
pip install uvicorn[standard]
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 常见问题

### Q: API Key 无效？
检查 Key 是否正确复制，注意首尾空格。

### Q: 端口冲突？
修改 `webapp/.env.local` 中的端口配置。

### Q: 预览不刷新？
点击预览面板的刷新按钮，或重启开发服务器。

---

*详见 [功能特性](./FEATURES.md) 和 [工作流说明](./WORKFLOW.md)*
