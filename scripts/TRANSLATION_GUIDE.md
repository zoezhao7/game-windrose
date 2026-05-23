# Translation Guide for Windrose Guides Multilingual Pages

This guide is the authoritative spec for translating hand-maintained English pages into
other languages. All translation agents should follow these rules.

## Source vs Target

- **Source**: English HTML at `F:\aicode\gamedoc\{path}\index.html` (e.g. `bosses/index.html`)
- **Target**: `F:\aicode\gamedoc\{lang}\{path}\index.html` (e.g. `zh/bosses/index.html`)
- The site root is `F:\aicode\gamedoc`. CSS path inside translated page should be `../../css/style.css` for 2-level deep paths like `/lang/X/`, and `../../../css/style.css` for 3-level deep like `/lang/X/Y/`.

## Glossary — Keep these in ENGLISH (do NOT translate)

**Game name & studio:** Windrose, Kraken Express, Pocketpair Publishing, Pocketpair, Steam, SteamCMD, WindroseServer.exe

**Boss names:** Thomas Richards, Israel Hands, High Priestess, Ghost Captain, Charon, Charon's Obols

**Biome names:** Coastal Jungle, Foothills, Cursed Swamps, Ashlands

**Ship names:** Sloop, Brigantine, Frigate, Ketch

**Crafting stations:** Workbench, Charcoal Kiln, Smelting Furnace, Weaponsmith, Armor Workshop, Alchemy Table, Cooking Fire, Shipyard, Millstone

**Item names (preserve as-is):** Stone Pickaxe, Copper Pickaxe, Iron Pickaxe, Stone Axe, Copper Axe, Bandage, Healing Potion, Antidote, Fast Travel Bell, Torn Sailcloth Bag, Sailor Backpack, Bosun Backpack, Rope, Sail Fabric, Plant Fiber, Coarse Fabric, Rough Hide, Tanned Leather, Copper Ingot, Iron Ingot, Copper Ore, Iron Ore, Sulfur, Gunpowder, Clay, Wood, Stone, Ash, Charcoal, Saber, Rapier, Club, Spear, Musket, Pistol, Blunderbuss, Heavy Club, Boarding Axe

**Talents/Trees:** Toughguy, Swashbuckler, Mariner, Ironclad, Gunner, Duelist, Sharpshooter

**Mechanics terms:** Early Access, co-op, dedicated server, NAT punch-through, UPnP, VPN, P2P, soulslite

**Acronyms / codes:** EA, NPC, POI, HP, MP, RPG, Lv, App ID, JSON, HTML, CSS

## What to translate

- All visible body text (paragraphs, headings, list items, button labels, table cells)
- `<title>` tag
- `<meta name="description">` and `<meta name="twitter:description">`
- All `og:title`, `og:description`, `twitter:title`
- `<img alt="...">` text
- `<button aria-label="...">` accessible labels (where descriptive)
- `<a aria-label="...">` accessible labels
- JSON-LD `name`, `headline`, `description`, FAQ `name`/`text` fields

## What to keep as-is

- All HTML tags, classes, IDs, data-* attributes
- All URLs in `href` and `src` (BUT see "Link rewriting" below)
- All `style="..."` inline CSS
- All `<script>` content (JavaScript code)
- All `<code>` and `<pre>` block contents
- File paths, command syntax
- Version numbers ("v0.4.2", "Patch 0.4.2")
- Dates in ISO format ("2026-04-14")
- Numerical values, percentages

## Link rewriting

Internal links in the original HTML reference English root paths. In the translated
version, internal links should point to the localized version if it exists, OR stay
pointing to the English root if no localized version exists.

**Paths that have localized versions (rewrite `/X` → `/{lang}/X`):**

- `/` (home)
- `/beginner-guide`, `/bosses`, `/ships`, `/weapons`, `/crafting`, `/resources`, `/guides`, `/builds`, `/faq`
- `/tools` (and `/tools/recipe-finder`, `/tools/progression-checklist`, `/tools/resource-planner`, `/tools/ship-selector`)
- `/news`
- `/search`
- `/server-guide`
- `/download`
- `/sources`
- `/database` (and all `/database/...` subpaths)
- `/about`, `/contact`, `/privacy`, `/terms`, `/pages` (we will translate these too)
- All `/guides/{slug}` strategy article paths
- `/crafting/{station}` subpaths (alchemy, building, cooking, smelting, workbench)
- `/bosses/{boss-slug}` paths (thomas-richards, israel-hands, high-priestess, ghost-captain, charons-obols)
- `/ships/{ship-slug}` paths (sloop, brigantine, frigate)
- `/resources/{resource-slug}` paths (copper, iron, clay, gunpowder, rare-materials)
- `/weapons/{weapons-slug}` paths (melee, ranged, armor)

**Paths that DO NOT have localized versions (KEEP as-is, pointing to English root):**

- `/database/items/{id}` (item detail pages — English only)
- `/news/{slug}` (news article details — English only)
- External URLs (Steam, playwindrose.com, etc.)
- Anchor links (`#some-id`)
- Image and asset URLs (`/imgs/...`, `/css/...`)

**Rewrite rule:** If a link href starts with `/` and the path (with or without trailing slash) is in the "has localized versions" list above, prepend `/{lang}` to make it `/{lang}/X`. Otherwise keep as-is.

Examples for Spanish (`lang=es`):
- `href="/bosses"` → `href="/es/bosses"`
- `href="/bosses/thomas-richards/"` → `href="/es/bosses/thomas-richards/"`
- `href="/database/items/saber/"` → `href="/database/items/saber/"` (unchanged — item details EN only)
- `href="https://store.steampowered.com/..."` → unchanged
- `href="/imgs/logo.png"` → unchanged
- `href="#faq"` → unchanged

## HTML head updates

1. `<html lang="en">` → `<html lang="{hlang}">` where hlang is the locale's HTML lang code:
   - zh → `zh-CN`
   - es → `es`
   - pt → `pt-BR`
   - de → `de`
   - fr → `fr`

2. `<link rel="canonical" href="https://windrosewiki.games/X">` → `https://windrosewiki.games/{lang}/X`

3. Add hreflang block AFTER canonical (replace any existing hreflang):
   ```html
   <link rel="alternate" hreflang="en" href="https://windrosewiki.games/X">
   <link rel="alternate" hreflang="es" href="https://windrosewiki.games/es/X">
   <link rel="alternate" hreflang="pt-BR" href="https://windrosewiki.games/pt/X">
   <link rel="alternate" hreflang="de" href="https://windrosewiki.games/de/X">
   <link rel="alternate" hreflang="fr" href="https://windrosewiki.games/fr/X">
   <link rel="alternate" hreflang="zh-CN" href="https://windrosewiki.games/zh/X">
   <link rel="alternate" hreflang="x-default" href="https://windrosewiki.games/X">
   ```
   (Replace X with the actual path, e.g. `bosses` or `crafting/alchemy`)

4. `<meta property="og:url" content="https://windrosewiki.games/X">` → update to localized

5. Add `<meta property="og:locale" content="{locale_og}">` where locale_og is:
   - zh → `zh_CN`
   - es → `es_ES`
   - pt → `pt_BR`
   - de → `de_DE`
   - fr → `fr_FR`

6. In JSON-LD:
   - Update all `"url"` fields to include `/{lang}` prefix
   - Update all `@id` URLs in `@graph`
   - Add `"inLanguage": "{hlang}"` to WebPage/WebSite entries
   - Translate `name`, `headline`, `description`, FAQ `name`/`text` to target language
   - Update breadcrumb item names to translated equivalents

## Header and footer replacement

The hand-maintained EN pages have hardcoded `<header>` and `<footer>` blocks.
Replace them with localized versions generated from `templates.py`.

**To get the localized header/footer**, use Python:

```python
import sys
sys.path.insert(0, r'F:\aicode\gamedoc\scripts')
from templates import header_html, footer_html, HAMBURGER_JS
from i18n import lang_switcher_html

lang = "es"  # or zh/pt/de/fr
header = header_html("bosses", lang, current_path="/bosses")  # adjust "bosses" and "/bosses" per page
footer = footer_html(lang)
print(header)
print(footer)
print(HAMBURGER_JS)
```

For the `active` arg (first positional): use the top-level section name without slash:
- bosses page → `"bosses"`
- crafting/alchemy → `"crafting"` (still highlights the Crafting nav)
- guides/mining-routes → `"guides"`
- weapons/melee → `"weapons"`

For `current_path`: use the full path WITH leading slash:
- bosses → `"/bosses"`
- crafting/alchemy → `"/crafting/alchemy"`
- guides → `"/guides"`

Replace the entire `<header class="header">...</header>` block in source with the
output of `header_html()`.

Replace the entire `<footer class="footer">...</footer>` block with `footer_html()`.

Replace the existing hamburger script at the end of body with `HAMBURGER_JS`.

## Quality criteria

- Translation should be natural and idiomatic for native readers
- Game-specific terminology must use the glossary above
- Don't add extra translator commentary or notes
- Don't change the page structure, layout, or design
- Preserve all interactive elements (forms, scripts, click handlers)
- Don't break HTML validity (close all tags, escape quotes, etc.)

## Language style notes

- **Chinese (zh)**: Simplified Chinese, gamer-friendly tone. Use 你 (informal). Brand "Windrose" stays English, refer to site as "Windrose 攻略站".
- **Spanish (es)**: Neutral Latin American Spanish. Use "tú" (informal). Avoid Spain-specific vocabulary where possible.
- **Portuguese (pt)**: Brazilian Portuguese (pt-BR). Use "você" (informal).
- **German (de)**: Use "Du" (informal, gaming standard). Compound nouns are fine.
- **French (fr)**: Modern, accessible French. Use "tu" (informal). Avoid overly formal constructions.

## Validation checklist (agent should self-verify)

After writing each translated file, verify:
1. File is valid HTML (no unclosed tags)
2. `<html lang="...">` has correct locale
3. canonical URL contains `/{lang}/`
4. hreflang block present with all 6 languages + x-default
5. Internal links rewritten correctly (spot-check 5)
6. No untranslated paragraphs left in body
7. Glossary terms (e.g. "Brigantine") stayed in English
8. JSON-LD has correct inLanguage
