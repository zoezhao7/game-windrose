"""
从 Next.js flight data 中提取完整的制作配方数据。
"""
import requests
from bs4 import BeautifulSoup
import json
import re

BASE_URL = 'https://windrosewiki.org'
url = '/database/items/eid-melee-weapon-saber-blank-base'

res = requests.get(BASE_URL + url, timeout=15)
soup = BeautifulSoup(res.text, 'html.parser')

scripts = soup.find_all('script')

# 收集所有 __next_f.push 的内容
flight_data = []
for script in scripts:
    content = script.string or ''
    if '__next_f' in content and ('Tier' in content or 'Station Lv' in content):
        flight_data.append(content)

print(f"找到 {len(flight_data)} 个包含 Tier/Station 的 flight data 脚本\n")

# 分析包含 Tier 信息最多的那个脚本
for i, content in enumerate(flight_data):
    print(f"\n--- Flight Data #{i}, 长度 {len(content)} ---")
    
    # 提取 Tier 数字
    tier_matches = re.findall(r'"Tier ",(\d+)', content)
    print(f"Tier 数字: {tier_matches}")
    
    # 提取 Station Lv 数字  
    station_matches = re.findall(r'"Station Lv ",(\d+)', content)
    print(f"Station Lv: {station_matches}")
    
    # 提取制作时间
    time_matches = re.findall(r'"children":"(\d+s \(\d+/min\))"', content)
    print(f"制作时间: {time_matches}")
    
    # 提取材料链接和数量
    # 格式: "href":"/database/items/xxx" ... "children":"Material Name" ... "×",数量
    mat_href_matches = re.findall(r'"href":"/database/items/([^"]+)"', content)
    print(f"材料链接: {mat_href_matches}")
    
    # 提取材料数量
    qty_matches = re.findall(r'"×",(\d+)', content)
    print(f"材料数量: {qty_matches}")
    
    # 提取材料图标
    img_matches = re.findall(r'"src":"(/windrose-data/images/[^"]+)"[^}]*"alt":"([^"]+)"', content)
    print(f"图片: {img_matches}")

    # 尝试找完整的 crafting section 上下文
    # 找到 "Tier " 前后 500 字符
    idx = content.find('"Tier "')
    if idx > 0:
        start = max(0, idx - 100)
        end = min(len(content), idx + 1500)
        snippet = content[start:end]
        # 解码转义
        snippet = snippet.replace('\\\\', '\\').replace('\\"', '"')
        print(f"\n完整 Crafting 上下文:")
        print(snippet[:2000])
