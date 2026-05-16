"""检查重复的旧数据条目"""
import json

with open('data/weapons.json', encoding='utf-8') as f:
    d = json.load(f)

items = d['items']

# 检查旧分类中缺少 icon 且名称与新采集数据重复的条目
old_melee = [i for i in items if i.get('category') == 'melee']
new_melee = [i for i in items if i.get('category') == 'melee-weapon']

print("=== 旧 category='melee' 条目 ===")
for o in old_melee:
    # 检查是否在新数据中已有同名条目
    matching = [n for n in new_melee if n['name'].lower() == o['name'].lower()]
    has_match = len(matching) > 0
    print(f"  id={o['id']:50s} name={o['name']:25s} icon={bool(o.get('icon')):5s} has_new_match={has_match}")

old_ranged = [i for i in items if i.get('category') == 'ranged']
new_ranged = [i for i in items if i.get('category') == 'range-weapon']

print("\n=== 旧 category='ranged' 条目 ===")
for o in old_ranged:
    matching = [n for n in new_ranged if n['name'].lower() == o['name'].lower()]
    has_match = len(matching) > 0
    print(f"  id={o['id']:50s} name={o['name']:25s} icon={bool(o.get('icon')):5s} has_new_match={has_match}")
