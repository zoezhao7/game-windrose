"""
将 scraped_items.json 中采集到的真实数据合并到现有的 data/*.json 中，
确保每个物品都能获得真实的 name、category、tier、description、icon 等字段。
同时生成一个统一的 all_items.json 供 gen_detail_pages.py 使用。
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, 'data')

# 加载采集到的全量数据
with open(os.path.join(DATA_DIR, 'scraped_items.json'), 'r', encoding='utf-8') as f:
    scraped = json.load(f)

# 按 slug 建立索引，方便查找
scraped_by_slug = {}
for item in scraped['items']:
    slug = item.get('slug', '')
    scraped_by_slug[slug] = item

# 按 id 也建立索引（id 就是 slug）
scraped_by_id = {}
for item in scraped['items']:
    scraped_by_id[item['id']] = item

print(f"已加载 {len(scraped['items'])} 条采集数据")

# 加载现有的各 data/*.json 文件
data_files = {
    'weapons': 'weapons.json',
    'bosses': 'bosses.json',
    'recipes': 'recipes.json',
    'resources': 'resources.json',
    'ships': 'ships.json',
}

updated_count = 0
for key, filename in data_files.items():
    fpath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(fpath):
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 获取物品列表（不同文件结构不同）
    item_lists = []
    if 'items' in data:
        item_lists.append(data['items'])
    if 'resources' in data:
        item_lists.append(data['resources'])
    if 'ships' in data:
        item_lists.append(data['ships'])

    for items_list in item_lists:
        for item in items_list:
            item_id = item.get('id', '')
            # 尝试在采集数据中找到匹配
            matched = scraped_by_id.get(item_id)
            if not matched:
                # 尝试用 slug 匹配
                slug = item.get('slug', '')
                matched = scraped_by_slug.get(slug)

            if matched:
                # 用采集到的真实数据更新（只更新非空字段，不覆盖已有好数据）
                if matched.get('name'):
                    item['name'] = matched['name']
                if matched.get('icon'):
                    item['icon'] = matched['icon']
                if matched.get('description'):
                    item['description'] = matched['description']
                if matched.get('category') and matched['category'] != 'unknown':
                    item['category'] = matched['category']
                if matched.get('tier') and matched['tier'] != 'common':
                    item['tier'] = matched['tier']
                if matched.get('confidence'):
                    item['confidence'] = matched['confidence']
                updated_count += 1

    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

print(f"已更新 {updated_count} 条现有记录")

# 找出采集到但现有 data/*.json 中不存在的物品
existing_ids = set()
for key, filename in data_files.items():
    fpath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for k in ['items', 'resources', 'ships']:
        if k in data:
            for item in data[k]:
                existing_ids.add(item.get('id', ''))

new_items = []
for item in scraped['items']:
    if item['id'] not in existing_ids:
        new_items.append(item)

print(f"采集数据中有 {len(new_items)} 个新物品不在现有 data/*.json 中")

# 将新物品按分类归入对应的 JSON 文件
# NOTE: 分类映射规则
CATEGORY_FILE_MAP = {
    'melee-weapon': 'weapons.json',
    'range-weapon': 'weapons.json',
    'ammo': 'weapons.json',
    'tool': 'weapons.json',
    'armor': 'weapons.json',
    'ring': 'weapons.json',
    'necklace': 'weapons.json',
    'backpack': 'weapons.json',
    'resource': 'resources.json',
    'metal': 'resources.json',
    'food': 'resources.json',
    'alchemy': 'resources.json',
    'medicine': 'resources.json',
    'ship-weapon': 'ships.json',
    'ship-hull-mod': 'ships.json',
    'ship-combat-order': 'ships.json',
    'misc': 'recipes.json',
    'default': 'recipes.json',
}

added_count = 0
for item in new_items:
    cat = item.get('category', 'misc')
    target_file = CATEGORY_FILE_MAP.get(cat, 'recipes.json')
    fpath = os.path.join(DATA_DIR, target_file)

    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 确定要追加到哪个列表
    if target_file == 'ships.json':
        if 'items' not in data:
            data['items'] = []
        data['items'].append(item)
    elif target_file == 'resources.json':
        if 'items' not in data:
            data['items'] = []
        data['items'].append(item)
    else:
        if 'items' not in data:
            data['items'] = []
        data['items'].append(item)

    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    added_count += 1

print(f"已新增 {added_count} 条物品到 data/*.json")
print(f"\n=== 合并完成 ===")
print(f"总计：更新 {updated_count} + 新增 {added_count} = {updated_count + added_count} 条")
