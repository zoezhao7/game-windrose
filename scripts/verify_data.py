"""
数据采集完整性验证脚本。
检查 scraped_items.json 中所有物品的字段完整度及对应图片是否存在。
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, 'data', 'scraped_items.json'), 'r', encoding='utf-8') as f:
    d = json.load(f)

items = d['items']
total = len(items)
has_icon = sum(1 for x in items if x.get('icon'))
has_desc = sum(1 for x in items if x.get('description'))
has_level = sum(1 for x in items if x.get('level') is not None)
has_category = sum(1 for x in items if x.get('category') and x['category'] != 'unknown')
has_rarity = sum(1 for x in items if x.get('tier') and x['tier'] != 'common')

# 检查图片文件是否真实存在
img_dir = os.path.join(ROOT, 'imgs', 'database', 'items')
img_files = set(os.listdir(img_dir)) if os.path.exists(img_dir) else set()
icon_exists = 0
icon_missing = []
for x in items:
    icon = x.get('icon', '')
    if icon:
        fname = icon.split('/')[-1]
        if fname in img_files:
            icon_exists += 1
        else:
            icon_missing.append(f"{x['name']} -> {fname}")

print("=== 数据采集完整性报告 ===")
print(f"总采集物品数: {total}")
print(f"有图标路径: {has_icon}/{total}")
print(f"图标文件真实存在: {icon_exists}/{has_icon}")
print(f"有描述: {has_desc}/{total}")
print(f"有等级: {has_level}/{total}")
print(f"有分类: {has_category}/{total}")
print(f"有稀有度(非common): {has_rarity}/{total}")
print(f"图片目录总文件数: {len(img_files)}")
print()

if icon_missing:
    print(f"图标缺失({len(icon_missing)}个):")
    for m in icon_missing[:20]:
        print(f"  {m}")
    if len(icon_missing) > 20:
        print(f"  ... 及其他 {len(icon_missing)-20} 个")
else:
    print("✅ 所有图标文件均存在！")

# 抽样展示几条数据
print()
print("=== 数据抽样 ===")
samples = ['Saber', 'Stone Bullet', 'Iron Bullet', 'Copper Ingot', 'Blunderbuss', 'Infantry Musket']
for name_key in samples:
    found = next((x for x in items if x['name'] == name_key), None)
    if found:
        icon_ok = "有" if found.get('icon') else "无"
        desc_ok = "有" if found.get('description') else "无"
        print(f"  {found['name']}: category={found['category']}, tier={found['tier']}, level={found.get('level')}, icon={icon_ok}, desc={desc_ok}")
    else:
        print(f"  {name_key}: 未找到")

# 分类统计
print()
print("=== 分类统计 ===")
cats = {}
for x in items:
    c = x.get('category', 'unknown')
    cats[c] = cats.get(c, 0) + 1
for c, n in sorted(cats.items(), key=lambda x: -x[1]):
    print(f"  {c}: {n}")
