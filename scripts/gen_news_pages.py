"""
新闻页面生成脚本

从 data/news.json 读取新闻数据，生成：
  1. /news/index.html — 新闻列表 Hub 页
  2. /news/{slug}/index.html — 每条 has_detail_page=true 的新闻详情页

运行方式：
  python scripts/gen_news_pages.py

NOTE: 本脚本会覆盖 news/index.html 和 news/*/index.html，
      如果页面已进入人工精修阶段，请谨慎运行。
"""

import datetime
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
NEWS_DIR = ROOT / "news"
SITE = "https://windrose-guides.com"
TODAY = datetime.date.today().isoformat()

# NOTE: 分类标签的显示名映射
CATEGORY_LABELS = {
    "patch_notes": "Patch Notes",
    "milestone": "Milestone",
    "preview": "Preview",
    "community": "Community",
    "media": "Media",
}


def load_json(path: Path) -> dict:
    """读取 JSON 文件并返回解析后的字典"""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def escape(text: str) -> str:
    """HTML 实体转义"""
    return html.escape(text, quote=True)


def slugify(text: str) -> str:
    """
    将标题转为 URL-safe slug
    NOTE: 只保留字母数字和连字符，用于自动生成 slug
    """
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")[:80]


def format_date(date_str: str) -> str:
    """
    将日期字符串格式化为人类可读格式
    支持 YYYY-MM-DD 和 'Month YYYY' 等格式
    """
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%b %d, %Y")
    except ValueError:
        return date_str


# NOTE: 共享模板组件，保持所有页面 header/footer/nav 一致
HEADER_HTML = """<header class="header">
    <div class="container">
      <a href="/" class="logo" aria-label="Windrose Guides Home"><img src="/imgs/logo.png" alt="Windrose Guides Logo" width="32" height="32"> Windrose Guides</a>
      <button class="hamburger" aria-label="Toggle navigation menu" aria-expanded="false"><span></span><span></span><span></span></button>
      <nav aria-label="Primary"><ul class="nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="/beginner-guide">Beginner Guide</a></li>
                <li><a href="/database">Database</a></li>
                <li><a href="/bosses">Bosses</a></li>
                <li><a href="/ships">Ships</a></li>
                <li><a href="/guides">Guides</a></li>
                <li><a href="/tools">Tools</a></li>
                <li><a href="/news" class="active">News</a></li>
                <li><a href="/search">Search 🔍</a></li>
            </ul></nav>
    </div>
  </header>"""

FOOTER_HTML = """<footer class="footer">
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
  </footer>"""

HAMBURGER_JS = """<script>(function(){var b=document.querySelector('.hamburger'),n=document.querySelector('.nav-links');if(!b||!n)return;b.addEventListener('click',function(){var o=n.classList.toggle('open');b.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});})();</script>"""


def build_news_card(item: dict) -> str:
    """
    生成单条新闻的卡片 HTML
    有详情页的条目渲染为可点击链接，无详情页的渲染为静态卡片
    """
    title = escape(item.get("title", item.get("name", "")))
    summary = escape(item.get("summary", ""))
    date_str = format_date(item.get("date", ""))
    category = item.get("category", "")
    author = item.get("author", "")
    has_detail = item.get("has_detail_page", False)

    # NOTE: 从 slug 中提取详情页路径，移除 'news/' 前缀
    slug_path = item.get("slug", "")
    if slug_path.startswith("news/"):
        detail_path = "/" + slug_path
    else:
        detail_path = ""

    category_badge = ""
    if category and category in CATEGORY_LABELS:
        category_badge = f'<span class="news-category news-category-{category}">{CATEGORY_LABELS[category]}</span>'

    author_html = f'<span>By {escape(author)}</span>' if author else ""

    meta_html = f"""<div class="news-card-meta">
      <time datetime="{escape(item.get('date', ''))}">{date_str}</time>
      {category_badge}
      {author_html}
    </div>"""

    read_more = ""
    if has_detail and detail_path:
        read_more = f'<span class="news-card-read-more">Read Full Analysis →</span>'

    card_inner = f"""<div class="news-card-body">
      {meta_html}
      <h3 class="news-card-title">{title}</h3>
      <p class="news-card-summary">{summary}</p>
      {read_more}
    </div>"""

    if has_detail and detail_path:
        return f'<a href="{detail_path}" class="news-card" id="news-{escape(item["id"])}">\n  {card_inner}\n</a>'
    else:
        return f'<article class="news-card" id="news-{escape(item["id"])}">\n  {card_inner}\n</article>'


def generate_list_page(items: list[dict]) -> str:
    """生成 /news/index.html 列表 Hub 页"""
    # NOTE: 按日期倒序排列，最新的在前面
    sorted_items = sorted(
        items,
        key=lambda x: x.get("date", "0000-00-00"),
        reverse=True,
    )

    # 构建新闻卡片列表
    cards_html = "\n".join(build_news_card(item) for item in sorted_items)

    # NOTE: CollectionPage + ItemList 帮助 Google 理解列表结构
    detail_items = [item for item in sorted_items if item.get("has_detail_page")]
    item_list_elements = []
    for idx, item in enumerate(detail_items, 1):
        slug_path = item.get("slug", "")
        url = f"{SITE}/{slug_path}" if slug_path.startswith("news/") else f"{SITE}/news"
        item_list_elements.append({
            "@type": "ListItem",
            "position": idx,
            "url": url,
            "name": item.get("title", item.get("name", "")),
        })

    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{SITE}/#website",
                "url": f"{SITE}/",
                "name": "Windrose Guides",
                "publisher": {"@id": f"{SITE}/#org"},
                "inLanguage": "en",
            },
            {
                "@type": "Organization",
                "@id": f"{SITE}/#org",
                "name": "Windrose Guides",
                "url": f"{SITE}/",
            },
            {
                "@type": "CollectionPage",
                "@id": f"{SITE}/news#webpage",
                "url": f"{SITE}/news",
                "name": "Windrose News & Updates (2026)",
                "description": "Latest Windrose news, patch notes, milestones, and guide impact analysis. Stay up to date with every Early Access update.",
                "dateModified": TODAY,
                "isPartOf": {"@id": f"{SITE}/#website"},
                "breadcrumb": {"@id": f"{SITE}/news#breadcrumb"},
                "inLanguage": "en",
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{SITE}/news#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "News"},
                ],
            },
            {
                "@type": "ItemList",
                "numberOfItems": len(item_list_elements),
                "itemListElement": item_list_elements,
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "Where can I find official Windrose patch notes?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Official patch notes are published on the Windrose Steam Community page. We summarize each patch here with a guide impact analysis showing which gameplay areas were affected.",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "How often does Windrose get updated?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "During Early Access, Windrose receives patches every 1-2 weeks for bug fixes and stability. Major content updates (like the Ashlands biome) are expected every few months.",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "What is the next major Windrose update?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "The Ashlands biome is the next confirmed major update, expected at least 6 months after the April 2026 Early Access launch. It will include new environments, resources, and boss encounters.",
                        },
                    },
                ],
            },
        ],
    }
    json_ld_str = json.dumps(json_ld, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Windrose News &amp; Updates: Patch Notes, Milestones &amp; Guide Impact (2026)</title>
  <meta name="description" content="Latest Windrose news, patch notes, and update analysis. Every patch summarized with guide impact — know what changed and which strategies to update.">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{SITE}/news">
  <link rel="stylesheet" href="../css/style.css">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{SITE}/news">
  <meta property="og:title" content="Windrose News &amp; Updates: Patch Notes &amp; Guide Impact (2026)">
  <meta property="og:description" content="Latest Windrose news, patch notes, and update analysis. Every patch summarized with guide impact.">
  <meta property="og:image" content="{SITE}/imgs/og.webp">
  <meta property="og:site_name" content="Windrose Guides">
  <meta property="article:published_time" content="2026-05-12">
  <meta property="article:modified_time" content="{TODAY}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Windrose News &amp; Updates (2026)">
  <meta name="twitter:description" content="Latest Windrose news, patch notes, and update analysis with guide impact summaries.">
  <meta name="twitter:image" content="{SITE}/imgs/og.webp">
  <script type="application/ld+json">
  {json_ld_str}
  </script>
</head>
<body>
  {HEADER_HTML}
  <nav class="breadcrumb" aria-label="Breadcrumb"><div class="container"><ol><li><a href="/">Home</a></li>
<li><span aria-current="page">News</span></li></ol></div></nav>
  <main class="container">
    <h1>Windrose News &amp; Updates</h1>

<p>Stay up to date with every <strong>Windrose</strong> patch, milestone, and development update. Each news item includes our <strong>Guide Impact Analysis</strong> — a breakdown of what changed and which guides you should revisit. Windrose is in <strong>Early Access</strong> (launched April 14, 2026), so updates come frequently.</p>

<div class="quick-stats"><div class="stat"><div class="stat-label">Total Updates</div><div class="stat-value">{len(sorted_items)}</div></div><div class="stat"><div class="stat-label">Latest Update</div><div class="stat-value">{format_date(sorted_items[0]["date"]) if sorted_items else "N/A"}</div></div><div class="stat"><div class="stat-label">Game Version</div><div class="stat-value">v0.10.0.5.120</div></div><div class="stat"><div class="stat-label">Next Major</div><div class="stat-value">Ashlands (6mo+)</div></div></div>

<h2>All Updates</h2>

<div class="news-card-list">
{cards_html}
</div>

<section><h2>How We Cover Updates</h2>
<p>When Kraken Express releases a patch that changes crafting recipes, enemy balance, server configurations, or player progression, we don't just copy the patch notes. Instead, we analyze the <strong>practical impact</strong> on our guides:</p>
<ul>
<li><strong>Recipe changes</strong> — We update the <a href="/crafting">Crafting Database</a> and flag affected items</li>
<li><strong>Balance changes</strong> — Our <a href="/weapons">Weapon Tier Lists</a> and <a href="/builds">Build Guides</a> get re-evaluated</li>
<li><strong>Boss adjustments</strong> — Strategy pages under <a href="/bosses">Bosses</a> are revised with new tactics</li>
<li><strong>Server updates</strong> — The <a href="/server-guide">Dedicated Server Guide</a> is refreshed with new configuration steps</li>
</ul>
<p>This approach gives you actionable information rather than raw patch text, saving you time and helping you adapt your gameplay quickly.</p>
</section>

<section><h2>Official Sources</h2>
<ul>
<li><a href="https://store.steampowered.com/app/3041230/Windrose/" rel="nofollow">Windrose on Steam</a> — Official store page and community hub</li>
<li><a href="https://playwindrose.com/windrose-crew/dedicated-server-guide" rel="nofollow">Official Dedicated Server Guide</a> — Server setup documentation</li>
<li><a href="https://store.steampowered.com/news/app/3041230" rel="nofollow">Steam News Hub</a> — All official announcements and patch notes</li>
</ul>
</section>

<section id="faq"><h2>Frequently Asked Questions</h2>
<details><summary>Where can I find official Windrose patch notes?</summary><div class="faq-answer"><p>Official patch notes are published on the <a href="https://store.steampowered.com/news/app/3041230" rel="nofollow">Windrose Steam Community page</a>. We summarize each patch here with a guide impact analysis showing which gameplay areas were affected.</p></div></details>
<details><summary>How often does Windrose get updated?</summary><div class="faq-answer"><p>During Early Access, Windrose receives patches every 1-2 weeks for bug fixes and stability. Major content updates (like the Ashlands biome) are expected every few months.</p></div></details>
<details><summary>What is the next major Windrose update?</summary><div class="faq-answer"><p>The <strong>Ashlands biome</strong> is the next confirmed major update, expected at least 6 months after the April 2026 Early Access launch. It will include new environments, resources, and boss encounters.</p></div></details>
</section>
  </main>
  {FOOTER_HTML}
  {HAMBURGER_JS}
</body>
</html>
"""


def generate_detail_page(item: dict, prev_item: dict | None, next_item: dict | None) -> str:
    """
    生成单条新闻的详情页 HTML
    包含文章正文、来源引用、前后导航和 FAQ
    """
    title = escape(item.get("title", item.get("name", "")))
    content = item.get("content", "<p>Content coming soon.</p>")
    date_str = format_date(item.get("date", ""))
    date_iso = item.get("date", TODAY)
    category = item.get("category", "")
    author = escape(item.get("author", "Windrose Guides"))
    summary = escape(item.get("summary", ""))
    guide_impact = escape(item.get("guide_impact", ""))

    category_badge = ""
    if category and category in CATEGORY_LABELS:
        category_badge = f'<span class="news-category news-category-{category}">{CATEGORY_LABELS[category]}</span>'

    # 来源链接
    source_box = ""
    sources = item.get("sources", [])
    if sources:
        source_title = escape(sources[0].get("title", "Official Source"))
        source_url = sources[0].get("url", "")
        if source_url:
            source_box = f"""<div class="news-source-box">
  <strong>📰 Official Source:</strong> <a href="{escape(source_url)}" rel="nofollow" target="_blank">{source_title} →</a>
</div>"""

    # 关联页面内链
    related_pages = item.get("related_pages", [])
    related_html = ""
    if related_pages:
        # NOTE: 将路径映射为人类可读的页面名称
        page_names = {
            "/": "Home",
            "/beginner-guide": "Beginner Guide",
            "/crafting": "Crafting Recipes",
            "/crafting/building": "Building Materials",
            "/resources": "Resources",
            "/bosses": "Bosses",
            "/ships": "Ships",
            "/weapons": "Weapons",
            "/builds": "Build Guides",
            "/building": "Building Guide",
            "/server-guide": "Dedicated Server Guide",
            "/download": "Download Windrose",
            "/faq": "FAQ",
            "/tools": "Tools",
            "/news": "News",
        }
        related_links = "".join(
            f'<li><a href="{p}">{page_names.get(p, p.strip("/").replace("-", " ").title())}</a></li>'
            for p in related_pages
        )
        related_html = f"""<aside class="related-guides">
  <h2>Related Guides</h2>
  <ul>{related_links}</ul>
</aside>"""

    # 前后导航
    nav_html = '<div class="news-nav">'
    if prev_item:
        prev_slug = prev_item.get("slug", "")
        prev_title = escape(prev_item.get("title", prev_item.get("name", "")))
        prev_href = f"/{prev_slug}" if prev_slug.startswith("news/") else "/news"
        nav_html += f'<a href="{prev_href}" class="prev"><span class="nav-label">← Previous</span><span class="nav-title">{prev_title}</span></a>'
    if next_item:
        next_slug = next_item.get("slug", "")
        next_title = escape(next_item.get("title", next_item.get("name", "")))
        next_href = f"/{next_slug}" if next_slug.startswith("news/") else "/news"
        nav_html += f'<a href="{next_href}" class="next"><span class="nav-label">Next →</span><span class="nav-title">{next_title}</span></a>'
    nav_html += "</div>"

    # JSON-LD
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{SITE}/#website",
                "url": f"{SITE}/",
                "name": "Windrose Guides",
                "publisher": {"@id": f"{SITE}/#org"},
                "inLanguage": "en",
            },
            {
                "@type": "Organization",
                "@id": f"{SITE}/#org",
                "name": "Windrose Guides",
                "url": f"{SITE}/",
            },
            {
                "@type": "WebPage",
                "@id": f"{SITE}/{item['slug']}#webpage",
                "url": f"{SITE}/{item['slug']}",
                "name": item.get("title", item.get("name", "")),
                "description": item.get("summary", ""),
                "dateModified": date_iso,
                "isPartOf": {"@id": f"{SITE}/#website"},
                "breadcrumb": {"@id": f"{SITE}/{item['slug']}#breadcrumb"},
                "inLanguage": "en",
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{SITE}/{item['slug']}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "News", "item": f"{SITE}/news"},
                    {"@type": "ListItem", "position": 3, "name": item.get("title", item.get("name", ""))},
                ],
            },
            {
                "@type": "NewsArticle",
                "headline": item.get("title", item.get("name", "")),
                "datePublished": date_iso,
                "dateModified": date_iso,
                "author": {"@type": "Person", "name": item.get("author", "Windrose Guides")},
                "publisher": {"@id": f"{SITE}/#org"},
                "mainEntityOfPage": f"{SITE}/{item['slug']}",
                "description": item.get("summary", ""),
            },
        ],
    }
    json_ld_str = json.dumps(json_ld, ensure_ascii=False)

    # 从 slug 推算 CSS 相对路径
    slug = item.get("slug", "news/unknown")
    depth = slug.count("/") + 1
    css_rel = "../" * depth + "css/style.css"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Windrose Guides</title>
  <meta name="description" content="{summary}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{SITE}/{item['slug']}">
  <link rel="stylesheet" href="{css_rel}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{SITE}/{item['slug']}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{summary}">
  <meta property="og:image" content="{SITE}/imgs/og.webp">
  <meta property="og:site_name" content="Windrose Guides">
  <meta property="article:published_time" content="{date_iso}">
  <meta property="article:modified_time" content="{date_iso}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{summary}">
  <meta name="twitter:image" content="{SITE}/imgs/og.webp">
  <script type="application/ld+json">
  {json_ld_str}
  </script>
</head>
<body>
  {HEADER_HTML}
  <nav class="breadcrumb" aria-label="Breadcrumb"><div class="container"><ol><li><a href="/">Home</a></li>
<li><a href="/news">News</a></li>
<li><span aria-current="page">{title}</span></li></ol></div></nav>
  <main class="container">
    <div class="news-detail-header">
      <h1>{title}</h1>
      <div class="news-detail-meta">
        <time datetime="{date_iso}">{date_str}</time>
        <span class="separator">·</span>
        {category_badge}
        <span class="separator">·</span>
        <span>By {author}</span>
      </div>
    </div>

    <article class="news-detail-content">
      {content}
    </article>

    {source_box}

    {related_html}

    {nav_html}

    <p style="margin-top:2rem;"><a href="/news">← Back to All News</a></p>
  </main>
  {FOOTER_HTML}
  {HAMBURGER_JS}
</body>
</html>
"""


def main() -> None:
    news_data = load_json(DATA_DIR / "news.json")
    items = news_data.get("items", [])

    if not items:
        print("No news items found in data/news.json")
        return

    # 生成列表页
    list_html = generate_list_page(items)
    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    (NEWS_DIR / "index.html").write_text(list_html, encoding="utf-8")
    print(f"Generated news/index.html ({len(items)} items)")

    # 筛选有详情页的条目并按日期排序
    detail_items = [
        item for item in items
        if item.get("has_detail_page") and item.get("slug", "").startswith("news/")
    ]
    detail_items.sort(key=lambda x: x.get("date", "0000-00-00"), reverse=True)

    # 生成详情页
    for idx, item in enumerate(detail_items):
        prev_item = detail_items[idx - 1] if idx > 0 else None
        next_item = detail_items[idx + 1] if idx < len(detail_items) - 1 else None

        slug = item["slug"]
        # slug 格式为 "news/some-slug"，提取 "some-slug" 部分
        slug_name = slug.replace("news/", "", 1)
        detail_dir = NEWS_DIR / slug_name
        detail_dir.mkdir(parents=True, exist_ok=True)

        detail_html = generate_detail_page(item, prev_item, next_item)
        (detail_dir / "index.html").write_text(detail_html, encoding="utf-8")
        print(f"Generated {slug}/index.html")

    print(f"Done. {len(detail_items)} detail pages generated.")


if __name__ == "__main__":
    main()
