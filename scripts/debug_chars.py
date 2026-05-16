"""Find the exact character sequence before quote marks in flight data"""
import requests
from bs4 import BeautifulSoup

url = 'https://windrosewiki.org/database/items/aid-ammo-firearm-projectile-stone-bullet-t01'
res = requests.get(url, timeout=15)
soup = BeautifulSoup(res.text, 'html.parser')

script = soup.find_all('script')[22]
content = script.string

# Find "Click" and show surrounding chars with ord values
idx = content.find('Click')
if idx > 0:
    snippet = content[idx-10:idx+30]
    for j, ch in enumerate(snippet):
        print(f"  pos[{j}] = {repr(ch)} (ord={ord(ch)})")
