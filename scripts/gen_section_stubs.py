"""
Generate stub pages for top-level sections that exist in English root but not in
language directories. Solves nav 404s like /es/bosses.

For each non-English language:
- Sections that have a localized Database equivalent (bosses, ships, weapons,
  crafting, resources): generate a stub page with a CTA to the localized DB +
  a fallback link to the English in-depth guide.
- Guides hub: generate a page listing all 7 translated guide articles.
- English-only sections (beginner-guide, builds, faq): generate a stub that
  informs the user the page is only in English and links to the English version.

Run automatically by build_site.py.
"""
import html as html_mod
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://windrosewiki.games"

from templates import header_html, footer_html, HAMBURGER_JS
from i18n import t, lang_url, hreflang_tags, LANG_HTML, DEFAULT, SUPPORTED


def esc(s):
    return html_mod.escape(str(s), quote=True)


# Sections WITH localized database equivalent: stub points to /{lang}/database/{db_path}
SECTIONS_WITH_DB = [
    # (url_segment, locale_section_label_key, db_subpath)
    ("bosses", "stub.section_bosses", "/database/bosses/"),
    ("ships", "stub.section_ships", "/database/ships/"),
    ("weapons", "stub.section_weapons", "/database/weapons/"),
    ("crafting", "stub.section_crafting", "/database/crafting/"),
    ("resources", "stub.section_resources", "/database/resources/"),
]

# Sections without a localized counterpart: link out to English
SECTIONS_ENGLISH_ONLY = [
    ("beginner-guide", "stub.section_beginner_guide"),
    ("builds", "stub.section_builds"),
    ("faq", "stub.section_faq"),
]

# All 7 guide article slugs and their meta_title keys (from existing locale)
GUIDE_ARTICLES = [
    ("mining-routes", "guides.mining_heading"),
    ("boss-progression", "guides.boss_prog_heading"),
    ("best-early-builds", "guides.builds_heading"),
    ("ship-building-naval-combat", "guides.ship_guide_heading"),
    ("sailing-navigation", "guides.sailing_heading"),
    ("crafting-progression", "guides.crafting_prog_heading"),
    ("coop-multiplayer", "guides.coop_heading"),
]


def render_page(slug, lang, title, body_html):
    """Wrap body in full HTML page with header/footer/lang-switcher."""
    hlang = LANG_HTML.get(lang, lang)
    canonical = f"{SITE}/{lang}/{slug}/"
    hreflang_html = "\n    ".join(hreflang_tags(slug, SITE))
    header = header_html(slug.split("/")[0], lang, current_path=f"/{slug}")
    footer = footer_html(lang)
    site_name = t("header.site_name", lang)

    # CSS depth: /lang/slug → 2 levels deep
    depth = 2 + slug.count("/")
    css_prefix = "../" * depth

    return f"""<!DOCTYPE html>
<html lang="{hlang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(title)} | {esc(site_name)}</title>
    <meta name="description" content="{esc(title)} — {esc(site_name)}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    {hreflang_html}
    <link rel="stylesheet" href="{css_prefix}css/style.css">
</head>
<body>
{header}
<main class="container" style="padding: 2rem 1rem;">
    <h1>{esc(title)}</h1>
    {body_html}
</main>
{footer}
{HAMBURGER_JS}
</body>
</html>
"""


def stub_with_db(lang, url_seg, label_key, db_path):
    """Stub for sections with a localized DB equivalent."""
    section_label = t(label_key, lang)
    title = section_label
    intro = t("stub.localized_db_intro", lang, section=section_label)
    db_btn = t("stub.view_db_btn", lang, section=section_label)
    en_btn = t("stub.view_english_btn", lang)
    back_home = t("stub.back_home", lang)

    body = f"""
    <p style="font-size: 1.1rem; margin: 1.5rem 0;">{esc(intro)}</p>

    <div class="cta-buttons" style="margin: 2.5rem 0;">
        <a href="{lang_url(db_path, lang)}" class="btn btn-primary">🗄️ {esc(db_btn)}</a>
        <a href="/{url_seg}" class="btn btn-secondary">📖 {esc(en_btn)}</a>
    </div>

    <p style="margin-top: 3rem;"><a href="{lang_url('', lang)}">{esc(back_home)}</a></p>
"""
    return render_page(url_seg, lang, title, body)


def stub_english_only(lang, url_seg, label_key):
    """Stub for sections that only exist in English."""
    section_label = t(label_key, lang)
    title = section_label
    intro = t("stub.english_only_intro", lang, section=section_label)
    en_btn = t("stub.view_english_btn", lang)
    back_home = t("stub.back_home", lang)

    body = f"""
    <p style="font-size: 1.1rem; margin: 1.5rem 0;">{esc(intro)}</p>

    <div class="cta-buttons" style="margin: 2.5rem 0;">
        <a href="/{url_seg}" class="btn btn-primary">📖 {esc(en_btn)}</a>
    </div>

    <p style="margin-top: 3rem;"><a href="{lang_url('', lang)}">{esc(back_home)}</a></p>
"""
    return render_page(url_seg, lang, title, body)


def stub_guides_hub(lang):
    """Stub for /lang/guides/ — lists all translated guide articles."""
    heading = t("stub.guides_hub_heading", lang)
    intro = t("stub.guides_hub_intro", lang)
    back_home = t("stub.back_home", lang)

    cards = []
    for slug, title_key in GUIDE_ARTICLES:
        guide_title = t(title_key, lang)
        href = lang_url(f"/guides/{slug}/", lang)
        cards.append(f"""        <a href="{href}" class="card quick-nav-card">
            <span class="nav-icon">📖</span>
            <h3>{esc(guide_title)}</h3>
        </a>""")

    cards_html = "\n".join(cards)
    body = f"""
    <p style="font-size: 1.1rem; margin: 1.5rem 0;">{esc(intro)}</p>

    <div class="quick-nav-grid" style="margin: 2rem 0;">
{cards_html}
    </div>

    <p style="margin-top: 3rem;"><a href="{lang_url('', lang)}">{esc(back_home)}</a></p>
"""
    return render_page("guides", lang, heading, body)


def write_stub(lang, url_seg, html):
    out = ROOT / lang / url_seg / "index.html"
    if out.exists():
        # Don't overwrite — generated pages from other scripts take priority
        return False
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return True


def main():
    total = 0
    for lang in SUPPORTED:
        if lang == DEFAULT:
            continue
        written = 0
        skipped = 0

        for url_seg, label_key, db_path in SECTIONS_WITH_DB:
            html = stub_with_db(lang, url_seg, label_key, db_path)
            if write_stub(lang, url_seg, html):
                written += 1
            else:
                skipped += 1

        for url_seg, label_key in SECTIONS_ENGLISH_ONLY:
            html = stub_english_only(lang, url_seg, label_key)
            if write_stub(lang, url_seg, html):
                written += 1
            else:
                skipped += 1

        # Guides hub
        if write_stub(lang, "guides", stub_guides_hub(lang)):
            written += 1
        else:
            skipped += 1

        total += written
        print(f"{lang}: wrote {written} stubs, skipped {skipped} (already exist)")

    print(f"\n✅ Generated {total} stub pages total.")


if __name__ == "__main__":
    main()
