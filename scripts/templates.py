"""共享 HTML 模板片段，供各生成脚本导入复用。"""
import html as html_mod

from i18n import t, lang_url, lang_switcher_html, DEFAULT

# 保留旧 NAV_ITEMS 用于向后兼容（未改造的脚本仍可导入）
NAV_ITEMS = [
    ("Home", "/"),
    ("Beginner Guide", "/beginner-guide"),
    ("Database", "/database"),
    ("Bosses", "/bosses"),
    ("Ships", "/ships"),
    ("Guides", "/guides"),
    ("Tools", "/tools"),
    ("News", "/news"),
    ("Search \U0001f50d", "/search"),
]

NAV_KEYS = [
    ("nav.home", "/"),
    ("nav.beginner_guide", "/beginner-guide"),
    ("nav.database", "/database"),
    ("nav.bosses", "/bosses"),
    ("nav.ships", "/ships"),
    ("nav.guides", "/guides"),
    ("nav.tools", "/tools"),
    ("nav.news", "/news"),
    ("nav.search", "/search"),
]


def nav_items(lang=DEFAULT):
    """生成导航 <li> 列表，支持多语言。"""
    items = []
    for key, href in NAV_KEYS:
        label = t(key, lang)
        url = lang_url(href, lang)
        items.append(f'<li><a href="{url}">{html_mod.escape(label)}</a></li>')
    return "\n".join(items)


def header_html(active="", lang=DEFAULT, current_path=None):
    """生成带多语言支持的 <header> HTML。

    active: 当前所在的顶级 section（用于导航高亮），如 "database" 或 "/tools"
    lang: 语言代码
    current_path: 完整的当前页面路径（用于语言切换器），如 "/database/weapons"。
                  默认从 active 推导（仅适用于顶级页面）。
    """
    items = []
    for key, href in NAV_KEYS:
        label = t(key, lang)
        url = lang_url(href, lang)
        is_active = False
        if active:
            if href == active:
                is_active = True
            elif href != "/" and active.startswith(href.strip("/")):
                is_active = True
        cls = ' class="active"' if is_active else ""
        current = ' aria-current="page"' if is_active else ""
        items.append(
            f'<li><a href="{url}"{cls}{current}>{html_mod.escape(label)}</a></li>'
        )
    nav = "".join(items)

    site_name = t("header.site_name", lang)
    logo_alt = t("header.logo_alt", lang)
    aria_home = t("header.aria_home", lang)
    aria_menu = t("header.aria_menu", lang)

    # 语言切换器（所有语言都显示，包括英文）
    switcher_path = current_path if current_path is not None else active
    switcher = lang_switcher_html(lang, switcher_path)
    switcher_html = f'\n        {switcher}' if switcher else ""

    home_url = lang_url("", lang)
    return (
        f'<header class="header"><div class="container">'
        f'<a href="{home_url}" class="logo" aria-label="{html_mod.escape(aria_home)}">'
        f'<img src="/imgs/logo.png" alt="{html_mod.escape(logo_alt)}" width="32" height="32"> '
        f'{html_mod.escape(site_name)}</a>'
        f'<button class="hamburger" aria-label="{html_mod.escape(aria_menu)}" aria-expanded="false">'
        f'<span></span><span></span><span></span></button>'
        f'{switcher_html}'
        f'<nav aria-label="Primary"><ul class="nav-links">'
        + nav +
        "</ul></nav></div></header>"
    )


def footer_html(lang=DEFAULT):
    """生成带多语言支持的 <footer> HTML。"""
    home_url = lang_url("", lang)
    brand_desc = t("footer.brand_desc", lang)
    col_guides = t("footer.col_guides", lang)
    col_database = t("footer.col_database", lang)
    col_explore = t("footer.col_explore", lang)
    site_name = t("header.site_name", lang)
    logo_alt = t("header.logo_alt", lang)
    copyright_text = t("footer.copyright", lang)

    def link(key, path):
        label = t(f"footer.{key}", lang)
        url = lang_url(path, lang)
        return f'<li><a href="{url}">{html_mod.escape(label)}</a></li>'

    guides_links = "\n".join([
            link("link_beginner", "/beginner-guide"),
            link("link_builds", "/builds"),
            link("link_server", "/server-guide"),
            link("link_download", "/download"),
            link("link_faq", "/faq"),
    ])
    database_links = "\n".join([
            link("link_crafting", "/crafting"),
            link("link_resources", "/resources"),
            link("link_bosses", "/bosses"),
            link("link_ships", "/ships"),
            link("link_weapons", "/weapons"),
    ])
    explore_links = "\n".join([
            link("link_tools", "/tools"),
            link("link_news", "/news"),
            link("link_sources", "/sources"),
            link("link_about", "/about"),
            link("link_contact", "/contact"),
    ])

    all_pages_url = lang_url("/pages", lang)
    privacy_url = lang_url("/privacy", lang)
    terms_url = lang_url("/terms", lang)
    all_pages_label = t("footer.link_all_pages", lang)
    privacy_label = t("footer.link_privacy", lang)
    terms_label = t("footer.link_terms", lang)

    return f'''<footer class="footer">
    <div class="container">
        <div class="footer-grid">
            <div class="footer-brand">
                <a href="{home_url}" class="footer-logo"><img src="/imgs/logo.png" alt="{html_mod.escape(logo_alt)}" width="28" height="28"> {html_mod.escape(site_name)}</a>
                <p>{html_mod.escape(brand_desc)}</p>
            </div>
            <div class="footer-col">
                <h4>{html_mod.escape(col_guides)}</h4>
                <ul>
                    {guides_links}
                </ul>
            </div>
            <div class="footer-col">
                <h4>{html_mod.escape(col_database)}</h4>
                <ul>
                    {database_links}
                </ul>
            </div>
            <div class="footer-col">
                <h4>{html_mod.escape(col_explore)}</h4>
                <ul>
                    {explore_links}
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <span>{html_mod.escape(copyright_text)}</span>
            <nav>
                <a href="{all_pages_url}">{html_mod.escape(all_pages_label)}</a>
                <a href="{privacy_url}">{html_mod.escape(privacy_label)}</a>
                <a href="{terms_url}">{html_mod.escape(terms_label)}</a>
            </nav>
        </div>
    </div>
  </footer>'''


HAMBURGER_JS = """<script>(function(){var b=document.querySelector('.hamburger'),n=document.querySelector('.nav-links');if(b&&n){b.addEventListener('click',function(){var o=n.classList.toggle('open');b.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});}var lb=document.querySelector('.lang-btn'),ls=document.querySelector('.lang-switcher');if(lb&&ls){lb.addEventListener('click',function(e){e.stopPropagation();var open=ls.classList.toggle('open');lb.setAttribute('aria-expanded',open?'true':'false');});document.addEventListener('click',function(e){if(!ls.contains(e.target)){ls.classList.remove('open');lb.setAttribute('aria-expanded','false');}});}})();</script>"""
