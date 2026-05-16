"""
直接导出包含 Tier 关键词的 script 标签原始内容，分析编码格式。
"""
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://windrosewiki.org'
url = '/database/items/eid-melee-weapon-saber-blank-base'

res = requests.get(BASE_URL + url, timeout=15)
soup = BeautifulSoup(res.text, 'html.parser')

scripts = soup.find_all('script')

for i, script in enumerate(scripts):
    content = script.string or ''
    if 'Tier' in content and 'Station Lv' in content:
        print(f"=== Script #{i}, 长度 {len(content)} ===\n")
        # 打印前 3000 字符
        print(content[:3000])
        print("\n\n... (中间省略) ...\n\n")
        # 打印最后 1000 字符
        print(content[-1000:])
        print(f"\n=== END Script #{i} ===\n")
