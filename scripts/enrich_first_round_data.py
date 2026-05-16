from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TODAY = "2026-05-12"


SOURCES = {
    "game_wiki_bosses": {
        "title": "Bosses | Windrose Wiki",
        "url": "https://game.wiki/windrose/bosses",
        "type": "wiki",
        "accessed": TODAY
    },
    "thegameswiki_bosses": {
        "title": "Bosses - Windrose Wiki | The Games Wiki",
        "url": "https://thegameswiki.com/windrose/wiki/bosses",
        "type": "wiki",
        "accessed": TODAY
    },
    "game_wiki_workbench": {
        "title": "Workbench | Windrose Wiki",
        "url": "https://game.wiki/windrose/workbench",
        "type": "wiki",
        "accessed": TODAY
    },
    "mobalytics_workbench": {
        "title": "Windrose How to Upgrade Your Workbench",
        "url": "https://mobalytics.gg/news/guides/how-to-upgrade-workbench-windrose",
        "type": "guide",
        "accessed": TODAY
    },
    "gamespot_workbench": {
        "title": "How To Upgrade Workbench Levels In Windrose",
        "url": "https://www.gamespot.com/articles/how-to-upgrade-workbench-levels-in-windrose/1100-6539435/",
        "type": "guide",
        "accessed": TODAY
    },
    "pcgamer_gunpowder": {
        "title": "How to make Gunpowder in Windrose",
        "url": "https://www.pcgamer.com/games/survival-crafting/windrose-gunpowder/",
        "type": "guide",
        "accessed": TODAY
    },
    "pcgamer_clay": {
        "title": "How to get clay in Windrose",
        "url": "https://www.pcgamer.com/games/survival-crafting/windrose-clay/",
        "type": "guide",
        "accessed": TODAY
    },
    "windrosewiki_clay": {
        "title": "Clay | Windrose Wiki",
        "url": "https://windrosewiki.com/wiki/resources/clay",
        "type": "wiki",
        "accessed": TODAY
    }
}


def write_json(name, payload):
    path = DATA / name
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}: {len(payload.get('items', []))} items")


def source(*keys):
    return [SOURCES[key] for key in keys]


def boss_item(
    boss_id,
    slug,
    name,
    order,
    category,
    location,
    biome,
    recommended_level,
    recommended_ship,
    unlocks,
    drops=None,
    confidence="community",
    notes=""
):
    return {
        "id": boss_id,
        "slug": slug,
        "name": name,
        "status": "published" if confidence != "unconfirmed" else "tracker",
        "confidence": confidence,
        "last_verified": TODAY,
        "data_type": "boss",
        "order": order,
        "category": category,
        "location": location,
        "biome": biome,
        "recommended_level": recommended_level,
        "recommended_ship": recommended_ship,
        "recommended_gear": [
            "Food buffs",
            "Healing consumables",
            "Rested buff",
            "Ranged weapon or firearm pressure",
            "Enough repair and travel supplies"
        ],
        "phases": [],
        "drops": drops or [],
        "unlocks": unlocks,
        "faq": [],
        "sources": source("game_wiki_bosses", "thegameswiki_bosses"),
        "notes": notes
    }


def build_bosses():
    return {
        "type": "boss_collection",
        "generated_at": TODAY,
        "items": [
            boss_item(
                "thomas-richards",
                "bosses/thomas-richards",
                "Thomas Richards",
                1,
                "story",
                "Coastal Jungle boss arena via Revenge Is Best Served Cold",
                "Coastal Jungle",
                "5 to 6",
                "none",
                ["Foothills", "higher crafting tier access", "iron-tier progression"],
                notes="game.wiki names the first arena boss as Boatswain with real name Thomas Richards; The Games Wiki lists Thomas Richards as the Coastal Jungle boss."
            ),
            boss_item(
                "israel-hands",
                "bosses/israel-hands",
                "Israel Hands",
                2,
                "story",
                "Foothills via Needle in a Haystack",
                "Foothills",
                "8 to 10",
                "unknown",
                ["Cursed Swamps", "next story progression gate"],
                drops=[
                    {"item": "Soul Eater greatsword", "quantity": "1", "confidence": "community"},
                    {"item": "Undead Essence", "quantity": "30", "confidence": "community"},
                    {"item": "Charon's Obol", "quantity": "1", "confidence": "community"}
                ],
                notes="The Games Wiki lists Soul Eater, Undead Essence, and Charon's Obol rewards for Israel Hands; keep community confidence until in-game verified."
            ),
            boss_item(
                "high-priestess",
                "bosses/high-priestess",
                "High Priestess",
                3,
                "story",
                "Cursed Swamps boss encounter",
                "Cursed Swamps",
                "12 to 15",
                "unknown",
                ["End of currently available main story", "Chapter 1 launch progression conclusion"],
                drops=[
                    {"item": "Charon's Obol", "quantity": "1", "confidence": "community"}
                ],
                notes="game.wiki lists High Priestess as the Cursed Swamps arena boss. The Games Wiki describes it as the late launch-biome boss."
            ),
            boss_item(
                "ghost-captain",
                "bosses/ghost-captain",
                "Ghost Captain",
                None,
                "optional",
                "Major dungeon encounter / Temple dungeon according to community coverage",
                "Unknown",
                "10 to 12",
                "unknown",
                ["Optional major loot route"],
                drops=[
                    {"item": "Soul Eater greatsword", "quantity": "1", "confidence": "community"}
                ],
                notes="The Games Wiki lists Ghost Captain as an optional or major dungeon encounter; not present in game.wiki's three arena boss roster, so keep as community/tracker until verified."
            ),
            {
                "id": "charons-obols-legacy-page",
                "slug": "bosses/charons-obols",
                "name": "Charon's Obols Legacy Page",
                "status": "needs_verification",
                "confidence": "unconfirmed",
                "last_verified": TODAY,
                "data_type": "boss",
                "order": None,
                "category": "unconfirmed",
                "location": "Needs verification",
                "biome": "Unknown",
                "recommended_level": "Needs verification",
                "recommended_ship": "unknown",
                "recommended_gear": [],
                "phases": [],
                "drops": [],
                "unlocks": [],
                "faq": [],
                "sources": source("game_wiki_bosses", "thegameswiki_bosses"),
                "notes": "Existing site has a Charon's Obols boss page, but current cross-checked wiki sources describe Charon's Obol as a reward/item and list Thomas Richards, Israel Hands, and High Priestess as the three arena bosses. Keep this page for migration but verify before promoting."
            }
        ]
    }


def recipe(recipe_id, name, materials, station="Workbench", station_level=None, category="unknown", result_quantity=1, comfort=None, sources=None, notes=""):
    return {
        "id": recipe_id,
        "slug": f"crafting/{station.lower()}#{recipe_id}",
        "name": name,
        "status": "published",
        "confidence": "community",
        "last_verified": TODAY,
        "category": category,
        "station": station,
        "station_level": station_level,
        "materials": materials,
        "result": {"item": name, "quantity": result_quantity},
        "unlock_condition": f"Workbench comfort {comfort}" if comfort else "Base station or needs verification",
        "uses": [],
        "related_pages": [],
        "sources": sources or source("game_wiki_workbench"),
        "notes": notes
    }


def build_recipes():
    items = [
        recipe("stone-axe", "Stone Axe", [{"item": "Stone", "quantity": 3}, {"item": "Wood", "quantity": 3}], station_level=1, category="tool"),
        recipe("stone-pickaxe", "Stone Pickaxe", [{"item": "Stone", "quantity": 3}, {"item": "Wood", "quantity": 3}], station_level=1, category="tool"),
        recipe("stone-bullet", "Stone Bullet", [{"item": "Stone", "quantity": 3}], station_level=1, category="ammo", result_quantity=5),
        recipe("bandage", "Bandage", [{"item": "Coarse Fabric", "quantity": 1}], station_level=1, category="consumable"),
        recipe("coarse-fabric", "Coarse Fabric", [{"item": "Plant Fiber", "quantity": 3}], station_level=1, category="material"),
        recipe("rope", "Rope", [{"item": "Plant Fiber", "quantity": 3}], station_level=1, category="material"),
        recipe("torn-sailcloth-bag", "Torn Sailcloth Bag", [{"item": "Coarse Fabric", "quantity": 2}, {"item": "Rope", "quantity": 1}], station_level=1, category="utility"),
        recipe("clay-pot", "Clay Pot", [{"item": "Clay", "quantity": 6}], station_level=1, category="container", comfort="+1"),
        recipe("copper-axe", "Copper Axe", [{"item": "Copper Ingot", "quantity": 5}, {"item": "Wood", "quantity": 5}], station_level=1, category="tool", comfort="+1"),
        recipe("copper-pickaxe", "Copper Pickaxe", [{"item": "Copper Ingot", "quantity": 5}, {"item": "Wood", "quantity": 5}], station_level=1, category="tool", comfort="+1"),
        recipe("copper-bullet", "Copper Bullet", [{"item": "Copper Ingot", "quantity": 1}], station_level=1, category="ammo", result_quantity=5, comfort="+1"),
        recipe("nails", "Nails", [{"item": "Copper Ingot", "quantity": 1}], station_level=1, category="material", result_quantity=5, comfort="+1", notes="Existing pages call these Copper Nails; game.wiki labels output as Nails."),
        recipe("copper-pot", "Copper Pot", [{"item": "Copper Ingot", "quantity": 5}], station_level=1, category="container", comfort="+1"),
        recipe("lamp", "Lamp", [{"item": "Copper Ingot", "quantity": 4}, {"item": "Rope", "quantity": 1}], station_level=1, category="utility", comfort="+1", notes="Existing page called this Empty Lamp; game.wiki labels output as Lamp."),
        recipe("fast-travel-bell", "Fast Travel Bell", [{"item": "Copper Ingot", "quantity": 10}, {"item": "Rope", "quantity": 3}], station_level=1, category="utility", comfort="+1"),
        recipe("shovel", "Shovel", [{"item": "Copper Ingot", "quantity": 3}, {"item": "Wood", "quantity": 10}], station_level=1, category="tool", comfort="+1"),
        recipe("combat-repair-kit", "Combat Repair Kit", [{"item": "Wooden Plank", "quantity": 5}, {"item": "Rum Bottle", "quantity": 1}, {"item": "Steel Nails", "quantity": 1}], station_level=1, category="repair", comfort="+1"),
        recipe("repair-kit", "Repair Kit", [{"item": "Wood", "quantity": 10}], station_level=1, category="repair", comfort="+1"),
        recipe("anvil", "Anvil", [{"item": "Foothills Iron Ingot", "quantity": 30}], station_level=2, category="station", comfort="+2"),
        recipe("wooden-plank", "Wooden Plank", [{"item": "Wood", "quantity": 2}], station_level=2, category="material", comfort="+2"),
        recipe("iron-axe", "Iron Axe", [{"item": "Foothills Iron Ingot", "quantity": 5}, {"item": "Wood", "quantity": 5}], station_level=2, category="tool", comfort="+2"),
        recipe("iron-pickaxe", "Iron Pickaxe", [{"item": "Foothills Iron Ingot", "quantity": 5}, {"item": "Wood", "quantity": 5}], station_level=2, category="tool", comfort="+2"),
        recipe("iron-bullet", "Iron Bullet", [{"item": "Foothills Iron Ingot", "quantity": 1}], station_level=2, category="ammo", result_quantity=5, comfort="+2"),
        recipe("ironware", "Ironware", [{"item": "Foothills Iron Ingot", "quantity": 5}], station_level=2, category="material", comfort="+2"),
        recipe("iron-nails", "Nails", [{"item": "Foothills Iron Ingot", "quantity": 1}], station_level=2, category="material", result_quantity=10, comfort="+1", notes="Existing page called these Iron Nails; game.wiki labels output as Nails."),
        recipe("millstone-parts", "Millstone Parts", [{"item": "Stone", "quantity": 15}], station_level=2, category="station_part", comfort="+2"),
        recipe("master-combat-repair-kit", "Master Combat Repair Kit", [{"item": "Timber", "quantity": 2}, {"item": "Rum Bottle", "quantity": 5}, {"item": "Steel Nails", "quantity": 3}], station_level=2, category="repair", comfort="+2"),
        recipe("sailor-backpack", "Sailor Backpack", [{"item": "Torn Sailcloth Bag", "quantity": 1}, {"item": "Rough Hide", "quantity": 5}, {"item": "Copper Ingot", "quantity": 2}], station_level=2, category="utility", comfort="+2"),
        recipe("simple-fishing-rod", "Simple Fishing Rod", [{"item": "Hardwood", "quantity": 5}, {"item": "Rope", "quantity": 3}, {"item": "Foothills Iron Ingot", "quantity": 2}], station_level=2, category="tool", comfort="+2"),
        recipe("bosun-backpack", "Bosun Backpack", [{"item": "Sailor Backpack", "quantity": 1}, {"item": "Tanned Leather", "quantity": 5}, {"item": "Foothills Iron Ingot", "quantity": 2}], station_level=3, category="utility", comfort="+3"),
        recipe("quartermaster-backpack", "Quartermaster Backpack", [{"item": "Bosun Backpack", "quantity": 1}, {"item": "Crocodile Hide Piece", "quantity": 5}], station_level=3, category="utility", comfort="+3"),
        recipe("timber", "Timber", [{"item": "Hardwood", "quantity": 3}], station_level=3, category="material", comfort="+3"),
        recipe("hewn-stone", "Hewn Stone", [{"item": "Stone", "quantity": 3}], station_level=3, category="material", comfort="+3"),
        recipe("tarred-planks", "Tarred Planks", [{"item": "Wooden Plank", "quantity": 1}, {"item": "Tar", "quantity": 1}], station_level=3, category="material", comfort="+3"),
        recipe("bullet-arborum", "Bullet Arborum", [{"item": "Ingot Arborum", "quantity": 1}], station_level=3, category="ammo", result_quantity=5, comfort="+3"),
        recipe("sawhorse", "Sawhorse", [{"item": "Wood", "quantity": 20}, {"item": "Copper Ingot", "quantity": 10}], station="Building", station_level=None, category="station", sources=source("mobalytics_workbench", "gamespot_workbench"), notes="Build near Workbench to upgrade it toward Level 2."),
        recipe("toolbox", "Toolbox", [{"item": "Wood", "quantity": 10}, {"item": "Nails", "quantity": 20}, {"item": "Foothills Iron Ingot", "quantity": 5}], station="Building", station_level=None, category="station", sources=source("mobalytics_workbench"), notes="Mobalytics describes Toolbox as the final Workbench upgrade extender for Level 3.")
    ]
    return {"type": "recipe_collection", "generated_at": TODAY, "items": items}


def resource_item(resource_id, name, rarity, biomes, locations, tool_required, refines_to, used_in, tips, sources, confidence="community", notes=""):
    return {
        "id": resource_id,
        "slug": f"resources/{resource_id.replace('-ore', '').replace('-ingot', '')}",
        "name": name,
        "status": "published",
        "confidence": confidence,
        "rarity": rarity,
        "biomes": biomes,
        "locations": locations,
        "tool_required": tool_required,
        "refines_to": refines_to,
        "used_in": used_in,
        "farming_tips": tips,
        "related_pages": ["crafting/workbench", "crafting/smelting"],
        "sources": sources,
        "last_verified": TODAY,
        "notes": notes
    }


def build_resources():
    return {
        "type": "resource_collection",
        "generated_at": TODAY,
        "items": [
            resource_item(
                "clay",
                "Clay",
                "common",
                ["Islands", "shorelines", "riverbanks", "low-lying muddy terrain"],
                ["Reddish-brown clay patches", "muddy ground deposits"],
                "Any pickaxe; Stone Pickaxe works",
                [],
                ["Charcoal Kiln", "Smelting Furnace", "Clay Pot", "Clay Bottle", "Alchemy Table"],
                ["Look for muddy patches in the open instead of caves", "Deposits can respawn after several in-game days according to PC Gamer"],
                source("windrosewiki_clay", "pcgamer_clay"),
                confidence="community",
                notes="Windrose Wiki gives high confidence metadata for clay; PC Gamer adds practical harvesting notes."
            ),
            resource_item(
                "gunpowder",
                "Gunpowder",
                "uncommon",
                ["Coastal Jungle", "Foothills"],
                ["Enemy camps with Black Mark pieces", "Crafted at Millstone after sulfur discovery"],
                "Millstone for crafting; no tool for looted gunpowder",
                [],
                ["Ranged weapons", "Ammo usage"],
                ["Crafting recipe is 10 Sulfur + 20 Ash at a Millstone", "Cannot craft until after Revenge Is Best Served Cold and Foothills progression", "Loot enemy camps if you need gunpowder before crafting is unlocked"],
                source("pcgamer_gunpowder"),
                confidence="community",
                notes="PC Gamer describes gunpowder unlock sequence and crafting recipe."
            ),
            resource_item(
                "sulfur",
                "Sulfur",
                "uncommon",
                ["Coastal Jungle", "Foothills"],
                ["Yellow-marbled stone-like deposits", "clumpy yellow sulfur deposits"],
                "Iron Pickaxe",
                [{"item": "Gunpowder", "recipe": "10 Sulfur + 20 Ash at Millstone"}],
                ["Gunpowder"],
                ["Can be visually subtle; inspect yellow marbling closely", "Recipe unlocks when sulfur is discovered"],
                source("pcgamer_gunpowder"),
                confidence="community",
                notes="PC Gamer says sulfur can be found in Coastal Jungle and Foothills but requires Iron Pickaxe to mine."
            ),
            resource_item(
                "ash",
                "Ash",
                "common",
                ["Camp/base crafting"],
                ["Charcoal Kiln byproduct", "Millstone conversion from charcoal"],
                "Charcoal Kiln or Millstone",
                [{"item": "Gunpowder", "recipe": "10 Sulfur + 20 Ash at Millstone"}],
                ["Gunpowder"],
                ["PC Gamer notes 2 Charcoal can be ground into 6 Ash at the Millstone, but charcoal is also needed for ingots"],
                source("pcgamer_gunpowder"),
                confidence="community"
            ),
            resource_item(
                "copper-ore",
                "Copper Ore",
                "common",
                ["Coastal Jungle"],
                ["Copper mine / cave deposits"],
                "Stone Pickaxe or better",
                [{"item": "Copper Ingot", "recipe": "6 Copper Ore + 1 Charcoal"}],
                ["Copper tools", "Nails", "Fast Travel Bell", "Copper Bullet"],
                ["Mine copper early, then return to smelt Copper Ingots for Workbench upgrades"],
                source("mobalytics_workbench"),
                confidence="community",
                notes="Mobalytics confirms copper mine progression leading into Copper Ingots and Workbench upgrade."
            ),
            resource_item(
                "foothills-iron-ore",
                "Foothills Iron Ore",
                "uncommon",
                ["Foothills"],
                ["Foothills iron deposits"],
                "Copper Pickaxe or better; exact gate needs verification",
                [{"item": "Foothills Iron Ingot", "recipe": "Iron Ore + Charcoal; quantity needs verification"}],
                ["Iron tools", "Anvil", "Toolbox", "Iron Bullet", "Sailor Backpack"],
                ["Foothills access is unlocked after Thomas Richards / Revenge Is Best Served Cold according to boss and gunpowder sources"],
                source("pcgamer_gunpowder", "game_wiki_bosses"),
                confidence="community"
            )
        ]
    }


def update_sources():
    return {
        "type": "source_collection",
        "generated_at": TODAY,
        "items": [
            {
                "id": key,
                "slug": "sources",
                "name": value["title"],
                "status": "published",
                "confidence": "internal",
                "preferred_source": value["url"],
                "source_type": value["type"],
                "update_rule": "Re-check before publishing affected gameplay data.",
                "sources": [value],
                "last_verified": TODAY,
                "notes": "Added during first structured data enrichment round."
            }
            for key, value in SOURCES.items()
        ]
    }


def main():
    write_json("bosses.json", build_bosses())
    write_json("recipes.json", build_recipes())
    write_json("resources.json", build_resources())
    write_json("sources.json", update_sources())


if __name__ == "__main__":
    main()
