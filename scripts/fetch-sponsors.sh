#!/bin/bash
# Fetch mbd sponsors and update README

MBD_APP_ID="0c59dda8a1bb11f19b9552540025c377"
MBD_API_KEY="${MBD_API_KEY}"

TS=$(date +%s)
PARAMS='{"page":1}'
SIGN=$(echo -n "${MBD_API_KEY}${PARAMS}${TS}${MBD_APP_ID}" | md5sum | cut -d' ' -f1)

curl -s -X POST "https://mbd.pub/@Zeon7744 \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"${MBD_APP_ID}\", \"params\": \"${PARAMS}\", \"ts\": ${TS}, \"sign\": \"${SIGN}\"}" \
  > /tmp/mbd_resp.json

python3 << 'PYEOF'
import json
import sys
import re

with open('/tmp/mbd_resp.json') as f:
    data = json.load(f)

if data.get('ec') != 200:
    print('API Error:', data.get('em'))
    sys.exit(1)

sponsors = data['data']['list']
lines = []
for s in sponsors[:20]:
    u = s.get('user', {})
    lines.append(f"- [{u.get('name', '匿名')}](https://mbd.pub/@Zeon7744 '')})")

sponsors_text = '\n'.join(lines) if lines else '暂无赞助者'

sponsor_section = f"""## 🙏 感谢赞助

{sponsors_text}

---
"""

content = open('README.md', encoding='utf-8').read()
pattern = r'## 🙏 感谢赞助\s*\n.*?(?=\n## |\Z)'

if '## 🙏 感谢赞助' in content:
    content = re.sub(pattern, sponsor_section + '\n', content, flags=re.DOTALL)
else:
    content = content.rstrip() + '\n\n' + sponsor_section

open('README.md', 'w', encoding='utf-8').write(content)
print('README updated with sponsors')
PYEOF
