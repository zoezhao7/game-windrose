"""
阶段2: 数据批量补充
- 配方扩充至100+
- 资源详情扩充
- 武器Tier List
- 船只详细数据
"""
import json, os
ROOT = r"F:\aicode\gamedoc"

def load_json(name):
    p = os.path.join(ROOT, "data", name)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json(name, data):
    p = os.path.join(ROOT, "data", name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  ✅ data/{name}")

# === 1. 扩充配方数据 ===
NEW_RECIPES = [
    # Workbench Lv1 - Tools
    {"id":"stone-axe","name":"Stone Axe","category":"tool","station":"workbench","station_level":1,
     "materials":[{"item":"Stone","qty":3},{"item":"Wood","qty":3}],"tips":"Basic wood chopping tool.","confidence":"verified"},
    {"id":"stone-pickaxe","name":"Stone Pickaxe","category":"tool","station":"workbench","station_level":1,
     "materials":[{"item":"Stone","qty":3},{"item":"Wood","qty":3}],"tips":"First mining tool. Mines Clay, Copper.","confidence":"verified"},
    {"id":"torch","name":"Torch","category":"tool","station":"workbench","station_level":1,
     "materials":[{"item":"Wood","qty":1},{"item":"Plant Fiber","qty":2}],"tips":"Essential for caves.","confidence":"verified"},
    {"id":"bandage","name":"Bandage","category":"consumable","station":"workbench","station_level":1,
     "materials":[{"item":"Coarse Fabric","qty":1}],"tips":"Basic healing. Always carry 10+.","confidence":"verified"},
    {"id":"coarse-fabric","name":"Coarse Fabric","category":"material","station":"workbench","station_level":1,
     "materials":[{"item":"Plant Fiber","qty":3}],"tips":"Used in bags, bandages, sails.","confidence":"verified"},
    {"id":"rope","name":"Rope","category":"material","station":"workbench","station_level":1,
     "materials":[{"item":"Plant Fiber","qty":3}],"tips":"Used in bags, bells, ship parts.","confidence":"verified"},
    {"id":"torn-sailcloth-bag","name":"Torn Sailcloth Bag","category":"equipment","station":"workbench","station_level":1,
     "materials":[{"item":"Coarse Fabric","qty":2},{"item":"Rope","qty":1}],"tips":"First inventory upgrade.","confidence":"verified"},
    {"id":"fast-travel-bell","name":"Fast Travel Bell","category":"structure","station":"workbench","station_level":1,
     "materials":[{"item":"Copper Ingot","qty":10},{"item":"Rope","qty":3}],"tips":"Place at bases for teleportation.","confidence":"verified"},
    # Structures
    {"id":"bonfire","name":"Bonfire","category":"structure","station":"hand","station_level":0,
     "materials":[{"item":"Wood","qty":5}],"tips":"Light, warmth, Ash production.","confidence":"verified"},
    {"id":"workbench","name":"Workbench","category":"structure","station":"hand","station_level":0,
     "materials":[{"item":"Wood","qty":5}],"tips":"Core crafting station.","confidence":"verified"},
    {"id":"cooking-fire","name":"Cooking Fire","category":"structure","station":"hand","station_level":0,
     "materials":[{"item":"Wood","qty":3},{"item":"Stone","qty":3}],"tips":"Cook food for better buffs.","confidence":"verified"},
    {"id":"tent","name":"Tent","category":"structure","station":"hand","station_level":0,
     "materials":[{"item":"Wood","qty":4},{"item":"Plant Fiber","qty":10}],"tips":"First shelter. Sets respawn.","confidence":"verified"},
    {"id":"charcoal-kiln","name":"Charcoal Kiln","category":"structure","station":"hand","station_level":0,
     "materials":[{"item":"Wood","qty":25},{"item":"Clay","qty":20}],"tips":"Converts Wood to Charcoal.","confidence":"verified"},
    {"id":"smelting-furnace","name":"Smelting Furnace","category":"structure","station":"hand","station_level":0,
     "materials":[{"item":"Clay","qty":15},{"item":"Stone","qty":30}],"tips":"Smelt ores into ingots.","confidence":"verified"},
    {"id":"armor-workshop","name":"Armor Workshop","category":"structure","station":"hand","station_level":0,
     "materials":[{"item":"Rough Hide","qty":5},{"item":"Wood","qty":10}],"tips":"Requires roof to place!","confidence":"community"},
    {"id":"weaponsmith","name":"Weaponsmith Workshop","category":"structure","station":"hand","station_level":0,
     "materials":[{"item":"Wood","qty":10},{"item":"Copper Ingot","qty":5}],"tips":"Requires roof!","confidence":"verified"},
    # Workbench upgrades
    {"id":"sawhorse","name":"Sawhorse","category":"upgrade","station":"workbench","station_level":1,
     "materials":[{"item":"Wood","qty":20},{"item":"Copper Ingot","qty":10}],"tips":"Place near WB for Lv2.","confidence":"verified"},
    {"id":"toolbox","name":"Toolbox","category":"upgrade","station":"workbench","station_level":2,
     "materials":[{"item":"Wood","qty":10},{"item":"Nails","qty":20},{"item":"Foothills Iron Ingot","qty":5}],"tips":"Place near WB for Lv3.","confidence":"verified"},
    # Copper tools
    {"id":"copper-pickaxe","name":"Copper Pickaxe","category":"tool","station":"workbench","station_level":1,
     "materials":[{"item":"Copper Ingot","qty":3},{"item":"Wood","qty":3}],"tips":"Mines Iron Ore.","confidence":"verified"},
    {"id":"copper-axe","name":"Copper Axe","category":"tool","station":"workbench","station_level":1,
     "materials":[{"item":"Copper Ingot","qty":3},{"item":"Wood","qty":3}],"tips":"Faster wood chopping.","confidence":"verified"},
    # Smelting
    {"id":"copper-ingot","name":"Copper Ingot","category":"material","station":"smelting-furnace","station_level":1,
     "materials":[{"item":"Poor Copper Ore","qty":6},{"item":"Charcoal","qty":1}],"tips":"Base metal for tools/weapons.","confidence":"verified"},
    {"id":"charcoal","name":"Charcoal","category":"material","station":"charcoal-kiln","station_level":1,
     "materials":[{"item":"Wood","qty":1}],"tips":"Fuel for smelting.","confidence":"verified"},
    {"id":"iron-ingot","name":"Foothills Iron Ingot","category":"material","station":"smelting-furnace","station_level":1,
     "materials":[{"item":"Iron Ore","qty":4},{"item":"Charcoal","qty":2}],"tips":"Advanced metal. Foothills region.","confidence":"community"},
    # Lv2 Workbench
    {"id":"sailor-backpack","name":"Sailor Backpack","category":"equipment","station":"workbench","station_level":2,
     "materials":[{"item":"Torn Sailcloth Bag","qty":1},{"item":"Rough Hide","qty":5},{"item":"Copper Ingot","qty":2}],"tips":"Medium inventory.","confidence":"verified"},
    {"id":"iron-pickaxe","name":"Iron Pickaxe","category":"tool","station":"workbench","station_level":2,
     "materials":[{"item":"Foothills Iron Ingot","qty":3},{"item":"Wood","qty":3}],"tips":"Mines Sulfur.","confidence":"community"},
    {"id":"iron-axe","name":"Iron Axe","category":"tool","station":"workbench","station_level":2,
     "materials":[{"item":"Foothills Iron Ingot","qty":3},{"item":"Wood","qty":3}],"tips":"Best axe tier.","confidence":"community"},
    # Lv3 Workbench
    {"id":"bosun-backpack","name":"Bosun Backpack","category":"equipment","station":"workbench","station_level":3,
     "materials":[{"item":"Sailor Backpack","qty":1},{"item":"Tanned Leather","qty":5},{"item":"Foothills Iron Ingot","qty":2}],"tips":"Max inventory.","confidence":"verified"},
    # Gunpowder
    {"id":"gunpowder","name":"Gunpowder","category":"material","station":"millstone","station_level":1,
     "materials":[{"item":"Sulfur","qty":10},{"item":"Ash","qty":20}],"result_qty":10,"tips":"For ranged weapons/cannons.","confidence":"verified"},
    # Weapons (Weaponsmith)
    {"id":"saber","name":"Saber","category":"weapon","station":"weaponsmith","station_level":1,
     "materials":[{"item":"Copper Ingot","qty":5},{"item":"Wood","qty":2}],"tips":"Fast, good reach. Best early melee.","confidence":"community"},
    {"id":"rapier","name":"Rapier","category":"weapon","station":"weaponsmith","station_level":1,
     "materials":[{"item":"Copper Ingot","qty":4},{"item":"Wood","qty":1}],"tips":"Highest DPS, short range.","confidence":"community"},
    {"id":"club","name":"Club","category":"weapon","station":"weaponsmith","station_level":1,
     "materials":[{"item":"Copper Ingot","qty":3},{"item":"Wood","qty":4}],"tips":"High stagger, slow.","confidence":"community"},
    {"id":"flintlock-pistol","name":"Flintlock Pistol","category":"weapon","station":"weaponsmith","station_level":1,
     "materials":[{"item":"Copper Ingot","qty":8},{"item":"Wood","qty":3}],"tips":"Ranged. Needs Gunpowder ammo.","confidence":"community"},
    {"id":"musket","name":"Musket","category":"weapon","station":"weaponsmith","station_level":2,
     "materials":[{"item":"Foothills Iron Ingot","qty":6},{"item":"Wood","qty":4}],"tips":"Long range, slow reload.","confidence":"community"},
    {"id":"cutlass","name":"Cutlass","category":"weapon","station":"weaponsmith","station_level":2,
     "materials":[{"item":"Foothills Iron Ingot","qty":5},{"item":"Wood","qty":2}],"tips":"Upgraded saber. Good all-rounder.","confidence":"community"},
    # Armor
    {"id":"survivors-boots","name":"Survivor's Boots","category":"armor","station":"armor-workshop","station_level":1,
     "materials":[{"item":"Rough Hide","qty":2},{"item":"Coarse Fabric","qty":2}],"tips":"First armor piece.","confidence":"verified"},
    {"id":"survivors-vest","name":"Survivor's Vest","category":"armor","station":"armor-workshop","station_level":1,
     "materials":[{"item":"Rough Hide","qty":4},{"item":"Coarse Fabric","qty":3}],"tips":"Early chest armor.","confidence":"community"},
    {"id":"survivors-gloves","name":"Survivor's Gloves","category":"armor","station":"armor-workshop","station_level":1,
     "materials":[{"item":"Rough Hide","qty":2},{"item":"Coarse Fabric","qty":1}],"tips":"Early hand armor.","confidence":"community"},
    {"id":"copper-helm","name":"Copper Helm","category":"armor","station":"armor-workshop","station_level":1,
     "materials":[{"item":"Copper Ingot","qty":4},{"item":"Rough Hide","qty":2}],"tips":"Medium head armor.","confidence":"community"},
    {"id":"copper-cuirass","name":"Copper Cuirass","category":"armor","station":"armor-workshop","station_level":1,
     "materials":[{"item":"Copper Ingot","qty":8},{"item":"Rough Hide","qty":4}],"tips":"Medium chest armor.","confidence":"community"},
    # Cooking
    {"id":"cooked-meat","name":"Cooked Meat","category":"food","station":"cooking-fire","station_level":1,
     "materials":[{"item":"Raw Meat","qty":1}],"tips":"Basic food. HP regen.","confidence":"verified"},
    {"id":"cooked-fish","name":"Cooked Fish","category":"food","station":"cooking-fire","station_level":1,
     "materials":[{"item":"Raw Fish","qty":1}],"tips":"Stamina boost food.","confidence":"community"},
    {"id":"stew","name":"Stew","category":"food","station":"cooking-fire","station_level":1,
     "materials":[{"item":"Raw Meat","qty":2},{"item":"Vegetable","qty":1}],"tips":"Strong buff. Stack with other food.","confidence":"community"},
    # Building materials
    {"id":"nails","name":"Nails","category":"material","station":"workbench","station_level":1,
     "materials":[{"item":"Copper Ingot","qty":1}],"result_qty":5,"tips":"For storage, ship repair, Toolbox.","confidence":"verified"},
    {"id":"planks","name":"Planks","category":"material","station":"workbench","station_level":1,
     "materials":[{"item":"Wood","qty":3}],"result_qty":2,"tips":"Building material.","confidence":"community"},
    {"id":"clay-pot","name":"Clay Pot","category":"material","station":"workbench","station_level":1,
     "materials":[{"item":"Clay","qty":3}],"tips":"Storage and alchemy.","confidence":"community"},
    {"id":"clay-bottle","name":"Clay Bottle","category":"material","station":"workbench","station_level":1,
     "materials":[{"item":"Clay","qty":2}],"tips":"Water storage, potion base.","confidence":"community"},
    # Alchemy
    {"id":"health-potion","name":"Health Potion","category":"consumable","station":"alchemy-table","station_level":1,
     "materials":[{"item":"Clay Bottle","qty":1},{"item":"Red Herb","qty":2}],"tips":"Instant large heal.","confidence":"community"},
    {"id":"stamina-potion","name":"Stamina Potion","category":"consumable","station":"alchemy-table","station_level":1,
     "materials":[{"item":"Clay Bottle","qty":1},{"item":"Green Herb","qty":2}],"tips":"Stamina recovery.","confidence":"community"},
    # Storage
    {"id":"storage-chest","name":"Storage Chest","category":"structure","station":"workbench","station_level":1,
     "materials":[{"item":"Wood","qty":10},{"item":"Nails","qty":5}],"tips":"Base storage. Build many.","confidence":"verified"},
    {"id":"large-chest","name":"Large Storage Chest","category":"structure","station":"workbench","station_level":2,
     "materials":[{"item":"Wood","qty":20},{"item":"Nails","qty":10},{"item":"Copper Ingot","qty":2}],"tips":"Double capacity.","confidence":"community"},
]

def expand_recipes():
    data = load_json("recipes.json")
    existing_ids = {r["id"] for r in data.get("recipes", [])}
    added = 0
    for r in NEW_RECIPES:
        if r["id"] not in existing_ids:
            data.setdefault("recipes", []).append(r)
            added += 1
    data["total"] = len(data.get("recipes", []))
    data["lastUpdated"] = "2026-05-13"
    save_json("recipes.json", data)
    print(f"    Added {added} recipes. Total: {data['total']}")


# === 2. 扩充资源数据 ===
NEW_RESOURCES = [
    {"id":"wood","name":"Wood","rarity":"common","biome":["all"],"source":"Chop trees","tool_required":"Any Axe or bare hands",
     "used_in":["bonfire","workbench","tent","charcoal-kiln","planks","nails"],"tips":"Most common resource. Always gather when passing trees.","confidence":"verified"},
    {"id":"stone","name":"Stone","rarity":"common","biome":["all"],"source":"Pick up loose rocks, mine boulders","tool_required":"None (loose) / Stone Pickaxe (boulders)",
     "used_in":["stone-pickaxe","stone-axe","cooking-fire","smelting-furnace"],"tips":"Found everywhere on the ground.","confidence":"verified"},
    {"id":"plant-fiber","name":"Plant Fiber","rarity":"common","biome":["all"],"source":"Harvest bushes and tall grass","tool_required":"None",
     "used_in":["coarse-fabric","rope","tent"],"tips":"Gather constantly. Needed for fabric and rope.","confidence":"verified"},
    {"id":"rough-hide","name":"Rough Hide","rarity":"uncommon","biome":["coastal-jungle"],"source":"Kill Boars","tool_required":"Any weapon",
     "used_in":["armor-workshop","survivors-boots","survivors-vest"],"tips":"Hunt boars near beaches. First animal drop.","confidence":"verified"},
    {"id":"tanned-leather","name":"Tanned Leather","rarity":"rare","biome":["foothills"],"source":"Process hides at Tanning Rack","tool_required":"Tanning Rack",
     "used_in":["bosun-backpack","advanced-armor"],"tips":"Mid-game material. Requires Foothills progression.","confidence":"community"},
    {"id":"salt","name":"Salt","rarity":"common","biome":["coastal"],"source":"Harvest salt deposits on beaches","tool_required":"Stone Pickaxe",
     "used_in":["cooking","preservation"],"tips":"Found along coastlines.","confidence":"community"},
    {"id":"rum","name":"Rum","rarity":"uncommon","biome":["pirate-camps"],"source":"Loot from pirate camps and shipwrecks","tool_required":"None",
     "used_in":["trading","crew-morale"],"tips":"Also found in Smuggler's Treasure locations.","confidence":"community"},
]

def expand_resources():
    data = load_json("resources.json")
    existing_ids = {r["id"] for r in data.get("resources", [])}
    added = 0
    for r in NEW_RESOURCES:
        if r["id"] not in existing_ids:
            data.setdefault("resources", []).append(r)
            added += 1
    data["total"] = len(data.get("resources", []))
    data["lastUpdated"] = "2026-05-13"
    save_json("resources.json", data)
    print(f"    Added {added} resources. Total: {data['total']}")


# === 3. 扩充船只数据 ===
def expand_ships():
    data = {
        "lastUpdated": "2026-05-13",
        "ships": [
            {"id":"ketch","name":"Ketch","tier":1,"size":"Small","crew":"1-2","speed":"Fast","hp":500,
             "cannons":4,"cargo":"Small","unlock":"Quest reward (free)",
             "variants":[
                 {"name":"Stock Ketch","cannons":4,"cargo":"Standard","notes":"Default variant"},
                 {"name":"Brethren Ketch","cannons":6,"cargo":"Reduced","notes":"More firepower"},
                 {"name":"Blackbeard Ketch","cannons":4,"cargo":"Large","notes":"More cargo space"}
             ],
             "pros":["Fastest ship","Easy to solo","Low material cost","Great for exploration"],
             "cons":["Low HP","Few cannons","Small cargo hold"],
             "best_for":"Solo exploration, resource runs, early game",
             "confidence":"community"},
            {"id":"brigantine","name":"Brigantine","tier":2,"size":"Medium","crew":"2-4","speed":"Moderate","hp":1200,
             "cannons":8,"cargo":"Medium","unlock":"Reputation Lv2 + Piastres",
             "variants":[
                 {"name":"Stock Brigantine","cannons":8,"cargo":"Standard","notes":"Balanced"},
                 {"name":"Brethren Brigantine","cannons":12,"cargo":"Reduced","notes":"Combat focus"},
                 {"name":"Blackbeard Brigantine","cannons":8,"cargo":"Large","notes":"Trading focus"}
             ],
             "pros":["Good balance of speed and firepower","Fits 2-4 crew well","Versatile"],
             "cons":["Requires reputation grind","More expensive to repair","Needs crew for full potential"],
             "best_for":"Small group play, balanced combat and exploration",
             "confidence":"community"},
            {"id":"frigate","name":"Frigate","tier":3,"size":"Large","crew":"4-10","speed":"Slow","hp":2500,
             "cannons":16,"cargo":"Large","unlock":"Reputation Lv3+ + expensive",
             "variants":[
                 {"name":"Stock Frigate","cannons":16,"cargo":"Standard","notes":"War machine"},
                 {"name":"Brethren Frigate","cannons":20,"cargo":"Reduced","notes":"Maximum firepower"},
                 {"name":"Blackbeard Frigate","cannons":16,"cargo":"Huge","notes":"Fleet cargo hauler"}
             ],
             "pros":["Highest HP","Most cannons","Huge cargo","Intimidating"],
             "cons":["Very slow","Expensive","Needs large crew","Hard to maneuver"],
             "best_for":"Large group naval combat, fleet operations",
             "confidence":"community"}
        ]
    }
    save_json("ships.json", data)
    print(f"    Ships: {len(data['ships'])} ships with variants")


# === 4. 扩充武器数据 ===
def expand_weapons():
    data = load_json("weapons.json")
    tier_list = {
        "lastUpdated": "2026-05-13",
        "note": "Tier rankings based on community consensus. Subject to balance patches.",
        "confidence": "community",
        "tiers": {
            "S": [{"name":"Cutlass","type":"melee","reason":"Best overall DPS + reach"},
                  {"name":"Musket","type":"ranged","reason":"Highest single-shot damage"}],
            "A": [{"name":"Rapier","type":"melee","reason":"Fast attacks, high DPS but short range"},
                  {"name":"Saber","type":"melee","reason":"Good reach, balanced"},
                  {"name":"Flintlock Pistol","type":"ranged","reason":"Quick draw, decent damage"}],
            "B": [{"name":"Club","type":"melee","reason":"High stagger but slow"},
                  {"name":"Boarding Axe","type":"melee","reason":"Good for ship combat"}],
            "C": [{"name":"Stone Axe","type":"melee","reason":"Early game only"},
                  {"name":"Stone Pickaxe","type":"melee","reason":"Emergency weapon"}]
        }
    }
    data["tier_list"] = tier_list
    data["lastUpdated"] = "2026-05-13"
    save_json("weapons.json", data)
    print(f"    Weapons tier list added")


if __name__ == "__main__":
    print("=== Phase 2: Bulk Data Expansion ===")
    expand_recipes()
    expand_resources()
    expand_ships()
    expand_weapons()
    print("\nPhase 2 complete!")
