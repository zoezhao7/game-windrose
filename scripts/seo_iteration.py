from pathlib import Path
from datetime import date
import html

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://windrose-guides.com"
TODAY = "2026-05-12"

from templates import NAV_ITEMS as NAV, header_html, footer_html, HAMBURGER_JS
from i18n import t, lang_url, hreflang_tags, LANG_HTML, DEFAULT, SUPPORTED

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


def breadcrumbs(items, lang=DEFAULT):
    home_label = t("nav.home", lang)
    home_url = lang_url("", lang) if lang != DEFAULT else "/"
    lis = [f'<li><a href="{home_url}">{esc(home_label)}</a></li>']
    graph = [
        {"@type": "ListItem", "position": 1, "name": home_label, "item": f"{SITE}/"}
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


def faq(items, lang=DEFAULT):
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
    faq_heading = t("common.faq_heading", lang)
    html_bits = [f'<section id="faq"><h2>{esc(faq_heading)}</h2>']
    for q, a in items:
        html_bits.append(f'<details><summary>{esc(q)}</summary><div class="faq-answer"><p>{a}</p></div></details>')
    html_bits.append("</section>")
    return "\n".join(html_bits), schema


def page(slug, title, description, h1, body, crumb_items, priority="0.7", changefreq="weekly", schema_extra=None, lang=DEFAULT):
    slug = str(slug).replace("\\", "/")
    # 多语言路径：英文在根路径，其他语言加 /{lang}/ 前缀
    if lang == DEFAULT:
        canonical = f"{SITE}/" if slug == "" else f"{SITE}/{slug}"
        file_slug = slug
    else:
        file_slug = f"{lang}/{slug}" if slug else lang
        canonical = f"{SITE}/{file_slug}"
    crumb_html, crumb_graph = breadcrumbs(crumb_items, lang)
    hlang = LANG_HTML.get(lang, lang)

    # hreflang 替代链接
    hreflang_list = hreflang_tags(slug, SITE)
    hreflang_html = "\n  ".join(hreflang_list)

    graph = [
        {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Windrose Guides", "publisher": {"@id": f"{SITE}/#org"}, "inLanguage": hlang},
        {"@type": "Organization", "@id": f"{SITE}/#org", "name": "Windrose Guides", "url": f"{SITE}/"},
        {"@type": "WebPage", "@id": f"{canonical}#webpage", "url": canonical, "name": h1, "description": description, "dateModified": TODAY, "isPartOf": {"@id": f"{SITE}/#website"}, "breadcrumb": {"@id": f"{canonical}#breadcrumb"}, "inLanguage": hlang},
        {"@type": "BreadcrumbList", "@id": f"{canonical}#breadcrumb", "itemListElement": crumb_graph},
        {"@type": "Article", "headline": h1, "datePublished": TODAY, "dateModified": TODAY, "author": {"@type": "Organization", "name": "Windrose Guides"}},
    ]
    if schema_extra:
        graph.extend(schema_extra)

    header = header_html(slug, lang)
    footer = footer_html(lang)

    html_doc = f'''<!DOCTYPE html>
<html lang="{hlang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{canonical}">
  {hreflang_html}
  <link rel="stylesheet" href="{css_path(file_slug)}">
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
  {header}
  <nav class="breadcrumb" aria-label="Breadcrumb"><div class="container"><ol>{crumb_html}</ol></div></nav>
  <main class="container">
    <h1>{esc(h1)}</h1>
    {body}
  </main>
  {footer}
  {HAMBURGER_JS}
</body>
</html>
'''
    out = ROOT / ("index.html" if file_slug == "" else Path(file_slug) / "index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_doc, encoding="utf-8")
    PAGES.append((file_slug, priority, changefreq, title, description))


def simple_cards(cards):
    return '<div class="quick-nav-grid">' + "".join(
        f'<a class="card quick-nav-card" href="{href}"><span class="nav-icon">{icon}</span><h3>{esc(title)}</h3><p>{esc(desc)}</p></a>'
        for icon, title, desc, href in cards
    ) + "</div>"


def build_pages(lang=DEFAULT):
    data_note_text = t("common.data_note", lang)
    faq_heading = t("common.faq_heading", lang)
    source_note = f'<p class="update-note"><strong>{esc(faq_heading.split()[0] if lang == "en" else "Note")}:</strong> {esc(data_note_text)}</p>'

    # URL placeholders shared across pages
    workbench_url = lang_url("/crafting/workbench", lang)
    smelting_url = lang_url("/crafting/smelting", lang)
    brigantine_url = lang_url("/ships/brigantine", lang)
    frigate_url = lang_url("/ships/frigate", lang)
    server_guide_url = lang_url("/server-guide", lang)

    def _faq_from_locale(faq_key, **subs):
        items = t(faq_key, lang) or []
        result = []
        for item in items:
            if not isinstance(item, dict):
                continue
            q = item.get("q", "")
            a = item.get("a_html", item.get("a", ""))
            if subs and "{" in a:
                try:
                    a = a.format(**subs)
                except (KeyError, IndexError):
                    pass
            result.append((q, a))
        return result

    # === Tools hub ===
    body = f"""
{stats([(t("tools.best_for", lang), t("tools.fast_planning", lang)), (t("nav.tools", lang), t("tools.tools_count", lang)), ("JavaScript", t("tools.js_none", lang))])}
<p>{t("body.tools_hub.intro_html", lang)}</p>
{simple_cards([
    ("#", t("tools.card_recipe_title", lang), t("tools.card_recipe_desc", lang), lang_url("/tools/recipe-finder", lang)),
    ("#", t("tools.card_progression_title", lang), t("tools.card_progression_desc", lang), lang_url("/tools/progression-checklist", lang)),
    ("#", t("tools.card_resource_title", lang), t("tools.card_resource_desc", lang), lang_url("/tools/resource-planner", lang)),
    ("#", t("tools.card_ship_title", lang), t("tools.card_ship_desc", lang), lang_url("/tools/ship-selector", lang)),
    ("#", t("tools.card_server_title", lang), t("tools.card_server_desc", lang), lang_url("/server-guide", lang)),
])}
<section><h2>{esc(t("tools.launch_priority_title", lang))}</h2><p>{esc(t("tools.launch_priority_desc", lang))}</p></section>
"""
    fh, fs = faq(_faq_from_locale("body.tools_hub.faqs"), lang)
    page(Path("tools"), t("tools.hub_meta_title", lang), t("tools.hub_meta_desc", lang), t("tools.hub_title", lang), body + fh, [(t("nav.tools", lang), None)], "0.8", schema_extra=[fs], lang=lang)

    # === Recipe finder ===
    recipe_rows = t("body.recipe_finder.table_rows", lang) or []
    body = f"""
{stats([(t("body.recipe_finder.stat_coverage", lang), t("body.recipe_finder.stat_coverage_value", lang)), (t("body.recipe_finder.stat_best_query", lang), t("body.recipe_finder.stat_best_query_value", lang)), (t("body.recipe_finder.stat_updated", lang), TODAY)])}
<p>{esc(t("tools.recipe_intro", lang))}</p>
{table([t("tools.recipe_table_item", lang), t("tools.recipe_table_station", lang), t("tools.recipe_table_materials", lang), t("tools.recipe_table_use", lang)], recipe_rows, t("tools.recipe_table_caption", lang))}
<section><h2>{esc(t("tools.recipe_how_title", lang))}</h2><ol><li>{esc(t("body.recipe_finder.how_step_1", lang))}</li><li>{esc(t("body.recipe_finder.how_step_2", lang))}</li><li>{t("body.recipe_finder.how_step_3_html", lang, workbench_url=workbench_url)}</li></ol></section>
{source_note}
"""
    fh, fs = faq(_faq_from_locale("body.recipe_finder.faqs", workbench_url=workbench_url, smelting_url=smelting_url), lang)
    page(Path("tools/recipe-finder"), t("tools.recipe_meta_title", lang), t("tools.recipe_meta_desc", lang), t("tools.recipe_heading", lang), body + fh, [(t("nav.tools", lang), lang_url("/tools", lang)), ("Recipe Finder", None)], "0.8", schema_extra=[fs], lang=lang)

    # === Progression checklist ===
    checklist_rows = t("body.progression.table_rows", lang) or []
    body = f"""
{stats([(t("body.progression.stat_route", lang), t("body.progression.stat_route_value", lang)), (t("body.progression.stat_focus", lang), t("body.progression.stat_focus_value", lang)), (t("body.progression.stat_format", lang), t("body.progression.stat_format_value", lang))])}
<p>{esc(t("body.progression.intro", lang))}</p>
{table(t("body.progression.table_headers", lang), checklist_rows, t("body.progression.table_caption", lang))}
<section><h2>{esc(t("body.progression.short_answer_title", lang))}</h2><p>{t("body.progression.short_answer_html", lang)}</p></section>
"""
    fh, fs = faq(_faq_from_locale("body.progression.faqs"), lang)
    page(Path("tools/progression-checklist"), t("tools.recipe_progression_meta_title", lang), t("tools.recipe_progression_meta_desc", lang), t("tools.recipe_progression_heading", lang), body + fh, [(t("nav.tools", lang), lang_url("/tools", lang)), ("Progression Checklist", None)], "0.8", schema_extra=[fs], lang=lang)

    # === Resource planner ===
    resource_rows = t("body.resource.table_rows", lang) or []
    body = f"""
{stats([(t("body.resource.stat_resources", lang), t("body.resource.stat_resources_value", lang)), (t("body.resource.stat_best_use", lang), t("body.resource.stat_best_use_value", lang)), (t("body.resource.stat_related", lang), t("body.resource.stat_related_value", lang))])}
<p>{esc(t("body.resource.intro", lang))}</p>
{table(t("body.resource.table_headers", lang), resource_rows, t("body.resource.table_caption", lang))}
<section><h2>{esc(t("body.resource.farming_order_title", lang))}</h2><p>{esc(t("body.resource.farming_order_p", lang))}</p></section>
"""
    fh, fs = faq(_faq_from_locale("body.resource.faqs"), lang)
    page(Path("tools/resource-planner"), t("tools.resource_meta_title", lang), t("tools.resource_meta_desc", lang), t("tools.resource_heading", lang), body + fh, [(t("nav.tools", lang), lang_url("/tools", lang)), ("Resource Planner", None)], "0.8", schema_extra=[fs], lang=lang)

    # === Ship selector ===
    ship_rows = t("body.ship_selector.table_rows", lang) or []
    body = f"""
{stats([(t("body.ship_selector.stat_ships", lang), "3"), (t("body.ship_selector.stat_best_overall", lang), "Brigantine"), (t("body.ship_selector.stat_solo_pick", lang), "Sloop")])}
<p>{esc(t("body.ship_selector.intro", lang))}</p>
{table(t("body.ship_selector.table_headers", lang), ship_rows, t("body.ship_selector.table_caption", lang))}
<section><h2>{esc(t("body.ship_selector.quick_rec_title", lang))}</h2><p>{t("body.ship_selector.quick_rec_html", lang, brigantine_url=brigantine_url, frigate_url=frigate_url)}</p></section>
"""
    fh, fs = faq(_faq_from_locale("body.ship_selector.faqs"), lang)
    page(Path("tools/ship-selector"), t("tools.ship_meta_title", lang), t("tools.ship_meta_desc", lang), t("tools.ship_heading", lang), body + fh, [(t("nav.tools", lang), lang_url("/tools", lang)), ("Ship Selector", None)], "0.8", schema_extra=[fs], lang=lang)

    # === Server guide ===
    server_rows = t("body.server_guide.table_rows", lang) or []
    setup_steps = t("body.server_guide.basic_setup_steps", lang) or []
    setup_steps_html = "".join(f"<li>{step}</li>" for step in setup_steps)
    body = f"""
{stats([(t("body.server_guide.stat_intent", lang), t("body.server_guide.stat_intent_value", lang)), (t("body.server_guide.stat_source_type", lang), t("body.server_guide.stat_source_type_value", lang)), (t("body.server_guide.stat_best_for", lang), t("body.server_guide.stat_best_for_value", lang))])}
<p>{esc(t("body.server_guide.intro", lang))}</p>
{table(t("body.server_guide.table_headers", lang), server_rows, t("body.server_guide.table_caption", lang))}
<section><h2>{esc(t("body.server_guide.steamcmd_title", lang))}</h2><pre><code>force_install_dir "C:\\Game_Servers\\Windrose_Server"
login anonymous
app_update 4129620 validate
quit</code></pre><p>{t("body.server_guide.steamcmd_after_html", lang)}</p></section>
<section><h2>{esc(t("body.server_guide.basic_setup_title", lang))}</h2><ol>{setup_steps_html}</ol></section>
<section><h2>{esc(t("body.server_guide.official_source_title", lang))}</h2><p>{t("body.server_guide.official_source_html", lang)}</p></section>
"""
    fh, fs = faq(_faq_from_locale("body.server_guide.faqs"), lang)
    page(Path("server-guide"), t("server_guide.meta_title", lang), t("server_guide.meta_desc", lang), t("server_guide.heading", lang), body + fh, [(t("server_guide.heading", lang), None)], "0.75", schema_extra=[fs], lang=lang)

    # === Download / system requirements style page ===
    download_rows = t("body.download.table_rows", lang) or []
    body = f"""
{stats([(t("body.download.stat_platform", lang), t("body.download.stat_platform_value", lang)), (t("body.download.stat_mode", lang), t("body.download.stat_mode_value", lang)), (t("body.download.stat_status", lang), t("body.download.stat_status_value", lang))])}
<p>{t("body.download.intro_html", lang)}</p>
{table(t("body.download.table_headers", lang), download_rows, t("body.download.table_caption", lang))}
<section><h2>{esc(t("body.download.ea_title", lang))}</h2><p>{esc(t("body.download.ea_p", lang))}</p></section>
<section><h2>{esc(t("body.download.before_title", lang))}</h2><p>{esc(t("body.download.before_p", lang))}</p></section>
"""
    fh, fs = faq(_faq_from_locale("body.download.faqs"), lang)
    page(Path("download"), t("download.meta_title", lang), t("download.meta_desc", lang), t("download.heading", lang), body + fh, [(t("download.heading", lang), None)], "0.65", schema_extra=[fs], lang=lang)

    # NOTE: crafting/alchemy、crafting/cooking、crafting/building 已改为手动维护 HTML。
    # NOTE: bosses 页面已改为手动维护 HTML。

    # === News page ===
    news_body = f"""
{stats([("Best Source", "Steam News"), ("Update Cadence", "After patches"), ("SEO Role", "Freshness")])}
<p>The news page should summarize official patch notes and point players back to affected guides. This gives Google freshness signals while keeping recipe and resource pages stable.</p>
{table(["Date", "Source", "Update", "Guide Impact"], [
    ["May 2026", "Steam / official updates", "Cloud save, dedicated server, and stability-related notices were active topics after launch.", "Server guide and troubleshooting should stay current."],
    ["April 2026", "Steam launch", "Windrose entered Early Access on Steam.", "All guides should be labeled Early Access and updated after patches."],
    ["Ongoing", "Official website and Steam news", "Dedicated server documentation and patch notes may change.", "Update /server-guide and FAQ first."],
], "Windrose news and update tracker")}
<section><h2>How We Use Patch Notes</h2><p>When a patch changes crafting, enemy balance, servers, or progression, update the affected guide first, then refresh the sitemap lastmod and this news index. Avoid copying full patch notes; summarize the practical impact for players.</p></section>
<section><h2>Official Links</h2><ul><li><a href="https://store.steampowered.com/app/3041230/Windrose/" rel="nofollow">Windrose on Steam</a></li><li><a href="https://playwindrose.com/windrose-crew/dedicated-server-guide" rel="nofollow">Official Dedicated Server Guide</a></li></ul></section>
"""
    fh, fs = faq([
        ("Where should I check official Windrose updates?", "Use the Steam page and official Windrose website first, then this page for guide impact summaries."),
        ("Why not mirror full patch notes?", "Summaries are better for SEO and user value, and they avoid duplicating official content."),
    ], lang)
    page(Path("news"), t("news.meta_title", lang), t("news.meta_desc", lang), t("news.heading", lang), news_body + fh, [(t("nav.news", lang), None)], "0.65", changefreq="daily", schema_extra=[fs], lang=lang)

    # === Sources page ===
    source_rows = t("body.sources.table_rows", lang) or []
    source_body = f"""
{stats([(t("body.sources.stat_purpose", lang), t("body.sources.stat_purpose_value", lang)), (t("body.sources.stat_status", lang), t("body.sources.stat_status_value", lang)), (t("body.sources.stat_use", lang), t("body.sources.stat_use_value", lang))])}
<p>{esc(t("body.sources.intro", lang))}</p>
{table(t("body.sources.table_headers", lang), source_rows, t("body.sources.table_caption", lang))}
"""
    page(Path("sources"), t("sources.meta_title", lang), t("sources.meta_desc", lang), t("sources.heading", lang), source_body, [(t("sources.heading", lang), None)], "0.45", "monthly", lang=lang)

    # === Guides: Mining ===
    mining_body = f"""
{stats([(t("body.guides.mining.stat_difficulty", lang), t("body.guides.mining.stat_difficulty_value", lang)), (t("body.guides.mining.stat_required_tool", lang), "Copper Pickaxe"), (t("body.guides.mining.stat_best_yield", lang), t("body.guides.mining.stat_best_yield_value", lang))])}
<p>{esc(t("body.guides.mining.intro", lang))}</p>
<section><h2>{esc(t("body.guides.mining.s1_title", lang))}</h2><p>{t("body.guides.mining.s1_html", lang)}</p></section>
<section><h2>{esc(t("body.guides.mining.s2_title", lang))}</h2><p>{t("body.guides.mining.s2_html", lang)}</p></section>
<section><h2>{esc(t("body.guides.mining.s3_title", lang))}</h2><p>{t("body.guides.mining.s3_html", lang)}</p></section>
"""
    fh, fs = faq(_faq_from_locale("body.guides.mining.faqs"), lang)
    page(Path("guides/mining-routes"), t("guides.mining_meta_title", lang), t("guides.mining_meta_desc", lang), t("guides.mining_heading", lang), mining_body + fh, [(t("nav.guides", lang), lang_url("/guides", lang)), ("Mining Routes", None)], "0.85", schema_extra=[fs], lang=lang)

    # === Guides: Boss progression ===
    boss_progression_body = f"""
{stats([(t("body.guides.boss_progression.stat_total", lang), t("body.guides.boss_progression.stat_total_value", lang)), (t("body.guides.boss_progression.stat_preparation", lang), t("body.guides.boss_progression.stat_preparation_value", lang)), (t("body.guides.boss_progression.stat_required_gear", lang), t("body.guides.boss_progression.stat_required_gear_value", lang))])}
<p>{esc(t("body.guides.boss_progression.intro", lang))}</p>
<section><h2>{esc(t("body.guides.boss_progression.s1_title", lang))}</h2><p>{t("body.guides.boss_progression.s1_html", lang)}</p></section>
<section><h2>{esc(t("body.guides.boss_progression.s2_title", lang))}</h2><p>{t("body.guides.boss_progression.s2_html", lang)}</p></section>
<section><h2>{esc(t("body.guides.boss_progression.s3_title", lang))}</h2><p>{t("body.guides.boss_progression.s3_html", lang)}</p></section>
"""
    fh, fs = faq(_faq_from_locale("body.guides.boss_progression.faqs"), lang)
    page(Path("guides/boss-progression"), t("guides.boss_prog_meta_title", lang), t("guides.boss_prog_meta_desc", lang), t("guides.boss_prog_heading", lang), boss_progression_body + fh, [(t("nav.guides", lang), lang_url("/guides", lang)), ("Boss Progression", None)], "0.85", schema_extra=[fs], lang=lang)

    # === Guides: Builds ===
    builds_body = f"""
{stats([(t("body.guides.builds.stat_playstyles", lang), t("body.guides.builds.stat_playstyles_value", lang)), (t("body.guides.builds.stat_respec", lang), t("body.guides.builds.stat_respec_value", lang)), (t("body.guides.builds.stat_meta", lang), t("body.guides.builds.stat_meta_value", lang))])}
<p>{esc(t("body.guides.builds.intro", lang))}</p>
<section><h2>{esc(t("body.guides.builds.s1_title", lang))}</h2><p>{t("body.guides.builds.s1_html", lang)}</p></section>
<section><h2>{esc(t("body.guides.builds.s2_title", lang))}</h2><p>{t("body.guides.builds.s2_html", lang)}</p></section>
<section><h2>{esc(t("body.guides.builds.s3_title", lang))}</h2><p>{t("body.guides.builds.s3_html", lang)}</p></section>
"""
    fh, fs = faq(_faq_from_locale("body.guides.builds.faqs"), lang)
    page(Path("guides/best-early-builds"), t("guides.builds_meta_title", lang), t("guides.builds_meta_desc", lang), t("guides.builds_heading", lang), builds_body + fh, [(t("nav.guides", lang), lang_url("/guides", lang)), ("Early Builds", None)], "0.85", schema_extra=[fs], lang=lang)

    # === Guides: Ship Building & Naval Combat ===
    ship_guide_body = f"""
{stats([(t("body.guides.ship_building.stat_ships", lang), t("body.guides.ship_building.stat_ships_value", lang)), (t("body.guides.ship_building.stat_cannons", lang), t("body.guides.ship_building.stat_cannons_value", lang)), (t("body.guides.ship_building.stat_boarding", lang), t("body.guides.ship_building.stat_boarding_value", lang))])}
<p>{esc(t("body.guides.ship_building.intro", lang))}</p>
<section><h2>{esc(t("body.guides.ship_building.s1_title", lang))}</h2><p>{t("body.guides.ship_building.s1_html", lang)}</p></section>
<section><h2>{esc(t("body.guides.ship_building.s2_title", lang))}</h2><p>{t("body.guides.ship_building.s2_html", lang)}</p></section>
<section><h2>{esc(t("body.guides.ship_building.s3_title", lang))}</h2>{t("body.guides.ship_building.s3_html", lang)}</section>
<section><h2>{esc(t("body.guides.ship_building.s4_title", lang))}</h2><p>{t("body.guides.ship_building.s4_html", lang)}</p></section>
"""
    fh, fs = faq(_faq_from_locale("body.guides.ship_building.faqs"), lang)
    page(Path("guides/ship-building-naval-combat"), t("guides.ship_guide_meta_title", lang), t("guides.ship_guide_meta_desc", lang), t("guides.ship_guide_heading", lang), ship_guide_body + fh, [(t("nav.guides", lang), lang_url("/guides", lang)), ("Naval Combat", None)], "0.85", schema_extra=[fs], lang=lang)

    # === Guides: Sailing & Navigation ===
    sailing_body = f"""
{stats([(t("body.guides.sailing.stat_map_size", lang), t("body.guides.sailing.stat_map_size_value", lang)), (t("body.guides.sailing.stat_fast_travel", lang), t("body.guides.sailing.stat_fast_travel_value", lang)), (t("body.guides.sailing.stat_navigation", lang), t("body.guides.sailing.stat_navigation_value", lang))])}
<p>{esc(t("body.guides.sailing.intro", lang))}</p>
<section><h2>{esc(t("body.guides.sailing.s1_title", lang))}</h2><p>{t("body.guides.sailing.s1_html", lang)}</p></section>
<section><h2>{esc(t("body.guides.sailing.s2_title", lang))}</h2><p>{t("body.guides.sailing.s2_html", lang)}</p></section>
<section><h2>{esc(t("body.guides.sailing.s3_title", lang))}</h2><p>{t("body.guides.sailing.s3_html", lang)}</p></section>
<section><h2>{esc(t("body.guides.sailing.s4_title", lang))}</h2>{t("body.guides.sailing.s4_html", lang)}</section>
"""
    fh, fs = faq(_faq_from_locale("body.guides.sailing.faqs"), lang)
    page(Path("guides/sailing-navigation"), t("guides.sailing_meta_title", lang), t("guides.sailing_meta_desc", lang), t("guides.sailing_heading", lang), sailing_body + fh, [(t("nav.guides", lang), lang_url("/guides", lang)), ("Sailing", None)], "0.85", schema_extra=[fs], lang=lang)

    # === Guides: Crafting Progression ===
    cprog_rows = t("body.guides.crafting_progression.table_rows", lang) or []
    craft_prog_body = f"""
{stats([(t("body.guides.crafting_progression.stat_stations", lang), t("body.guides.crafting_progression.stat_stations_value", lang)), (t("body.guides.crafting_progression.stat_tiers", lang), t("body.guides.crafting_progression.stat_tiers_value", lang)), (t("body.guides.crafting_progression.stat_key_gate", lang), t("body.guides.crafting_progression.stat_key_gate_value", lang))])}
<p>{esc(t("body.guides.crafting_progression.intro", lang))}</p>
<section><h2>{esc(t("body.guides.crafting_progression.s1_title", lang))}</h2><p>{t("body.guides.crafting_progression.s1_html", lang)}</p></section>
<section><h2>{esc(t("body.guides.crafting_progression.s2_title", lang))}</h2>
{table(t("body.guides.crafting_progression.table_headers", lang), cprog_rows, t("body.guides.crafting_progression.table_caption", lang))}
</section>
<section><h2>{esc(t("body.guides.crafting_progression.s3_title", lang))}</h2>{t("body.guides.crafting_progression.s3_html", lang)}</section>
"""
    fh, fs = faq(_faq_from_locale("body.guides.crafting_progression.faqs"), lang)
    page(Path("guides/crafting-progression"), t("guides.crafting_prog_meta_title", lang), t("guides.crafting_prog_meta_desc", lang), t("guides.crafting_prog_heading", lang), craft_prog_body + fh, [(t("nav.guides", lang), lang_url("/guides", lang)), ("Crafting Progression", None)], "0.85", schema_extra=[fs], lang=lang)

    # === Guides: Co-op & Multiplayer ===
    coop_body = f"""
{stats([(t("body.guides.coop.stat_max_players", lang), t("body.guides.coop.stat_max_players_value", lang)), (t("body.guides.coop.stat_recommended", lang), t("body.guides.coop.stat_recommended_value", lang)), (t("body.guides.coop.stat_server_types", lang), t("body.guides.coop.stat_server_types_value", lang))])}
<p>{esc(t("body.guides.coop.intro", lang))}</p>
<section><h2>{esc(t("body.guides.coop.s1_title", lang))}</h2><p>{t("body.guides.coop.s1_html", lang)}</p></section>
<section><h2>{esc(t("body.guides.coop.s2_title", lang))}</h2>{t("body.guides.coop.s2_html", lang)}</section>
<section><h2>{esc(t("body.guides.coop.s3_title", lang))}</h2><p>{t("body.guides.coop.s3_html", lang)}</p></section>
<section><h2>{esc(t("body.guides.coop.s4_title", lang))}</h2><p>{t("body.guides.coop.s4_html", lang, server_guide_url=server_guide_url)}</p></section>
"""
    fh, fs = faq(_faq_from_locale("body.guides.coop.faqs"), lang)
    page(Path("guides/coop-multiplayer"), t("guides.coop_meta_title", lang), t("guides.coop_meta_desc", lang), t("guides.coop_heading", lang), coop_body + fh, [(t("nav.guides", lang), lang_url("/guides", lang)), ("Co-op Guide", None)], "0.85", schema_extra=[fs], lang=lang)

    # === Search page ===
    search_intro = t("body.search.intro", lang)
    search_placeholder = t("body.search.placeholder", lang)
    search_no_results = t("body.search.no_results", lang)
    search_body = f"""
<p>{esc(search_intro)}</p>
<div class="search-container" style="margin: 2rem 0;">
    <input type="text" id="searchInput" placeholder="{esc(search_placeholder)}" style="width: 100%; padding: 1rem; font-size: 1.1rem; border-radius: 8px; border: 1px solid var(--border); background: var(--bg-surface); color: var(--text); outline: none; transition: border-color 0.2s;">
    <div id="searchResults" style="margin-top: 1.5rem; display: flex; flex-direction: column; gap: 1rem;"></div>
</div>
<script>
    document.addEventListener('DOMContentLoaded', () => {{
        const input = document.getElementById('searchInput');
        const results = document.getElementById('searchResults');
        let searchData = [];

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
                results.innerHTML = '<p style="color: var(--text-muted);">{esc(search_no_results)}</p>';
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
"""
    page(Path("search"), t("search.meta_title", lang), t("search.meta_desc", lang), t("search.heading", lang), search_body, [(t("nav.search", lang), None)], "0.9", lang=lang)

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
        # 检测是否为多语言页面（/{lang}/... 前缀）
        lang_prefix = None
        base_slug = slug
        for lang_code in SUPPORTED:
            prefix = lang_code
            if slug == prefix:
                lang_prefix = lang_code
                base_slug = ""
                break
            elif slug.startswith(prefix + "/"):
                lang_prefix = lang_code
                base_slug = slug[len(prefix) + 1:]
                break
        priority = "0.6"
        if base_slug == "":
            priority = "1.0" if lang_prefix is None else "0.8"
        elif base_slug in {"beginner-guide", "crafting/workbench", "resources/copper", "tools", "tools/recipe-finder", "tools/progression-checklist"}:
            priority = "0.9"
        elif base_slug.split("/")[0] in {"crafting", "resources", "bosses", "ships", "weapons", "builds", "server-guide"}:
            priority = "0.8"
        changefreq = "daily" if base_slug == "news" else "weekly"
        existing.append((slug, priority, changefreq, base_slug, lang_prefix))
    existing.sort(key=lambda x: (x[0].count("/"), x[0]))

    # 构建 hreflang 映射：base_slug → {lang_code: full_slug}
    lang_variants = {}
    for slug, _, _, base_slug, lang_prefix in existing:
        lang_code = lang_prefix or DEFAULT
        lang_variants.setdefault(base_slug, {})[lang_code] = slug

    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for slug, priority, changefreq, base_slug, lang_prefix in existing:
        loc = f"{SITE}/" if slug == "" else f"{SITE}/{slug}"
        # hreflang 替代链接
        hreflang_links = ""
        variants = lang_variants.get(base_slug, {})
        if len(variants) > 1:
            link_parts = []
            for lc in SUPPORTED:
                if lc in variants:
                    vs = variants[lc]
                    href = f"{SITE}/" if vs == "" else f"{SITE}/{vs}"
                    link_parts.append(f'\n    <xhtml:link rel="alternate" hreflang="{LANG_HTML[lc]}" href="{href}"/>')
            # x-default 指向英文版本
            default_slug = variants.get(DEFAULT, "")
            default_href = f"{SITE}/" if default_slug == "" else f"{SITE}/{default_slug}"
            link_parts.append(f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{default_href}"/>')
            hreflang_links = "".join(link_parts)

        parts.append(f'''  <url>
    <loc>{loc}</loc>{hreflang_links}
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>''')
    parts.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(parts) + "\n", encoding="utf-8")


def main():
    # 生成所有语言版本的页面
    for lang in SUPPORTED:
        if lang == DEFAULT:
            build_pages(lang)
        else:
            # 非英语页面：使用翻译后的标题/meta，正文暂保留英文
            build_pages(lang)
    update_home()
    update_css()
    write_todo()
    update_llms()
    update_sitemap()
    print(f"Generated {len(PAGES)} SEO pages and refreshed site files.")


if __name__ == "__main__":
    main()
