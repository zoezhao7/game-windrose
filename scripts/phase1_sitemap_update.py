"""阶段1: 更新 sitemap.xml 和 llms.txt 包含新 Guide 页面"""
import os
from datetime import date

ROOT = r"F:\aicode\gamedoc"
TODAY = date.today().isoformat()

# === 新增 Sitemap 条目 ===
NEW_URLS = [
    ("/guides", "weekly", "0.8"),
    ("/guides/mining-routes", "monthly", "0.7"),
    ("/guides/boss-progression", "monthly", "0.7"),
    ("/guides/best-early-builds", "monthly", "0.7"),
    ("/guides/crafting-progression", "monthly", "0.7"),
    ("/guides/sailing-navigation", "monthly", "0.7"),
    ("/guides/coop-multiplayer", "monthly", "0.7"),
    ("/guides/ship-building-naval-combat", "monthly", "0.7"),
]

def update_sitemap():
    path = os.path.join(ROOT, "sitemap.xml")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_entries = ""
    for url, freq, priority in NEW_URLS:
        full_url = f"https://windrosewiki.games{url}"
        if full_url not in content:
            new_entries += f"""  <url>
    <loc>{full_url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>\n"""

    if new_entries:
        content = content.replace("</urlset>", new_entries + "</urlset>")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅ sitemap.xml — Added {len(NEW_URLS)} URLs")
    else:
        print("  ⏭️ sitemap.xml — URLs already exist")


def update_llms():
    path = os.path.join(ROOT, "llms.txt")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    guides_section = """
### [Strategy Guides](https://windrosewiki.games/guides)
- [Mining Routes](https://windrosewiki.games/guides/mining-routes): Optimized mining routes for Copper, Iron, Clay, Sulfur
- [Boss Progression](https://windrosewiki.games/guides/boss-progression): Phase-by-phase boss strategies and progression order
- [Best Early Builds](https://windrosewiki.games/guides/best-early-builds): Optimal stat allocation for DPS, Tank, Balanced
- [Crafting Progression](https://windrosewiki.games/guides/crafting-progression): Efficient crafting order from Day 1 to endgame
- [Sailing & Navigation](https://windrosewiki.games/guides/sailing-navigation): Wind mechanics, ship types, ocean survival
- [Co-op Guide](https://windrosewiki.games/guides/coop-multiplayer): Server setup, role specialization, crew coordination
- [Naval Combat](https://windrosewiki.games/guides/ship-building-naval-combat): Ship building, upgrading, and combat tactics
"""

    if "Strategy Guides" not in content:
        # 在 Getting Started 后插入
        content = content.replace(
            "### [Crafting Recipes]",
            guides_section + "\n### [Crafting Recipes]"
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  ✅ llms.txt — Added Strategy Guides section")
    else:
        print("  ⏭️ llms.txt — Guides already listed")


if __name__ == "__main__":
    print("=== Phase 1: Update Sitemap & llms.txt ===")
    update_sitemap()
    update_llms()
    print("Done!")
