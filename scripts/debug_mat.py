"""Debug material pattern matching"""
import requests
from bs4 import BeautifulSoup
import re

url = 'https://windrosewiki.org/database/items/aid-ammo-firearm-projectile-stone-bullet-t01'
res = requests.get(url, timeout=15)
soup = BeautifulSoup(res.text, 'html.parser')

scripts = soup.find_all('script')
all_flight = []
for script in scripts:
    content = script.string or ''
    if '__next_f' in content:
        all_flight.append(content)

full_text = "\n".join(all_flight)
text = full_text.replace(chr(92), '')

# 找到 "Click to view Stone" 的上下文
idx = text.find('Click to view Stone')
if idx >= 0:
    snippet = text[max(0, idx-200):idx+400]
    print(f"Context around 'Click to view Stone':")
    print(repr(snippet))
    print()
    print("Readable:")
    print(snippet)
else:
    # 搜索所有 Click to view
    all_clicks = [(m.start(), m.group()) for m in re.finditer(r'Click to view [A-Z][a-z]+', text)]
    print(f"All Click to view: {all_clicks}")
