"""
DeepSeek-based bulk translator for windrose-guides.com.

Strategy: parse source HTML, extract translatable text segments (text nodes,
specific attributes, JSON-LD strings), batch them through DeepSeek's API in
small JSON payloads, then write a fully reconstructed HTML with:
- localized header/footer/hamburger from templates.py
- updated <html lang>, canonical, hreflang, og:locale
- rewritten internal links
- translated body text + meta + JSON-LD names/descriptions/FAQs

Glossary terms in TRANSLATION_GUIDE.md are passed in the prompt as a strict
"DO NOT translate" list. The script also uses placeholder substitution to
shield code blocks, scripts, URLs, and version numbers.

Run:
    python scripts/translate_with_deepseek.py es bosses
    python scripts/translate_with_deepseek.py es bosses ships weapons
    python scripts/translate_with_deepseek.py all all   # everything

Pages are listed in HAND_PAGES below. Languages: zh es pt de fr (skip en).

Cost-control: each chunk is bounded to ~1500 chars; max ~30 chunks per page;
single language at a time; ThreadPool concurrency=4 for chunk requests.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import html as html_mod
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

from bs4 import BeautifulSoup, Comment, Doctype, NavigableString, Tag
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from templates import header_html, footer_html, HAMBURGER_JS  # noqa: E402

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-e045f84ceea8482db07c53282c789ecd")
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash")
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

SITE = "https://windrose-guides.com"

LANG_HTML_ATTR = {
    "zh": "zh-CN",
    "es": "es",
    "pt": "pt-BR",
    "de": "de",
    "fr": "fr",
}
LANG_OG_LOCALE = {
    "zh": "zh_CN",
    "es": "es_ES",
    "pt": "pt_BR",
    "de": "de_DE",
    "fr": "fr_FR",
}
LANG_LABEL = {
    "zh": "Simplified Chinese (use 你 informal form, gamer-friendly tone)",
    "es": "neutral Latin American Spanish (use tú informal form)",
    "pt": "Brazilian Portuguese (pt-BR, use você informal form)",
    "de": "German (use Du informal form, gaming standard)",
    "fr": "modern French (use tu informal form)",
}

# Active section per page (for header_html nav highlight)
PAGE_ACTIVE = {
    "beginner-guide": "beginner-guide",
    "bosses": "bosses",
    "bosses/charons-obols": "bosses",
    "bosses/ghost-captain": "bosses",
    "bosses/high-priestess": "bosses",
    "bosses/israel-hands": "bosses",
    "bosses/thomas-richards": "bosses",
    "ships": "ships",
    "ships/brigantine": "ships",
    "ships/frigate": "ships",
    "ships/sloop": "ships",
    "weapons": "weapons",
    "weapons/armor": "weapons",
    "weapons/melee": "weapons",
    "weapons/ranged": "weapons",
    "crafting": "crafting",
    "crafting/alchemy": "crafting",
    "crafting/building": "crafting",
    "crafting/cooking": "crafting",
    "crafting/smelting": "crafting",
    "crafting/workbench": "crafting",
    "resources": "resources",
    "resources/clay": "resources",
    "resources/copper": "resources",
    "resources/gunpowder": "resources",
    "resources/iron": "resources",
    "resources/rare-materials": "resources",
    "guides": "guides",
    "builds": "guides",
    "faq": "guides",
    "about": "",
    "contact": "",
    "privacy": "",
    "terms": "",
    "pages": "",
    "download": "",
    "database": "database",
    "database/bosses": "database",
}

# All hand-maintained pages we want translated (excluding news/items details)
HAND_PAGES = list(PAGE_ACTIVE.keys())

# Paths that have localized counterparts (rewrite /X → /{lang}/X)
LOCALIZED_PATHS = {
    "/", "/beginner-guide", "/bosses", "/ships", "/weapons", "/crafting",
    "/resources", "/guides", "/builds", "/faq", "/tools",
    "/tools/recipe-finder", "/tools/progression-checklist",
    "/tools/resource-planner", "/tools/ship-selector",
    "/news", "/search", "/server-guide", "/download", "/sources",
    "/database", "/about", "/contact", "/privacy", "/terms", "/pages",
}
# Plus prefix-based: /guides/*, /crafting/*, /bosses/*, /ships/*, /resources/*,
# /weapons/*, /database/*
LOCALIZED_PREFIXES = (
    "/guides/", "/crafting/", "/bosses/", "/ships/", "/resources/",
    "/weapons/", "/database/",
)
# Exception: /database/items/* is English only
ENGLISH_ONLY_PREFIXES = ("/database/items/", "/news/")

GLOSSARY = """
KEEP THESE TERMS IN ENGLISH (do not translate, use exactly as written):
Windrose, Kraken Express, Pocketpair Publishing, Pocketpair, Steam, SteamCMD, WindroseServer.exe,
Thomas Richards, Israel Hands, High Priestess, Ghost Captain, Charon, Charon's Obols,
Coastal Jungle, Foothills, Cursed Swamps, Ashlands,
Sloop, Brigantine, Frigate, Ketch,
Workbench, Charcoal Kiln, Smelting Furnace, Weaponsmith, Armor Workshop, Alchemy Table, Cooking Fire, Shipyard, Millstone,
Stone Pickaxe, Copper Pickaxe, Iron Pickaxe, Stone Axe, Copper Axe, Bandage, Healing Potion, Antidote, Fast Travel Bell,
Torn Sailcloth Bag, Sailor Backpack, Bosun Backpack, Rope, Sail Fabric, Plant Fiber, Coarse Fabric, Rough Hide, Tanned Leather,
Copper Ingot, Iron Ingot, Copper Ore, Iron Ore, Sulfur, Gunpowder, Clay, Wood, Stone, Ash, Charcoal,
Saber, Rapier, Club, Spear, Musket, Pistol, Blunderbuss, Heavy Club, Boarding Axe,
Toughguy, Swashbuckler, Mariner, Ironclad, Gunner, Duelist, Sharpshooter,
Early Access, co-op, dedicated server, NAT punch-through, UPnP, VPN, P2P, soulslite,
EA, NPC, POI, HP, MP, RPG, Lv, App ID, JSON, HTML, CSS
"""


# ========== Translation core ==========

def translate_batch(strings: List[str], lang: str, retry: int = 3) -> List[str]:
    """Translate a list of strings via DeepSeek. Returns same-length list.

    Uses a JSON-encoded numbered request to keep ordering reliable.
    """
    if not strings:
        return []
    target = LANG_LABEL[lang]
    items = "\n".join(f"{i}|||{s}" for i, s in enumerate(strings))
    system = (
        f"You are a professional translator for a video game wiki website. "
        f"Translate from English to {target}. "
        f"{GLOSSARY}\n"
        "RULES:\n"
        "1. Output ONLY the translations, one per line, in the SAME format: <index>|||<translation>\n"
        "2. Preserve any HTML tags, entities (&amp; &lt; etc.), placeholders ({0}, {n}), and emoji exactly.\n"
        "3. Do not add commentary, notes, or extra formatting.\n"
        "4. Keep numbers, percentages, dates, version codes (v0.4.2) unchanged.\n"
        "5. CRITICAL: Tokens like @@G0@@, @@G1@@, @@G42@@ are placeholder markers. "
        "Keep them EXACTLY as-is in the output (do not translate, do not modify, do not add spaces around).\n"
        "6. If input is empty or pure whitespace, output it unchanged.\n"
    )
    user = f"Translate these {len(strings)} strings to {target}:\n\n{items}"

    last_err = None
    for attempt in range(retry):
        try:
            r = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                stream=False,
                temperature=0.2,
                timeout=120,
            )
            content = r.choices[0].message.content.strip()
            # Parse numbered response
            out = [None] * len(strings)
            for line in content.split("\n"):
                line = line.strip()
                if not line or "|||" not in line:
                    continue
                idx_str, _, val = line.partition("|||")
                try:
                    idx = int(idx_str.strip())
                    if 0 <= idx < len(strings):
                        out[idx] = val
                except ValueError:
                    continue
            # Fill missing with original
            for i, v in enumerate(out):
                if v is None:
                    out[i] = strings[i]
            return out
        except Exception as e:
            last_err = e
            print(f"  ! batch attempt {attempt + 1} failed: {e}", file=sys.stderr)
            time.sleep(2 + attempt * 2)
    print(f"  ! batch FAILED after {retry} attempts: {last_err}", file=sys.stderr)
    return strings  # fallback to original


def chunk_strings(strings: List[str], max_chars: int = 1500, max_items: int = 25) -> List[List[int]]:
    """Group string indices into chunks not exceeding char/item limits."""
    chunks = []
    current = []
    current_chars = 0
    for i, s in enumerate(strings):
        slen = len(s)
        if current and (current_chars + slen > max_chars or len(current) >= max_items):
            chunks.append(current)
            current = []
            current_chars = 0
        current.append(i)
        current_chars += slen
    if current:
        chunks.append(current)
    return chunks


GLOSSARY_TERMS = [
    "Windrose", "Kraken Express", "Pocketpair Publishing", "Pocketpair",
    "Steam", "SteamCMD", "WindroseServer.exe",
    "Thomas Richards", "Israel Hands", "High Priestess", "Ghost Captain",
    "Charon's Obols", "Charon",
    "Coastal Jungle", "Foothills", "Cursed Swamps", "Ashlands",
    "Sloop", "Brigantine", "Frigate", "Ketch",
    "Workbench", "Charcoal Kiln", "Smelting Furnace", "Weaponsmith",
    "Armor Workshop", "Alchemy Table", "Cooking Fire", "Shipyard", "Millstone",
    "Stone Pickaxe", "Copper Pickaxe", "Iron Pickaxe", "Stone Axe", "Copper Axe",
    "Bandage", "Healing Potion", "Antidote", "Fast Travel Bell",
    "Torn Sailcloth Bag", "Sailor Backpack", "Bosun Backpack",
    "Rope", "Sail Fabric", "Plant Fiber", "Coarse Fabric", "Rough Hide", "Tanned Leather",
    "Copper Ingot", "Iron Ingot", "Copper Ore", "Iron Ore",
    "Sulfur", "Gunpowder", "Clay", "Charcoal",
    "Saber", "Rapier", "Club", "Spear", "Musket", "Pistol", "Blunderbuss",
    "Heavy Club", "Boarding Axe",
    "Toughguy", "Swashbuckler", "Mariner", "Ironclad", "Gunner", "Duelist", "Sharpshooter",
    "Early Access", "co-op", "dedicated server", "NAT punch-through", "UPnP",
    "App ID", "soulslite",
    # Common items mentioned in pages
    "Soul Eater", "Bonfire", "Bacon and Eggs", "Coconut Milk", "Seafood Platter",
    "Silver Ingot", "Undead Essence", "Repair Kits", "Combat Repair Kits",
]


def protect_glossary(strings: List[str]) -> Tuple[List[str], List[Dict[int, str]]]:
    """Replace glossary terms with placeholders @@G0@@, @@G1@@... per string.

    Returns (protected_strings, per_string_replacement_maps) so we can restore
    after translation. Sorts terms longest-first to avoid partial matches.
    """
    sorted_terms = sorted(GLOSSARY_TERMS, key=len, reverse=True)
    out_strings = []
    out_maps = []
    for s in strings:
        repl_map = {}
        protected = s
        idx = 0
        for term in sorted_terms:
            if term in protected:
                placeholder = f"@@G{idx}@@"
                # Replace all occurrences
                if placeholder in protected:
                    idx += 1
                    placeholder = f"@@G{idx}@@"
                protected = protected.replace(term, placeholder)
                repl_map[idx] = term
                idx += 1
        out_strings.append(protected)
        out_maps.append(repl_map)
    return out_strings, out_maps


def restore_glossary(strings: List[str], maps: List[Dict[int, str]]) -> List[str]:
    out = []
    for s, m in zip(strings, maps):
        for idx, term in m.items():
            s = s.replace(f"@@G{idx}@@", term)
        out.append(s)
    return out


def translate_all(strings: List[str], lang: str, max_workers: int = 4) -> List[str]:
    """Translate all strings, chunked and concurrent."""
    if not strings:
        return []
    # Protect glossary terms before sending to LLM
    protected, maps = protect_glossary(strings)
    chunks = chunk_strings(protected)
    print(f"  · {len(strings)} segments → {len(chunks)} chunks", flush=True)
    out = list(protected)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {}
        for ci, idxs in enumerate(chunks):
            sub = [protected[i] for i in idxs]
            futures[ex.submit(translate_batch, sub, lang)] = (ci, idxs)
        for f in concurrent.futures.as_completed(futures):
            ci, idxs = futures[f]
            try:
                result = f.result()
                for j, val in zip(idxs, result):
                    out[j] = val
            except Exception as e:
                print(f"  ! chunk {ci} crashed: {e}", file=sys.stderr)
    # Restore glossary
    out = restore_glossary(out, maps)
    return out


# ========== HTML processing ==========

SKIP_TAGS = {"script", "style", "code", "pre", "noscript"}
TRANSLATABLE_ATTRS = {"alt", "title", "placeholder", "aria-label"}

# Whitespace-only regex
WS_RE = re.compile(r"^\s*$")


def is_translatable_text(s: str) -> bool:
    if not s or WS_RE.match(s):
        return False
    # Skip pure numbers/symbols
    if re.match(r"^[\d\s.,%\-+x×→←↑↓·•/]+$", s):
        return False
    # Skip if it's ALL non-letters (emoji-only etc.)
    if not re.search(r"[A-Za-z]", s):
        return False
    return True


def collect_text_nodes(soup: BeautifulSoup) -> List[Tuple[NavigableString, str]]:
    """Find all text nodes that should be translated.

    Returns list of (node, text) tuples.
    """
    nodes = []
    for el in soup.find_all(string=True):
        if isinstance(el, (Comment, Doctype)):
            continue
        parent = el.parent
        if parent is None:
            continue
        # Walk up to check skip tags
        cur = parent
        skip = False
        while cur is not None and cur.name is not None:
            if cur.name.lower() in SKIP_TAGS:
                skip = True
                break
            cur = cur.parent
        if skip:
            continue
        text = str(el)
        if is_translatable_text(text):
            nodes.append((el, text))
    return nodes


def collect_attr_values(soup: BeautifulSoup) -> List[Tuple[Tag, str, str]]:
    """Find translatable attribute values. Returns list of (tag, attr_name, value)."""
    out = []
    for tag in soup.find_all(True):
        for attr in TRANSLATABLE_ATTRS:
            if tag.has_attr(attr):
                val = tag.get(attr)
                if isinstance(val, str) and is_translatable_text(val):
                    out.append((tag, attr, val))
    return out


def collect_meta_content(soup: BeautifulSoup) -> List[Tuple[str, Tag, str]]:
    """Find <meta> content fields that need translation, and <title>.

    Returns list of (kind, tag, original_text) where kind is 'title' or 'meta'.
    """
    out = []
    title = soup.find("title")
    if title and title.string and is_translatable_text(title.string):
        out.append(("title", title, str(title.string)))
    meta_names_to_translate = {
        "description", "twitter:title", "twitter:description",
    }
    meta_props_to_translate = {
        "og:title", "og:description", "og:site_name",
    }
    for m in soup.find_all("meta"):
        name = m.get("name") or ""
        prop = m.get("property") or ""
        if name in meta_names_to_translate or prop in meta_props_to_translate:
            content = m.get("content")
            if isinstance(content, str) and is_translatable_text(content):
                out.append(("meta", m, content))
    return out


# JSON-LD: translate "name", "headline", "description", FAQ "name"/"text",
# breadcrumb "name", but NOT URL/@id fields.
JSONLD_TRANSLATE_KEYS = {"name", "headline", "description", "text", "alternativeHeadline"}


def walk_jsonld(obj, collect):
    """Recursively walk JSON-LD dict/list and collect translatable strings.

    Returns a parallel structure where strings to translate are replaced with
    placeholders (collect appends originals; we substitute back later).
    """
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in JSONLD_TRANSLATE_KEYS and isinstance(v, str) and is_translatable_text(v):
                idx = len(collect)
                collect.append(v)
                out[k] = ("__T_PLACEHOLDER__", idx)
            else:
                out[k] = walk_jsonld(v, collect)
        return out
    if isinstance(obj, list):
        return [walk_jsonld(x, collect) for x in obj]
    return obj


def jsonld_substitute(obj, translations):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if isinstance(v, tuple) and len(v) == 2 and v[0] == "__T_PLACEHOLDER__":
                out[k] = translations[v[1]]
            else:
                out[k] = jsonld_substitute(v, translations)
        return out
    if isinstance(obj, list):
        return [jsonld_substitute(x, translations) for x in obj]
    return obj


# ========== Link rewriting ==========

def is_localized_path(href: str) -> bool:
    if not href.startswith("/"):
        return False
    if href.startswith(ENGLISH_ONLY_PREFIXES):
        return False
    if href.startswith(("/imgs/", "/css/", "/js/", "/fonts/", "/locales/")):
        return False
    if href.startswith("/#"):
        return False
    # Check exact paths or known prefixes
    path = href.split("?")[0].split("#")[0].rstrip("/")
    if path == "":
        return True  # /
    if path in LOCALIZED_PATHS or path + "/" in LOCALIZED_PATHS:
        return True
    if any(path.startswith(p.rstrip("/")) for p in LOCALIZED_PATHS):
        return True
    if any(href.startswith(p) for p in LOCALIZED_PREFIXES):
        return True
    return False


def rewrite_link(href: str, lang: str) -> str:
    if not is_localized_path(href):
        return href
    if href.startswith(f"/{lang}/") or href == f"/{lang}":
        return href
    if href == "/":
        return f"/{lang}/"
    return f"/{lang}{href}"


def rewrite_all_links(soup: BeautifulSoup, lang: str):
    for a in soup.find_all("a", href=True):
        a["href"] = rewrite_link(a["href"], lang)
    # Also rewrite form actions if any
    for f in soup.find_all("form", action=True):
        f["action"] = rewrite_link(f["action"], lang)


def rewrite_jsonld_urls(obj, lang: str):
    """Rewrite URL/@id fields inside JSON-LD to localized paths."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in ("url", "@id", "item") and isinstance(v, str):
                # Match site URLs
                if v.startswith(SITE):
                    rest = v[len(SITE):] or "/"
                    if rest.startswith(f"/{lang}/") or rest == f"/{lang}":
                        out[k] = v
                    elif is_localized_path(rest):
                        if rest == "/":
                            out[k] = f"{SITE}/{lang}/"
                        else:
                            out[k] = f"{SITE}/{lang}{rest}"
                    else:
                        out[k] = v
                else:
                    out[k] = v
            else:
                out[k] = rewrite_jsonld_urls(v, lang)
        return out
    if isinstance(obj, list):
        return [rewrite_jsonld_urls(x, lang) for x in obj]
    return obj


# ========== Head metadata updates ==========

def update_canonical_and_hreflang(soup: BeautifulSoup, page_path: str, lang: str):
    """Update canonical, og:url, og:locale, twitter URLs, and hreflang."""
    # Canonical
    can = soup.find("link", rel="canonical")
    if can:
        can["href"] = f"{SITE}/{lang}/{page_path}"

    # og:url, og:locale, twitter:url, og:image (keep)
    for m in soup.find_all("meta"):
        prop = m.get("property") or ""
        name = m.get("name") or ""
        if prop == "og:url":
            m["content"] = f"{SITE}/{lang}/{page_path}"
        elif name == "twitter:url":
            m["content"] = f"{SITE}/{lang}/{page_path}"

    # Insert/update og:locale
    head = soup.find("head")
    og_locale = head.find("meta", property="og:locale") if head else None
    if og_locale:
        og_locale["content"] = LANG_OG_LOCALE[lang]
    elif head:
        new_meta = soup.new_tag("meta", attrs={"property": "og:locale", "content": LANG_OG_LOCALE[lang]})
        if can:
            can.insert_after(new_meta)
        else:
            head.append(new_meta)

    # Remove existing hreflang links and add fresh block
    for a in soup.find_all("link", rel="alternate"):
        if a.get("hreflang"):
            a.decompose()
    if can and head:
        anchor = can
        # Add hreflang block after canonical
        hreflang_pairs = [
            ("en", f"{SITE}/{page_path}"),
            ("es", f"{SITE}/es/{page_path}"),
            ("pt-BR", f"{SITE}/pt/{page_path}"),
            ("de", f"{SITE}/de/{page_path}"),
            ("fr", f"{SITE}/fr/{page_path}"),
            ("zh-CN", f"{SITE}/zh/{page_path}"),
            ("x-default", f"{SITE}/{page_path}"),
        ]
        for hl, url in hreflang_pairs:
            tag = soup.new_tag("link", rel="alternate", hreflang=hl, href=url)
            anchor.insert_after(tag)
            anchor = tag


# ========== Header / footer / hamburger replacement ==========

def replace_header_footer(soup: BeautifulSoup, page_path: str, lang: str):
    active = PAGE_ACTIVE.get(page_path, "")
    new_header = BeautifulSoup(header_html(active, lang, current_path=f"/{page_path}"), "html.parser")
    new_footer = BeautifulSoup(footer_html(lang), "html.parser")

    old_header = soup.find("header", class_="header")
    if old_header:
        old_header.replace_with(new_header)
    else:
        # Insert at start of body
        body = soup.find("body")
        if body:
            body.insert(0, new_header)

    old_footer = soup.find("footer", class_="footer")
    if old_footer:
        old_footer.replace_with(new_footer)
    else:
        body = soup.find("body")
        if body:
            body.append(new_footer)

    # Remove all hamburger-related <script> blocks at end of body, then append HAMBURGER_JS
    for s in soup.find_all("script"):
        sc = s.string or ""
        if "hamburger" in sc.lower() and "addEventListener" in sc:
            s.decompose()
    # Append fresh hamburger script
    body = soup.find("body")
    if body:
        ham_soup = BeautifulSoup(HAMBURGER_JS, "html.parser")
        body.append(ham_soup)


# ========== CSS depth ==========

def fix_css_depth(soup: BeautifulSoup, page_path: str):
    """Adjust ../css/style.css path based on /lang/<path> depth."""
    # /lang/X/        → 2 levels up: ../../css/...
    # /lang/X/Y/      → 3 levels up: ../../../css/...
    parts = [p for p in page_path.split("/") if p]
    depth = 1 + len(parts)  # +1 for the lang dir
    prefix = "../" * depth
    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href", "")
        if "/css/style.css" in href or href.endswith("style.css"):
            link["href"] = prefix + "css/style.css"


# ========== Main translate function ==========

def translate_page(page_path: str, lang: str) -> bool:
    src_file = ROOT / page_path / "index.html"
    if not src_file.exists():
        print(f"  ✗ source missing: {src_file}")
        return False
    dst_file = ROOT / lang / page_path / "index.html"
    dst_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n=== {lang}/{page_path} ===")
    src_html = src_file.read_text(encoding="utf-8")
    soup = BeautifulSoup(src_html, "html.parser")

    # 1. Set <html lang>
    html_tag = soup.find("html")
    if html_tag:
        html_tag["lang"] = LANG_HTML_ATTR[lang]

    # 2. Collect all translatable strings
    text_nodes = collect_text_nodes(soup)
    attr_items = collect_attr_values(soup)
    meta_items = collect_meta_content(soup)

    # JSON-LD scripts: parse, walk, substitute
    jsonld_scripts = []
    jsonld_strings = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            walked = walk_jsonld(data, jsonld_strings)
            jsonld_scripts.append((script, walked))
        except (json.JSONDecodeError, TypeError):
            pass

    text_strings = [t for _, t in text_nodes]
    attr_strings = [v for _, _, v in attr_items]
    meta_strings = [orig for _, _, orig in meta_items]

    all_strings = text_strings + attr_strings + meta_strings + jsonld_strings
    print(f"  · text nodes: {len(text_strings)}, attrs: {len(attr_strings)}, meta: {len(meta_strings)}, jsonld: {len(jsonld_strings)}")

    if all_strings:
        translations = translate_all(all_strings, lang)
    else:
        translations = []

    # Split back
    n_text = len(text_strings)
    n_attr = len(attr_strings)
    n_meta = len(meta_strings)
    text_t = translations[:n_text]
    attr_t = translations[n_text:n_text + n_attr]
    meta_t = translations[n_text + n_attr:n_text + n_attr + n_meta]
    jsonld_t = translations[n_text + n_attr + n_meta:]

    # 3. Apply translations to text nodes
    for (node, _), new in zip(text_nodes, text_t):
        node.replace_with(NavigableString(new))

    # 4. Apply to attributes
    for (tag, attr, _), new in zip(attr_items, attr_t):
        tag[attr] = new

    # 5. Apply to meta + title
    for (kind, tag, _), new in zip(meta_items, meta_t):
        if kind == "title":
            tag.string = new
        else:
            tag["content"] = new

    # 6. Apply to JSON-LD
    for script, walked in jsonld_scripts:
        substituted = jsonld_substitute(walked, jsonld_t)
        # Add inLanguage at top level if missing
        if isinstance(substituted, dict):
            substituted.setdefault("inLanguage", LANG_HTML_ATTR[lang])
            if "@graph" in substituted and isinstance(substituted["@graph"], list):
                for node in substituted["@graph"]:
                    if isinstance(node, dict) and node.get("@type") in (
                        "WebSite", "WebPage", "Article", "FAQPage"
                    ):
                        node.setdefault("inLanguage", LANG_HTML_ATTR[lang])
        # Rewrite URLs in JSON-LD
        substituted = rewrite_jsonld_urls(substituted, lang)
        script.string = json.dumps(substituted, ensure_ascii=False, indent=2)

    # 7. Update canonical/hreflang/og:locale
    update_canonical_and_hreflang(soup, page_path, lang)

    # 8. Rewrite all internal links
    rewrite_all_links(soup, lang)

    # 9. Replace header/footer with localized versions
    replace_header_footer(soup, page_path, lang)

    # 10. Fix CSS depth
    fix_css_depth(soup, page_path)

    # 11. Write output
    out_html = str(soup)
    dst_file.write_text(out_html, encoding="utf-8")
    print(f"  ✓ wrote {dst_file} ({len(out_html)} bytes)")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("lang", help="lang code or 'all'")
    parser.add_argument("pages", nargs="+", help="page paths (e.g. bosses) or 'all'")
    parser.add_argument("--workers", type=int, default=4, help="concurrent chunk requests")
    args = parser.parse_args()

    langs = ["zh", "es", "pt", "de", "fr"] if args.lang == "all" else [args.lang]
    pages = HAND_PAGES if args.pages == ["all"] else args.pages

    total = len(langs) * len(pages)
    done = 0
    failed = []
    for lang in langs:
        if lang not in LANG_HTML_ATTR:
            print(f"!! unknown lang: {lang}")
            continue
        for page in pages:
            try:
                ok = translate_page(page, lang)
                done += 1
                if not ok:
                    failed.append(f"{lang}/{page}")
            except Exception as e:
                print(f"  ✗ FAILED {lang}/{page}: {e}", file=sys.stderr)
                failed.append(f"{lang}/{page}")
            print(f"  → progress: {done}/{total}", flush=True)

    print(f"\n=== Done: {done}/{total} ===")
    if failed:
        print("Failed:", failed)


if __name__ == "__main__":
    main()
