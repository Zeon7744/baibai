#!/bin/bash
# 更新爱发电赞助者名单和短剧项目展示

AFDIAN_USER_ID="0c59dda8a1bb11f19b9552540025c377"
AFDIAN_TOKEN="${AFDIAN_TOKEN}"

# 获取时间戳
TS=$(date +%s)
PARAMS='{"page":1}'
SIGN=$(echo -n "${AFDIAN_TOKEN}${PARAMS}${TS}${AFDIAN_USER_ID}" | md5sum | cut -d' ' -f1)

# 调用爱发电API
curl -s -X POST "https://afdian.net/api/open/query-sponsor" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"${AFDIAN_USER_ID}\", \"params\": \"${PARAMS}\", \"ts\": ${TS}, \"sign\": \"${SIGN}\"}" \
  > /tmp/afdian_resp.json

# 使用Python处理JSON并更新README
python3 << 'PYEOF'
import json
import re
import os
import glob

# 读取爱发电响应
with open('/tmp/afdian_resp.json') as f:
    data = json.load(f)

if data.get('ec') != 200:
    print('API Error:', data.get('em'))
    exit(1)

# 生成赞助者列表
sponsors = data['data']['list']
sponsor_lines = []
for s in sponsors[:20]:
    u = s.get('user', {})
    sponsor_lines.append(f"- [{u.get('name', '匿名')}](https://afdian.net/u/{u.get('user_id', '')})")

sponsors_text = '\n'.join(sponsor_lines) if sponsor_lines else '暂无赞助者'

sponsors_section = f"""## 🙏 感谢赞助

{sponsors_text}

---

"""

# 扫描短剧项目
script_dirs = glob.glob('../短剧生成助手/短剧项目/*')
drama_list = []
for d in script_dirs:
    if os.path.isdir(d):
        project_name = os.path.basename(d)
        # 查找剧本文件
        script_file = None
        for f in glob.glob(os.path.join(d, '*_完整剧本.md')):
            script_file = f
            break
        
        if script_file:
            drama_list.append({
                'name': project_name,
                'path': f'../短剧生成助手/短剧项目/{project_name}',
                'script': os.path.basename(script_file)
            })

# 生成短剧项目列表
drama_section = """## 🎬 短剧项目

"""
if drama_list:
    for drama in sorted(drama_list, key=lambda x: x['name']):
        drama_section += f"- **{drama['name']}** - [`{drama['script']}`]({drama['path']}/{drama['script']})\n"
else:
    drama_section += "暂无短剧项目\n"

drama_section += """

---

## 📝 使用说明

### 创作短剧

使用 [编剧工坊](https://zeon7744.github.io/baibai/编剧工坊.html) 进行短剧创作：

1. 打开编剧工坊网页
2. 选择创作模式（要素生成/小说改编）
3. 填写故事要素或上传小说
4. 生成并导出剧本
5. 将剧本文件添加到 `短剧项目/{剧名}/` 目录
6. 提交到GitHub，自动同步到Gitee

### 三平台联动

- **GitHub**: [主仓库](https://github.com/Zeon7744/baibai) — 代码与创作工具
- **Gitee**: [镜像仓库](https://gitee.com/Zeon7744/baibai) — 国内同步镜像
- **爱发电**: [赞助页面](https://ifdian.net/a/Zeon7744) — 支持创作者

---

"""

# 读取现有README
content = open('README.md', encoding='utf-8').read()

# 替换赞助者部分
if '## 🙏 感谢赞助' in content:
    pattern = r'## 🙏 感谢赞助\s*\n.*?(?=\n## |\\Z)'
    content = re.sub(pattern, sponsors_section.strip() + '\n', content, flags=re.DOTALL)
else:
    content = content.rstrip() + '\n\n' + sponsors_section

# 替换短剧项目部分（在感谢赞助之前插入）
drama_placeholder = '<!-- DRAMA_PROJECTS -->'
if drama_placeholder in content:
    content = content.replace(drama_placeholder, drama_section.strip())
else:
    # 如果没有占位符，插入到感谢赞助之前
    if '## 🙏 感谢赞助' in content:
        content = content.replace('## 🙏 感谢赞助', drama_section.strip() + '\n\n## 🙏 感谢赞助')

# 写回README
open('README.md', 'w', encoding='utf-8').write(content)

print(f'Updated README: {len(drama_list)} drama projects, {len(sponsors)} sponsors')
PYEOF
