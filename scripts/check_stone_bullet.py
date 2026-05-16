"""直接检查 Stone Bullet 所有包含 Click to view 的 script"""
import requests
from bs4 import BeautifulSoup
import re

url = 'https://windrosewiki.org/database/items/aid-ammo-firearm-projectile-stone-bullet-t01'
res = requests.get(url, timeout=15)
soup = BeautifulSoup(res.text, 'html.parser')

scripts = soup.find_all('script')
for i, script in enumerate(scripts):
    content = script.string or ''
    if not content:
        continue
    decoded = content.replace('\\"', '"').replace('\\\\', '\\')
    if 'Click to view' in decoded:
        print(f"\n=== Script #{i}, len={len(content)} ===")
        # 找所有 Click to view 条目
        clicks = re.findall(r'"title":"Click to view ([^"]+)"', decoded)
        print(f"Click to view: {clicks}")
        
        # 找 href
        hrefs = re.findall(r'"href":"(/database/(?:items|stations)/[^"]+)"', decoded)
        print(f"hrefs: {hrefs}")
        
        # 找时间
        times = re.findall(r'"children":"(\d+s \(\d+/min\))"', decoded)
        print(f"times: {times}")
        
        # 找数量
        qtys = re.findall(r'\["×",(\d+)\]', decoded)
        print(f"qtys: {qtys}")
        
        # 找图片
        imgs = re.findall(r'"src":"(/windrose-data/images/[^"]+)"', decoded)
        print(f"imgs: {imgs}")
