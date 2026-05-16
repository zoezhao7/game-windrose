"""
从现有 data/*.json 中提取 Level 和 Attack 数值，输出到 data/item-stats.json。

Level 提取优先级：
  1. item.level (直接数值)
  2. crafting.tiers[].level 最大值（scraped_items_v2.json）
  3. station_level（recipes.json）
  4. tier（ships.json ships 数组，数值型 tier）

Attack 提取优先级：
  1. item.attack / item.damage / item.atk（当前数据中不存在）
  2. cannons（ships.json ships 数组）

输出：data/item-stats.json
格式：{ "item_id": { "level": 3, "attack": null } }
"""

import json, os

PROJECT = r"F:\aicode\gamedoc"
OUTPUT = os.path.join(PROJECT, "data", "item-stats.json")


def load_json(filename):
    path = os.path.join(PROJECT, "data", filename)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_items(data, key="items"):
    items = data.get(key, data)
    if isinstance(items, dict):
        items = list(items.values())
    return [i for i in items if isinstance(i, dict)]


def extract_level(item):
    # 1. direct level
    lv = item.get("level")
    if isinstance(lv, (int, float)):
        return int(lv)

    # 2. crafting.tiers max level
    crafting = item.get("crafting", {})
    if isinstance(crafting, dict):
        tiers = crafting.get("tiers", [])
        if tiers:
            max_lv = max((t.get("level", 0) for t in tiers if isinstance(t.get("level"), (int, float))), default=0)
            if max_lv > 0:
                return int(max_lv)

    # 3. station_level
    sl = item.get("station_level")
    if isinstance(sl, (int, float)):
        return int(sl)

    # 4. tier (numeric only, ships.json ships)
    tier = item.get("tier")
    if isinstance(tier, (int, float)):
        return int(tier)

    return None


def extract_attack(item):
    # 1. direct attack/damage/atk
    for key in ("attack", "damage", "atk"):
        val = item.get(key)
        if isinstance(val, (int, float)):
            return int(val)

    # 2. cannons (ships)
    cannons = item.get("cannons")
    if isinstance(cannons, (int, float)):
        return int(cannons)

    return None


def main():
    stats = {}

    # ── 1. scraped_items_v2.json ──
    scraped = load_json("scraped_items_v2.json")
    if scraped:
        for item in get_items(scraped):
            item_id = item.get("id")
            if not item_id:
                continue
            lv = extract_level(item)
            atk = extract_attack(item)
            if lv is not None or atk is not None:
                stats[item_id] = {"level": lv, "attack": atk}

    # ── 2. weapons.json ──
    weapons = load_json("weapons.json")
    if weapons:
        for item in get_items(weapons):
            item_id = item.get("id")
            if not item_id or item_id in stats:
                continue
            lv = extract_level(item)
            atk = extract_attack(item)
            if lv is not None or atk is not None:
                stats[item_id] = {"level": lv, "attack": atk}

    # ── 3. recipes.json ──
    recipes = load_json("recipes.json")
    if recipes:
        for item in get_items(recipes):
            item_id = item.get("id")
            if not item_id or item_id in stats:
                continue
            lv = extract_level(item)
            atk = extract_attack(item)
            if lv is not None or atk is not None:
                stats[item_id] = {"level": lv, "attack": atk}

    # ── 4. resources.json ──
    resources = load_json("resources.json")
    if resources:
        for item in get_items(resources, "items") + get_items(resources, "resources"):
            item_id = item.get("id")
            if not item_id or item_id in stats:
                continue
            lv = extract_level(item)
            atk = extract_attack(item)
            if lv is not None or atk is not None:
                stats[item_id] = {"level": lv, "attack": atk}

    # ── 5. ships.json ──
    ships_data = load_json("ships.json")
    if ships_data:
        for item in get_items(ships_data):
            item_id = item.get("id")
            if not item_id or item_id in stats:
                continue
            lv = extract_level(item)
            atk = extract_attack(item)
            if lv is not None or atk is not None:
                stats[item_id] = {"level": lv, "attack": atk}
        # ship 本体（ships 数组）
        for ship in ships_data.get("ships", []):
            item_id = ship.get("id")
            if not item_id or item_id in stats:
                continue
            lv = extract_level(ship)
            atk = extract_attack(ship)
            stats[item_id] = {"level": lv, "attack": atk}

    # ── 6. bosses.json ──
    bosses = load_json("bosses.json")
    if bosses:
        for item in get_items(bosses):
            item_id = item.get("id")
            if not item_id:
                continue
            lv = extract_level(item)
            atk = extract_attack(item)
            if lv is not None or atk is not None:
                stats[item_id] = {"level": lv, "attack": atk}

    # ── 统计 ──
    with_level = sum(1 for v in stats.values() if v["level"] is not None)
    with_attack = sum(1 for v in stats.values() if v["attack"] is not None)

    # ── 写出 ──
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"✅ data/item-stats.json")
    print(f"   总计: {len(stats)} 条")
    print(f"   有 Level: {with_level} 条")
    print(f"   有 Attack: {with_attack} 条")

    # 打印 level 分布
    lv_dist = {}
    for v in stats.values():
        lv = v["level"]
        if lv is not None:
            lv_dist[lv] = lv_dist.get(lv, 0) + 1
    if lv_dist:
        print(f"   Level 分布: {dict(sorted(lv_dist.items()))}")


if __name__ == "__main__":
    main()