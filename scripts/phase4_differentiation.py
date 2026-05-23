"""
阶段4: 长期差异化
- 中文版本框架搭建 (zh/ 目录)
- AdSense 申请准备 (ads.txt + 广告位预留)
- 独家内容框架 (隐藏内容/彩蛋页)
- 内容新鲜度自动化 (最后更新时间戳)
"""
import os, json
from datetime import date

ROOT = r"F:\aicode\gamedoc"
TODAY = date.today().isoformat()

def write_file(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ {rel}")


# === 1. 中文版本框架 ===
def create_zh_framework():
    """创建中文版首页框架"""
    html = '''<!DOCTYPE html><html lang="zh-CN"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Windrose 攻略站 — 非官方中文Wiki、制作配方与Boss攻略 (2026)</title>
<meta name="description" content="Windrose 完整中文攻略：工作台制作配方、资源位置、Boss攻略、船只指南、新手教程。2026年更新。">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<link rel="canonical" href="https://windrosewiki.games/zh/">
<link rel="alternate" hreflang="en" href="https://windrosewiki.games/">
<link rel="alternate" hreflang="zh" href="https://windrosewiki.games/zh/">
<link rel="alternate" hreflang="x-default" href="https://windrosewiki.games/">
<link rel="stylesheet" href="../css/style.css">
<meta property="og:type" content="website">
<meta property="og:url" content="https://windrosewiki.games/zh/">
<meta property="og:title" content="Windrose 攻略站 — 非官方中文Wiki (2026)">
<meta property="og:description" content="Windrose 完整中文攻略数据库">
<meta property="og:image" content="https://windrosewiki.games/imgs/og.webp">
<meta property="og:locale" content="zh_CN">
</head><body>
<header class="header"><div class="container">
<a href="/zh/" class="logo"><img src="/imgs/logo.png" alt="Windrose 攻略 Logo" width="32" height="32"> Windrose 攻略</a>
<button class="hamburger" aria-label="切换导航" aria-expanded="false"><span></span><span></span><span></span></button>
<nav><ul class="nav-links">
<li><a href="/zh/" class="active">首页</a></li>
<li><a href="/zh/beginner-guide">新手指南</a></li>
<li><a href="/zh/crafting">制作配方</a></li>
<li><a href="/zh/resources">资源位置</a></li>
<li><a href="/zh/bosses">Boss攻略</a></li>
<li><a href="/zh/ships">船只指南</a></li>
<li><a href="/">English</a></li>
</ul></nav></div></header>

<main><div class="container">
<section class="hero">
<h1>Windrose 攻略站 — 非官方中文Wiki</h1>
<p class="tagline">你的 Windrose 最佳伙伴 — 制作配方、资源位置、Boss攻略、船只指南，一站搞定</p>
<div class="cta-buttons">
<a href="/zh/beginner-guide" class="btn btn-primary">新手指南</a>
<a href="/zh/crafting" class="btn btn-primary">制作配方</a>
</div>
</section>

<section>
<h2>快速导航</h2>
<div class="quick-nav-grid">
<a href="/zh/beginner-guide" class="card quick-nav-card"><span class="nav-icon">🧭</span><h3>新手指南</h3><p>Windrose 第一天到第十天完全攻略。生存基础、首艘船、早期优先事项。</p></a>
<a href="/zh/crafting" class="card quick-nav-card"><span class="nav-icon">🔨</span><h3>制作配方</h3><p>全部工作台1-3级配方，含材料需求和解锁条件。</p></a>
<a href="/zh/resources" class="card quick-nav-card"><span class="nav-icon">⛏️</span><h3>资源位置</h3><p>铜矿、铁矿、黏土、硫磺、火药等资源的获取位置和方法。</p></a>
<a href="/zh/bosses" class="card quick-nav-card"><span class="nav-icon">💀</span><h3>Boss攻略</h3><p>攻击模式、弱点分析、单人/组队攻略，逐阶段击破策略。</p></a>
<a href="/zh/ships" class="card quick-nav-card"><span class="nav-icon">⛵</span><h3>船只指南</h3><p>三种船只对比、变体详解、建造材料和海战定位。</p></a>
<a href="/guides/" class="card quick-nav-card"><span class="nav-icon">📖</span><h3>深度攻略 (English)</h3><p>采矿路线、Build推荐、航海技巧等深度攻略文章。</p></a>
</div>
</section>

<section>
<h2>游戏信息</h2>
<div class="game-info-grid">
<div class="info-item"><div class="info-value">Kraken Express</div><div class="info-label">开发商</div></div>
<div class="info-item"><div class="info-value">2026-04-14</div><div class="info-label">发售日期 (EA)</div></div>
<div class="info-item"><div class="info-value">海盗生存RPG</div><div class="info-label">类型</div></div>
<div class="info-item"><div class="info-value">Soulslite</div><div class="info-label">战斗系统</div></div>
<div class="info-item"><div class="info-value">1-10人</div><div class="info-label">多人协作</div></div>
<div class="info-item"><div class="info-value">50-70小时</div><div class="info-label">通关时长</div></div>
</div>
</section>

<div class="update-note">
<strong>翻译说明：</strong>中文版攻略站正在建设中。目前提供首页导航框架，详细攻略内容请先参考 <a href="/">英文版</a>。我们将持续翻译核心攻略页面。
</div>

</div></main>

<footer class="footer"><div class="container"><div class="footer-bottom">
<span>&copy; 2026 Windrose Guides. 非官方粉丝资源。与 Kraken Express 无关。</span>
<nav><a href="/">English</a><a href="/privacy">隐私政策</a><a href="/terms">服务条款</a></nav>
</div></div></footer>
<script>(function(){var b=document.querySelector('.hamburger'),n=document.querySelector('.nav-links');if(!b||!n)return;b.addEventListener('click',function(){var o=n.classList.toggle('open');b.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});})();</script>
</body></html>'''
    write_file("zh/index.html", html)


# === 2. AdSense 准备 ===
def prepare_adsense():
    """更新 ads.txt 和在 CSS 中添加广告位预留样式"""
    # ads.txt 已存在，确认内容
    ads_path = os.path.join(ROOT, "ads.txt")
    with open(ads_path, "r") as f:
        content = f.read()
    print(f"  ℹ️ ads.txt exists: {content.strip()}")

    # 添加广告位预留 CSS
    css_path = os.path.join(ROOT, "css", "style.css")
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()

    ad_css = """
/* --- AdSense 广告位预留 (CLS 防护) --- */
.ad-slot {
  min-height: 90px;
  background: rgba(255,255,255,0.02);
  border: 1px dashed var(--border);
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  font-size: 0.75rem;
  margin: 1.5rem 0;
}
.ad-slot-sidebar {
  min-height: 250px;
  background: rgba(255,255,255,0.02);
  border: 1px dashed var(--border);
  border-radius: var(--radius);
}
@media (max-width: 768px) {
  .ad-slot { min-height: 50px; }
}
"""
    if ".ad-slot" not in css:
        css += ad_css
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(css)
        print("  ✅ css/style.css — Added ad slot CSS")
    else:
        print("  ⏭️ css/style.css — Ad slots already defined")


# === 3. 独家内容页面 ===
def create_exclusive_content():
    """创建隐藏内容/彩蛋追踪页面"""
    html = '''<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Windrose Secrets & Easter Eggs — Hidden Content Tracker (2026) | Windrose Guides</title>
<meta name="description" content="Track hidden content, Easter eggs, and secrets in Windrose. Community-discovered hidden locations, items, and mechanics.">
<link rel="canonical" href="https://windrosewiki.games/guides/secrets">
<link rel="stylesheet" href="../../css/style.css">
</head><body>
<header class="header"><div class="container"><a href="/" class="logo"><img src="/imgs/logo.png" alt="Windrose Guides Logo" width="32" height="32"> Windrose Guides</a>
<button class="hamburger" aria-label="Toggle navigation" aria-expanded="false"><span></span><span></span><span></span></button>
<nav><ul class="nav-links"><li><a href="/">Home</a></li><li><a href="/beginner-guide">Beginner Guide</a></li><li><a href="/guides" class="active">Guides</a></li><li><a href="/crafting">Crafting</a></li><li><a href="/resources">Resources</a></li><li><a href="/bosses">Bosses</a></li><li><a href="/ships">Ships</a></li><li><a href="/weapons">Weapons</a></li><li><a href="/builds">Builds</a></li><li><a href="/faq">FAQ</a></li><li><a href="/news">News</a></li></ul></nav></div></header>
<div class="container"><nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li><a href="/guides/">Guides</a></li><li>Secrets & Easter Eggs</li></ol></nav></div>
<main class="container">
<h1>Windrose Secrets &amp; Easter Eggs — Hidden Content Tracker</h1>
<p>This page tracks community-discovered hidden content, Easter eggs, and secret mechanics in Windrose. All entries are <strong>player-verified or community-reported</strong> — nothing here comes from data mining.</p>

<div class="update-note"><strong>Contribute:</strong> Found a secret we haven't listed? Share it on our Discord or Reddit and we'll add it with credit!</div>

<section><h2>🗝️ Known Secrets</h2>
<div class="table-responsive"><table>
<thead><tr><th>Secret</th><th>Location</th><th>Details</th><th>Status</th></tr></thead>
<tbody>
<tr><td><strong>Smuggler's Treasure</strong></td><td>Starting Island, Coastal Jungle</td><td>Break wood pile → basement → chest with 10 Gunpowder + 4 Rum</td><td><span class="badge badge-uncommon">Verified</span></td></tr>
<tr><td><strong>Hidden Cave Music</strong></td><td>Deep cave systems</td><td>Some caves play unique ambient music when you reach the deepest chamber</td><td><span class="badge badge-rare">Community</span></td></tr>
<tr><td><strong>Pearl Ammunition</strong></td><td>Beach enemies</td><td>Right-click scallop shells → Pearls work as emergency ammo</td><td><span class="badge badge-uncommon">Verified</span></td></tr>
<tr><td><strong>Pirate History Lore</strong></td><td>Boss encounters</td><td>Each boss is inspired by a real historical pirate — check item descriptions for lore</td><td><span class="badge badge-rare">Community</span></td></tr>
<tr><td><strong>Sea Shanty Collection</strong></td><td>Various locations</td><td>Hidden sea shanties can be found as loot throughout the world</td><td><span class="badge badge-epic">Unconfirmed</span></td></tr>
</tbody></table></div></section>

<section><h2>🔍 Under Investigation</h2>
<ul>
<li><strong>Hidden underwater caves</strong> — Reports of explorable caves beneath the ocean surface (needs verification)</li>
<li><strong>Special NPC dialogue</strong> — Wearing specific armor sets may trigger unique NPC conversations</li>
<li><strong>Weather-dependent events</strong> — Certain events may only occur during storms or specific times of day</li>
<li><strong>Developer room</strong> — Unconfirmed reports of a hidden area with developer messages</li>
</ul>
</section>

<section><h2>🏆 Achievement Secrets</h2>
<p>Some Steam achievements hint at hidden content. Watch this space as the community uncovers them!</p>
</section>

<aside class="related-guides"><h2>Related</h2><ul>
<li><a href="/guides/">All Strategy Guides</a></li>
<li><a href="/guides/boss-progression/">Boss Progression & Lore</a></li>
<li><a href="/faq/">FAQ</a></li>
</ul></aside>
</main>
<footer class="footer"><div class="container"><div class="footer-bottom"><span>&copy; 2026 Windrose Guides.</span><nav><a href="/pages">All Pages</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a></nav></div></div></footer>
<script>(function(){var b=document.querySelector('.hamburger'),n=document.querySelector('.nav-links');if(!b||!n)return;b.addEventListener('click',function(){var o=n.classList.toggle('open');b.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});})();</script>
</body></html>'''
    write_file("guides/secrets/index.html", html)


# === 4. 更新 sitemap 和 hreflang ===
def update_sitemap_phase4():
    path = os.path.join(ROOT, "sitemap.xml")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_urls = [
        ("https://windrosewiki.games/zh/", "weekly", "0.7"),
        ("https://windrosewiki.games/guides/secrets", "monthly", "0.6"),
    ]
    entries = ""
    for url, freq, pri in new_urls:
        if url not in content:
            entries += f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority></url>\n'

    if entries:
        content = content.replace("</urlset>", entries + "</urlset>")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  ✅ sitemap.xml — Phase 4 URLs added")

    # 英文首页添加 hreflang
    index_path = os.path.join(ROOT, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        idx = f.read()
    if 'hreflang="zh"' not in idx:
        idx = idx.replace(
            '<link rel="canonical"',
            '<link rel="alternate" hreflang="en" href="https://windrosewiki.games/">\n    <link rel="alternate" hreflang="zh" href="https://windrosewiki.games/zh/">\n    <link rel="alternate" hreflang="x-default" href="https://windrosewiki.games/">\n    <link rel="canonical"'
        )
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(idx)
        print("  ✅ index.html — hreflang tags added")


# === 5. 更新 llms.txt ===
def update_llms_phase4():
    path = os.path.join(ROOT, "llms.txt")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "Chinese Version" not in content:
        addition = """
### [Chinese Version / 中文版](https://windrosewiki.games/zh/)
- [中文首页](https://windrosewiki.games/zh/): Windrose 非官方中文攻略站首页

### [Secrets & Easter Eggs](https://windrosewiki.games/guides/secrets)
- [Hidden Content Tracker](https://windrosewiki.games/guides/secrets): Community-discovered secrets, Easter eggs, and hidden mechanics
"""
        content = content.replace("## Contact", addition + "\n## Contact")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  ✅ llms.txt — Phase 4 sections added")


if __name__ == "__main__":
    print("=== Phase 4: Long-term Differentiation ===")
    create_zh_framework()
    prepare_adsense()
    create_exclusive_content()
    update_sitemap_phase4()
    update_llms_phase4()
    print("\nPhase 4 complete!")
