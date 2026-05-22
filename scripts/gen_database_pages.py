"""
从 data/*.json 批量生成 Database 双栏布局页面。
侧边栏结构：
  类别
  概述
  所有商品  976   ← 绿色高亮
  ▶ Weapons     77   ← 点击展开/折叠
    View all Weapons  ← 绿色链接
    Melee Weapons  43
    Ranged Weapons 19
    ...
"""
import json, os, html as html_mod
from templates import header_html, footer_html, HAMBURGER_JS
from i18n import t, lang_url, hreflang_tags, LANG_HTML, DEFAULT, SUPPORTED

PROJECT = r"F:\aicode\gamedoc"

# ── 侧边栏结构定义 ───────────────────────────────────────
# NOTE: 分类层级定义
SIDEBAR_CATS = [
    {
        "key": "weapons", "label": "Weapons", "count": 77,
        "label_trans": "database.weapons",
        "view_all": "/database/weapons/", "view_all_label": "View all Weapons",
        "children": [
            {"key": "melee_weapons", "label": "Melee Weapons", "count": 43, "href": "/database/weapons/melee/"},
            {"key": "ranged_weapons", "label": "Ranged Weapons", "count": 19, "href": "/database/weapons/ranged/"},
            {"key": "tools", "label": "Tools", "count": 8, "href": "/database/weapons/tools/"},
            {"key": "ammo", "label": "Ammo", "count": 7, "href": "/database/weapons/ammo/"},
        ]
    },
    {
        "key": "ships", "label": "Ships", "count": 45,
        "label_trans": "database.ships_label",
        "view_all": "/database/ships/", "view_all_label": "View all Ships",
        "children": [
            {"key": "ship_weapons", "label": "Ship Weapons", "count": 29, "href": "/database/ships/ship-weapons/"},
            {"key": "hull_modules", "label": "Hull Modules", "count": 10, "href": "/database/ships/hull-modules/"},
            {"key": "combat_orders", "label": "Combat Orders", "count": 5, "href": "/database/ships/combat-orders/"},
        ]
    },
    {
        "key": "resources", "label": "Resources", "count": 138,
        "label_trans": "database.resources_label",
        "view_all": "/database/resources/", "view_all_label": "View all Resources",
        "children": [
            {"key": "resources_label", "label": "Resources", "count": 135, "href": "/database/resources/resources/"},
            {"key": "metals", "label": "Metals", "count": 3, "href": "/database/resources/metals/"},
        ]
    },
    {
        "key": "consumables", "label": "Consumables", "count": 65,
        "label_trans": "database.consumables_label",
        "view_all": "/database/consumables/", "view_all_label": "View all Consumables",
        "children": [
            {"key": "food", "label": "Food", "count": 50, "href": "/database/consumables/food/"},
            {"key": "alchemy", "label": "Alchemy", "count": 11, "href": "/database/consumables/alchemy/"},
            {"key": "medicine", "label": "Medicine", "count": 4, "href": "/database/consumables/medicine/"},
        ]
    },
    {
        "key": "equipment", "label": "Equipment", "count": 106,
        "label_trans": "database.equipment_label",
        "view_all": "/database/equipment/", "view_all_label": "View all Equipment",
        "children": [
            {"key": "armor", "label": "Armor", "count": 41, "href": "/database/equipment/armor/"},
            {"key": "rings", "label": "Rings", "count": 36, "href": "/database/equipment/rings/"},
            {"key": "necklaces", "label": "Necklaces", "count": 24, "href": "/database/equipment/necklaces/"},
            {"key": "backpacks", "label": "Backpacks", "count": 5, "href": "/database/equipment/backpacks/"},
        ]
    },
    {
        "key": "misc", "label": "Misc", "count": 520,
        "label_trans": "database.misc_label",
        "view_all": "/database/misc/", "view_all_label": "View all Misc",
        "children": [
            {"key": "misc_label", "label": "Misc", "count": 514, "href": "/database/misc/misc/"},
            {"key": "default_label", "label": "Default", "count": 6, "href": "/database/misc/default/"},
        ]
    },
]

TOTAL_ITEMS = sum(c["count"] for c in SIDEBAR_CATS)

CURRENT_LANG = DEFAULT


def sidebar_html(active_key="all", lang=None):
    if lang is None:
        lang = CURRENT_LANG
    """
    生成侧边栏 HTML，active_key 决定哪个分类高亮。
    当某个 category key 匹配 active_key 时该分类展开，否则折叠。
    """
    lines = []
    lines.append('<aside class="db-sidebar">')
    lines.append(f'  <div class="db-sidebar-title">{html_mod.escape(t("database.sidebar_categories", lang))}</div>')
    lines.append('  <ul class="db-nav">')

    # 概述
    ov_cls = ' active' if active_key == "overview" else ""
    overview_label = t("database.sidebar_overview", lang)
    overview_url = lang_url("/database/", lang)
    lines.append(f'    <li><a href="{overview_url}" class="db-nav-top{ov_cls}">{html_mod.escape(overview_label)}</a></li>')

    # 所有商品
    all_cls = ' active' if active_key == "all" else ""
    all_label = t("database.sidebar_all_items", lang)
    all_url = lang_url("/database/", lang)
    lines.append(f'    <li><a href="{all_url}" class="db-nav-top{all_cls}">{html_mod.escape(all_label)} <span class="db-count">{TOTAL_ITEMS}</span></a></li>')

    # 各分类
    for cat in SIDEBAR_CATS:
        is_open = (cat["key"] == active_key)
        arrow = "▼" if is_open else "▶"
        collapsed = "" if is_open else " collapsed"

        # 翻译分类标签：优先用 label_trans (来自 SIDEBAR_CATS) 指定的 key
        cat_label_key = cat.get("label_trans", f"database.{cat['key']}")
        cat_label = t(cat_label_key, lang)
        # 回退到原始 English label
        if cat_label == cat_label_key:
            cat_label = cat["label"]

        view_all_url = lang_url(cat["view_all"], lang)
        view_all_label = t("database.view_all", lang, name=cat["label"])

        lines.append(f'    <li>')
        lines.append(f'      <div class="db-cat" data-cat="{cat["key"]}">')
        lines.append(f'        <span class="db-arrow">{arrow}</span>')
        lines.append(f'        <span class="db-cat-label">{html_mod.escape(cat_label)}</span>')
        lines.append(f'        <span class="db-count">{cat["count"]}</span>')
        lines.append(f'      </div>')
        lines.append(f'      <ul class="db-sub{collapsed}" id="sub-{cat["key"]}">')
        lines.append(f'        <li><a href="{view_all_url}" class="db-sub-viewall">{html_mod.escape(view_all_label)}</a></li>')
        for child in cat["children"]:
            child_label_key = f"database.{child['key']}"
            child_label = t(child_label_key, lang)
            if child_label == child_label_key:
                child_label = child["label"]
            child_url = lang_url(child["href"], lang)
            lines.append(f'        <li><a href="{child_url}" class="db-sub-item">{html_mod.escape(child_label)} <span class="db-count">{child["count"]}</span></a></li>')
        lines.append(f'      </ul>')
        lines.append(f'    </li>')

    lines.append('  </ul>')
    lines.append('</aside>')
    return "\n".join(lines)


# ── 侧边栏 JS（展开/折叠逻辑） ───────────────────────────
SIDEBAR_JS = """
document.querySelectorAll('.db-cat').forEach(function(cat){
    cat.addEventListener('click',function(){
        var sub=document.getElementById('sub-'+this.dataset.cat);
        var arrow=this.querySelector('.db-arrow');
        if(sub){
            sub.classList.toggle('collapsed');
            arrow.textContent=sub.classList.contains('collapsed')?'▶':'▼';
        }
    });
});
"""


# ── 页面模板 ──────────────────────────────────────────────
def make_page(title, meta_desc, breadcrumb, active_key, heading, desc, cards_html, guide_link="", css_depth=2, lang=None, rel_path=""):
    if lang is None:
        lang = CURRENT_LANG
    guide_banner = ""
    if guide_link:
        guide_label = t("common.view_full_guide", lang)
        guide_banner = f'<div class="db-guide-link">📖 <a href="{guide_link}">{html_mod.escape(guide_label)}</a></div>'

    hlang = LANG_HTML.get(lang, lang)
    card_count = cards_html.count('db-card')

    # 翻译后的 UI 文本
    search_ph = t("database.search_placeholder", lang)
    showing = t("database.showing_items", lang, n=card_count)
    sort_label = t("database.sort", lang)
    sort_name = t("database.sort_name", lang)
    sort_rarity = t("database.sort_rarity", lang)
    db_breadcrumb = t("database.breadcrumb", lang)
    db_header = t("database.header_meta", lang)

    # hreflang
    # breadcrumb slug 需要从当前页面推断（由 write_page 传入）
    hreflang_html = ""  # 在 write_page 中补全

    # 语言切换器相关：header 和 footer
    h = header_html("database", lang, current_path=f"/database/{rel_path}" if rel_path else "/database")
    f = footer_html(lang)

    return f"""<!DOCTYPE html>
<html lang="{hlang}">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_mod.escape(title)} | Windrose Guides</title>
<meta name="description" content="{html_mod.escape(meta_desc)}">
<link rel="stylesheet" href="/css/style.css">
<link rel="stylesheet" href="/database/db-style.css">
</head>
<body>
{h}

<div class="db-layout">
{sidebar_html(active_key, lang)}
<main class="db-main">
    <div class="db-breadcrumbs"><span>{html_mod.escape(db_breadcrumb)}</span> / {breadcrumb}</div>
    <div class="db-header-meta">{html_mod.escape(db_header)}</div>
    <h1>{heading}</h1>
    <p class="db-desc">{desc}</p>
    {guide_banner}
    <div class="db-toolbar">
        <input type="text" class="db-search-input" placeholder="{html_mod.escape(search_ph)}" id="dbSearch" onkeyup="filterCards()">
        <div class="db-toolbar-meta">{html_mod.escape(showing)}
            <label>{html_mod.escape(sort_label)} <select class="db-sort-select" onchange="sortCards(this.value)"><option value="name">{html_mod.escape(sort_name)}</option><option value="rarity">{html_mod.escape(sort_rarity)}</option></select></label>
        </div>
    </div>
    <div class="db-grid" id="dbGrid">
{cards_html}
    </div>
</main>
</div>
{f}
<script>
document.querySelector('.hamburger').addEventListener('click',function(){{this.classList.toggle('open');document.querySelector('.nav-links').classList.toggle('open');}});
function filterCards(){{var q=document.getElementById('dbSearch').value.toLowerCase();document.querySelectorAll('.db-card').forEach(function(c){{c.style.display=c.textContent.toLowerCase().includes(q)?'':'none';}});}}
{SIDEBAR_JS}
function sortCards(by){{
    var grid=document.getElementById('dbGrid');
    var cards=Array.from(grid.querySelectorAll('.db-card'));
    cards.sort(function(a,b){{
        if(by==='name')return a.querySelector('.db-card-title').textContent.localeCompare(b.querySelector('.db-card-title').textContent);
        var ro={{'epic':0,'rare':1,'uncommon':2,'common':3}};
        var ra=a.querySelector('.db-badge'),rb=b.querySelector('.db-badge');
        var va=ra?ro[ra.textContent.toLowerCase().trim()]||9:9;
        var vb=rb?ro[rb.textContent.toLowerCase().trim()]||9:9;
        return va-vb;
    }});
    cards.forEach(function(c){{grid.appendChild(c);}});
}}
</script>
</body></html>"""


# ── 卡片 HTML ────────────────────────────────────────────
def item_link(item_id):
    """生成物品详情页链接"""
    return f"/database/items/{item_id}/"

def card(name, subtype, rarity="uncommon", link=None, icon="", item_id=""):
    """link 为 None 时自动从 item_id 生成"""
    if link is None:
        link = item_link(item_id) if item_id else "#"
    rarity_cls = {"epic":"rarity-epic","rare":"rarity-rare","uncommon":"rarity-uncommon","common":"rarity-common"}.get(rarity, "rarity-uncommon")
    title_cls = {"epic":"title-epic","rare":"title-rare","uncommon":"title-uncommon"}.get(rarity, "")
    icon_html = f'<img src="{icon}" alt="{html_mod.escape(name)}" onerror="this.style.display=\'none\'">' if icon else ""
    return f"""        <a href="{link}" class="db-card">
            <div class="db-card-icon">{icon_html}</div>
            <div class="db-card-content">
                <h3 class="db-card-title {title_cls}">{html_mod.escape(name)}</h3>
                <p class="db-card-type">{html_mod.escape(subtype)}</p>
                <span class="db-badge {rarity_cls}">{rarity.capitalize()}</span>
            </div>
        </a>"""


def write_page(rel_path, content, lang=None):
    """写入页面文件，支持多语言目录结构"""
    if lang is None:
        lang = CURRENT_LANG
    if lang == DEFAULT:
        full_path = os.path.join(PROJECT, "database", rel_path, "index.html")
    else:
        full_path = os.path.join(PROJECT, lang, "database", rel_path, "index.html")
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)


# ── 加载数据 ──────────────────────────────────────────────
with open(os.path.join(PROJECT, "data/weapons.json"), encoding="utf-8") as f:
    weapons_data = json.load(f)
with open(os.path.join(PROJECT, "data/bosses.json"), encoding="utf-8") as f:
    bosses_data = json.load(f)
with open(os.path.join(PROJECT, "data/recipes.json"), encoding="utf-8") as f:
    recipes_data = json.load(f)
with open(os.path.join(PROJECT, "data/resources.json"), encoding="utf-8") as f:
    resources_data = json.load(f)
with open(os.path.join(PROJECT, "data/ships.json"), encoding="utf-8") as f:
    ships_data = json.load(f)
with open(os.path.join(PROJECT, "data/scraped_items_v2.json"), encoding="utf-8") as f:
    scraped_data = json.load(f)

# 按名称建立 scraped 数据索引，用于合并到 weapons.json
SCRAPED_BY_NAME = {}
for item in scraped_data.get("items", []):
    name = item.get("name", "").strip().lower()
    if name:
        existing = SCRAPED_BY_NAME.get(name)
        if not existing or (item.get("description") and not existing.get("description")):
            SCRAPED_BY_NAME[name] = item

# NOTE: 同时匹配旧分类名和采集数据的分类名，按 id 去重，优先保留有 icon 的条目
# 旧数据中混入的非武器条目黑名单（攻略表格行标题被错误当作武器条目）
_GARBAGE_IDS = {
    "standard-pirates", "heavy-armored-enemies", "fast-agile-enemies",
    "enemy-groups", "bosses",
}

def _dedup_items(items):
    """按 id 去重，优先保留有 icon 字段的条目"""
    seen = {}
    for w in items:
        wid = w["id"]
        if wid in _GARBAGE_IDS:
            continue
        if wid not in seen or (w.get("icon") and not seen[wid].get("icon")):
            seen[wid] = w
    return list(seen.values())

def _merge_scraped(weapon_items):
    """将 scraped 数据按名称合并到 weapons.json 数据中，避免重复卡片"""
    merged_by_name = {}
    for w in weapon_items:
        name = w.get("name", "").strip().lower()
        if not name:
            continue
        scraped = SCRAPED_BY_NAME.get(name)
        if scraped:
            # 使用 scraped 数据，但保留 weapons.json 中的 category 和 best_use 等有用字段
            merged = dict(scraped)
            if w.get("category") and not merged.get("category"):
                merged["category"] = w["category"]
            if w.get("best_use") and not merged.get("best_use"):
                merged["best_use"] = w["best_use"]
            merged_by_name[name] = merged
        else:
            # 没有 scraped 数据时，尝试从旧数据提取描述并修复 tier
            merged = dict(w)
            if merged.get("tier") in ("unranked", None):
                merged["tier"] = "common"
            if not merged.get("description") and merged.get("pros"):
                # 从 pros 提取描述性文字（跳过速度/伤害等标签）
                for p in merged["pros"]:
                    if len(p) > 15 and ";" in p:
                        merged["description"] = p
                        break
                if not merged.get("description"):
                    # 取最长的一条作为描述
                    descs = [p for p in merged["pros"] if len(p) > 10]
                    if descs:
                        merged["description"] = max(descs, key=len)
            merged_by_name[name] = merged
    return list(merged_by_name.values())

_all_weapons_raw = weapons_data.get("items", [])
# 合并 scraped 数据（按名称去重，避免同一武器出现两个卡片）
_all_weapons = _merge_scraped(_all_weapons_raw)
melee_items = _dedup_items([w for w in _all_weapons if w.get("category") in ("melee", "melee-weapon")])
ranged_items = _dedup_items([w for w in _all_weapons if w.get("category") in ("ranged", "range-weapon")])
ammo_items = _dedup_items([w for w in _all_weapons if w.get("category") == "ammo"])
tool_items = _dedup_items([w for w in _all_weapons if w.get("category") == "tool"])
armor_items = _dedup_items([w for w in _all_weapons if w.get("category") == "armor"])

ring_items = _dedup_items([w for w in _all_weapons if w.get("category") == "ring"])
necklace_items = _dedup_items([w for w in _all_weapons if w.get("category") == "necklace"])
backpack_items = _dedup_items([w for w in _all_weapons if w.get("category") == "backpack"])

_ship_items = ships_data.get("items", [])
ship_weapon_items = [s for s in _ship_items if s.get("category") == "ship-weapon"]
hull_module_items = [s for s in _ship_items if s.get("category") == "ship-hull-mod"]
combat_order_items = [s for s in _ship_items if s.get("category") == "ship-combat-order"]

_res_all = resources_data.get("items", []) + resources_data.get("resources", [])
alchemy_items = [r for r in _res_all if r.get("category") == "alchemy"]
medicine_items = [r for r in _res_all if r.get("category") == "medicine"]
metal_items = [r for r in _res_all if r.get("category") == "metal"]

_all_recipes_raw = recipes_data.get("items", [])
misc_items = [r for r in _all_recipes_raw if r.get("category") in ("misc", "default")]

# NOTE: 默认 fallback 图标，仅在数据缺少 icon 时使用
FALLBACK_MELEE_ICON = "/imgs/icon_weapon.png"
FALLBACK_RANGED_ICON = "/imgs/weapon_musket.png"

tier_weapons = []
for tier_name, tier_items in weapons_data.get("tier_list", {}).get("tiers", {}).items():
    rarity_map = {"S": "epic", "A": "rare", "B": "uncommon", "C": "common"}
    for item in tier_items:
        tier_weapons.append({"name": item["name"], "type": item["type"], "tier": tier_name, "rarity": rarity_map.get(tier_name, "uncommon")})


# ── 生成页面 ──────────────────────────────────────────────
# NOTE: 页面生成代码在模块级别执行（import 时自动生成英文版）。
# 对于非英文语言，调用 build_other_languages() 函数。

def build_all(lang=DEFAULT):
    """Generate all database list pages for the given language."""
    global CURRENT_LANG
    CURRENT_LANG = lang

    # 1. Weapons 总页面
    cards = []
    seen_names = set()
    for w in melee_items:
        icon = w.get("icon", FALLBACK_MELEE_ICON)
        rarity = w.get("tier", "uncommon")
        cards.append(card(w["name"], "Melee Weapon", rarity, icon=icon, item_id=w["id"]))
        seen_names.add(w["name"])
    for w in ranged_items:
        icon = w.get("icon", FALLBACK_RANGED_ICON)
        rarity = w.get("tier", "rare")
        cards.append(card(w["name"], "Ranged Weapon", rarity, icon=icon, item_id=w["id"]))
        seen_names.add(w["name"])
    for w in ammo_items:
        icon = w.get("icon", "")
        rarity = w.get("tier", "uncommon")
        cards.append(card(w["name"], "Ammo", rarity, icon=icon, item_id=w["id"]))
        seen_names.add(w["name"])
    for w in tool_items:
        icon = w.get("icon", "")
        rarity = w.get("tier", "uncommon")
        cards.append(card(w["name"], "Tool", rarity, icon=icon, item_id=w["id"]))
        seen_names.add(w["name"])
    for w in armor_items:
        icon = w.get("icon", "")
        rarity = w.get("tier", "epic")
        cards.append(card(w["name"], "Armor Set", rarity, icon=icon, item_id=w["id"]))
        seen_names.add(w["name"])
    for tw in tier_weapons:
        if tw["name"] not in seen_names:
            tw_id = tw["name"].lower().replace(" ", "-").replace("'", "")
            icon = FALLBACK_MELEE_ICON if tw["type"] == "melee" else FALLBACK_RANGED_ICON
            cards.append(card(tw["name"], f'{tw["type"].capitalize()} • Tier {tw["tier"]}', tw["rarity"], icon=icon, item_id=tw_id))
            seen_names.add(tw["name"])
    write_page("weapons", make_page("Windrose Weapons Database", "Browse all weapons in Windrose.", "Weapons", "weapons", "Weapons", f"{len(cards)} weapons.", "\n".join(cards), "/weapons/", rel_path="weapons"))
    print(f"  database/weapons/ ({len(cards)} cards)")

    # 1a. Melee
    cards = []
    seen_names = set()
    for w in melee_items:
        icon = w.get("icon", FALLBACK_MELEE_ICON)
        rarity = w.get("tier", "uncommon")
        subtype = w.get("description", "")[:40] + "…" if w.get("description") else w.get("best_use", "General")
        cards.append(card(w["name"], f'Melee • {subtype}', rarity, icon=icon, item_id=w["id"]))
        seen_names.add(w["name"])
    for tw in tier_weapons:
        if tw["type"] == "melee" and tw["name"] not in seen_names:
            tw_id = tw["name"].lower().replace(" ", "-").replace("'", "")
            cards.append(card(tw["name"], f'Melee • Tier {tw["tier"]}', tw["rarity"], icon=FALLBACK_MELEE_ICON, item_id=tw_id))
            seen_names.add(tw["name"])
    write_page("weapons/melee", make_page("Melee Weapons", "All melee weapons in Windrose.", "Weapons / Melee", "weapons", "Melee Weapons", f"{len(cards)} melee weapons.", "\n".join(cards), "/weapons/melee/", css_depth=3, rel_path="weapons/melee"))
    print(f"  database/weapons/melee/ ({len(cards)} cards)")

    # 1b. Ranged
    cards = []
    seen_names = set()
    for w in ranged_items:
        icon = w.get("icon", FALLBACK_RANGED_ICON)
        rarity = w.get("tier", "rare")
        subtype = w.get("description", "")[:40] + "…" if w.get("description") else w.get("best_use", "General")
        cards.append(card(w["name"], f'Ranged • {subtype}', rarity, icon=icon, item_id=w["id"]))
        seen_names.add(w["name"])
    for tw in tier_weapons:
        if tw["type"] == "ranged" and tw["name"] not in seen_names:
            tw_id = tw["name"].lower().replace(" ", "-").replace("'", "")
            cards.append(card(tw["name"], f'Ranged • Tier {tw["tier"]}', tw["rarity"], icon=FALLBACK_RANGED_ICON, item_id=tw_id))
            seen_names.add(tw["name"])
    write_page("weapons/ranged", make_page("Ranged Weapons", "All ranged weapons.", "Weapons / Ranged", "weapons", "Ranged Weapons", f"{len(cards)} ranged weapons.", "\n".join(cards), "/weapons/ranged/", css_depth=3, rel_path="weapons/ranged"))
    print(f"  database/weapons/ranged/ ({len(cards)} cards)")

    # 1c. Ammo
    cards = []
    seen_names = set()
    for w in ammo_items:
        icon = w.get("icon", "")
        rarity = w.get("tier", "uncommon")
        cards.append(card(w["name"], "Ammo", rarity, icon=icon, item_id=w["id"]))
        seen_names.add(w["name"])
    for r in recipes_data.get("items", []):
        if r.get("category") == "ammo" and r["name"] not in seen_names:
            icon = r.get("icon", "")
            cards.append(card(r["name"], "Ammo", "uncommon", icon=icon, item_id=r["id"]))
            seen_names.add(r["name"])
    write_page("weapons/ammo", make_page("Ammo", "All ammo types.", "Weapons / Ammo", "weapons", "Ammunition", f"{len(cards)} ammo types.", "\n".join(cards), css_depth=3, rel_path="weapons/ammo"))
    print(f"  database/weapons/ammo/ ({len(cards)} cards)")

    # 1d. Tools
    cards = []
    seen_names = set()
    for w in tool_items:
        icon = w.get("icon", "")
        rarity = w.get("tier", "uncommon")
        cards.append(card(w["name"], f'Tool', rarity, icon=icon, item_id=w["id"]))
        seen_names.add(w["name"])
    for r in recipes_data.get("items", []):
        if r.get("category") == "tool" and r["name"] not in seen_names:
            rarity = "uncommon" if r.get("station_level", 1) == 1 else "rare"
            icon = r.get("icon", "")
            cards.append(card(r["name"], f'Tool • {r.get("station","?")}', rarity, icon=icon, item_id=r["id"]))
            seen_names.add(r["name"])
    write_page("weapons/tools", make_page("Tools", "All tools.", "Weapons / Tools", "weapons", "Tools", f"{len(cards)} tools.", "\n".join(cards), css_depth=3, rel_path="weapons/tools"))
    print(f"  database/weapons/tools/ ({len(cards)} cards)")

    # 2. Armor
    cards = []
    for w in armor_items:
        icon = w.get("icon", "")
        rarity = w.get("tier", "rare")
        cards.append(card(w["name"], f'Armor • {w.get("best_use", "General")}', rarity, icon=icon, item_id=w["id"]))
    write_page("equipment/armor", make_page("Windrose Armor", "All armor sets.", "Equipment / Armor", "equipment", "Armor Sets", f"{len(cards)} armor sets.", "\n".join(cards), css_depth=3, rel_path="equipment/armor"))
    print(f"  database/equipment/armor/ ({len(cards)} cards)")

    # 3. Bosses
    cards = []
    img_map = {"thomas-richards": "/imgs/thomas_richards.png", "israel-hands": "/imgs/israel_hands.png", "high-priestess": "/imgs/high_priestess.png", "ghost-captain": "/imgs/ghost_captain.png"}
    for b in bosses_data.get("items", []):
        rarity = "epic" if b.get("category") == "story" else "rare"
        boss_link = f"/bosses/{b['id']}/"
        cards.append(card(b["name"], f'{b.get("biome","Unknown")} • Lv {b.get("recommended_level","?")}', rarity, icon=img_map.get(b["id"], ""), link=boss_link))
    write_page("bosses", make_page("Windrose Bosses", "All bosses.", "Bosses", "all", "Bosses", f"{len(cards)} boss encounters.", "\n".join(cards), "/bosses/", rel_path="bosses"))
    print(f"  database/bosses/ ({len(cards)} cards)")

    # 4. Crafting 总页面
    all_recipes = recipes_data.get("items", [])
    station_groups = {}
    for r in all_recipes:
        station = r.get("station", "Unknown")
        station_groups.setdefault(station, []).append(r)

    cards = []
    for r in all_recipes:
        station = r.get("station", "Unknown")
        rarity = "uncommon" if r.get("station_level", 1) == 1 else ("rare" if r.get("station_level", 1) == 2 else "epic")
        cards.append(card(r["name"], f'{station} Lv{r.get("station_level","?")} • {r.get("category","item").capitalize()}', rarity, icon=r.get("icon", ""), item_id=r["id"]))
    write_page("crafting", make_page("Windrose Crafting", "All crafting recipes.", "Crafting", "all", "Crafting Recipes", f"{len(cards)} recipes.", "\n".join(cards), "/crafting/", rel_path="crafting"))
    print(f"  database/crafting/ ({len(cards)} cards)")

    # 4a. 各工作站子页面
    for station_name, recipes in station_groups.items():
        station_slug = station_name.lower().replace(" ", "-")
        cards = []
        for r in recipes:
            mats_raw = r.get("materials", [])[:3]
            mats = ", ".join([f'{m.get("quantity","?")}x {m.get("item","?")}' if isinstance(m, dict) else str(m) for m in mats_raw])
            rarity = "uncommon" if r.get("station_level", 1) == 1 else ("rare" if r.get("station_level", 1) == 2 else "epic")
            cards.append(card(r["name"], mats if mats else r.get("category","item").capitalize(), rarity, icon=r.get("icon", ""), item_id=r["id"]))
        write_page(f"crafting/{station_slug}", make_page(f"{station_name} Recipes", f"All {station_name} recipes.", f"Crafting / {station_name}", "all", f"{station_name} Recipes", f"{len(cards)} recipes.", "\n".join(cards), f"/crafting/{station_slug}/", css_depth=3))
        print(f"  database/crafting/{station_slug}/ ({len(cards)} cards)")

    # 5. Resources
    cards = []
    for r in resources_data.get("items", []):
        rarity = r.get("rarity", "common")
        biome = ", ".join(r.get("biomes", [])[:2])
        cards.append(card(r["name"], f'{biome} • {r.get("tool_required","Unknown")}', rarity, icon=r.get("icon", ""), item_id=r["id"]))
    for r in resources_data.get("resources", []):
        rarity = r.get("rarity", "common")
        biome = ", ".join(r.get("biome", [])[:2])
        cards.append(card(r["name"], f'{biome} • {r.get("tool_required","None")}', rarity, icon=r.get("icon", ""), item_id=r["id"]))
    write_page("resources", make_page("Windrose Resources", "All resources.", "Resources", "resources", "Resources", f"{len(cards)} resources.", "\n".join(cards), "/resources/", rel_path="resources"))
    print(f"  database/resources/ ({len(cards)} cards)")

    # 5a. Resources sub (without metals)
    non_metal = [r for r in resources_data.get("items", []) if r.get("category") != "metal"] + \
                [r for r in resources_data.get("resources", []) if r.get("category") != "metal"]
    cards_rs = []
    for r in non_metal:
        rarity = r.get("rarity", "common")
        biome = ", ".join(r.get("biomes", r.get("biome", []))[:2])
        cards_rs.append(card(r["name"], f'{biome} • {r.get("tool_required","Unknown")}', rarity, icon=r.get("icon", ""), item_id=r.get("id", r["name"].lower().replace(" ", "-"))))
    write_page("resources/resources", make_page("Windrose Resources", "All resources.", "Resources / Resources", "resources", "Resources", f"{len(cards_rs)} resources.", "\n".join(cards_rs), css_depth=3, rel_path="resources/resources"))
    print(f"  database/resources/resources/ ({len(cards_rs)} cards)")

    # 6. Ships
    cards = []
    ship_imgs = {"ketch": "/imgs/ship_ketch.png", "brigantine": "/imgs/ship_brigantine.png", "frigate": "/imgs/ship_frigate.png"}
    for s in ships_data.get("ships", []):
        cards.append(card(s["name"], f'Tier {s["tier"]} • {s["crew"]} crew • {s["cannons"]} cannons', "epic" if s["tier"]==3 else ("rare" if s["tier"]==2 else "uncommon"), icon=ship_imgs.get(s["id"], ""), item_id=s["id"]))
        for v in s.get("variants", []):
            v_id = v["name"].lower().replace(" ", "-").replace("'", "")
            cards.append(card(v["name"], f'{v.get("notes","")} • {v["cannons"]} cannons', "rare", icon=ship_imgs.get(s["id"], ""), item_id=s["id"]))
    write_page("ships", make_page("Windrose Ships", "All ships.", "Ships", "ships", "Ships & Variants", f"{len(cards)} ships.", "\n".join(cards), "/ships/", rel_path="ships"))
    print(f"  database/ships/ ({len(cards)} cards)")

    # 7. Consumables overview
    food_cards = []
    for r in recipes_data.get("items", []):
        if r.get("category") in ("consumable", "food"):
            food_cards.append(card(r["name"], f'{r.get("station","?")}', "uncommon", icon=r.get("icon", ""), item_id=r["id"]))
    alch_cards = []
    for r in alchemy_items:
        rarity_c = r.get("rarity", "uncommon")
        desc_c = r.get("description", "") or r.get("effect", "")
        alch_cards.append(card(r["name"], desc_c[:40] if desc_c else "Alchemy", rarity_c, icon=r.get("icon", ""), item_id=r.get("id", r["name"].lower().replace(" ", "-"))))
    med_cards = []
    for r in medicine_items:
        rarity_c = r.get("rarity", "uncommon")
        desc_c = r.get("description", "") or r.get("effect", "")
        med_cards.append(card(r["name"], desc_c[:40] if desc_c else "Medicine", rarity_c, icon=r.get("icon", ""), item_id=r.get("id", r["name"].lower().replace(" ", "-"))))
    all_consumable_cards = food_cards + alch_cards + med_cards
    write_page("consumables", make_page("Windrose Consumables", "All consumables, food, alchemy and medicine.", "Consumables", "consumables", "Consumables", f"{len(all_consumable_cards)} items." if all_consumable_cards else "Data coming soon.", "\n".join(all_consumable_cards) if all_consumable_cards else '<div style="text-align:center;padding:3rem;color:#8b949e;">🍖 Coming soon</div>', rel_path="consumables"))
    print(f"  database/consumables/ ({len(all_consumable_cards)} cards)")

    # 7a. Food
    write_page("consumables/food", make_page("Windrose Food", "All food and consumables.", "Consumables / Food", "consumables", "Food & Consumables", f"{len(food_cards)} items." if food_cards else "Data coming soon.", "\n".join(food_cards) if food_cards else '<div style="text-align:center;padding:3rem;color:#8b949e;">🍖 Coming soon</div>', css_depth=3, rel_path="consumables/food"))
    print(f"  database/consumables/food/ ({len(food_cards)} cards)")

    # 7b. Alchemy
    cards = []
    for r in alchemy_items:
        rarity = r.get("rarity", "uncommon")
        desc = r.get("description", "") or r.get("effect", "")
        cards.append(card(r["name"], desc[:40] if desc else "Alchemy", rarity, icon=r.get("icon", ""), item_id=r.get("id", r["name"].lower().replace(" ", "-"))))
    write_page("consumables/alchemy", make_page("Windrose Alchemy", "All alchemy items and elixirs.", "Consumables / Alchemy", "consumables", "Alchemy & Elixirs", f"{len(cards)} items." if cards else "Data coming soon.", "\n".join(cards) if cards else '<div style="text-align:center;padding:3rem;color:#8b949e;">🧪 Coming soon</div>', css_depth=3, rel_path="consumables/alchemy"))
    print(f"  database/consumables/alchemy/ ({len(cards)} cards)")

    # 7c. Medicine
    cards = []
    for r in medicine_items:
        rarity = r.get("rarity", "uncommon")
        desc = r.get("description", "") or r.get("effect", "")
        cards.append(card(r["name"], desc[:40] if desc else "Medicine", rarity, icon=r.get("icon", ""), item_id=r.get("id", r["name"].lower().replace(" ", "-"))))
    write_page("consumables/medicine", make_page("Windrose Medicine", "All healing potions and medicine.", "Consumables / Medicine", "consumables", "Medicine & Potions", f"{len(cards)} items." if cards else "Data coming soon.", "\n".join(cards) if cards else '<div style="text-align:center;padding:3rem;color:#8b949e;">💊 Coming soon</div>', css_depth=3, rel_path="consumables/medicine"))
    print(f"  database/consumables/medicine/ ({len(cards)} cards)")

    # 8. Equipment overview + sub-pages
    armor_cards_eq = []
    for w in armor_items:
        icon = w.get("icon", "")
        rarity = w.get("tier", "rare")
        armor_cards_eq.append(card(w["name"], f'Armor • {w.get("best_use", "General")}', rarity, icon=icon, item_id=w["id"]))

    # 8a. Rings
    cards = []
    for r in ring_items:
        icon = r.get("icon", "")
        rarity = r.get("tier", "uncommon")
        desc = r.get("description", "") or r.get("best_use", "Ring")
        cards.append(card(r["name"], desc[:50], rarity, icon=icon, item_id=r["id"]))
    write_page("equipment/rings", make_page("Windrose Rings", "All rings and their stats.", "Equipment / Rings", "equipment", "Rings", f"{len(cards)} rings." if cards else "Data coming soon.", "\n".join(cards) if cards else '<div style="text-align:center;padding:3rem;color:#8b949e;">💍 Coming soon</div>', css_depth=3, rel_path="equipment/rings"))
    print(f"  database/equipment/rings/ ({len(cards)} cards)")

    # 8b. Necklaces
    cards = []
    for r in necklace_items:
        icon = r.get("icon", "")
        rarity = r.get("tier", "uncommon")
        desc = r.get("description", "") or r.get("best_use", "Necklace")
        cards.append(card(r["name"], desc[:50], rarity, icon=icon, item_id=r["id"]))
    write_page("equipment/necklaces", make_page("Windrose Necklaces", "All necklaces and their stats.", "Equipment / Necklaces", "equipment", "Necklaces", f"{len(cards)} necklaces." if cards else "Data coming soon.", "\n".join(cards) if cards else '<div style="text-align:center;padding:3rem;color:#8b949e;">📿 Coming soon</div>', css_depth=3, rel_path="equipment/necklaces"))
    print(f"  database/equipment/necklaces/ ({len(cards)} cards)")

    # 8c. Backpacks
    cards = []
    for r in backpack_items:
        icon = r.get("icon", "")
        rarity = r.get("tier", "uncommon")
        desc = r.get("description", "") or r.get("best_use", "Backpack")
        cards.append(card(r["name"], desc[:50], rarity, icon=icon, item_id=r["id"]))
    write_page("equipment/backpacks", make_page("Windrose Backpacks", "All backpacks and inventory expansions.", "Equipment / Backpacks", "equipment", "Backpacks", f"{len(cards)} backpacks." if cards else "Data coming soon.", "\n".join(cards) if cards else '<div style="text-align:center;padding:3rem;color:#8b949e;">🎒 Coming soon</div>', css_depth=3, rel_path="equipment/backpacks"))
    print(f"  database/equipment/backpacks/ ({len(cards)} cards)")

    # 8d. Equipment overview
    ring_cards_eq = []
    for r in ring_items:
        icon = r.get("icon", "")
        rarity = r.get("tier", "uncommon")
        ring_cards_eq.append(card(r["name"], r.get("description", r.get("best_use", "Ring"))[:50], rarity, icon=icon, item_id=r["id"]))
    neck_cards_eq = []
    for r in necklace_items:
        icon = r.get("icon", "")
        rarity = r.get("tier", "uncommon")
        neck_cards_eq.append(card(r["name"], r.get("description", r.get("best_use", "Necklace"))[:50], rarity, icon=icon, item_id=r["id"]))
    bp_cards_eq = []
    for r in backpack_items:
        icon = r.get("icon", "")
        rarity = r.get("tier", "uncommon")
        bp_cards_eq.append(card(r["name"], r.get("description", r.get("best_use", "Backpack"))[:50], rarity, icon=icon, item_id=r["id"]))
    all_eq_cards = armor_cards_eq + ring_cards_eq + neck_cards_eq + bp_cards_eq
    write_page("equipment", make_page("Windrose Equipment", "All equipment: armor, rings, necklaces, backpacks.", "Equipment", "equipment", "Equipment", f"{len(all_eq_cards)} items.", "\n".join(all_eq_cards) if all_eq_cards else '<div style="text-align:center;padding:3rem;color:#8b949e;">🛡️ Coming soon</div>', rel_path="equipment"))
    print(f"  database/equipment/ ({len(all_eq_cards)} cards)")

    # 9. Ship sub-pages
    # 9a. Ship Weapons
    cards = []
    for s in ship_weapon_items:
        rarity = s.get("rarity", "rare" if any(k in s.get("name", "").lower() for k in ("tempered", "devastating", "perfectly")) else "uncommon")
        desc = s.get("description", "") or s.get("effect", "")
        cards.append(card(s["name"], desc[:50] if desc else "Ship Weapon", rarity, icon=s.get("icon", ""), item_id=s.get("id", s["name"].lower().replace(" ", "-"))))
    write_page("ships/ship-weapons", make_page("Windrose Ship Weapons", "All ship-mounted weapons.", "Ships / Ship Weapons", "ships", "Ship Weapons", f"{len(cards)} weapons." if cards else "Data coming soon.", "\n".join(cards) if cards else '<div style="text-align:center;padding:3rem;color:#8b949e;">🚢 Coming soon</div>', css_depth=3, rel_path="ships/ship-weapons"))
    print(f"  database/ships/ship-weapons/ ({len(cards)} cards)")

    # 9b. Hull Modules
    cards = []
    for s in hull_module_items:
        rarity = s.get("rarity", "uncommon")
        desc = s.get("description", "") or s.get("effect", "")
        cards.append(card(s["name"], desc[:50] if desc else "Hull Module", rarity, icon=s.get("icon", ""), item_id=s.get("id", s["name"].lower().replace(" ", "-"))))
    write_page("ships/hull-modules", make_page("Windrose Hull Modules", "All ship hull bracing modules.", "Ships / Hull Modules", "ships", "Hull Modules", f"{len(cards)} modules." if cards else "Data coming soon.", "\n".join(cards) if cards else '<div style="text-align:center;padding:3rem;color:#8b949e;">🛡️ Coming soon</div>', css_depth=3, rel_path="ships/hull-modules"))
    print(f"  database/ships/hull-modules/ ({len(cards)} cards)")

    # 9c. Combat Orders
    cards = []
    for s in combat_order_items:
        rarity = s.get("rarity", "rare")
        desc = s.get("description", "") or s.get("effect", "")
        cards.append(card(s["name"], desc[:50] if desc else "Combat Order", rarity, icon=s.get("icon", ""), item_id=s.get("id", s["name"].lower().replace(" ", "-"))))
    write_page("ships/combat-orders", make_page("Windrose Combat Orders", "All naval combat tactics.", "Ships / Combat Orders", "ships", "Combat Orders", f"{len(cards)} orders." if cards else "Data coming soon.", "\n".join(cards) if cards else '<div style="text-align:center;padding:3rem;color:#8b949e;">⚓ Coming soon</div>', css_depth=3, rel_path="ships/combat-orders"))
    print(f"  database/ships/combat-orders/ ({len(cards)} cards)")

    # 10. Metals
    cards = []
    for r in metal_items:
        rarity = r.get("rarity", "common")
        biome = ", ".join(r.get("biomes", r.get("biome", []))[:2])
        cards.append(card(r["name"], f'{biome} • {r.get("tool_required", "Unknown")}', rarity, icon=r.get("icon", ""), item_id=r.get("id", r["name"].lower().replace(" ", "-"))))
    write_page("resources/metals", make_page("Windrose Metals", "All metal resources.", "Resources / Metals", "resources", "Metals", f"{len(cards)} metals." if cards else "Data coming soon.", "\n".join(cards) if cards else '<div style="text-align:center;padding:3rem;color:#8b949e;">⛏️ Coming soon</div>', css_depth=3, rel_path="resources/metals"))
    print(f"  database/resources/metals/ ({len(cards)} cards)")

    # 11. Misc overview + sub-pages
    misc_only = [r for r in misc_items if r.get("category") == "misc"]
    default_only = [r for r in misc_items if r.get("category") == "default"]

    all_misc_cards = []
    for r in misc_items:
        station = r.get("station", "Unknown")
        rarity = "uncommon" if r.get("station_level", 1) <= 1 else ("rare" if r.get("station_level", 1) == 2 else "epic")
        all_misc_cards.append(card(r["name"], f'{station} • {r.get("category", "misc").capitalize()}', rarity, icon=r.get("icon", ""), item_id=r.get("id", r["name"].lower().replace(" ", "-"))))
    write_page("misc", make_page("Windrose Misc Items", "Miscellaneous and uncategorized items.", "Misc", "misc", "Misc Items", f"{len(all_misc_cards)} items." if all_misc_cards else "Data coming soon.", "\n".join(all_misc_cards) if all_misc_cards else '<div style="text-align:center;padding:3rem;color:#8b949e;">📦 Coming soon</div>', rel_path="misc"))
    print(f"  database/misc/ ({len(all_misc_cards)} cards)")

    misc_cards = []
    for r in misc_only:
        station = r.get("station", "Unknown")
        rarity = "uncommon" if r.get("station_level", 1) <= 1 else ("rare" if r.get("station_level", 1) == 2 else "epic")
        misc_cards.append(card(r["name"], f'{station} • Misc', rarity, icon=r.get("icon", ""), item_id=r.get("id", r["name"].lower().replace(" ", "-"))))
    write_page("misc/misc", make_page("Windrose Misc", "Miscellaneous items.", "Misc / Misc", "misc", "Miscellaneous", f"{len(misc_cards)} items." if misc_cards else "Data coming soon.", "\n".join(misc_cards) if misc_cards else '<div style="text-align:center;padding:3rem;color:#8b949e;">📦 Coming soon</div>', css_depth=3, rel_path="misc/misc"))
    print(f"  database/misc/misc/ ({len(misc_cards)} cards)")

    def_cards = []
    for r in default_only:
        station = r.get("station", "Unknown")
        rarity = "uncommon"
        def_cards.append(card(r["name"], f'{station} • Default', rarity, icon=r.get("icon", ""), item_id=r.get("id", r["name"].lower().replace(" ", "-"))))
    write_page("misc/default", make_page("Windrose Default Items", "Default category items.", "Misc / Default", "misc", "Default Items", f"{len(def_cards)} items." if def_cards else "Data coming soon.", "\n".join(def_cards) if def_cards else '<div style="text-align:center;padding:3rem;color:#8b949e;">📦 Coming soon</div>', css_depth=3, rel_path="misc/default"))
    print(f"  database/misc/default/ ({len(def_cards)} cards)")

    print(f"\n✅ All database list pages generated (en)!")



def main():
    """Build database pages for every supported language."""
    for lang in SUPPORTED:
        print(f"\n--- Building database pages [lang={lang}] ---")
        build_all(lang)
    print(f"\n✅ All database list pages generated for {len(SUPPORTED)} languages.")


if __name__ == "__main__":
    main()

