# GitHub Workflow 文件上传指南

## 当前状态
- ✅ GitHub仓库已创建：https://github.com/Zeon7744/baibai
- ✅ README.md 和 docs/ 目录已上传
- ⚠️ workflow文件因Token权限限制需手动上传

## 手动上传步骤

### 1. 访问仓库
打开 https://github.com/Zeon7744/baibai

### 2. 创建目录
- 点击 `Add file` > `Create new file`
- 在文件名输入框中输入：`.github/workflows/sync-to-gitee.yml`
- GitHub会自动创建目录结构

### 3. 粘贴第一个文件内容
复制以下内容到编辑器：

```yaml
name: Sync to Gitee

on:
  push:
    branches: [main, master]
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Sync to Gitee
        env:
          GITEE_TOKEN: ${{ secrets.GITEE_TOKEN }}
          GITEE_USER: ${{ secrets.GITEE_USER }}
        run: |
          # 添加 Gitee remote
          git remote add gitee https://${{ secrets.GITEE_USER }}:${GITEE_TOKEN}@gitee.com/${{ secrets.GITEE_USER }}/baibai.git
          # 推送所有分支
          git push gitee --all --force
          # 推送标签
          git push gitee --tags --force
```

### 4. 提交文件
- 滚动到页面底部
- 点击 `Commit new file`

### 5. 重复上述步骤创建第二个文件
文件名：`.github/workflows/afdian-sponsors.yml`

内容：
```yaml
name: 更新爱发电赞助者名单

on:
  schedule:
    - cron: '0 9 * * *'
  workflow_dispatch:

jobs:
  update-sponsors:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Fetch Afdian Sponsors
        env:
          AFDIAN_USER_ID: "0c59dda8a1bb11f19b9552540025c377"
          AFDIAN_TOKEN: "${{ secrets.AFDIAN_TOKEN }}"
        run: |
          TS=$(date +%s)
          PARAMS='{"page":1}'
          SIGN=$(echo -n "${AFDIAN_TOKEN}${PARAMS}${TS}${AFDIAN_USER_ID}" | md5sum | cut -d' ' -f1)
          
          RESPONSE=$(curl -s -X POST "https://afdian.net/api/open/query-sponsor" \
            -H "Content-Type: application/json" \
            -d "{\"user_id\": \"${AFDIAN_USER_ID}\", \"params\": \"${PARAMS}\", \"ts\": ${TS}, \"sign\": \"${SIGN}\"}")
          
          echo "$RESPONSE" | python3 -c "
import json,sys
data=json.load(sys.stdin)
if data.get('ec')!=200:
    print('API Error:',data.get('em'));sys.exit(1)
sponsors=data['data']['list']
lines=[]
for s in sponsors[:20]:
    u=s.get('user',{})
    lines.append(f\"- [{u.get('name','匿名')}](https://afdian.net/u/{u.get('user_id','')})\")
print('\n'.join(lines))
" > /tmp/sponsors.txt
          cat /tmp/sponsors.txt

      - name: Update README
        run: |
          SPONSORS=$(cat /tmp/sponsors.txt 2>/dev/null || echo "暂无赞助者")
          
          python3 << PYEOF
import re
content = open("README.md", encoding="utf-8").read()
sponsor_section = f"""## 🙏 感谢赞助

{SPONSORS}

---
"""
          pattern = r'## 🙏 感谢赞助\s*\n.*?(?=\n## |\Z)'
          if "## 🙏 感谢赞助" in content:
              content = re.sub(pattern, sponsor_section + "\n", content, flags=re.DOTALL)
          else:
              content = content.rstrip() + "\n\n" + sponsor_section
          open("README.md", "w", encoding="utf-8").write(content)
PYEOF

      - name: Commit and Push
        run: |
          git config user.email "action@github.com"
          git config user.name "GitHub Action"
          git add README.md
          git diff --staged --quiet || git commit -m "chore: update afdian sponsors"
          git push
```

## 配置 GitHub Secrets

上传完文件后，需要配置 Secrets：

1. 进入仓库 Settings > Secrets and variables > Actions
2. 点击 `New repository secret`
3. 添加以下三个Secret：

| Secret名称 | 值 |
|-----------|-----|
| AFDIAN_TOKEN | WTcfMbUpkvFdACswPruY3ySxG87KJ45e |
| GITEE_TOKEN | 03be1ea3a7dbd34d1a7669426ea133d8 |
| GITEE_USER | Zeon7744 |

## 验证

上传完成后，访问 https://github.com/Zeon7744/baibai/actions 确认workflow是否显示。
