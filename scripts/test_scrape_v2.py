"""
测试 v2 爬虫的解析逻辑，只处理 3 个代表性物品。
"""
import json
import sys
sys.path.insert(0, '.')
from scripts.scrape_competitor import fetch_page, parse_item, BASE_URL

test_urls = [
    '/database/items/eid-cannon-12-cold-barrels-advanced',  # 12-Pounder: Tempered (有 Attack/Level)
    '/database/items/eid-melee-weapon-saber-blank-base',  # Saber - 有 3 级制作
    '/database/items/aid-ammo-firearm-projectile-stone-bullet-t01',  # Stone Bullet
    '/database/items/did-resource-wood-t01',  # Wood - 资源，可能无制作
]

for url in test_urls:
    item_id = url.split('/')[-1]
    html = fetch_page(f"{BASE_URL}{url}")
    item = parse_item(html, item_id, url)

    if item:
        print(f"\n{'='*60}")
        print(f"物品: {item['name']}")
        print(f"分类: {item['category']}, 稀有度: {item['tier']}")
        print(f"Level: {item.get('level')}, Attack: {item.get('attack')}")
        print(f"图标: {item['icon']}")
        print(f"概述: {item['description'][:80]}...")

        crafting = item.get('crafting', {})
        tiers = crafting.get('tiers', [])
        if tiers:
            print(f"制作配方: {len(tiers)} 级")
            for t in tiers:
                print(f"  Tier {t['level']}: {t['station']}, {t['time']}")
                for m in t['materials']:
                    print(f"    - {m['name']} x{m['amount']} icon={m['icon'][:30] if m['icon'] else 'NONE'}...")
        else:
            print("制作配方: 无")
    else:
        print(f"\n[FAIL] {url} 解析失败")
