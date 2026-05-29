"""Apply keyword-first title/meta + 4-boss stats to all localized boss pages.

Mirrors the EN changes already shipped in /bosses/* across DE/ES/FR/PT/ZH.

For the hub page (X/bosses/index.html):
  - <title>, <meta description>, og:title/desc, twitter:title/desc
  - JSON-LD WebPage.name + Article.headline
  - <h1>, hero subtitle, quick-stats trio (Total/Story/Optional)

For sub-pages (X/bosses/<slug>/index.html):
  - <title>, <meta description>, og:title/desc, twitter:title/desc
  - JSON-LD WebPage.name + Article.headline (when present)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "scripts" / "boss_locale_data.json").read_text(encoding="utf-8"))


def replace_meta_attr(html, attr_name, attr_value, new_content_html_escaped):
    """Replace the content="..." of a <meta> whose `attr_name` equals `attr_value`.
    Handles both attribute orders: <meta name="x" content="y"> and reversed.
    `new_content_html_escaped` MUST already have & < > " encoded.
    """
    # name/property first, content second
    pat1 = re.compile(
        r'(<meta[^>]*\b' + re.escape(attr_name) + r'\s*=\s*"' + re.escape(attr_value) + r'"[^>]*\bcontent\s*=\s*")[^"]*(")',
        re.IGNORECASE,
    )
    # content first, name/property second
    pat2 = re.compile(
        r'(<meta[^>]*\bcontent\s*=\s*")[^"]*("[^>]*\b' + re.escape(attr_name) + r'\s*=\s*"' + re.escape(attr_value) + r'")',
        re.IGNORECASE,
    )
    new_html, n1 = pat1.subn(lambda m: m.group(1) + new_content_html_escaped + m.group(2), html, count=1)
    if n1 == 0:
        new_html, n2 = pat2.subn(lambda m: m.group(1) + new_content_html_escaped + m.group(2), html, count=1)
        return new_html, n2
    return new_html, n1


def html_escape_attr(s):
    return (
        s.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def replace_title(html, new_title):
    return re.sub(
        r"<title>.*?</title>",
        f"<title>{html_escape_attr(new_title).replace('&quot;', '\"')}</title>",
        html,
        count=1,
        flags=re.DOTALL,
    )


def replace_jsonld_webpage_name(html, new_name):
    """Replace the 'name' field inside the WebPage JSON-LD node."""
    # Find @type: WebPage block, then replace its "name": "..."
    pat = re.compile(
        r'(\"@type\"\s*:\s*\"WebPage\"[^{}]*?\"name\"\s*:\s*\")[^\"]*(\")',
        re.DOTALL,
    )
    return pat.sub(lambda m: m.group(1) + json_str_escape(new_name) + m.group(2), html, count=1)


def replace_jsonld_article_headline(html, new_headline):
    pat = re.compile(
        r'(\"@type\"\s*:\s*\"Article\"[^{}]*?\"headline\"\s*:\s*\")[^\"]*(\")',
        re.DOTALL,
    )
    return pat.sub(lambda m: m.group(1) + json_str_escape(new_headline) + m.group(2), html, count=1)


def json_str_escape(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


# ---------------------------------------------------------------------------
# Hub page
# ---------------------------------------------------------------------------

def update_hub(lang, data):
    p = ROOT / lang / "bosses" / "index.html"
    html = p.read_text(encoding="utf-8")
    orig = html

    title = data["title"]
    desc = data["desc"]

    html = replace_title(html, title)
    for (attr, val), new in [
        (("name", "description"), html_escape_attr(desc)),
        (("name", "twitter:title"), html_escape_attr(data["tw_title"])),
        (("name", "twitter:description"), html_escape_attr(data["tw_desc"])),
        (("property", "og:title"), html_escape_attr(data["og_title"])),
        (("property", "og:description"), html_escape_attr(data["og_desc"])),
    ]:
        html, n = replace_meta_attr(html, attr, val, new)
        if n == 0:
            print(f"  [warn] {p}: meta {attr}={val} not found")

    html = replace_jsonld_webpage_name(html, title)
    html = replace_jsonld_article_headline(html, title)

    # H1
    html = re.sub(
        r"(<h1[^>]*>).*?(</h1>)",
        lambda m: m.group(1) + html_escape_attr(data["h1"]).replace("&quot;", '"') + m.group(2),
        html,
        count=1,
        flags=re.DOTALL,
    )
    # Hero subtitle
    html = re.sub(
        r'(<p class="hero-subtitle">).*?(</p>)',
        lambda m: m.group(1) + html_escape_attr(data["sub"]).replace("&quot;", '"') + m.group(2),
        html,
        count=1,
        flags=re.DOTALL,
    )
    # Quick stats — replace the entire <div class="quick-stats">…</div> trio
    new_stats = (
        '<div class="quick-stats">'
        f'<div class="stat"><div class="stat-label">{data["stat1_label"]}</div><div class="stat-value">{data["stat1_value"]}</div></div>'
        f'<div class="stat"><div class="stat-label">{data["stat2_label"]}</div><div class="stat-value">{data["stat2_value"]}</div></div>'
        f'<div class="stat"><div class="stat-label">{data["stat3_label"]}</div><div class="stat-value">{data["stat3_value"]}</div></div>'
        '</div>'
    )
    html = re.sub(
        r'<div class="quick-stats">.*?</div>\s*</div>(?=\s*<h2)|<div class="quick-stats">.*?</div>\s*(?=<h2)',
        new_stats + "\n",
        html,
        count=1,
        flags=re.DOTALL,
    )

    if html == orig:
        print(f"  [warn] {p}: no changes")
        return False
    p.write_text(html, encoding="utf-8")
    print(f"  ✓ {p}")
    return True


# ---------------------------------------------------------------------------
# Sub-page (only title + description + JSON-LD name/headline; H1 left intact)
# ---------------------------------------------------------------------------

def update_sub(lang, slug, data):
    p = ROOT / lang / "bosses" / slug / "index.html"
    if not p.exists():
        print(f"  [skip] {p} (missing)")
        return False
    html = p.read_text(encoding="utf-8")
    orig = html
    title = data["title"]
    desc = data["desc"]

    # Twitter/OG often duplicate title; we keep them in sync with the new title/desc
    # Build short variants by stripping the trailing " | Windrose Wiki" if present
    short_title = re.sub(r"\s*\|\s*Windrose Wiki\s*$", "", title)
    short_title = re.sub(r"\s*\(2026\)$", " (2026)", short_title)

    html = replace_title(html, title)
    for (attr, val), new in [
        (("name", "description"), html_escape_attr(desc)),
        (("name", "twitter:title"), html_escape_attr(short_title)),
        (("name", "twitter:description"), html_escape_attr(desc)),
        (("property", "og:title"), html_escape_attr(short_title)),
        (("property", "og:description"), html_escape_attr(desc)),
    ]:
        html, _ = replace_meta_attr(html, attr, val, new)

    html = replace_jsonld_webpage_name(html, title)
    html = replace_jsonld_article_headline(html, title)

    if html == orig:
        print(f"  [warn] {p}: no changes")
        return False
    p.write_text(html, encoding="utf-8")
    print(f"  ✓ {p}")
    return True


def main():
    print("=== Hub pages ===")
    for lang, d in DATA["hub"].items():
        update_hub(lang, d)
    print()
    print("=== Sub-pages ===")
    for slug, langs in DATA["sub"].items():
        for lang, d in langs.items():
            update_sub(lang, slug, d)


if __name__ == "__main__":
    main()
