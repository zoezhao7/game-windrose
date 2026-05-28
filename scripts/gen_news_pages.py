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
SITE = "https://windrosewiki.games"
TODAY = datetime.date.today().isoformat()

from templates import header_html, footer_html, HAMBURGER_JS
from i18n import t, lang_url, hreflang_tags, LANG_HTML, DEFAULT, SUPPORTED

# NOTE: 分类标签的显示名映射（使用翻译 key）
CATEGORY_LABEL_KEYS = {
    "patch_notes": "news.category_patch_notes",
    "milestone": "news.category_milestone",
    "preview": "news.category_preview",
    "community": "news.category_community",
    "media": "news.category_media",
}

# 向后兼容：保留 CATEGORY_LABELS 为英文默认值
CATEGORY_LABELS = {
    "patch_notes": "Patch Notes",
    "milestone": "Milestone",
    "preview": "Preview",
    "community": "Community",
    "media": "Media",
}

# NOTE: 来源徽标 — 让读者一眼分辨是官方公告、外媒、SteamDB 还是社区帖
SOURCE_BADGES = {
    "steam_official": ("Steam Announcement", "source-steam-official"),
    "steam_media":    ("Press Coverage",     "source-steam-media"),
    "steamdb":        ("SteamDB Build",      "source-steamdb"),
    "steam_discussions": ("Community Thread", "source-steam-discussions"),
}


def source_badge_html(item: dict) -> str:
    src = item.get("source", "")
    if src not in SOURCE_BADGES:
        return ""
    label, css_cls = SOURCE_BADGES[src]
    return f'<span class="news-source-badge {css_cls}">{label}</span>'


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


# NOTE: HEADER_HTML, FOOTER_HTML, HAMBURGER_JS 已从 templates.py 导入，消除重复定义


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

    src_badge = source_badge_html(item)

    author_html = f'<span>By {escape(author)}</span>' if author else ""

    meta_html = f"""<div class="news-card-meta">
      <time datetime="{escape(item.get('date', ''))}">{date_str}</time>
      {category_badge}
      {src_badge}
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


def generate_list_page(items: list[dict], lang=DEFAULT) -> str:
    """生成 /news/index.html 列表 Hub 页，支持多语言。"""
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

    hlang = LANG_HTML.get(lang, lang)
    h = header_html("news", lang)
    f = footer_html(lang)

    # hreflang 替代链接
    hreflang_list = hreflang_tags("news", SITE)
    hreflang_html = "\n  ".join(hreflang_list)

    # 多语言路径
    if lang == DEFAULT:
        canonical = f"{SITE}/news"
        css_rel = "../css/style.css"
    else:
        canonical = f"{SITE}/{lang}/news"
        css_rel = "../../css/style.css"

    # 翻译的 UI 文本
    news_heading = t("news.heading", lang)
    news_intro = t("news.intro", lang)
    stat_total = t("news.stat_total", lang)
    stat_latest = t("news.stat_latest", lang)
    stat_version = t("news.stat_version", lang)
    stat_next = t("news.stat_next", lang)
    all_updates = t("news.all_updates", lang)
    faq_heading = t("common.faq_heading", lang)
    home_label = t("nav.home", lang)
    home_url = lang_url("/", lang)
    news_meta_title = t("news.meta_title", lang)
    news_meta_desc = t("news.meta_desc", lang)
    nav_news = t("nav.news", lang)
    how_we_cover_title = t("news.how_we_cover_title", lang)
    how_we_cover_p1 = t("news.how_we_cover_p1", lang)
    how_we_cover_p2 = t("news.how_we_cover_p2", lang)
    impact_recipes = t("news.impact_recipes", lang)
    impact_balance = t("news.impact_balance", lang)
    impact_bosses = t("news.impact_bosses", lang)
    impact_server = t("news.impact_server", lang)
    official_sources_title = t("news.official_sources_title", lang)
    source_steam = t("news.source_steam", lang)
    source_server = t("news.source_server", lang)
    source_news = t("news.source_news", lang)

    return f"""<!DOCTYPE html>
<html lang="{hlang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(news_meta_title)}</title>
  <meta name="description" content="{html.escape(news_meta_desc)}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{canonical}">
  {hreflang_html}
  <link rel="stylesheet" href="{css_rel}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <meta property="og:title" content="{html.escape(news_meta_title)}">
  <meta property="og:description" content="{html.escape(news_meta_desc)}">
  <meta property="og:image" content="{SITE}/imgs/og.webp">
  <meta property="og:site_name" content="Windrose Guides">
  <meta property="article:published_time" content="2026-05-12">
  <meta property="article:modified_time" content="{TODAY}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(news_meta_title)}">
  <meta name="twitter:description" content="{html.escape(news_meta_desc)}">
  <meta name="twitter:image" content="{SITE}/imgs/og.webp">
  <script type="application/ld+json">
  {json_ld_str}
  </script>
</head>
<body>
  {h}
  <nav class="breadcrumb" aria-label="Breadcrumb"><div class="container"><ol><li><a href="{home_url}">{html.escape(home_label)}</a></li>
<li><span aria-current="page">{html.escape(nav_news)}</span></li></ol></div></nav>
  <main class="container">
    <h1>{html.escape(news_heading)}</h1>

<p>{html.escape(news_intro)}</p>

<div class="quick-stats"><div class="stat"><div class="stat-label">{html.escape(stat_total)}</div><div class="stat-value">{len(sorted_items)}</div></div><div class="stat"><div class="stat-label">{html.escape(stat_latest)}</div><div class="stat-value">{format_date(sorted_items[0]["date"]) if sorted_items else "N/A"}</div></div><div class="stat"><div class="stat-label">{html.escape(stat_version)}</div><div class="stat-value">v0.10.0.5.120</div></div><div class="stat"><div class="stat-label">{html.escape(stat_next)}</div><div class="stat-value">Ashlands (6mo+)</div></div></div>

<h2>{html.escape(all_updates)}</h2>

<div class="news-card-list">
{cards_html}
</div>

<section><h2>{html.escape(how_we_cover_title)}</h2>
<p>{html.escape(how_we_cover_p1)}</p>
<ul>
<li>{impact_recipes.replace("Crafting Database", f'<a href="{lang_url("/crafting", lang)}">Crafting Database</a>')}</li>
<li>{impact_balance.replace("Weapon Tier Lists", f'<a href="{lang_url("/weapons", lang)}">Weapon Tier Lists</a>').replace("Build Guides", f'<a href="{lang_url("/builds", lang)}">Build Guides</a>')}</li>
<li>{impact_bosses.replace("Bosses", f'<a href="{lang_url("/bosses", lang)}">Bosses</a>')}</li>
<li>{impact_server.replace("Dedicated Server Guide", f'<a href="{lang_url("/server-guide", lang)}">Dedicated Server Guide</a>')}</li>
</ul>
<p>{html.escape(how_we_cover_p2)}</p>
</section>

<section><h2>{html.escape(official_sources_title)}</h2>
<ul>
<li><a href="https://store.steampowered.com/app/3041230/Windrose/" rel="nofollow">{html.escape(source_steam)}</a></li>
<li><a href="https://playwindrose.com/windrose-crew/dedicated-server-guide" rel="nofollow">{html.escape(source_server)}</a></li>
<li><a href="https://store.steampowered.com/news/app/3041230" rel="nofollow">{html.escape(source_news)}</a></li>
</ul>
</section>

<section id="faq"><h2>{html.escape(faq_heading)}</h2>
<details><summary>Where can I find official Windrose patch notes?</summary><div class="faq-answer"><p>Official patch notes are published on the <a href="https://store.steampowered.com/news/app/3041230" rel="nofollow">Windrose Steam Community page</a>. We summarize each patch here with a guide impact analysis showing which gameplay areas were affected.</p></div></details>
<details><summary>How often does Windrose get updated?</summary><div class="faq-answer"><p>During Early Access, Windrose receives patches every 1-2 weeks for bug fixes and stability. Major content updates (like the Ashlands biome) are expected every few months.</p></div></details>
<details><summary>What is the next major Windrose update?</summary><div class="faq-answer"><p>The <strong>Ashlands biome</strong> is the next confirmed major update, expected at least 6 months after the April 2026 Early Access launch. It will include new environments, resources, and boss encounters.</p></div></details>
</section>
  </main>
  {f}
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

    src_badge = source_badge_html(item)
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
  {header_html("news")}
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
        {f'<span class="separator">·</span>{src_badge}' if src_badge else ''}
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
  {footer_html()}
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

    # 生成列表页（所有语言）
    for lang in SUPPORTED:
        list_html = generate_list_page(items, lang)
        if lang == DEFAULT:
            list_dir = NEWS_DIR
        else:
            list_dir = ROOT / lang / "news"
        list_dir.mkdir(parents=True, exist_ok=True)
        (list_dir / "index.html").write_text(list_html, encoding="utf-8")
        print(f"Generated news/index.html ({len(items)} items) [lang={lang}]")

    # 筛选有详情页的条目并按日期排序
    detail_items = [
        item for item in items
        if item.get("has_detail_page") and item.get("slug", "").startswith("news/")
    ]
    detail_items.sort(key=lambda x: x.get("date", "0000-00-00"), reverse=True)

    # 生成详情页（仅英文 — 详情页数据量大，不做多语言）
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
