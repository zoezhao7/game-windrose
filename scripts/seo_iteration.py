from pathlib import Path
from datetime import date
import html

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://windrose-guides.com"
TODAY = "2026-05-12"

from templates import NAV_ITEMS as NAV

PAGES = []


def esc(value):
    return html.escape(str(value), quote=True)


def slug_to_depth(slug):
    slug = str(slug).replace("\\", "/")
    if slug == "":
        return 0
    return len(slug.strip("/").split("/"))


def css_path(slug):
    depth = slug_to_depth(slug)
    return "css/style.css" if depth == 0 else "../" * depth + "css/style.css"


def nav_html(active):
    active = str(active).replace("\\", "/")
    items = []
    active_root = "/" + active.split("/")[0] if active else "/"
    for label, href in NAV:
        cls = ' class="active"' if href == active_root or (href != "/" and active.startswith(href.strip("/"))) else ""
        current = ' aria-current="page"' if cls else ""
        items.append(f'<li><a href="{href}"{cls}{current}>{label}</a></li>')
    return "\n".join(items)


def breadcrumbs(items):
    lis = ['<li><a href="/">Home</a></li>']
    graph = [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"}
    ]
    for i, (name, href) in enumerate(items, start=2):
        if href:
            lis.append(f'<li><a href="{href}">{esc(name)}</a></li>')
            graph.append({"@type": "ListItem", "position": i, "name": name, "item": f"{SITE}{href}"})
        else:
            lis.append(f'<li><span aria-current="page">{esc(name)}</span></li>')
            graph.append({"@type": "ListItem", "position": i, "name": name})
    return "\n".join(lis), graph


def jsonish(obj):
    if isinstance(obj, dict):
        return "{" + ",".join(f'"{esc(k)}":{jsonish(v)}' for k, v in obj.items()) + "}"
    if isinstance(obj, list):
        return "[" + ",".join(jsonish(v) for v in obj) + "]"
    if obj is None:
        return "null"
    if isinstance(obj, (int, float)):
        return str(obj)
    return '"' + str(obj).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def table(headers, rows, caption):
    head = "".join(f'<th scope="col">{esc(h)}</th>' for h in headers)
    body_rows = []
    for row in rows:
        cells = "".join(f"<td>{cell}</td>" for cell in row)
        body_rows.append(f"<tr>{cells}</tr>")
    return f'''
<div class="table-responsive">
  <table>
    <caption>{esc(caption)}</caption>
    <thead><tr>{head}</tr></thead>
    <tbody>
      {''.join(body_rows)}
    </tbody>
  </table>
</div>'''


def stats(items):
    return '<div class="quick-stats">' + "".join(
        f'<div class="stat"><div class="stat-label">{esc(k)}</div><div class="stat-value">{v}</div></div>'
        for k, v in items
    ) + "</div>"


def faq(items):
    schema = {
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in items
        ],
    }
    html_bits = ['<section id="faq"><h2>Frequently Asked Questions</h2>']
    for q, a in items:
        html_bits.append(f'<details><summary>{esc(q)}</summary><div class="faq-answer"><p>{a}</p></div></details>')
    html_bits.append("</section>")
    return "\n".join(html_bits), schema


def page(slug, title, description, h1, body, crumb_items, priority="0.7", changefreq="weekly", schema_extra=None):
    slug = str(slug).replace("\\", "/")
    canonical = f"{SITE}/" if slug == "" else f"{SITE}/{slug}"
    crumb_html, crumb_graph = breadcrumbs(crumb_items)
    graph = [
        {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Windrose Guides", "publisher": {"@id": f"{SITE}/#org"}, "inLanguage": "en"},
        {"@type": "Organization", "@id": f"{SITE}/#org", "name": "Windrose Guides", "url": f"{SITE}/"},
        {"@type": "WebPage", "@id": f"{canonical}#webpage", "url": canonical, "name": h1, "description": description, "dateModified": TODAY, "isPartOf": {"@id": f"{SITE}/#website"}, "breadcrumb": {"@id": f"{canonical}#breadcrumb"}, "inLanguage": "en"},
        {"@type": "BreadcrumbList", "@id": f"{canonical}#breadcrumb", "itemListElement": crumb_graph},
        {"@type": "Article", "headline": h1, "datePublished": TODAY, "dateModified": TODAY, "author": {"@type": "Organization", "name": "Windrose Guides"}},
    ]
    if schema_extra:
        graph.extend(schema_extra)
    html_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{canonical}">
  <link rel="stylesheet" href="{css_path(slug)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:image" content="{SITE}/imgs/og.webp">
  <meta property="og:site_name" content="Windrose Guides">
  <meta property="article:published_time" content="{TODAY}">
  <meta property="article:modified_time" content="{TODAY}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="twitter:image" content="{SITE}/imgs/og.webp">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@graph":{jsonish(graph)}}}
  </script>
</head>
<body>
  <header class="header">
    <div class="container">
      <a href="/" class="logo" aria-label="Windrose Guides Home"><img src="/imgs/logo.png" alt="Windrose Guides Logo" width="32" height="32"> Windrose Guides</a>
      <button class="hamburger" aria-label="Toggle navigation menu" aria-expanded="false"><span></span><span></span><span></span></button>
      <nav aria-label="Primary"><ul class="nav-links">{nav_html(slug)}</ul></nav>
    </div>
  </header>
  <nav class="breadcrumb" aria-label="Breadcrumb"><div class="container"><ol>{crumb_html}</ol></div></nav>
  <main class="container">
    <h1>{esc(h1)}</h1>
    {body}
  </main>
  <footer class="footer">
    <div class="container">
        <div class="footer-grid">
            <div class="footer-brand">
                <a href="/" class="footer-logo"><img src="/imgs/logo.png" alt="Windrose Guides Logo" width="28" height="28"> Windrose Guides</a>
                <p>Your complete Windrose wiki, database, and guide hub. Crafting recipes, resource maps, boss strategies, ship builds, and more &mdash; all in one place.</p>
            </div>
            <div class="footer-col">
                <h4>Guides</h4>
                <ul>
                    <li><a href="/beginner-guide">Beginner Guide</a></li>
                    <li><a href="/builds">Build Guides</a></li>
                    <li><a href="/server-guide">Server Guide</a></li>
                    <li><a href="/download">Download</a></li>
                    <li><a href="/faq">FAQ</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>Database</h4>
                <ul>
                    <li><a href="/crafting">Crafting</a></li>
                    <li><a href="/resources">Resources</a></li>
                    <li><a href="/bosses">Bosses</a></li>
                    <li><a href="/ships">Ships</a></li>
                    <li><a href="/weapons">Weapons</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>Explore</h4>
                <ul>
                    <li><a href="/tools">Tools</a></li>
                    <li><a href="/news">News</a></li>
                    <li><a href="/sources">Sources</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <span>&copy; 2026 Windrose Guides. Unofficial fan resource. Not affiliated with Kraken Express or Pocketpair Publishing.</span>
            <nav>
                <a href="/pages">All Pages</a>
                <a href="/privacy">Privacy Policy</a>
                <a href="/terms">Terms of Service</a>
            </nav>
        </div>
    </div>
  </footer>
  <script>(function(){{var b=document.querySelector('.hamburger'),n=document.querySelector('.nav-links');if(!b||!n)return;b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');}});}})();</script>
</body>
</html>
'''
    out = ROOT / ("index.html" if slug == "" else Path(slug) / "index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_doc, encoding="utf-8")
    PAGES.append((slug, priority, changefreq, title, description))


def simple_cards(cards):
    return '<div class="quick-nav-grid">' + "".join(
        f'<a class="card quick-nav-card" href="{href}"><span class="nav-icon">{icon}</span><h3>{esc(title)}</h3><p>{esc(desc)}</p></a>'
        for icon, title, desc, href in cards
    ) + "</div>"


def build_pages():
    source_note = '<p class="update-note"><strong>Data note:</strong> Windrose is in Early Access, so recipes, stats, and boss details can change. This guide favors verified official descriptions, Steam news, and repeatable in-game progression steps over unconfirmed rumor.</p>'

    # Tools hub
    body = f'''
{stats([("Best For", "Fast planning"), ("Tools", "5"), ("JavaScript", "None required")])}
<p><strong>Windrose Tools</strong> is a compact hub for practical planning pages: recipes, progression checklists, server setup, resource routing, and ship selection. Heartopia.gg wins a lot of search intent by giving players utilities, not just articles; this section gives Windrose Guides the same kind of high-intent landing area.</p>
{simple_cards([
    ("#", "Workbench Recipe Finder", "Jump straight to Lv1-Lv3 tools, bags, repair kits, bullets, and station unlocks.", "/tools/recipe-finder"),
    ("#", "Progression Checklist", "Follow the early-game path from bonfire to copper tools, first ship, crew rescue, and Foothills.", "/tools/progression-checklist"),
    ("#", "Resource Planner", "See which resources unlock each major crafting tier and which tool you need to gather them.", "/tools/resource-planner"),
    ("#", "Ship Selector", "Compare Sloop, Brigantine, and Frigate by role, handling, firepower, and solo/co-op fit.", "/tools/ship-selector"),
    ("#", "Server Setup", "Dedicated server ports, SteamCMD launch flow, and hosting checklist for co-op groups.", "/server-guide"),
])}
<section><h2>Launch Priority Tools</h2><p>The first promotion-ready version should make the recipe finder, progression checklist, and server setup page the main utility targets. These pages match search phrases with strong intent: players want exact materials, what to do next, or how to host with friends.</p></section>
'''
    fh, fs = faq([
        ("Does Windrose Guides have interactive tools?", "The current tools are static, crawlable planning pages. Interactive filters can be added later without changing the URLs."),
        ("Why add tools before more articles?", "Tools attract repeated visits and earn links because they solve a player task faster than a long article."),
    ])
    page(Path("tools"), "Windrose Tools: Recipe Finder, Progression Checklist & Server Setup (2026)", "Windrose tools hub for recipes, progression, resources, ship comparison, and dedicated server setup. Built for fast planning and Google SEO.", "Windrose Tools Hub", body + fh, [("Tools", None)], "0.8", schema_extra=[fs])

    # Recipe finder
    recipe_rows = [
        ["Stone Axe", "Lv1 Workbench", "3 Stone + 3 Wood", "First tree harvesting upgrade"],
        ["Stone Pickaxe", "Lv1 Workbench", "3 Stone + 3 Wood", "Required for copper, clay, and cave progression"],
        ["Bandage", "Lv1 Workbench", "1 Coarse Fabric", "Core healing item for early fights"],
        ["Torn Sailcloth Bag", "Lv1 Workbench", "2 Coarse Fabric + 1 Rope", "First inventory upgrade"],
        ["Copper Pickaxe", "Lv1 Workbench", "5 Copper Ingot + 5 Wood", "Opens stronger ore progression"],
        ["Fast Travel Bell", "Lv1 Workbench", "10 Copper Ingot + 3 Rope", "Unlocks convenient return points"],
        ["Sailor Backpack", "Lv2 Workbench", "Torn Sailcloth Bag + Rough Hide + Copper Ingot", "Mid-game storage upgrade"],
        ["Bosun Backpack", "Lv3 Workbench", "Sailor Backpack + Tanned Leather + Foothills Iron Ingot", "Late storage upgrade"],
    ]
    body = f'''
{stats([("Coverage", "Lv1-Lv3"), ("Best Query", "Windrose recipes"), ("Updated", TODAY)])}
<p>This static recipe finder gives Google and players a clean answer for the most searched crafting questions: what station makes an item, what materials it costs, and why it matters in progression.</p>
{table(["Item", "Station", "Materials", "Use"], recipe_rows, "High-value Windrose crafting recipes")}
<section><h2>How to Use This Finder</h2><ol><li>Start with the item you want to craft.</li><li>Check the station level and whether the recipe belongs to early copper or Foothills iron progression.</li><li>Open the full <a href="/crafting/workbench">Workbench Recipes</a> page for the complete table.</li></ol></section>
{source_note}
'''
    fh, fs = faq([
        ("What is the most important early recipe?", "Stone Pickaxe is the key early recipe because it starts copper and clay progression."),
        ("Which recipe increases inventory space?", "Torn Sailcloth Bag is the first storage upgrade, followed later by Sailor Backpack and Bosun Backpack."),
        ("Where are the full recipes?", 'Use the <a href="/crafting/workbench">Workbench Recipes</a>, <a href="/crafting/smelting">Smelting</a>, and crafting subcategory pages.'),
    ])
    page(Path("tools/recipe-finder"), "Windrose Recipe Finder: Workbench Materials & Crafting Uses (2026)", "Find Windrose recipes fast: workbench level, materials, progression use, bags, bullets, repair kits, tools, and copper or iron unlocks.", "Windrose Recipe Finder", body + fh, [("Tools", "/tools"), ("Recipe Finder", None)], "0.8", schema_extra=[fs])

    # Progression checklist
    checklist_rows = [
        ["1", "Build Bonfire and Workbench", "Wood, Stone, Plant Fiber", "Creates the basic crafting loop"],
        ["2", "Craft Stone Pickaxe", "3 Stone + 3 Wood", "Mine copper ore and clay"],
        ["3", "Build Charcoal Kiln", "25 Wood + 20 Clay", "Turn wood into charcoal for smelting"],
        ["4", "Build Smelting Furnace", "15 Clay + 30 Stone", "Convert copper ore into ingots"],
        ["5", "Craft Copper Tools", "Copper Ingots + Wood", "Speed up harvesting and unlock stronger materials"],
        ["6", "Prepare Combat Kit", "Bandages, repair kit, food", "Survive caves and pirate camps"],
        ["7", "Claim First Ship", "Main quest progress", "Start island-to-island exploration"],
        ["8", "Push Foothills", "Copper gear, ship supplies", "Unlock iron, sulfur, and later progression"],
    ]
    body = f'''
{stats([("Route", "Starter Island to Foothills"), ("Focus", "Crafting unlocks"), ("Format", "Checklist")])}
<p>The fastest reliable Windrose start is not to build a huge base immediately. Build only what unlocks tools, smelting, healing, and your first ship, then move toward the next island chain with enough supplies to recover from mistakes.</p>
{table(["Step", "Goal", "Materials or Requirement", "Why It Matters"], checklist_rows, "Windrose early progression checklist")}
<section><h2>Promotion-Ready Short Answer</h2><p><strong>To progress quickly in Windrose, craft a Stone Pickaxe, mine copper and clay, build a Charcoal Kiln and Smelting Furnace, smelt Copper Ingots, then craft Copper tools before pushing toward your first ship and Foothills.</strong></p></section>
'''
    fh, fs = faq([
        ("Should I build a permanent base early?", "No. A small camp near resources is more efficient until you understand the island layout and unlock better tools."),
        ("What should I carry before leaving the first island?", "Bring bandages, food, repair materials, copper tools, and enough wood or stone to rebuild basic stations."),
    ])
    page(Path("tools/progression-checklist"), "Windrose Progression Checklist: Early Game Route to First Ship (2026)", "Step-by-step Windrose progression checklist from bonfire and workbench to copper tools, first ship, crew rescue, and Foothills.", "Windrose Progression Checklist", body + fh, [("Tools", "/tools"), ("Progression Checklist", None)], "0.8", schema_extra=[fs])

    # Resource planner
    resource_rows = [
        ["Wood", "Trees, driftwood, wreckage", "Axe", "Bonfire, Workbench, repairs, charcoal"],
        ["Stone", "Ground rocks and deposits", "Pickaxe", "Stone tools, furnace, bullets"],
        ["Plant Fiber", "Plants and shoreline gathering", "Hands or tool", "Rope, Coarse Fabric, bags, bandages"],
        ["Clay", "Riverbanks and wet ground patches", "Stone Pickaxe", "Kiln, furnace, bottles, pots"],
        ["Copper Ore", "Copper cave icons and deposits", "Stone Pickaxe", "Copper Ingots, tools, bell, bullets"],
        ["Iron Ore", "Foothills deposits", "Copper Pickaxe", "Iron tools, Lv2 recipes, advanced bags"],
        ["Gunpowder", "Smuggler stashes, pirate camps, later crafting", "Combat or Millstone", "Ammunition and ranged builds"],
        ["Sulfur", "Foothills yellow deposits", "Iron Pickaxe", "Late gunpowder crafting"],
    ]
    body = f'''
{stats([("Resources", "8 core"), ("Best Use", "Route planning"), ("Related", "Crafting + builds")])}
<p>Use this planner to decide what to farm before you craft a station or leave an island. The most common player mistake is collecting random materials without knowing which tool gate they are trying to open.</p>
{table(["Resource", "Where to Get It", "Tool or Gate", "Primary Uses"], resource_rows, "Windrose resource planner")}
<section><h2>Best Farming Order</h2><p>Wood, stone, and plant fiber come first. Clay and copper unlock smelting. Copper tools bridge into iron. Iron and sulfur push the late resource chain for stronger tools, backpacks, and ammunition.</p></section>
'''
    fh, fs = faq([
        ("What resource should I farm first?", "Wood and stone are first, but copper and clay are the first real progression resources."),
        ("Where should I farm gunpowder early?", "Use smuggler stashes and pirate camps before you can craft gunpowder from sulfur and ash."),
    ])
    page(Path("tools/resource-planner"), "Windrose Resource Planner: Copper, Iron, Clay, Gunpowder & Uses (2026)", "Plan Windrose resource farming by tool gate, location, and crafting use. Covers copper, iron, clay, gunpowder, sulfur, wood, stone, and fiber.", "Windrose Resource Planner", body + fh, [("Tools", "/tools"), ("Resource Planner", None)], "0.8", schema_extra=[fs])

    # Ship selector
    ship_rows = [
        ["Sloop", "Solo scouting, fast travel between islands", "Fast", "Low", "Low", "New solo players"],
        ["Brigantine", "Balanced exploration and co-op combat", "Medium", "Medium", "Medium", "Most crews"],
        ["Frigate", "Heavy naval battles and late fights", "Slow", "High", "High", "Prepared groups"],
    ]
    body = f'''
{stats([("Ships", "3"), ("Best Overall", "Brigantine"), ("Solo Pick", "Sloop")])}
<p>Pick your Windrose ship by job, not by size. The Sloop is easiest to maneuver, the Brigantine is the safest all-rounder, and the Frigate is a commitment to firepower and crew coordination.</p>
{table(["Ship", "Best Use", "Handling", "Firepower", "Durability", "Recommended For"], ship_rows, "Windrose ship selector")}
<section><h2>Quick Recommendation</h2><p>For most players, build toward the <a href="/ships/brigantine">Brigantine</a>. It has enough control for exploration and enough strength for fights without forcing the slow handling of a <a href="/ships/frigate">Frigate</a>.</p></section>
'''
    fh, fs = faq([
        ("What is the best solo ship?", "The Sloop is the easiest solo ship because speed and turning matter more when you do not have a full crew."),
        ("What is the best general ship?", "The Brigantine is the best default recommendation because it balances speed, firepower, and survival."),
    ])
    page(Path("tools/ship-selector"), "Windrose Ship Selector: Sloop vs Brigantine vs Frigate (2026)", "Compare Windrose ships by speed, handling, firepower, durability, solo play, and co-op roles. Choose Sloop, Brigantine, or Frigate.", "Windrose Ship Selector", body + fh, [("Tools", "/tools"), ("Ship Selector", None)], "0.8", schema_extra=[fs])

    # Server guide
    server_rows = [
        ["Server package", "Install the Windrose Dedicated Server through Steam tools or SteamCMD"],
        ["SteamCMD app id", "<code>4129620</code>"],
        ["OS status", "Official guide currently describes the dedicated server as Windows-only"],
        ["Ports", "Ports are dynamically assigned through NAT punch-through; make sure UPnP works and disable proxy/VPN while testing"],
        ["World settings", "Set region, password, player count, server name, and save behavior before launch"],
        ["Firewall", "Allow <code>WindroseServer.exe</code> through Windows Defender Firewall or host firewall"],
        ["Backups", "Back up world saves before patches and before changing server settings"],
    ]
    body = f'''
{stats([("Intent", "Host co-op"), ("Source Type", "Official guide + checklist"), ("Best For", "Groups")])}
<p>Windrose supports co-op play, and dedicated hosting is one of the strongest utility topics for search. This page turns the official server setup flow into a simple pre-launch checklist for players who want a persistent world.</p>
{table(["Area", "Checklist"], server_rows, "Windrose dedicated server setup checklist")}
<section><h2>SteamCMD Install Commands</h2><pre><code>force_install_dir "C:\\Game_Servers\\Windrose_Server"
login anonymous
app_update 4129620 validate
quit</code></pre><p>To update later, rerun <code>app_update 4129620 validate</code>. Keep the dedicated server version matched to the current game client after patches.</p></section>
<section><h2>Basic Setup Flow</h2><ol><li>Install the dedicated server package through SteamCMD or Steam tools.</li><li>Configure server name, password, region, player count, and save behavior while the server is shut down.</li><li>Make sure UPnP is available for NAT punch-through, then disable proxy or VPN during first connection tests.</li><li>Add firewall and antivirus exceptions for <code>WindroseServer.exe</code>.</li><li>Start the server, test connection from a separate client, and back up saves before major patches.</li></ol></section>
<section><h2>Official Source</h2><p>For exact launch arguments, config fields, and troubleshooting, use the official <a href="https://playwindrose.com/dedicated-server-guide/" rel="nofollow">Windrose Dedicated Server Guide</a>. This page is a player-friendly checklist and should be updated whenever the official guide changes.</p></section>
'''
    fh, fs = faq([
        ("Can I host a Windrose dedicated server?", "Yes. The official guide supports SteamCMD installation with app id 4129620 and gives the current config workflow."),
        ("Does the dedicated server run on Linux?", "The official guide currently describes it as Windows-only, so treat Linux or headless setups as unsupported unless the official documentation changes."),
        ("Should I back up my server save?", "Yes. Back up before patches, before changing difficulty or world settings, and before migrating hosts."),
    ])
    page(Path("server-guide"), "Windrose Dedicated Server Guide: Hosting Checklist & Setup Tips (2026)", "Windrose dedicated server setup checklist for co-op groups: install flow, ports, firewall, passwords, saves, backups, and official guide link.", "Windrose Dedicated Server Guide", body + fh, [("Server Guide", None)], "0.75", schema_extra=[fs])

    # Download / system requirements style page
    body = f'''
{stats([("Platform", "PC / Steam"), ("Mode", "Single-player + online co-op"), ("Status", "Early Access")])}
<p><strong>Windrose is available on Steam for PC in Early Access.</strong> This page exists because download and system requirement searches often convert better than broad guide searches, and they help players confirm they are looking at the right game before using the wiki.</p>
{table(["Topic", "Answer"], [
    ["Where to get Windrose", '<a href="https://store.steampowered.com/app/3041230/Windrose/" rel="nofollow">Steam store page</a>'],
    ["Developer", "Kraken Express"],
    ["Publisher", "Kraken Express / Pocketpair Publishing"],
    ["Release date", "14 Apr, 2026"],
    ["Genre", "Action, Adventure, RPG, Early Access"],
    ["Features", "Single-player, online co-op, Steam Cloud, Family Sharing"],
    ["Languages", "English plus multiple supported interface/subtitle languages"],
    ["Progression focus", "Crafting stations, resources, crew, ships, bosses, island exploration, and dedicated servers"],
], "Windrose download and game info")}
<section><h2>What Early Access Includes</h2><p>According to the Steam page, the Early Access version is a playable survival adventure with optional co-op, three biomes, roughly thirty procedurally generated islands, more than ninety hand-crafted points of interest, three playable ships, naval combat with boarding, building, crafting, stats, talents, armor, weapons, factions, reputation, and NPC workers.</p></section>
<section><h2>Before You Buy</h2><p>Windrose is still changing during Early Access, so guides should be treated as living references. Check Steam announcements for patch notes before assuming a recipe, boss requirement, or server option is final.</p></section>
'''
    fh, fs = faq([
        ("Is Windrose on Steam?", 'Yes. The official PC listing is on <a href="https://store.steampowered.com/app/3041230/Windrose/" rel="nofollow">Steam</a>.'),
        ("Is Windrose finished?", "No. It is an Early Access game, so content and balance can change."),
    ])
    page(Path("download"), "Windrose Download: Steam Page, Early Access & Game Info (2026)", "Find Windrose on Steam, confirm Early Access status, developer, publisher, platform, co-op focus, and what to check before using guides.", "Windrose Download & Game Info", body + fh, [("Download", None)], "0.65", schema_extra=[fs])

    # NOTE: crafting/alchemy、crafting/cooking、crafting/building 已改为手动维护 HTML，
    # 不再由脚本生成，避免覆盖人工精修内容。

    # NOTE: bosses 页面已改为手动维护 HTML，不再由脚本生成，避免覆盖人工精修内容。

    # Upgrade news page
    news_body = f'''
{stats([("Best Source", "Steam News"), ("Update Cadence", "After patches"), ("SEO Role", "Freshness")])}
<p>The news page should summarize official patch notes and point players back to affected guides. This gives Google freshness signals while keeping recipe and resource pages stable.</p>
{table(["Date", "Source", "Update", "Guide Impact"], [
    ["May 2026", "Steam / official updates", "Cloud save, dedicated server, and stability-related notices were active topics after launch.", "Server guide and troubleshooting should stay current."],
    ["April 2026", "Steam launch", "Windrose entered Early Access on Steam.", "All guides should be labeled Early Access and updated after patches."],
    ["Ongoing", "Official website and Steam news", "Dedicated server documentation and patch notes may change.", "Update /server-guide and FAQ first."],
], "Windrose news and update tracker")}
<section><h2>How We Use Patch Notes</h2><p>When a patch changes crafting, enemy balance, servers, or progression, update the affected guide first, then refresh the sitemap lastmod and this news index. Avoid copying full patch notes; summarize the practical impact for players.</p></section>
<section><h2>Official Links</h2><ul><li><a href="https://store.steampowered.com/app/3041230/Windrose/" rel="nofollow">Windrose on Steam</a></li><li><a href="https://playwindrose.com/windrose-crew/dedicated-server-guide" rel="nofollow">Official Dedicated Server Guide</a></li></ul></section>
'''
    fh, fs = faq([
        ("Where should I check official Windrose updates?", "Use the Steam page and official Windrose website first, then this page for guide impact summaries."),
        ("Why not mirror full patch notes?", "Summaries are better for SEO and user value, and they avoid duplicating official content."),
    ])
    page(Path("news"), "Windrose News & Updates: Patch Notes Impact Tracker (2026)", "Windrose news and update tracker summarizing Steam, official website, dedicated server, and guide-impact changes for Early Access players.", "Windrose News & Updates", news_body + fh, [("News", None)], "0.65", changefreq="daily", schema_extra=[fs])

    # Add source log
    source_body = f'''
{stats([("Purpose", "Trust"), ("Status", "Living log"), ("Use", "Content QA")])}
<p>This source log tracks where key site claims should be verified. It helps keep the guide promotable without pretending every Early Access detail is final.</p>
{table(["Topic", "Preferred Source", "Update Rule"], [
    ["Game metadata", "Steam store page and official site", "Update when Steam or official page changes"],
    ["Dedicated servers", "Official playwindrose.com server guide", "Update immediately after official guide changes"],
    ["Patch notes", "Steam news and official announcements", "Summarize impact, do not duplicate full notes"],
    ["Recipes and resources", "In-game verification plus reputable community guides", "Mark uncertain values clearly and remove unfinished draft language from visible pages"],
    ["Boss strategy", "In-game testing, video evidence, and patch-specific notes", "Separate confirmed mechanics from recommendations"],
], "Windrose Guides source policy")}
'''
    page(Path("sources"), "Windrose Guides Sources & Update Policy (2026)", "Source policy for Windrose Guides: official Steam data, playwindrose.com server docs, patch notes, in-game verification, and Early Access update rules.", "Windrose Guides Sources & Update Policy", source_body, [("Sources", None)], "0.45", "monthly")

    # Task 2: 3 Deep Guides
    mining_body = f'''
{stats([("Difficulty", "Medium"), ("Required Tool", "Copper Pickaxe"), ("Best Yield", "Foothills")])}
<p>Mining is the core of mid-game progression. This guide covers the most efficient routes for Copper, Iron, and Sulfur to minimize travel time and maximize yield.</p>
<section><h2>1. Early Copper Route (Starter Island)</h2><p>Before leaving the starter island, locate the two cave icons. Bring a Stone Pickaxe and at least 3 torches. Clear the caves entirely, which should yield about 60-80 Poor Copper Ore. Smelt this immediately to craft your Copper Pickaxe and Weaponsmith.</p></section>
<section><h2>2. The Foothills Iron Loop</h2><p>Once you reach the Foothills, Iron Ore becomes your bottleneck. The best route starts at the Southern coast fast travel bell, heading north along the cliff base. You will encounter 4-5 iron deposits. <strong>Always bring a Brigantine or larger ship</strong> to store the heavy ore, as inventory weight will limit you quickly.</p></section>
<section><h2>3. Sulfur & Gunpowder Farming</h2><p>Sulfur spawns near volcanic vents in the Foothills and Cursed Swamps. Combine Sulfur with Ash (from burning wood) at the Alchemy Table to craft Gunpowder. A single run through the Eastern Swamp vents yields enough for ~100 bullets.</p></section>
'''
    fh, fs = faq([("What is the best pickaxe?", "The Iron Pickaxe is the most efficient for all mid-game ores."), ("Do ores respawn?", "Yes, ore nodes typically respawn after 2 in-game days.")])
    page(Path("guides/mining-routes"), "Best Mining Routes: Copper, Iron & Sulfur (2026)", "The most efficient mining routes in Windrose. Farm Copper, Iron, and Sulfur quickly to upgrade your ship and weapons.", "Best Mining Routes & Ore Farming", mining_body + fh, [("Guides", "/guides"), ("Mining Routes", None)], "0.85", schema_extra=[fs])

    boss_progression_body = f'''
{stats([("Total Bosses", "3 Confirmed"), ("Preparation", "High"), ("Required Gear", "Iron Tier")])}
<p>Bosses in Windrose are major progression gates. You cannot access certain islands or craft advanced ship parts without defeating them. Here is the optimal progression path and strategy for each.</p>
<section><h2>1. Thomas Richards (Coastal Jungle)</h2><p><strong>Level 5-6.</strong> The first major roadblock. Richards uses slow, heavy saber swings. <strong>Strategy:</strong> Wait for his 3-hit combo to finish, then heavy attack. Do not get greedy. A simple Rapier is highly effective here due to its fast attack speed.</p></section>
<section><h2>2. Israel Hands (Foothills)</h2><p><strong>Level 8-10.</strong> Hands uses firearms and calls reinforcements. <strong>Strategy:</strong> Use the pillars in the arena to block his musket shots. Focus on clearing his crew first, then chip away at his health. Bring at least 10 Healing Potions.</p></section>
<section><h2>3. The High Priestess (Cursed Swamps)</h2><p><strong>Level 12-15.</strong> A magic-based boss with massive AoE attacks. <strong>Strategy:</strong> Mobility is key. Use a Sloop to reach her island quickly if you die. Equip armor with high elemental resistance. Her attacks inflict Poison, so bring Antidotes crafted at the Alchemy Table.</p></section>
'''
    fh, fs = faq([("Can I skip bosses?", "No, story bosses drop key items needed for crafting the Brigantine and Frigate."), ("Do bosses scale in co-op?", "Yes, bosses gain increased health and damage for each additional player in the server.")])
    page(Path("guides/boss-progression"), "Boss Progression & Strategy Guide (2026)", "Complete boss progression guide for Windrose. Learn how to defeat Thomas Richards, Israel Hands, and the High Priestess.", "Boss Progression & Strategy Guide", boss_progression_body + fh, [("Guides", "/guides"), ("Boss Progression", None)], "0.85", schema_extra=[fs])

    builds_body = f'''
{stats([("Playstyles", "Melee, Ranged, Hybrid"), ("Respec", "Free"), ("Meta", "Agility/Crit")])}
<p>Your build determines your combat effectiveness. Because respecs are free, you can experiment, but these three early-game builds will carry you safely to the late game.</p>
<section><h2>1. The Swashbuckler (Agility/Crit)</h2><p><strong>Weapons:</strong> Rapier or Saber + Pistol<br><strong>Talents:</strong> Focus on the 'Duelist' tree. Maximize dodge i-frames and critical hit chance.<br><strong>Playstyle:</strong> Fast-paced hit-and-run. Use the Pistol to stagger enemies, then dash in for critical melee strikes. Excellent for solo players.</p></section>
<section><h2>2. The Ironclad (Strength/Vitality)</h2><p><strong>Weapons:</strong> Heavy Club or Boarding Axe + Blunderbuss<br><strong>Talents:</strong> Focus on the 'Toughguy' tree. Maximize HP, Stamina, and Perfect Block window.<br><strong>Playstyle:</strong> Stand your ground. Perfect block enemy attacks to stagger them, then deliver massive heavy attacks. Best for co-op frontlining.</p></section>
<section><h2>3. The Gunner (Perception/Resourcefulness)</h2><p><strong>Weapons:</strong> Musket + Dual Pistols<br><strong>Talents:</strong> Focus on the 'Sharpshooter' tree. Maximize ranged damage and ammo crafting efficiency.<br><strong>Playstyle:</strong> Keep your distance. This build requires heavy farming for Gunpowder and Lead, but safely deletes enemies before they reach you.</p></section>
'''
    fh, fs = faq([("Can I respec my talents?", "Yes, respecs are completely free at any time from the character menu."), ("What is the best solo build?", "The Swashbuckler (Agility/Crit) provides the mobility needed to survive multiple enemies alone.")])
    page(Path("guides/best-early-builds"), "Best Early Game Builds & Talents (2026)", "The best early game builds in Windrose. Choose between the Swashbuckler, Ironclad, or Gunner playstyles to dominate combat.", "Best Early Game Builds & Talents", builds_body + fh, [("Guides", "/guides"), ("Early Builds", None)], "0.85", schema_extra=[fs])

    # --- 阶段 1 补充：4 篇额外深度攻略 ---

    # 1) Ship Building & Naval Combat
    ship_guide_body = f'''
{stats([("Ships", "Sloop / Brigantine / Frigate"), ("Cannons", "3 Types"), ("Boarding", "Yes")])}
<p>Naval combat is one of Windrose's most unique systems. This guide covers everything from upgrading your starter Sloop to commanding a Frigate fleet in late-game naval battles.</p>
<section><h2>1. Your First Ship: The Sloop</h2><p>You receive a free Sloop after completing the starter island quest chain. The Sloop is fast and agile but fragile — it has only <strong>2 cannon slots</strong> and low hull HP. Use it primarily for <strong>scouting islands</strong> and <strong>avoiding fights</strong>. If enemies engage, outrun them rather than trading shots.</p></section>
<section><h2>2. Upgrading to the Brigantine</h2><p>The Brigantine requires defeating the first boss (Thomas Richards) to unlock its blueprint. Materials: <strong>80 Wood + 40 Copper Nails + 20 Iron Ingots + 10 Rope + Sail Fabric</strong>. The Brigantine has 4 cannon slots, significantly more HP, and can carry a full crew of 4 players comfortably. This is where naval combat becomes viable.</p></section>
<section><h2>3. Naval Combat Mechanics</h2><ul><li><strong>Wind Direction</strong> — Your ship speed depends on wind angle. Sailing with the wind gives maximum speed; sailing against it slows you to a crawl. Use the wind indicator on your compass.</li><li><strong>Cannon Types</strong> — Round shot for hull damage, grape shot for crew damage, chain shot for mast damage. Always carry all three.</li><li><strong>Boarding</strong> — When an enemy ship is disabled (mast destroyed), pull alongside and press F to board. Boarding is the fastest way to loot pirate ships.</li><li><strong>Repair Kits</strong> — Craft Ship Repair Kits before any naval engagement. A single hole below the waterline will slowly sink your ship.</li></ul></section>
<section><h2>4. The Frigate (Late Game)</h2><p>The Frigate is a floating fortress with <strong>8 cannon slots</strong>, massive HP, and cargo space. It requires defeating Israel Hands and gathering Foothills-tier materials. Only build a Frigate if you have a co-op crew of 3+ — solo players cannot operate all cannons effectively.</p></section>
'''
    fh, fs = faq([("Which ship should I build first?", "Always upgrade to the Brigantine first. It is the best balance of firepower and maneuverability."), ("Can my ship be destroyed permanently?", "No. If your ship sinks, it respawns at the nearest dock, but you lose all cargo stored on board.")])
    page(Path("guides/ship-building-naval-combat"), "Ship Building & Naval Combat Guide (2026)", "Complete Windrose ship building and naval combat guide. Learn how to upgrade ships, use cannons, board enemies, and dominate the seas.", "Ship Building & Naval Combat Guide", ship_guide_body + fh, [("Guides", "/guides"), ("Naval Combat", None)], "0.85", schema_extra=[fs])

    # 2) Sailing & Navigation
    sailing_body = f'''
{stats([("Map Size", "30+ Islands"), ("Fast Travel", "Bell System"), ("Navigation", "Compass + Wind")])}
<p>Windrose's world is massive — over 30 procedurally generated islands across three biomes. Knowing how to navigate efficiently saves hours of gameplay time.</p>
<section><h2>1. Understanding the Wind System</h2><p>Wind direction changes every in-game day. The <strong>compass HUD</strong> shows the current wind direction with a small arrow. Sailing with the wind (downwind) gives maximum speed. Sailing at 90° to the wind (beam reach) gives about 70% speed. Sailing directly into the wind (upwind) reduces you to 30% speed. <strong>Plan your routes</strong> based on wind direction to avoid painfully slow crossings.</p></section>
<section><h2>2. Map Markers & Exploration</h2><p><strong>Right-click</strong> the map to place custom markers. Always check "Show on minimap" so markers appear on your HUD. Mark these immediately: <strong>home bases, resource nodes, cave entrances, boss arenas, and dangerous areas</strong>. There is no limit to the number of markers.</p></section>
<section><h2>3. Fast Travel Network</h2><p>Craft <strong>Fast Travel Bells</strong> (10 Copper Ingot + 3 Rope) and place them strategically. Recommended locations: your main base, Foothills landing, Cursed Swamps entrance, and near each boss arena. You can teleport between any two bells instantly, but <strong>your ship does not teleport with you</strong> — plan accordingly.</p></section>
<section><h2>4. Island Biomes</h2><ul><li><strong>Coastal Jungle</strong> — Starter biome. Low-level enemies, abundant wood and copper. Safe for new players.</li><li><strong>Foothills</strong> — Mid-game. Iron ore, sulfur, tougher enemies. Requires copper-tier gear minimum.</li><li><strong>Cursed Swamps</strong> — Late game. Poisonous enemies, rare materials, the High Priestess boss. Bring antidotes and iron-tier gear.</li></ul></section>
'''
    fh, fs = faq([("Does my ship teleport with fast travel?", "No. Your ship stays where you left it. You must sail it manually to your destination."), ("How do I find new islands?", "Sail toward unexplored areas on your map. New islands appear as fog lifts when you get close enough.")])
    page(Path("guides/sailing-navigation"), "Sailing & Navigation Guide: Wind, Maps & Fast Travel (2026)", "Master Windrose sailing and navigation. Learn the wind system, map markers, fast travel bells, and island biome progression.", "Sailing & Navigation Guide", sailing_body + fh, [("Guides", "/guides"), ("Sailing", None)], "0.85", schema_extra=[fs])

    # 3) Crafting Progression
    craft_prog_body = f'''
{stats([("Stations", "7 Main"), ("Tiers", "Stone → Copper → Iron"), ("Key Gate", "Workbench Level")])}
<p>Crafting in Windrose follows a strict tier system. Understanding which stations unlock which recipes — and in what order — prevents wasted resources and backtracking.</p>
<section><h2>1. The Crafting Tier Ladder</h2><p>Progression follows this order: <strong>Hand Crafting → Workbench Lv1 → Charcoal Kiln + Smelting Furnace → Workbench Lv2 → Weaponsmith → Armor Workshop → Workbench Lv3</strong>. Each tier unlocks recipes that feed into the next, creating a clear upgrade path.</p></section>
<section><h2>2. Station Requirements</h2>
{table(["Station", "Materials", "Prerequisite", "Key Recipes"], [
    ["Workbench Lv1", "5 Wood", "None", "Stone tools, bags, bandages, rope"],
    ["Charcoal Kiln", "25 Wood + 20 Clay", "Stone Pickaxe", "Charcoal (fuel for smelting)"],
    ["Smelting Furnace", "15 Clay + 30 Stone", "Stone Pickaxe", "Copper Ingots, Iron Ingots"],
    ["Weaponsmith", "10 Wood + 5 Copper Ingot", "Copper, roof required", "Saber, Rapier, Club, firearms"],
    ["Armor Workshop", "Rough Hide (from Boars)", "Roof required", "All armor sets"],
    ["Workbench Lv2", "Sawhorse addon", "20 Wood + 10 Copper Ingot", "Mid-tier tools, Sailor Backpack"],
    ["Workbench Lv3", "Toolbox addon", "10 Wood + 20 Nails + 5 Iron", "Late tools, Bosun Backpack"],
], "Windrose crafting station progression")}
</section>
<section><h2>3. Common Mistakes</h2><ul><li><strong>Don't skip the Charcoal Kiln.</strong> Many players try to smelt ore without charcoal. The kiln is mandatory.</li><li><strong>Build stations under roofs.</strong> The Weaponsmith and Armor Workshop require a roof to be placed.</li><li><strong>Recipes are material-gated.</strong> Some recipes only appear after you pick up a specific material for the first time.</li></ul></section>
'''
    fh, fs = faq([("Why can't I see a recipe?", "Most recipes are hidden until you collect the primary material. Pick up new resources to unlock recipes automatically."), ("What is the most important crafting station?", "The Smelting Furnace is the most important mid-game station because it converts raw ore into usable ingots.")])
    page(Path("guides/crafting-progression"), "Crafting Progression: All Stations & Unlock Order (2026)", "Complete Windrose crafting progression guide. Learn the station unlock order, material requirements, and common mistakes to avoid.", "Crafting Progression Guide", craft_prog_body + fh, [("Guides", "/guides"), ("Crafting Progression", None)], "0.85", schema_extra=[fs])

    # 4) Co-op & Multiplayer Guide
    coop_body = f'''
{stats([("Max Players", "Up to 10"), ("Recommended", "2-4"), ("Server Types", "P2P + Dedicated")])}
<p>Windrose shines in co-op. This guide covers how to set up multiplayer, what to expect with different group sizes, and strategies for efficient crew play.</p>
<section><h2>1. How to Play Co-op</h2><p>From the main menu, select <strong>"Host Game"</strong> to create a session, or <strong>"Join Game"</strong> to browse public sessions. You can also join friends directly through Steam. Private servers require a password set by the host.</p></section>
<section><h2>2. Crew Roles</h2><p>In an ideal crew of 4:</p><ul><li><strong>Captain (1)</strong> — Steers the ship, manages navigation, calls targets during naval combat.</li><li><strong>Gunner (1-2)</strong> — Operates cannons during naval battles. Switches between ammo types as needed.</li><li><strong>Scout/Gatherer (1)</strong> — Explores ahead, gathers resources, marks dangers on the map.</li><li><strong>Boarder (1)</strong> — Specializes in melee combat for ship boarding and dungeon clearing.</li></ul></section>
<section><h2>3. Shared Progression</h2><p>Progression is tied to the <strong>world save</strong>, not individual characters. All players share the same world state, quest progress, and base. <strong>However, character levels and talents are per-character.</strong> This means a new player joining a late-game world will be under-leveled — they should grind POIs and quests to catch up.</p></section>
<section><h2>4. Dedicated Servers</h2><p>For persistent worlds that run 24/7, set up a <strong>dedicated server</strong> using SteamCMD (App ID: 4129620). See our <a href="/server-guide">Dedicated Server Guide</a> for step-by-step setup. Dedicated servers prevent progress loss when the host disconnects.</p></section>
'''
    fh, fs = faq([("Can I play Windrose solo?", "Yes. The game is fully playable solo, though some bosses and naval combat are significantly easier with a crew."), ("Do items transfer between worlds?", "No. Characters keep their level and talents, but inventory and equipment are tied to each world save.")])
    page(Path("guides/coop-multiplayer"), "Co-op & Multiplayer Guide: Crew Roles, Servers & Tips (2026)", "Complete Windrose co-op and multiplayer guide. Learn crew roles, shared progression, dedicated server setup, and best practices for group play.", "Co-op & Multiplayer Guide", coop_body + fh, [("Guides", "/guides"), ("Co-op Guide", None)], "0.85", schema_extra=[fs])

    # Task 4: Search Page
    search_body = f'''
<p>Use the search bar below to find guides, recipes, resources, and boss strategies across the entire Windrose Guides database.</p>
<div class="search-container" style="margin: 2rem 0;">
    <input type="text" id="searchInput" placeholder="Search for items, bosses, guides..." style="width: 100%; padding: 1rem; font-size: 1.1rem; border-radius: 8px; border: 1px solid var(--border); background: var(--bg-surface); color: var(--text); outline: none; transition: border-color 0.2s;">
    <div id="searchResults" style="margin-top: 1.5rem; display: flex; flex-direction: column; gap: 1rem;"></div>
</div>
<script>
    document.addEventListener('DOMContentLoaded', () => {{
        const input = document.getElementById('searchInput');
        const results = document.getElementById('searchResults');
        let searchData = [];

        // Fetch search index (pages.json)
        fetch('/data/search-index.json')
            .then(res => res.json())
            .then(data => {{ searchData = data; }})
            .catch(err => console.error("Search index failed to load.", err));

        input.addEventListener('input', (e) => {{
            const query = e.target.value.toLowerCase().trim();
            results.innerHTML = '';
            if (query.length < 2) return;

            const matches = searchData.filter(item => 
                item.title.toLowerCase().includes(query) || 
                item.description.toLowerCase().includes(query)
            ).slice(0, 10);

            if (matches.length === 0) {{
                results.innerHTML = '<p style="color: var(--text-muted);">No results found.</p>';
                return;
            }}

            matches.forEach(item => {{
                const el = document.createElement('a');
                el.href = item.url;
                el.className = 'card quick-nav-card';
                el.style.display = 'block';
                el.innerHTML = `<h3 style="margin-bottom:0.2rem; color:var(--accent);">${{item.title}}</h3><p style="font-size:0.85rem; color:var(--text-secondary);">${{item.description}}</p>`;
                results.appendChild(el);
            }});
        }});
    }});
</script>
'''
    page(Path("search"), "Search Windrose Guides (2026)", "Search the entire Windrose Guides database for recipes, items, bosses, and guides.", "Search Windrose Guides", search_body, [("Search", None)], "0.9")



def update_home():
    # NOTE: 首页（index.html）由手动维护，不再通过脚本注入内容。
    # 之前的逻辑因 HTML 实体（&amp;）与纯文本（&）不匹配导致重复注入 bug。
    pass


def update_css():
    p = ROOT / "css/style.css"
    text = p.read_text(encoding="utf-8")
    add = '''

.update-note {
  padding: 0.85rem 1rem;
  border-left: 4px solid var(--accent);
  background: #fff7f5;
  border-radius: 4px;
}

.content-section,
.page-hero {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

:focus-visible {
  outline: 3px solid var(--accent-light);
  outline-offset: 2px;
}
'''
    if ".update-note" not in text:
        text += add
    p.write_text(text, encoding="utf-8")


def write_todo():
    content = f'''# Windrose Guides Iteration TODO - Promotion Readiness

Updated: {TODAY}

## Competitor Gap: heartopia.gg

- [x] Add high-intent utility hub similar to competitor tool/database entry points.
- [x] Add crawlable tools pages: recipe finder, progression checklist, resource planner, ship selector.
- [x] Add official/download intent page so brand searches have a clean landing page.
- [x] Add dedicated server guide page because co-op hosting has strong search intent.
- [x] Remove visible "coming soon" positioning from alchemy, cooking, building-materials, bosses, and news pages.
- [x] Add source/update policy to improve trust for Early Access data.
- [x] Refresh sitemap and llms.txt so new pages are discoverable by Google and AI crawlers.
- [ ] Add original screenshots or generated WebP article images for the top 10 pages.
- [ ] Add real interactive filtering for recipe/resource tools once structured data is available.
- [ ] Add multilingual P1 pages after English pages stabilize.

## SEO Launch Gate

- [x] At least 40 crawlable HTML pages.
- [x] Every new SEO page has title, meta description, canonical, robots, OG, Twitter, breadcrumb, Article JSON-LD, FAQ where useful.
- [x] Major pages include tables, short-answer paragraphs, FAQ, and related internal links.
- [x] `sitemap.xml`, `robots.txt`, and `llms.txt` exist.
- [x] No top-priority new page uses "coming soon" as its main content.
- [ ] Run external rich-result validation after deployment.
- [ ] Connect Google Search Console and submit sitemap after DNS is live.
- [ ] Replace placeholder AdSense `ads.txt` after account approval.

## Content Backlog

- [ ] Verify exact patch/current version from Steam before public promotion.
- [ ] Expand Charon's Obols with exact arena, attack names, drops, and screenshots.
- [ ] Add dedicated pages for Blackbeard and starter boss when reliable data is available.
- [ ] Build JSON data files for recipes/resources so pages can be regenerated safely.
- [ ] Add image assets under `/imgs/` and update `og:image` per major section.
'''
    (ROOT / "docs" / "ITERATION_TODO_PROMOTION.md").write_text(content, encoding="utf-8")


def update_llms():
    path = ROOT / "llms.txt"
    text = path.read_text(encoding="utf-8")
    additions = '''

### [Tools](https://windrose-guides.com/tools)
- [Recipe Finder](https://windrose-guides.com/tools/recipe-finder): Workbench level, materials, and crafting use lookup
- [Progression Checklist](https://windrose-guides.com/tools/progression-checklist): Early route from first camp to copper tools, first ship, and Foothills
- [Resource Planner](https://windrose-guides.com/tools/resource-planner): Core resources by location, tool gate, and primary use
- [Ship Selector](https://windrose-guides.com/tools/ship-selector): Sloop vs Brigantine vs Frigate comparison

### [Utility Pages](https://windrose-guides.com/download)
- [Download & Game Info](https://windrose-guides.com/download): Steam page, Early Access status, developer, publisher, and platform
- [Dedicated Server Guide](https://windrose-guides.com/server-guide): Hosting checklist and official server documentation link
- [Sources & Update Policy](https://windrose-guides.com/sources): Verification policy for Early Access guide data
'''
    if "Recipe Finder" not in text:
        text = text.replace("## Key Topics", additions + "\n## Key Topics")
    path.write_text(text, encoding="utf-8")


def update_sitemap():
    existing = []
    for f in ROOT.rglob("*.html"):
        if ".git" in f.parts or "docs" in f.parts or "scripts" in f.parts or "skills" in f.parts:
            continue
        rel = f.relative_to(ROOT).as_posix()
        if rel == "index.html":
            slug = ""
        elif rel.endswith("/index.html"):
            slug = rel[:-len("/index.html")]
        else:
            slug = rel[:-len(".html")]
        if slug == "404":
            continue
        priority = "0.6"
        if slug == "":
            priority = "1.0"
        elif slug in {"beginner-guide", "crafting/workbench", "resources/copper", "tools", "tools/recipe-finder", "tools/progression-checklist"}:
            priority = "0.9"
        elif slug.split("/")[0] in {"crafting", "resources", "bosses", "ships", "weapons", "builds", "server-guide"}:
            priority = "0.8"
        changefreq = "daily" if slug == "news" else "weekly"
        existing.append((slug, priority, changefreq))
    existing.sort(key=lambda x: (x[0].count("/"), x[0]))
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for slug, priority, changefreq in existing:
        loc = f"{SITE}/" if slug == "" else f"{SITE}/{slug}"
        parts.append(f'''  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>''')
    parts.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(parts) + "\n", encoding="utf-8")


def main():
    build_pages()
    update_home()
    update_css()
    write_todo()
    update_llms()
    update_sitemap()
    print(f"Generated {len(PAGES)} SEO pages and refreshed site files.")


if __name__ == "__main__":
    main()
