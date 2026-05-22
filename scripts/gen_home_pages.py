"""
Generate localized homepages for non-English languages.

The English root index.html is hand-crafted and not touched.
The zh/index.html exists as a hand-edited file and is also preserved (only generates if absent).
For es/, de/, fr/, pt/, this writes a full localized homepage using homepage.* locale keys.

Run: python scripts/gen_home_pages.py
"""
import html as html_mod
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://windrose-guides.com"

from templates import header_html, footer_html, HAMBURGER_JS
from i18n import t, lang_url, hreflang_tags, LANG_HTML, DEFAULT, SUPPORTED, LANG_NAMES

# Languages that should be auto-generated.
# Skip English (manual root index.html) and Chinese (existing hand-edited zh/index.html).
SKIP_LANGS = {DEFAULT, "zh"}


def esc(s):
    return html_mod.escape(str(s), quote=True)


def jsonld_for_lang(lang):
    """Build JSON-LD graph for the homepage."""
    hlang = LANG_HTML.get(lang, lang)
    canonical = f"{SITE}/{lang}/" if lang != DEFAULT else f"{SITE}/"
    return json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": f"{SITE}/#website",
                "url": f"{SITE}/",
                "name": t("header.site_name", lang),
                "publisher": {"@id": f"{SITE}/#org"},
                "inLanguage": hlang,
            },
            {
                "@type": "Organization",
                "@id": f"{SITE}/#org",
                "name": t("header.site_name", lang),
                "url": f"{SITE}/",
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{SITE}/imgs/logo.webp",
                    "width": "512",
                    "height": "512",
                },
            },
            {
                "@type": "VideoGame",
                "name": "Windrose",
                "alternateName": ["Windrose: Pirate Survival RPG"],
                "description": t("homepage.hero_desc", lang),
                "genre": ["Survival", "Adventure", "Action RPG", "Souls-like"],
                "gamePlatform": ["PC"],
                "playMode": ["SinglePlayer", "CoOp", "MultiPlayer"],
                "author": {"@type": "Organization", "name": "Kraken Express"},
                "publisher": {"@type": "Organization", "name": "Kraken Express / Pocketpair Publishing"},
                "datePublished": "2026-04-14",
            },
            {
                "@type": "WebPage",
                "@id": f"{canonical}#webpage",
                "url": canonical,
                "name": t("homepage.hero_title", lang),
                "description": t("homepage.hero_desc", lang),
                "dateModified": "2026-05-18",
                "isPartOf": {"@id": f"{SITE}/#website"},
                "inLanguage": hlang,
            },
        ],
    }, ensure_ascii=False)


def quick_nav_card(icon, title_key, desc_key, href_path, lang):
    """One quick nav card."""
    title = esc(t(f"homepage.{title_key}", lang))
    desc = esc(t(f"homepage.{desc_key}", lang))
    href = lang_url(href_path, lang)
    return f"""                <a href="{href}" class="card quick-nav-card">
                    <span class="nav-icon">{icon}</span>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </a>"""


def feature_card(icon, title_key, desc_key, lang):
    title = esc(t(f"homepage.{title_key}", lang))
    desc = esc(t(f"homepage.{desc_key}", lang))
    return f"""                <div class="feature-card">
                    <div class="feature-card-icon">{icon}</div>
                    <div class="feature-card-title">{title}</div>
                    <p class="feature-card-desc">{desc}</p>
                </div>"""


def db_showcase_card(icon, label_key, cat_key, href_path, lang):
    label = esc(t(f"homepage.{label_key}", lang))
    cat = esc(t(f"homepage.{cat_key}", lang))
    href = lang_url(href_path, lang)
    return f"""                <a href="{href}" class="db-showcase-card">
                    <span class="db-showcase-icon">{icon}</span>
                    <span class="db-showcase-name">{label}</span>
                    <span class="db-showcase-category">{cat}</span>
                </a>"""


def build_home(lang):
    """Build the full homepage HTML for a given language."""
    hlang = LANG_HTML.get(lang, lang)
    canonical = f"{SITE}/{lang}/"
    locale_og = {"zh": "zh_CN", "es": "es_ES", "pt": "pt_BR", "de": "de_DE", "fr": "fr_FR", "en": "en_US"}.get(lang, "en_US")

    hreflang_html = "\n    ".join(hreflang_tags("", SITE))
    jsonld = jsonld_for_lang(lang)
    header = header_html("/", lang)
    footer = footer_html(lang)

    badge = esc(t("homepage.badge", lang))
    hero_title = esc(t("homepage.hero_title", lang))
    hero_subtitle = esc(t("homepage.hero_subtitle", lang))
    hero_desc = esc(t("homepage.hero_desc", lang))
    h_items = esc(t("homepage.highlight_items", lang))
    h_bosses = esc(t("homepage.highlight_bosses", lang))
    h_ships = esc(t("homepage.highlight_ships", lang))
    h_coop = esc(t("homepage.highlight_coop", lang))
    cta_beginner = esc(t("homepage.cta_beginner", lang))
    cta_database = esc(t("homepage.cta_database", lang))
    cta_workbench = esc(t("homepage.cta_workbench", lang))

    quick_nav_title = esc(t("homepage.quick_nav_title", lang))
    quick_nav_desc = esc(t("homepage.quick_nav_desc", lang))

    what_is_title = esc(t("homepage.what_is_title", lang))
    what_is_p1 = t("homepage.what_is_p1", lang)
    what_is_p2 = t("homepage.what_is_p2", lang)
    core_systems_title = esc(t("homepage.core_systems_title", lang))
    core_systems_desc = esc(t("homepage.core_systems_desc", lang))

    db_title = esc(t("homepage.db_title", lang))
    db_desc = esc(t("homepage.db_desc", lang))
    db_cta_text = esc(t("homepage.db_cta_text", lang))
    db_cta_btn = esc(t("homepage.db_cta_btn", lang))

    game_info_title = esc(t("homepage.game_info_title", lang))
    game_info_developer = esc(t("homepage.game_info_developer", lang))
    game_info_release = esc(t("homepage.game_info_release", lang))
    game_info_genre = esc(t("homepage.game_info_genre", lang))
    game_info_combat = esc(t("homepage.game_info_combat", lang))
    game_info_coop = esc(t("homepage.game_info_coop", lang))
    game_info_playtime = esc(t("homepage.game_info_playtime", lang))

    links_title = esc(t("homepage.links_title", lang))

    nav_cards = "\n".join([
        quick_nav_card("🧭", "card_beginner_title", "card_beginner_desc", "/beginner-guide/", lang),
        quick_nav_card("🔨", "card_workbench_title", "card_workbench_desc", "/crafting/", lang),
        quick_nav_card("⛏️", "card_resources_title", "card_resources_desc", "/resources/", lang),
        quick_nav_card("💀", "card_bosses_title", "card_bosses_desc", "/bosses/", lang),
        quick_nav_card("⛵", "card_ships_title", "card_ships_desc", "/ships/", lang),
        quick_nav_card("⚔️", "card_weapons_title", "card_weapons_desc", "/weapons/", lang),
        quick_nav_card("🛠️", "card_tools_title", "card_tools_desc", "/tools/", lang),
        quick_nav_card("🎯", "card_builds_title", "card_builds_desc", "/builds/", lang),
        quick_nav_card("📖", "card_guides_title", "card_guides_desc", "/guides/", lang),
        quick_nav_card("❓", "card_faq_title", "card_faq_desc", "/faq/", lang),
        quick_nav_card("📰", "card_news_title", "card_news_desc", "/news/", lang),
    ])

    feature_cards = "\n".join([
        feature_card("🔨", "feature_crafting_title", "feature_crafting_desc", lang),
        feature_card("⚔️", "feature_combat_title", "feature_combat_desc", lang),
        feature_card("⛵", "feature_sailing_title", "feature_sailing_desc", lang),
        feature_card("⛏️", "feature_resource_title", "feature_resource_desc", lang),
        feature_card("📈", "feature_progression_title", "feature_progression_desc", lang),
    ])

    db_cards = "\n".join([
        db_showcase_card("⚔️", "db_weapons", "db_weapons_cat", "/database/weapons/", lang),
        db_showcase_card("🛡️", "db_equipment", "db_equipment_cat", "/database/equipment/", lang),
        db_showcase_card("⛵", "db_ships", "db_ships_cat", "/database/ships/", lang),
        db_showcase_card("⛏️", "db_resources", "db_resources_cat", "/database/resources/", lang),
        db_showcase_card("🔨", "db_crafting", "db_crafting_cat", "/database/crafting/", lang),
        db_showcase_card("🍖", "db_consumables", "db_consumables_cat", "/database/consumables/", lang),
    ])

    util_cards = "\n".join([
        quick_nav_card("⬇️", "card_download_title", "card_download_desc", "/download/", lang),
        quick_nav_card("🖥️", "card_server_title", "card_server_desc", "/server-guide/", lang),
        quick_nav_card("📑", "card_sources_title", "card_sources_desc", "/sources/", lang),
    ])

    return f"""<!DOCTYPE html>
<html lang="{hlang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{hero_title} (2026)</title>
    <meta name="description" content="{hero_desc}">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <link rel="canonical" href="{canonical}">
    {hreflang_html}

    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{hero_title}">
    <meta property="og:description" content="{hero_desc}">
    <meta property="og:image" content="{SITE}/imgs/og_home.png">
    <meta property="og:site_name" content="{esc(t('header.site_name', lang))}">
    <meta property="og:locale" content="{locale_og}">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{hero_title}">
    <meta name="twitter:description" content="{hero_desc}">
    <meta name="twitter:image" content="{SITE}/imgs/og_home.png">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="../css/style.css">

    <script type="application/ld+json">
    {jsonld}
    </script>
</head>
<body>

{header}

<main>
    <section class="hero" style="background-image: linear-gradient(rgba(10, 14, 26, 0.8), rgba(10, 14, 26, 0.9)), url('/imgs/hero_bg.png'); background-size: cover; background-position: center; border-radius: 0; padding: 6rem 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        <div class="container" style="text-align: center;">
            <span class="hero-badge">⚓ {badge}</span>
            <h1>{hero_title}</h1>
            <p class="tagline" style="justify-content: center; margin-bottom: 1rem;">{hero_subtitle}</p>
            <p class="hero-desc">{hero_desc}</p>
            <div class="hero-highlights">
                <span class="hero-highlight-tag">🗃️ {h_items}</span>
                <span class="hero-highlight-tag">💀 {h_bosses}</span>
                <span class="hero-highlight-tag">⛵ {h_ships}</span>
                <span class="hero-highlight-tag">🤝 {h_coop}</span>
            </div>
            <div class="cta-buttons" style="justify-content: center;">
                <a href="{lang_url('/beginner-guide/', lang)}" class="btn btn-primary">🧭 {cta_beginner}</a>
                <a href="{lang_url('/database/', lang)}" class="btn btn-primary">🗄️ {cta_database}</a>
                <a href="{lang_url('/crafting/', lang)}" class="btn btn-secondary">🔨 {cta_workbench}</a>
            </div>
        </div>
    </section>

    <div class="container">

        <section>
            <h2>{quick_nav_title}</h2>
            <p>{quick_nav_desc}</p>
            <div class="quick-nav-grid">
{nav_cards}
            </div>
        </section>

        <section>
            <h2>{what_is_title}</h2>
            <div class="about-game-intro">
                <p>{what_is_p1}</p>
                <p>{what_is_p2}</p>
            </div>

            <h3>{core_systems_title}</h3>
            <p>{core_systems_desc}</p>
            <div class="feature-grid">
{feature_cards}
            </div>
        </section>

        <section>
            <h2>{db_title}</h2>
            <p>{db_desc}</p>
            <div class="db-showcase-grid" style="grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));">
{db_cards}
            </div>
            <p style="margin-top:1.5rem;">{db_cta_text}</p>
            <div class="cta-buttons" style="justify-content: center;">
                <a href="{lang_url('/database/', lang)}" class="btn btn-primary">🗄️ {db_cta_btn}</a>
            </div>
        </section>

        <section>
            <h2>{game_info_title}</h2>
            <div class="game-info-grid">
                <div class="info-item"><div class="info-value">Kraken Express</div><div class="info-label">{game_info_developer}</div></div>
                <div class="info-item"><div class="info-value">2026-04-14</div><div class="info-label">{game_info_release}</div></div>
                <div class="info-item"><div class="info-value">RPG</div><div class="info-label">{game_info_genre}</div></div>
                <div class="info-item"><div class="info-value">Soulslite</div><div class="info-label">{game_info_combat}</div></div>
                <div class="info-item"><div class="info-value">1-10</div><div class="info-label">{game_info_coop}</div></div>
                <div class="info-item"><div class="info-value">50-70h</div><div class="info-label">{game_info_playtime}</div></div>
            </div>
        </section>

        <section>
            <h2>{links_title}</h2>
            <div class="quick-nav-grid">
{util_cards}
            </div>
        </section>

    </div>
</main>

{footer}
{HAMBURGER_JS}
</body>
</html>
"""


def main():
    written = []
    skipped = []
    for lang in SUPPORTED:
        if lang in SKIP_LANGS:
            skipped.append(lang)
            continue
        out_path = ROOT / lang / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(build_home(lang), encoding="utf-8")
        written.append(lang)
    print(f"Wrote homepages for: {written}")
    print(f"Skipped (manual or default): {skipped}")


if __name__ == "__main__":
    main()
