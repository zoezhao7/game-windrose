"""Debug the actual escape sequences in flight data"""
import requests
from bs4 import BeautifulSoup
import re

url = 'https://windrosewiki.org/database/items/aid-ammo-firearm-projectile-stone-bullet-t01'
res = requests.get(url, timeout=15)
soup = BeautifulSoup(res.text, 'html.parser')

scripts = soup.find_all('script')
for i, script in enumerate(scripts):
    content = script.string or ''
    if '__next_f' not in content:
        continue
    if 'Stone' not in content and 'stone' not in content:
        continue
    
    print(f"\n=== Script #{i} (len={len(content)}) ===")
    # Show raw bytes around "Click to view"
    idx = content.find('Click to view')
    if idx >= 0:
        raw = content[max(0, idx-50):idx+80]
        print(f"RAW around 'Click to view': {repr(raw)}")
    
    # Check what escape chars are actually present
    has_backslash_quote = '\\"' in content
    has_double_backslash = '\\\\' in content
    print(f"Contains backslash-quote: {has_backslash_quote}")
    print(f"Contains double-backslash: {has_double_backslash}")
    
    # Try different unescape approaches
    decoded1 = content.replace('\\"', '"')
    decoded2 = content.replace('\\\\', '\\').replace('\\"', '"')
    
    has_click_d1 = 'Click to view' in decoded1
    has_click_d2 = 'Click to view' in decoded2
    print(f"After decode1: has Click to view = {has_click_d1}")
    print(f"After decode2: has Click to view = {has_click_d2}")
    
    # Check if material pattern matches
    for decoded in [content, decoded1, decoded2]:
        mats = re.findall(r'"title":"Click to view ([^"]+)"', decoded)
        if mats:
            print(f"  Found materials: {mats}")
            break
    
    # Also try the raw content pattern matching
    mats_raw = re.findall(r'Click to view ([^\\]+?)\\', content)
    if mats_raw:
        print(f"  Raw pattern materials: {mats_raw}")
