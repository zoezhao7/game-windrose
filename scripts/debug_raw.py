"""找出 flight data 实际的 raw bytes"""
import requests
from bs4 import BeautifulSoup

url = 'https://windrosewiki.org/database/items/aid-ammo-firearm-projectile-stone-bullet-t01'
res = requests.get(url, timeout=15)
soup = BeautifulSoup(res.text, 'html.parser')

scripts = soup.find_all('script')
script = scripts[22]  # Contains Stone material
content = script.string

# Show exact bytes around "Click to view"
idx = content.find('Click to view')
raw = content[idx-30:idx+30]
print(f"Raw repr: {repr(raw)}")

# Count actual backslashes
bs_count = raw.count('\\')
print(f"Backslash count in snippet: {bs_count}")

# Try simple approach: just replace \\\" with " (literal backslash-backslash-quote)
test = content
test = test.replace('\\\\\\\"', '"')  # 3 backslashes + quote
test = test.replace('\\\\\"', '"')    # 2 backslashes + quote  
test = test.replace('\\\"', '"')      # 1 backslash + quote
print(f"\nAfter all replaces, 'Click to view' found: {'Click to view' in test}")

import re
mats = re.findall(r'"title":"Click to view ([^"]+)"', test)
print(f"Materials found: {mats}")
hrefs = re.findall(r'"href":"(/database/items/[^"]+)"', test)
print(f"hrefs: {hrefs}")
