#!/bin/bash
# 更新爱发电赞助者名单和短剧项目展示

AFDIAN_USER_ID="0c59dda8a1bb11f19b9552540025c377"
AFDIAN_TOKEN="${AFDIAN_TOKEN}"

# 如果没有TOKEN，跳过爱发电更新
if [ -z "$AFDIAN_TOKEN" ]; then
    echo "Warning: AFDIAN_TOKEN not set, skipping sponsor update"
    AFDIAN_ERROR=true
else
    # 获取时间戳
    TS=$(date +%s)
    PARAMS='{"page":1}'
    SIGN=$(echo -n "${AFDIAN_TOKEN}${PARAMS}${TS}${AFDIAN_USER_ID}" | md5sum | cut -d' ' -f1)

    # 调用爱发电API
    curl -s -X POST "https://afdian.net/api/open/query-sponsor" \
      -H "Content-Type: application/json" \
      -d "{\"user_id\": \"${AFDIAN_USER_ID}\", \"params\": \"${PARAMS}\", \"ts\": ${TS}, \"sign\": \"${SIGN}\"}" \
      > /tmp/afdian_resp.json

    # 检查响应
    if [ ! -s /tmp/afdian_resp.json ]; then
        echo "Error: Empty response from Afdian API"
        AFDIAN_ERROR=true
    fi
fi

# 使用Python处理JSON并更新README
python3 << 'PYEOF'
import json
import re
import os
import glob

# 读取爱发电响应（如果存在）
sponsors_text = '暂无赞助者'
afdian_error = os.environ.get('AFDIAN_ERROR', 'false') == 'true'

if not afdian_error and os.path.exists('/tmp/afdian_resp.json'):
    try:
        with open('/tmp/afdian_resp.json') as f:
            content = f.read().strip()
            if content:
                data = json.loads(content)
                if data.get('ec') == 200:
                    sponsors = data['data']['list']
                    sponsor_lines = []
                    for s in sponsors[:20]:
                        u = s.get('user', {})
                        sponsor_lines.append(f"- [{u.get('name', '匿名')}](https://afdian.net/u/{u.get('user_id', '')})")
                    sponsors_text = '\n'.join(sponsor_lines) if sponsor_lines else '暂无赞助者'
                    print(f"Updated {len(sponsors)} sponsors")
                else:
                    print(f"API Error: {data.get('em')}")
            else:
                print("Empty API response")
    except Exception as e:
        print(f"Error parsing sponsors: {e}")

# 扫描短剧项目
script_dir = '../短剧生成助手/短剧项目'
project_dir = '短剧项目'
drama_list = []

# 优先从本地短剧项目目录读取
if os.path.exists(project_dir):
    script_dirs = glob.glob(os.path.join(project_dir, '*'))
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
                    'script': os.path.basename(script_file)
                })
else:
    print(f"Directory {project_dir} not found")

# 生成短剧项目列表
drama_section = """## 🎬 短剧项目

"""
if drama_list:
    for drama in sorted(drama_list, key=lambda x: x['name']):
        drama_section += f"- **{drama['name']}** - [`{drama['script']}`](./短剧项目/{drama['name']}/{drama['script']})\n"
else:
    drama_section += "暂无短剧项目\n"

drama_section += """

---

"""

# 生成感谢赞助部分
sponsors_section = f"""## 🙏 感谢赞助

{sponsors_text}

---

"""

# 读取现有README
try:
    content = open('README.md', encoding='utf-8').read()
except Exception as e:
    print(f"Error reading README: {e}")
    exit(1)

# 替换短剧项目部分
drama_placeholder = '<!-- DRAMA_PROJECTS -->'
if drama_placeholder in content:
    content = content.replace(drama_placeholder, drama_section.strip())
else:
    # 如果没有占位符，插入到感谢赞助之前
    if '## 🙏 感谢赞助' in content:
        content = content.replace('## 🙏 感谢赞助', drama_section.strip() + '\n\n## 🙏 感谢赞助')

# 替换赞助者部分
if '## 🙏 感谢赞助' in content:
    pattern = r'## 🙏 感谢赞助\s*\n.*?(?=\n## |\Z)'
    content = re.sub(pattern, sponsors_section.strip() + '\n', content, flags=re.DOTALL)
else:
    content = content.rstrip() + '\n\n' + sponsors_section

# 写回README
try:
    open('README.md', 'w', encoding='utf-8').write(content)
    print('README updated successfully')
except Exception as e:
    print(f"Error writing README: {e}")
    exit(1)

print(f'Updated README: {len(drama_list)} drama projects')
PYEOF
