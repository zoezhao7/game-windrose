"""
阶段1: 生成 Guides Hub 页面
"""
import os

ROOT = r"F:\aicode\gamedoc"

# 通用页面模板片段
def header_html(active=""):
    links = [
        ("/", "Home"), ("/beginner-guide", "Beginner Guide"), ("/guides", "Guides"),
        ("/crafting", "Crafting"), ("/resources", "Resources"), ("/bosses", "Bosses"),
        ("/ships", "Ships"), ("/weapons", "Weapons"), ("/builds", "Builds"),
        ("/faq", "FAQ"), ("/news", "News"),
    ]
    li = "".join(f'<li><a href="{u}"{" class=\"active\"" if u==active else ""}>{t}</a></li>' for u,t in links)
    return f'''<header class="header"><div class="container">
<a href="/" class="logo" aria-label="Windrose Guides Home"><img src="/imgs/logo.png" alt="Windrose Guides Logo" width="32" height="32"> Windrose Guides</a>
<button class="hamburger" aria-label="Toggle navigation" aria-expanded="false"><span></span><span></span><span></span></button>
<nav><ul class="nav-links">{li}</ul></nav></div></header>'''

def footer_html():
    return '''<footer class="footer"><div class="container"><div class="footer-grid">
<div class="footer-brand"><a href="/" class="footer-logo"><img src="/imgs/logo.png" alt="Windrose Guides Logo" width="28" height="28"> Windrose Guides</a>
<p>Your complete Windrose wiki, database, and guide hub.</p></div>
<div class="footer-col"><h4>Guides</h4><ul><li><a href="/beginner-guide">Beginner Guide</a></li><li><a href="/guides">Strategy Guides</a></li><li><a href="/builds">Build Guides</a></li><li><a href="/server-guide">Server Guide</a></li><li><a href="/faq">FAQ</a></li></ul></div>
<div class="footer-col"><h4>Database</h4><ul><li><a href="/crafting">Crafting</a></li><li><a href="/resources">Resources</a></li><li><a href="/bosses">Bosses</a></li><li><a href="/ships">Ships</a></li><li><a href="/weapons">Weapons</a></li></ul></div>
<div class="footer-col"><h4>Explore</h4><ul><li><a href="/tools">Tools</a></li><li><a href="/news">News</a></li><li><a href="/sources">Sources</a></li><li><a href="/about">About</a></li><li><a href="/contact">Contact</a></li></ul></div>
</div><div class="footer-bottom"><span>&copy; 2026 Windrose Guides. Not affiliated with Kraken Express.</span>
<nav><a href="/pages">All Pages</a><a href="/privacy">Privacy Policy</a><a href="/terms">Terms of Service</a></nav></div></div></footer>
<script>(function(){var b=document.querySelector('.hamburger'),n=document.querySelector('.nav-links');if(!b||!n)return;b.addEventListener('click',function(){var o=n.classList.toggle('open');b.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});})();</script>'''

def page_wrapper(title, desc, canonical, css_path, breadcrumbs, body, active="", jsonld=""):
    bc_html = "".join(f'<li><a href="{u}">{t}</a></li>' if u else f'<li>{t}</li>' for t,u in breadcrumbs)
    return f'''<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title><meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<link rel="canonical" href="{canonical}"><link rel="stylesheet" href="{css_path}">
<meta property="og:type" content="article"><meta property="og:url" content="{canonical}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="https://windrose-guides.com/imgs/og.webp">
<meta property="og:site_name" content="Windrose Guides">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}"><meta name="twitter:description" content="{desc}">
{jsonld}</head><body>
{header_html(active)}
<div class="container"><nav class="breadcrumb" aria-label="Breadcrumb"><ol>{bc_html}</ol></nav></div>
<main class="container">{body}</main>
{footer_html()}</body></html>'''


def write_page(rel_path, content):
    path = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ {rel_path}")


# === Guides Hub ===
GUIDES = [
    ("mining-routes", "⛏️", "Best Mining Routes & Resource Farming",
     "Optimized mining routes for Copper, Iron, Clay, Sulfur, and Gunpowder.", "Popular"),
    ("boss-progression", "💀", "Boss Progression & Strategy Guide",
     "Phase-by-phase breakdowns for every known boss encounter.", "Strategy"),
    ("best-early-builds", "🎯", "Best Early-Game Builds (2026)",
     "Optimal stat allocation and gear progression for your first 20 hours.", "Popular"),
    ("crafting-progression", "🔨", "Crafting Progression Path",
     "Most efficient crafting order from Day 1 to endgame.", "Deep Dive"),
    ("sailing-navigation", "🧭", "Sailing & Navigation Mastery",
     "Wind mechanics, navigation tips, cargo management.", "Deep Dive"),
    ("coop-multiplayer", "👥", "Co-op & Multiplayer Guide",
     "Server setup, role specialization, crew coordination.", "Multiplayer"),
    ("ship-building-naval-combat", "⚓", "Ship Building & Naval Combat",
     "Building, upgrading, and fighting with your ship.", "Strategy"),
]

def gen_guides_hub():
    cards = ""
    for slug, icon, title, desc, badge in GUIDES:
        cards += f'''<a href="/guides/{slug}/" class="card quick-nav-card">
<span class="nav-icon">{icon}</span><h3>{title}</h3>
<p>{desc}</p><span class="badge badge-legendary" style="margin-top:0.5rem;">{badge}</span></a>\n'''

    body = f'''<section class="hero"><h1>Windrose Strategy Guides — Deep-Dive Walkthroughs</h1>
<p class="tagline">Go beyond the basics. In-depth guides covering optimal routes, boss strategies, build planning, and advanced tactics.</p></section>
<section><h2>Featured Guides</h2><div class="quick-nav-grid">{cards}</div></section>
<section><h2>Why These Guides?</h2>
<p>While most Windrose databases focus on <strong>what</strong> items exist, our strategy guides explain <strong>how</strong> to use them effectively and <strong>why</strong> certain approaches work better. Each guide is written from hands-on gameplay and cross-referenced with community insights.</p>
<div class="update-note"><strong>Early Access Note:</strong> Windrose is in Early Access (v0.10.0.5.120). Guides are verified for current patch.</div></section>
<aside class="related-guides"><h2>Other Resources</h2><ul>
<li><a href="/beginner-guide/">Beginner Guide — Day 1-10</a></li>
<li><a href="/crafting/">Crafting Database</a></li>
<li><a href="/resources/">Resource Database</a></li>
<li><a href="/tools/">Tools & Calculators</a></li>
<li><a href="/faq/">FAQ (30+)</a></li></ul></aside>'''

    return page_wrapper(
        "Windrose Strategy Guides — Deep-Dive Walkthroughs (2026) | Windrose Guides",
        "In-depth Windrose strategy guides: mining routes, boss progression, best builds, crafting paths, sailing tips, co-op tactics, and naval combat.",
        "https://windrose-guides.com/guides", "../css/style.css",
        [("Home", "/"), ("Strategy Guides", None)], body, "/guides"
    )


if __name__ == "__main__":
    print("=== Phase 1: Generating Guides Hub ===")
    write_page("guides/index.html", gen_guides_hub())
    print("Done!")
