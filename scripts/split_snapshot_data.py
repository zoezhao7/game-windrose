from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
TODAY = "2026-05-12"


def load_snapshot():
    return json.loads((DATA_DIR / "html-content-snapshot.json").read_text(encoding="utf-8"))["items"]


def page_type(slug):
    if slug == "":
        return "home"
    root = slug.split("/")[0]
    if root in {"bosses", "resources", "ships", "weapons", "builds", "crafting", "tools", "building"}:
        return root
    if root in {"download", "server-guide", "sources", "news", "faq", "about", "contact", "privacy", "terms", "404", "beginner-guide"}:
        return root
    return "page"


def common(item, data_type, confidence="community", status="published"):
    slug = item["slug"]
    return {
        "id": slug.replace("/", "-") if slug else "home",
        "slug": slug,
        "name": item.get("h1") or item.get("title") or slug,
        "status": status,
        "confidence": confidence,
        "last_verified": TODAY,
        "source_page": item.get("source_file"),
        "data_type": data_type,
        "sources": [
            {
                "title": "Existing site HTML content snapshot",
                "url": item.get("source_file"),
                "type": "internal",
                "accessed": TODAY
            }
        ],
        "notes": "Migrated from existing HTML snapshot. Needs structured verification during phase two."
    }


def table_rows_by_caption(item, pattern):
    rows = []
    for table in item.get("tables", []):
        caption = table.get("caption", "")
        if re.search(pattern, caption, re.I):
            rows.extend(table.get("rows", []))
    return rows


def write_json(name, payload):
    path = DATA_DIR / name
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


def build_pages(items):
    pages = []
    for item in items:
        base = common(item, "page", confidence="internal")
        base.update({
            "title": item.get("title", ""),
            "description": item.get("description", ""),
            "h1": item.get("h1", ""),
            "page_type": page_type(item.get("slug", "")),
            "headings": item.get("headings", []),
            "faq": item.get("faq", []),
            "links": item.get("links", [])
        })
        pages.append(base)
    return {"type": "page_collection", "generated_at": TODAY, "items": pages}


def build_bosses(items):
    boss_pages = [item for item in items if item["slug"].startswith("bosses")]
    bosses = []
    for item in boss_pages:
        if item["slug"] == "bosses":
            continue
        base = common(item, "boss")
        name = item.get("h1", "").replace("Windrose ", "").replace(" Boss Guide", "").replace(": Strategy, Tips & Drops (2026)", "").replace(": Strategy, Phases & Drops (2026)", "").replace(" (2026)", "")
        base.update({
            "name": name or base["name"],
            "order": None,
            "category": "story" if "charons-obols" in item["slug"] else "unconfirmed",
            "location": "Needs verification",
            "biome": "Unknown",
            "recommended_level": "Needs verification",
            "recommended_ship": "brigantine" if "charons-obols" in item["slug"] else "unknown",
            "recommended_gear": [],
            "phases": [],
            "drops": [],
            "unlocks": [],
            "faq": item.get("faq", [])
        })
        for stat_row in table_rows_by_caption(item, "difficulty|requirements|overview"):
            if stat_row:
                base.setdefault("table_rows", []).append(stat_row)
        bosses.append(base)
    return {"type": "boss_collection", "generated_at": TODAY, "items": bosses}


def build_resources(items):
    resource_pages = [item for item in items if item["slug"].startswith("resources/")]
    resources = []
    for item in resource_pages:
        base = common(item, "resource")
        base.update({
            "rarity": "unknown",
            "biomes": [],
            "locations": [],
            "tool_required": "Needs verification",
            "refines_to": [],
            "used_in": [],
            "farming_tips": [],
            "related_pages": [link["href"].strip("/") for link in item.get("links", []) if link.get("href", "").startswith("/")]
        })
        for table in item.get("tables", []):
            caption = table.get("caption", "")
            if "recipe" in caption.lower():
                base["refines_to"].append({"caption": caption, "rows": table.get("rows", [])})
            if "using" in caption.lower() or "use" in caption.lower():
                base["used_in"].extend(table.get("rows", []))
        resources.append(base)
    return {"type": "resource_collection", "generated_at": TODAY, "items": resources}


def build_recipes(items):
    recipe_pages = [item for item in items if item["slug"].startswith("crafting/")]
    recipes = []
    for item in recipe_pages:
        for table in item.get("tables", []):
            headers = table.get("headers", [])
            for index, row in enumerate(table.get("rows", [])):
                if not row:
                    continue
                recipe_name = row[0]
                if not recipe_name or recipe_name.lower() in {"result", "item"}:
                    continue
                recipe = {
                    "id": re.sub(r"[^a-z0-9]+", "-", recipe_name.lower()).strip("-") or f"{item['id']}-{index}",
                    "slug": item["slug"],
                    "name": recipe_name,
                    "status": "published",
                    "confidence": "community",
                    "last_verified": TODAY,
                    "category": "unknown",
                    "station": item["slug"].split("/")[-1].title(),
                    "station_level": None,
                    "materials": row[1] if len(row) > 1 else "Needs verification",
                    "result": row[2] if len(row) > 2 else recipe_name,
                    "unlock_condition": "Needs verification",
                    "uses": row[3:] if len(row) > 3 else [],
                    "source_table": table.get("caption", ""),
                    "sources": [
                        {
                            "title": "Existing site HTML content snapshot",
                            "url": item.get("source_file"),
                            "type": "internal",
                            "accessed": TODAY
                        }
                    ],
                    "notes": f"Migrated from table headers: {headers}"
                }
                recipes.append(recipe)
    return {"type": "recipe_collection", "generated_at": TODAY, "items": recipes}


def build_ships(items):
    ship_pages = [item for item in items if item["slug"].startswith("ships/")]
    ships = []
    for item in ship_pages:
        base = common(item, "ship")
        base.update({
            "role": "Needs verification",
            "speed": "unknown",
            "firepower": "unknown",
            "durability": "unknown",
            "handling": "unknown",
            "crew_fit": "unknown",
            "recommended_for": [],
            "weaknesses": []
        })
        ships.append(base)
    return {"type": "ship_collection", "generated_at": TODAY, "items": ships}


def build_weapons(items):
    weapon_pages = [item for item in items if item["slug"].startswith("weapons/")]
    weapons = []
    for item in weapon_pages:
        for table in item.get("tables", []):
            for index, row in enumerate(table.get("rows", [])):
                if not row:
                    continue
                name = row[0]
                weapons.append({
                    "id": re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or f"{item['id']}-{index}",
                    "slug": item["slug"],
                    "name": name,
                    "status": "published",
                    "confidence": "community",
                    "last_verified": TODAY,
                    "category": item["slug"].split("/")[-1],
                    "tier": "unranked",
                    "damage_type": "unknown",
                    "materials": [],
                    "best_use": row[1] if len(row) > 1 else "Needs verification",
                    "pros": row[2:] if len(row) > 2 else [],
                    "cons": [],
                    "related_builds": [],
                    "sources": [{"title": "Existing site HTML content snapshot", "url": item.get("source_file"), "type": "internal", "accessed": TODAY}],
                    "notes": f"Migrated from {table.get('caption', 'HTML table')}"
                })
    return {"type": "weapon_collection", "generated_at": TODAY, "items": weapons}


def build_builds(items):
    build_pages = [item for item in items if item["slug"].startswith("builds/")]
    builds = []
    for item in build_pages:
        base = common(item, "build")
        role = item["slug"].split("/")[-1].replace("-builds", "")
        base.update({
            "role": role,
            "recommended_weapons": [],
            "recommended_armor": [],
            "recommended_ship": "unknown",
            "stats_priority": [],
            "playstyle": item.get("description", ""),
            "progression_steps": [h["text"] for h in item.get("headings", [])]
        })
        builds.append(base)
    return {"type": "build_collection", "generated_at": TODAY, "items": builds}


def build_tools(items):
    tool_pages = [item for item in items if item["slug"].startswith("tools")]
    tools = []
    for item in tool_pages:
        base = common(item, "tool_page", confidence="internal")
        base.update({
            "purpose": item.get("description", ""),
            "inputs": [],
            "outputs": ["static HTML table", "FAQ", "internal links"],
            "related_data_files": [],
            "faq": item.get("faq", [])
        })
        tools.append(base)
    return {"type": "tool_collection", "generated_at": TODAY, "items": tools}


def build_news(items):
    news_page = next((item for item in items if item["slug"] == "news"), None)
    news = []
    if news_page:
        for table in news_page.get("tables", []):
            for index, row in enumerate(table.get("rows", [])):
                title = row[2] if len(row) > 2 else f"News item {index + 1}"
                news.append({
                    "id": re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or f"news-{index + 1}",
                    "slug": "news",
                    "title": title,
                    "name": title,
                    "status": "published",
                    "confidence": "community",
                    "date": row[0] if row else "Needs verification",
                    "source_name": row[1] if len(row) > 1 else "Needs verification",
                    "source_url": "",
                    "summary": title,
                    "guide_impact": row[3] if len(row) > 3 else "",
                    "sources": [{"title": "Existing site HTML content snapshot", "url": news_page.get("source_file"), "type": "internal", "accessed": TODAY}],
                    "last_verified": TODAY,
                    "notes": "Migrated from news page table."
                })
    return {"type": "news_collection", "generated_at": TODAY, "items": news}


def build_sources(items):
    source_page = next((item for item in items if item["slug"] == "sources"), None)
    sources = []
    if source_page:
        for table in source_page.get("tables", []):
            for index, row in enumerate(table.get("rows", [])):
                topic = row[0] if row else f"Source {index + 1}"
                sources.append({
                    "id": re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-"),
                    "slug": "sources",
                    "name": topic,
                    "status": "published",
                    "confidence": "internal",
                    "preferred_source": row[1] if len(row) > 1 else "",
                    "update_rule": row[2] if len(row) > 2 else "",
                    "sources": [{"title": "Existing site HTML content snapshot", "url": source_page.get("source_file"), "type": "internal", "accessed": TODAY}],
                    "last_verified": TODAY,
                    "notes": "Migrated from source policy page."
                })
    return {"type": "source_collection", "generated_at": TODAY, "items": sources}


def main():
    items = load_snapshot()
    write_json("pages.json", build_pages(items))
    write_json("bosses.json", build_bosses(items))
    write_json("resources.json", build_resources(items))
    write_json("recipes.json", build_recipes(items))
    write_json("ships.json", build_ships(items))
    write_json("weapons.json", build_weapons(items))
    write_json("builds.json", build_builds(items))
    write_json("tools.json", build_tools(items))
    write_json("news.json", build_news(items))
    write_json("sources.json", build_sources(items))


if __name__ == "__main__":
    main()
