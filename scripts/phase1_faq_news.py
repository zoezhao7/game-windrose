"""
阶段1: 扩充 FAQ 至 30+ 题 + 创建 Steam News 脚本
同时更新首页导航加入 Guides 入口
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from phase1_guides_hub import page_wrapper, write_page

ROOT = r"F:\aicode\gamedoc"

# === 1. 扩充 FAQ 数据 ===
NEW_FAQ_ITEMS = [
    ("How do I get Sulfur in Windrose?",
     "Sulfur is found in the Foothills region. You need an Iron Pickaxe to mine Sulfur deposits. Sulfur is used to craft Gunpowder at the Millstone (10 Sulfur + 20 Ash = 10 Gunpowder)."),
    ("How do I build a Charcoal Kiln?",
     "Craft a Charcoal Kiln at any open area: 25 Wood + 20 Clay. It converts Wood into Charcoal, which is essential for smelting ores. You need Clay first — mine it from dark soil patches near water."),
    ("What are Sea Shanties?",
     "Sea Shanties are songs your crew can play while sailing. They provide passive buffs to the crew. You can find new shanties as loot or quest rewards throughout the game."),
    ("How do I hire NPC crew members?",
     "Visit towns and interact with recruitable NPCs. You need to meet Reputation requirements and pay Piastres. Crew members can man cannons, repair the ship, and fight during boarding actions."),
    ("Is there PvP in Windrose?",
     "Windrose is primarily a PvE co-op game. There is no forced PvP. All multiplayer is cooperative — up to 10 players working together against AI enemies and bosses."),
    ("How do I extend the Rested buff?",
     "Build diverse Decoration items in your base. The more unique decoration sub-categories you place, the longer the Rested buff lasts. The Rested buff boosts various stats including stamina regen."),
    ("What does the Millstone do?",
     "The Millstone is a crafting station that produces Gunpowder (10 Sulfur + 20 Ash) and processes various materials. It requires Iron-tier progression to build."),
    ("How do I repair my ship?",
     "Carry Wood and Nails on your ship. When damaged, use repair materials from your inventory while near the damaged hull section. Always stock repair mats before long voyages."),
    ("What are Piastres used for?",
     "Piastres are the in-game currency used to buy ships at the Wharf, hire crew, and purchase items from merchants. Earn them by completing quests, selling loot, and clearing POIs."),
    ("How do I increase Reputation?",
     "Complete faction quests, clear POIs, and help NPCs. Higher Reputation unlocks better ships, crew options, and merchant inventory. Each faction has its own Reputation track."),
    ("Can I play Windrose offline?",
     "Yes, Windrose supports single-player offline mode. Your world saves locally. You can also host a world and invite friends for co-op."),
    ("What's the Ashlands update?",
     "The Ashlands is the first major content update planned for Windrose, at least 6 months after Early Access launch. It will add new biomes, bosses, ships, and story content. The developer confirmed no save/server wipes."),
]

def update_faq_data():
    """将新FAQ条目添加到 data/news.json 旁边的地方记录"""
    faq_path = os.path.join(ROOT, "data", "faq-expansion.json")
    data = {"added": "2026-05-13", "new_items": NEW_FAQ_ITEMS, "total_target": "32+"}
    with open(faq_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  ✅ data/faq-expansion.json ({len(NEW_FAQ_ITEMS)} new items)")


# === 2. Steam News 获取脚本 ===
STEAM_NEWS_SCRIPT = '''"""
Steam News 自动获取脚本 — Windrose Guides
用法: python scripts/fetch_steam_news.py

从 Steam Web API 获取 Windrose 最新新闻并更新 data/news.json
"""
import json
import os
import logging
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Windrose Steam App ID
STEAM_APP_ID = "3041230"
STEAM_NEWS_URL = f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid={STEAM_APP_ID}&count=10&maxlength=500&format=json"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS_JSON = os.path.join(ROOT, "data", "news.json")


def fetch_steam_news() -> list[dict]:
    """从 Steam API 获取最新新闻"""
    try:
        req = Request(STEAM_NEWS_URL, headers={"User-Agent": "WindroseGuides/1.0"})
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        items = data.get("appnews", {}).get("newsitems", [])
        results = []
        for item in items:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "date": datetime.fromtimestamp(item.get("date", 0)).strftime("%Y-%m-%d"),
                "author": item.get("author", ""),
                "feed_label": item.get("feedlabel", ""),
                "contents_snippet": item.get("contents", "")[:300],
                "source": "steam_api",
                "confidence": "official",
                "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })
        logger.info(f"Fetched {len(results)} news items from Steam API")
        return results
    except URLError as e:
        logger.error(f"Failed to fetch Steam news: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []


def update_news_json(new_items: list[dict]) -> None:
    """更新 data/news.json，合并新闻并去重"""
    existing = {"lastUpdated": "", "items": []}
    if os.path.exists(NEWS_JSON):
        with open(NEWS_JSON, "r", encoding="utf-8") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                pass

    existing_urls = {item.get("url") for item in existing.get("items", [])}
    added = 0
    for item in new_items:
        if item["url"] not in existing_urls:
            existing.setdefault("items", []).insert(0, item)
            added += 1

    existing["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")
    existing["total"] = len(existing.get("items", []))

    with open(NEWS_JSON, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    logger.info(f"Added {added} new items. Total: {existing['total']}")


if __name__ == "__main__":
    logger.info("Fetching Windrose news from Steam API...")
    items = fetch_steam_news()
    if items:
        update_news_json(items)
        logger.info("News update complete!")
    else:
        logger.warning("No news fetched. Check network or Steam API availability.")
'''


# === 3. 更新首页导航 ===
def update_homepage_nav():
    """在首页导航中加入 Guides 链接"""
    index_path = os.path.join(ROOT, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 在 Beginner Guide 后面加入 Guides 链接
    old_nav = '<li><a href="/beginner-guide">Beginner Guide</a></li>'
    new_nav = '<li><a href="/beginner-guide">Beginner Guide</a></li>\n                <li><a href="/guides">Guides</a></li>'

    if '/guides">' not in content:
        content = content.replace(old_nav, new_nav)
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  ✅ index.html — Added Guides nav link")
    else:
        print("  ⏭️ index.html — Guides link already exists")

    # 在 Quick Navigation 中加入 Guides 卡片
    guides_card = '''<a href="/guides/" class="card quick-nav-card">
                    <span class="nav-icon">📖</span>
                    <h3>Strategy Guides</h3>
                    <p>Deep-dive walkthroughs: mining routes, boss strategies, best builds, crafting paths, and naval combat tactics.</p>
                </a>'''

    if 'Strategy Guides</h3>' not in content:
        # 在 FAQ 卡片前插入
        content = content.replace(
            '<a href="/faq/" class="card quick-nav-card">',
            guides_card + '\n                ' + '<a href="/faq/" class="card quick-nav-card">'
        )
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  ✅ index.html — Added Guides card to Quick Navigation")
    else:
        print("  ⏭️ index.html — Guides card already exists")


if __name__ == "__main__":
    print("=== Phase 1: FAQ + News + Homepage Update ===")

    # 1. FAQ expansion data
    update_faq_data()

    # 2. Steam news script
    news_script_path = os.path.join(ROOT, "scripts", "fetch_steam_news.py")
    with open(news_script_path, "w", encoding="utf-8") as f:
        f.write(STEAM_NEWS_SCRIPT)
    print(f"  ✅ scripts/fetch_steam_news.py")

    # 3. Homepage update
    update_homepage_nav()

    print("Done!")
