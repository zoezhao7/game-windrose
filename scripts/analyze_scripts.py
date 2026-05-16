"""
分析竞品页面中 script 标签里的嵌入式 JSON 数据。
Next.js 通常会把页面数据以 JSON 形式嵌入 script 标签中。
"""
import requests
from bs4 import BeautifulSoup
import json
import re

BASE_URL = 'https://windrosewiki.org'
url = '/database/items/eid-melee-weapon-saber-blank-base'

res = requests.get(BASE_URL + url, timeout=15)
soup = BeautifulSoup(res.text, 'html.parser')

# 查找所有 script 标签
scripts = soup.find_all('script')
print(f"找到 {len(scripts)} 个 script 标签\n")

for i, script in enumerate(scripts):
    content = script.string or ''
    if not content:
        src = script.get('src', '')
        if src:
            print(f"Script #{i}: external src={src[:80]}")
        continue

    # 找包含物品数据的 script
    if 'Saber' in content or 'saber' in content:
        print(f"Script #{i}: 包含 'Saber', 长度={len(content)}")

        # 尝试找 JSON 数据
        # Next.js 常见格式: self.__next_f.push([...])
        if '__next_f' in content:
            print("  → 检测到 Next.js flight data")
            # 提取所有 JSON-like 内容
            # 找包含 crafting/materials 的片段
            if 'Copper' in content or 'material' in content.lower() or 'craft' in content.lower():
                print("  → 包含制作相关数据！")
                # 打印相关片段
                for keyword in ['Tier', 'Station', 'material', 'craft', 'Copper', 'ingredient']:
                    idx = content.lower().find(keyword.lower())
                    if idx >= 0:
                        start = max(0, idx - 50)
                        end = min(len(content), idx + 200)
                        snippet = content[start:end].replace('\\n', '\n').replace('\\"', '"')
                        print(f"\n  片段 [{keyword}] 位置 {idx}:")
                        print(f"  {snippet}")
        elif 'application/json' in str(script.get('type', '')):
            print("  → JSON-LD 或内联 JSON")
            try:
                data = json.loads(content)
                print(f"  → 解析成功: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}")
            except:
                print(f"  → 解析失败，前200字符: {content[:200]}")

# 也尝试找 __NEXT_DATA__
next_data_script = soup.find('script', id='__NEXT_DATA__')
if next_data_script:
    print("\n找到 __NEXT_DATA__!")
    data = json.loads(next_data_script.string)
    print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
else:
    print("\n未找到 __NEXT_DATA__ script 标签")

# 检查是否有 JSON-LD
jsonld = soup.find('script', type='application/ld+json')
if jsonld:
    print("\n找到 JSON-LD:")
    print(jsonld.string[:500] if jsonld.string else 'empty')
