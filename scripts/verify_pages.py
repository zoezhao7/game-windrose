"""验证生成的页面中关键字段是否正确渲染"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITEMS_DIR = os.path.join(ROOT, 'database', 'items')

# 抽查几个代表性物品
samples = {
    'eid-melee-weapon-saber-blank-base': {
        'name': 'Saber',
        'checks': ['saber', 'Uncommon', 'crafting-premium', 'Copper Ingot', 'Rough Hide', 'Tier 1', 'Tier 2', 'Tier 3', 'weaponsmith', '1s (60/min)']
    },
    'aid-ammo-firearm-projectile-stone-bullet-t01': {
        'name': 'Stone Bullet',
        'checks': ['stone-bullet', 'Uncommon', 'crafting-premium', 'Stone', 'Workbench', '1s (300/min)']
    },
    'did-resource-wood-t01': {
        'name': 'Wood',
        'checks': ['wood', 'Common', 'Overview', 'building material']
    },
}

total_ok = 0
total_fail = 0

for item_id, expected in samples.items():
    page_path = os.path.join(ITEMS_DIR, item_id, 'index.html')
    if not os.path.exists(page_path):
        print(f"FAIL: {expected['name']} 页面不存在: {page_path}")
        total_fail += 1
        continue

    with open(page_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"\n=== {expected['name']} ({item_id}) ===")
    for check in expected['checks']:
        found = check.lower() in content.lower()
        status = "OK" if found else "FAIL"
        if not found:
            total_fail += 1
        else:
            total_ok += 1
        print(f"  [{status}] '{check}'")

# 统计总页面数
page_count = sum(1 for d in os.listdir(ITEMS_DIR) if os.path.isfile(os.path.join(ITEMS_DIR, d, 'index.html')))

# 统计有 crafting 面板的页面数
crafting_count = 0
for d in os.listdir(ITEMS_DIR):
    idx = os.path.join(ITEMS_DIR, d, 'index.html')
    if os.path.isfile(idx):
        with open(idx, 'r', encoding='utf-8') as f:
            if 'crafting-premium' in f.read():
                crafting_count += 1

print(f"\n=== 总体统计 ===")
print(f"详情页总数: {page_count}")
print(f"含制作面板: {crafting_count}")
print(f"抽检通过: {total_ok}")
print(f"抽检失败: {total_fail}")
