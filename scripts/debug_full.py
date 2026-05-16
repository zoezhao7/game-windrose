"""直接测试 flight data 解析"""
import requests
from bs4 import BeautifulSoup
import re

url = 'https://windrosewiki.org/database/items/aid-ammo-firearm-projectile-stone-bullet-t01'
res = requests.get(url, timeout=15)
soup = BeautifulSoup(res.text, 'html.parser')

scripts = soup.find_all('script')

# 收集所有 flight data
all_flight = []
for script in scripts:
    content = script.string or ''
    if '__next_f' in content:
        all_flight.append(content)

print(f"Flight data scripts: {len(all_flight)}")

full_text = "\n".join(all_flight)
BACKSLASH = chr(92)
text = full_text.replace(BACKSLASH, '')

print(f"Full text length after unescape: {len(text)}")
print(f"Contains 'Click to view': {'Click to view' in text}")
print(f"Contains 'Tier ': {'Tier ' in text}")
print(f"Contains '/database/items/': {'/database/items/' in text}")
print(f"Contains '/database/stations/': {'/database/stations/' in text}")

# 直接测试正则
station_link = re.search(
    r'"href":"/database/stations/([^"]+)"[^}]*?"title":"Click to view ([^"]+)"',
    text
)
if station_link:
    print(f"Station: {station_link.group(2)}")
else:
    print("Station regex not matched")
    # 尝试更简单的
    s2 = re.search(r'Click to view (\w+)', text)
    if s2:
        print(f"Simple Click to view match: {s2.group(0)}")

# 测试材料正则
mat_pattern = r'"title":"Click to view ([^"]+)"[^}]*?"href":"(/database/items/[^"]+)"'
mat_matches = list(re.finditer(mat_pattern, text))
print(f"Material matches: {len(mat_matches)}")
for m in mat_matches:
    print(f"  {m.group(1)} -> {m.group(2)}")

# 制作时间
time_match = re.search(r'"children":"(\d+s \(\d+/min\))"', text)
print(f"Time: {time_match.group(1) if time_match else 'NONE'}")

# 数量
qty_matches = re.findall(r'\["×",(\d+)\]', text)
print(f"Quantities: {qty_matches}")

# 找引号位置验证
idx = text.find('Click to view')
if idx >= 0:
    snippet = text[idx-30:idx+60]
    print(f"\nSnippet around Click to view: {repr(snippet)}")
