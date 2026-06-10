"""
从 data/*.json 批量生成 Database 物品详情页。
详情页为双栏布局：左栏显示图片、基础属性和概述卡片；右栏显示高级制作面板及其他信息。
所有详情页统一使用 /database/items/{id}/index.html 路径。
"""
import json, os, re, html as html_mod
from collections import defaultdict
from urllib.parse import quote
from templates import header_html

PROJECT = r"F:\aicode\gamedoc"
SITE = "https://windrosewiki.games"

# ── 全局 enrichment 索引(在所有数据加载完成后由 build_indexes() 填充)──
# USED_IN[material_name] = [(consumer_id, consumer_name, tier_level), ...]
# ARMOR_SET_PARTS[(set_name, variant)] = [(slot, item_id, item_name), ...]
# NAME_TO_ID[item_name] = item_id (用于把 used-in 中的物料名转链接)
USED_IN = defaultdict(list)
ARMOR_SET_PARTS = defaultdict(list)
NAME_TO_ID = {}

ARMOR_SLOT_LABELS = {
    "head": "Head", "hands": "Hands", "torso": "Torso",
    "legs": "Legs", "feet": "Feet",
}
ARMOR_SLOT_ORDER = ["head", "torso", "hands", "legs", "feet"]


def build_indexes(all_items):
    """根据完整 item 列表预计算反向索引。only call after all data loaded."""
    USED_IN.clear()
    ARMOR_SET_PARTS.clear()
    NAME_TO_ID.clear()
    for it in all_items:
        iid = it.get("id")
        name = it.get("name")
        if iid and name:
            NAME_TO_ID.setdefault(name, iid)
    armor_re = re.compile(r"^eid-armor-([a-z]+)-(base|advanced)-([a-z]+)$")
    for it in all_items:
        # 反向 used-in: 谁的 recipe 用了这个 item.name
        for tier in (it.get("crafting") or {}).get("tiers", []):
            for m in tier.get("materials", []):
                mname = m.get("name") if isinstance(m, dict) else None
                if mname:
                    USED_IN[mname].append(
                        (it["id"], it.get("name", "?"), tier.get("level", "?"))
                    )
        # 护甲套装: id 模式 eid-armor-{set}-{variant}-{slot}
        m = armor_re.match(it.get("id", "") or "")
        if m:
            set_name, variant, slot = m.group(1), m.group(2), m.group(3)
            if slot in ARMOR_SLOT_LABELS:
                ARMOR_SET_PARTS[(set_name, variant)].append(
                    (slot, it["id"], it.get("name", "?"))
                )


def should_noindex(item):
    """决定 item 详情页是否加 noindex,follow。

    规则(任一满足即 noindex):
    - description 含已知 placeholder('does not ship a long description')
    - category == misc 且无任何 used-in 反向链(钥匙/笔记/任务道具,无人会搜)
    - description < 50 字符 且无 used-in 反向链(内容确实薄)
    """
    desc = item.get("description") or ""
    if "does not ship a long description" in desc:
        return True
    has_backref = bool(USED_IN.get(item.get("name", "")))
    if has_backref:
        return False
    if item.get("category") == "misc":
        return True
    if len(desc) < 50:
        return True
    return False


def render_used_in_section(item):
    """渲染 'Used in' 反向链区块。无 backref 时返回空字符串。"""
    backrefs = USED_IN.get(item.get("name", ""), [])
    if not backrefs:
        return ""
    # 同名(item 在多个 tier 反复出现)合并去重,按 consumer_name 排序
    seen = set()
    unique = []
    for cid, cname, _tier in backrefs:
        if cid in seen:
            continue
        seen.add(cid)
        unique.append((cid, cname))
    unique.sort(key=lambda x: x[1].lower())
    n = len(unique)
    item_name = item.get("name", "this item")
    intro = (f'<p class="detail-text">{esc(item_name)} appears as a crafting material in '
             f'<strong>{n}</strong> recipe{"s" if n != 1 else ""} across the Windrose database. '
             f'Use these links to jump straight to the consumers and check station, '
             f'tier and full material list.</p>')
    pills = []
    for cid, cname in unique[:80]:  # cap to 80 to keep HTML manageable
        pills.append(
            f'<a href="/database/items/{cid}/" class="mat-pill">'
            f'<span class="mat-name">{esc(cname)}</span></a>'
        )
    more = ""
    if n > 80:
        more = f'<p class="detail-text" style="margin-top:.5rem;opacity:.7">…and {n - 80} more.</p>'
    return (
        f'<div class="detail-section">'
        f'<div class="detail-section-title">Used in recipes ({n})</div>'
        f'{intro}'
        f'<div class="mat-pill-row" style="display:flex;flex-wrap:wrap;gap:.5rem">{"".join(pills)}</div>'
        f'{more}'
        f'</div>'
    )


def render_set_parts_section(item):
    """对护甲件渲染 'Set parts' 区块,列出同套装其它件的链接。"""
    iid = item.get("id", "") or ""
    m = re.match(r"^eid-armor-([a-z]+)-(base|advanced)-([a-z]+)$", iid)
    if not m:
        return ""
    set_name, variant, this_slot = m.group(1), m.group(2), m.group(3)
    parts = ARMOR_SET_PARTS.get((set_name, variant), [])
    if len(parts) < 2:
        return ""
    by_slot = {slot: (pid, pname) for slot, pid, pname in parts}
    ordered = []
    for slot in ARMOR_SLOT_ORDER:
        if slot in by_slot:
            ordered.append((slot, *by_slot[slot]))
    set_label = set_name.capitalize() + (" (Advanced)" if variant == "advanced" else "")
    intro = (f'<p class="detail-text">Part of the <strong>{esc(set_label)}</strong> armor set. '
             f'Equip the full set to maintain visual consistency and stack stat coverage across all slots.</p>')
    pills = []
    for slot, pid, pname in ordered:
        is_self = (slot == this_slot)
        cls = "mat-pill" + (" mat-pill-current" if is_self else "")
        label = ARMOR_SLOT_LABELS[slot]
        if is_self:
            pills.append(
                f'<span class="{cls}" aria-current="page">'
                f'<span class="mat-name">{esc(label)}: {esc(pname)}</span></span>'
            )
        else:
            pills.append(
                f'<a href="/database/items/{pid}/" class="{cls}">'
                f'<span class="mat-name">{esc(label)}: {esc(pname)}</span></a>'
            )
    return (
        f'<div class="detail-section">'
        f'<div class="detail-section-title">{esc(set_label)} set ({len(parts)} pieces)</div>'
        f'{intro}'
        f'<div class="mat-pill-row" style="display:flex;flex-wrap:wrap;gap:.5rem">{"".join(pills)}</div>'
        f'</div>'
    )


def esc(text):
    """HTML 转义"""
    return html_mod.escape(str(text)) if text else ""


def slug_to_link(item_id):
    """物品 ID 转为详情页链接"""
    return f"/database/items/{item_id}/"


def normalize_item_id(item_id):
    return str(item_id).replace("/'", "'")


def item_url(item_id):
    """生成合法的公开 item URL，用于 canonical 和 JSON-LD。"""
    clean_id = normalize_item_id(item_id)
    return f"{SITE}/database/items/{quote(clean_id, safe='')}/"


def mat_pill_html(mat):
    """渲染材料为圆润胶囊形式"""
    if isinstance(mat, dict):
        qty = mat.get("quantity", mat.get("amount", "?"))
        name = mat.get("item", mat.get("name", "?"))
        item_id = mat.get("item_id", name.lower().replace(" ", "-").replace("'", ""))
        # 为了兼容性，如果没有图标则不显示 <img>，CSS 会自适应
        icon = mat.get("icon", "")
        img_html = f'<img src="{icon}" alt="{esc(name)}" width="24" height="24" loading="lazy">' if icon else ""
        return f'<a href="{slug_to_link(item_id)}" class="mat-pill">{img_html}<span class="mat-name">{esc(name)}</span><span class="mat-count">×{qty}</span></a>'
    elif isinstance(mat, str) and "+" in mat:
        parts = mat.split("+")
        pills = []
        for p in parts:
            p = p.strip()
            parts_space = p.split(" ", 1)
            if len(parts_space) == 2 and parts_space[0].isdigit():
                qty = parts_space[0]
                name = parts_space[1]
                item_id = name.lower().replace(" ", "-").replace("'", "")
                pills.append(f'<a href="{slug_to_link(item_id)}" class="mat-pill"><span class="mat-name">{esc(name)}</span><span class="mat-count">×{qty}</span></a>')
            else:
                pills.append(f'<span class="mat-pill"><span class="mat-name">{esc(p)}</span></span>')
        return "".join(pills)
    else:
        return f'<span class="mat-pill"><span class="mat-name">{esc(str(mat))}</span></span>'


def stat_row(label, value):
    """渲染单个属性行"""
    if value is None or value == "" or value == "unknown":
        return ""
    return f'<div class="detail-stat-box"><div class="stat-label">{esc(label)}</div><div class="stat-value">{esc(str(value))}</div></div>'


def stat_row_list(label, value):
    """用于右侧其他信息的横排属性行"""
    if value is None or value == "" or value == "unknown":
        return ""
    return f'<div class="detail-stat"><span class="detail-stat-label">{esc(label)}</span><span class="detail-stat-value">{esc(str(value))}</span></div>'


def build_jsonld(item, name, item_id, desc, icon, category_label, category_href):
    """生成详情页 JSON-LD：Product + BreadcrumbList，含配方时再加 HowTo"""
    page_url = item_url(item_id)
    image_url = icon if icon.startswith("http") else f"{SITE}{icon}"

    additional_props = []
    item_stats_data = ITEM_STATS.get(item_id, {})
    stats = item.get("stats", {})
    if isinstance(stats, dict):
        for k, v in stats.items():
            if v in (None, "", "unknown"):
                continue
            additional_props.append({
                "@type": "PropertyValue",
                "name": k.replace("_", " ").title(),
                "value": str(v),
            })
    for k in ("level", "attack"):
        v = item_stats_data.get(k)
        if v is not None:
            additional_props.append({
                "@type": "PropertyValue",
                "name": k.capitalize(),
                "value": str(v),
            })
    rarity = item.get("rarity") or item.get("tier")
    if rarity:
        additional_props.append({
            "@type": "PropertyValue",
            "name": "Rarity",
            "value": str(rarity).capitalize(),
        })

    product = {
        "@type": "Product",
        "@id": f"{page_url}#product",
        "name": name,
        "description": desc,
        "image": image_url,
        "category": category_label,
        "url": page_url,
        "brand": {"@type": "Brand", "name": "Windrose"},
    }
    if additional_props:
        product["additionalProperty"] = additional_props

    breadcrumb = {
        "@type": "BreadcrumbList",
        "@id": f"{page_url}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Database", "item": f"{SITE}/database/"},
            {"@type": "ListItem", "position": 2, "name": category_label, "item": f"{SITE}{category_href}"},
            {"@type": "ListItem", "position": 3, "name": name, "item": page_url},
        ],
    }

    graph = [product, breadcrumb]

    crafting = item.get("crafting", {})
    tiers = crafting.get("tiers", [])
    if not tiers:
        materials = crafting.get("materials") or item.get("materials", [])
        if materials:
            tiers = [{
                "level": 1,
                "station": item.get("station", crafting.get("station", "")),
                "time": crafting.get("time", ""),
                "materials": materials,
            }]
    if tiers:
        first = tiers[0]
        mats = first.get("materials", [])
        supplies = []
        if isinstance(mats, list):
            for m in mats:
                if isinstance(m, dict):
                    mat_name = m.get("item") or m.get("name")
                    qty = m.get("quantity", m.get("amount", ""))
                    if not mat_name:
                        continue
                    supply = {"@type": "HowToSupply", "name": mat_name}
                    if qty:
                        supply["requiredQuantity"] = str(qty)
                    supplies.append(supply)
        station = first.get("station") or item.get("station") or "Crafting Station"
        howto = {
            "@type": "HowTo",
            "@id": f"{page_url}#howto",
            "name": f"How to craft {name}",
            "description": f"Craft {name} at {station} in Windrose.",
            "tool": [{"@type": "HowToTool", "name": station}] if station else [],
        }
        if supplies:
            howto["supply"] = supplies
        if first.get("time"):
            howto["totalTime"] = str(first["time"])
        graph.append(howto)

    payload = {"@context": "https://schema.org", "@graph": graph}
    return f'<script type="application/ld+json">{json.dumps(payload, ensure_ascii=False)}</script>'


def detail_page(item, category_label, category_href, css_depth=3):
    """
    生成物品详情页 HTML（双栏：左概览，右制作+其他信息）。
    """
    name = item.get("name", "Unknown")
    item_id = normalize_item_id(item.get("id", "unknown"))
    rarity = item.get("rarity", item.get("tier", ""))
    category = item.get("category", "")
    data_type = item.get("data_type", category)

    # 稀有度徽章
    rarity_cls = {"epic": "rarity-epic", "rare": "rarity-rare", "S": "rarity-epic",
                  "A": "rarity-rare", "B": "rarity-uncommon", "C": "rarity-common",
                  "uncommon": "rarity-uncommon", "common": "rarity-common"}.get(str(rarity), "rarity-common")
    rarity_label = str(rarity).capitalize() if rarity else "Unknown"

    # 默认图标
    icon = item.get("icon", f"/imgs/database/items/{item_id}.webp")
    icon_html = f'<img src="{icon}" alt="{esc(name)}" width="300" height="300" loading="eager" onerror="this.src=\'/imgs/database/items/placeholder.webp\'">'

    css_prefix = "../" * css_depth

    # 置信度标签
    confidence = item.get("confidence", "")
    verified = item.get("last_verified", "")
    conf_html = ""
    if confidence:
        conf_color = {"official": "#3fb950", "verified": "#3fb950", "community": "#d29922", "unconfirmed": "#f85149"}.get(confidence, "#8b949e")
        conf_html = f' <span class="db-badge" style="color:{conf_color};border:1px solid {conf_color}33;background:{conf_color}15;margin-left:0.5rem;font-size:0.8rem;vertical-align:middle">{confidence.capitalize()}</span>'

    # 子类型描述
    subtype = item.get("subcategory", category).replace("_", " ").capitalize()
    if item.get("station"):
        subtype = f'{item.get("station")} Recipe'

    # ── 构建左栏属性 (Stat Grid) ──────────────────────────────────
    left_stats_html = ""

    stats = item.get("stats", {})
    if isinstance(stats, dict) and stats:
        left_stats_html = "".join([stat_row(k.replace("_", " ").title(), v) for k, v in stats.items()])

    # Level & Attack: read from data/item-stats.json
    item_stats = ITEM_STATS.get(item_id, {})
    if item_stats.get("level") is not None:
        left_stats_html += stat_row("Level", item_stats["level"])
    if item_stats.get("attack") is not None:
        left_stats_html += stat_row("Attack", item_stats["attack"])

    # Extra info
    if data_type == "boss":
        left_stats_html += stat_row("Biome", item.get("biome"))
    elif data_type == "ship":
        left_stats_html += stat_row("Size", item.get("size"))
        left_stats_html += stat_row("Crew", item.get("crew"))

    # 不再兜底显示 Type（Type 已在面包屑/标题区域显示）

    stat_grid_html = f'<div class="detail-stat-grid">{left_stats_html}</div>'

    # 概述卡片
    desc = item.get("description", f"A key item in the {category_label} category.")
    quote = item.get("quote", "")
    quote_html = f'<p class="overview-quote">{esc(quote)}</p>' if quote else ""
    overview_html = f'''<div class="detail-overview-card">
        <div class="overview-title">Overview</div>
        <p class="overview-text">{esc(desc)}</p>
        {quote_html}
    </div>'''


    # ── 构建右栏信息 ──────────────────────────────────
    
    # 1. 高级制作面板
    crafting_html = ""
    crafting = item.get("crafting", {})
    tiers = crafting.get("tiers", [])
    if not tiers:
        materials = crafting.get("materials")
        if not materials:
            materials = item.get("materials", [])
        if materials:
            tiers = [{"level": 1, "station": item.get("station", crafting.get("station", "")), "time": crafting.get("time", ""), "materials": materials}]
    
    if tiers:
        tier_cards = ""
        for i, tier in enumerate(tiers):
            level_num = tier.get("level", i + 1)
            lvl_name = tier.get("name", f"Tier {level_num}")
            st = tier.get("station", item.get("station", crafting.get("station", "Crafting Station")))
            tm = tier.get("time", crafting.get("time", "1s"))
            
            mats = tier.get("materials", [])
            if isinstance(mats, list):
                mats_html = "".join([mat_pill_html(m) for m in mats])
            else:
                mats_html = mat_pill_html(mats)
                
            tier_cards += f'''
            <div class="tier-card">
                <div class="tier-indicator tier-{level_num}">
                    <span class="dot"></span>
                    <span class="line"></span>
                </div>
                <div class="tier-content">
                    <div class="tier-top">
                        <span class="tier-name">{esc(lvl_name)}</span>
                        <div class="tier-reqs">
                            <span class="req">{esc(st)}</span>
                            <span class="req" style="margin-left:8px;color:#8b949e">⏱ {esc(tm)}</span>
                        </div>
                    </div>
                    <div class="tier-mats">
                        {mats_html}
                    </div>
                </div>
            </div>'''

        main_station = item.get("station", crafting.get("station", "Crafting Station"))
        station_icon = crafting.get("station_icon", "")
        station_icon_html = f'<img src="{station_icon}" alt="{esc(main_station)}" width="24" height="24" loading="lazy" style="vertical-align:middle;margin-right:8px;">' if station_icon else ""
        
        crafting_html = f'''<section class="detail-crafting-premium" id="crafting">
            <div class="crafting-premium-header">
                <div class="header-titles">
                    <h2 class="title">Crafting</h2>
                    <p class="subtitle">Where and how this entry can be fabricated, including station requirements and ingredients.</p>
                </div>
                <div class="station-badge">
                    {station_icon_html}<span>{esc(main_station)}</span>
                </div>
            </div>
            <div class="crafting-tiers-list">
                {tier_cards}
            </div>
        </section>'''

    # 其他信息块 (复用原有的 detail-section)
    other_sections = ""
    
    # Drops
    drops = item.get("drops", item.get("drop_sources", []))
    if drops:
        items_html = "".join([f'<li>{esc(str(d))}</li>' for d in drops])
        label = "Drops" if data_type == "boss" else "Drop Sources"
        other_sections += f'<div class="detail-section"><div class="detail-section-title">{label}</div><ul class="detail-text">{items_html}</ul></div>'

    # Gear
    gear = item.get("recommended_gear", [])
    if gear:
        items_html = "".join([f'<li>{esc(g)}</li>' for g in gear])
        other_sections += f'<div class="detail-section"><div class="detail-section-title">Recommended Gear</div><ul class="detail-text">{items_html}</ul></div>'

    # Unlocks
    unlocks = item.get("unlocks", [])
    if unlocks:
        items_html = "".join([f'<span class="detail-tag">{esc(u)}</span>' for u in unlocks])
        other_sections += f'<div class="detail-section"><div class="detail-section-title">Unlocks</div><div class="detail-tags">{items_html}</div></div>'

    # Used In
    used_in = item.get("used_in", [])
    if used_in:
        items_html = "".join([f'<li><a href="{slug_to_link(u.lower().replace(" ", "-"))}">{esc(u)}</a></li>' for u in used_in])
        other_sections += f'<div class="detail-section"><div class="detail-section-title">Used In</div><ul class="detail-links">{items_html}</ul></div>'

    # Locations
    biomes = item.get("biomes", item.get("biome", []))
    locations = item.get("locations", [])
    tool_req = item.get("tool_required", "")
    if biomes or locations:
        rows = stat_row_list("Tool Required", tool_req)
        if isinstance(biomes, list) and biomes:
            rows += stat_row_list("Biomes", ", ".join(biomes))
        if isinstance(locations, list) and locations:
            rows += stat_row_list("Locations", ", ".join(locations))
        other_sections += f'<div class="detail-section"><div class="detail-section-title">Where to Find</div><div class="detail-stats">{rows}</div></div>'

    # Tips
    tips = item.get("farming_tips", [])
    if tips:
        items_html = "".join([f'<li>{esc(t)}</li>' for t in tips])
        other_sections += f'<div class="detail-section"><div class="detail-section-title">Farming Tips</div><ul class="detail-text">{items_html}</ul></div>'

    # Pros/Cons
    pros = item.get("pros", [])
    cons = item.get("cons", [])
    if pros or cons:
        content = ""
        if pros:
            content += '<div style="margin-bottom:0.5rem"><strong style="color:#3fb950">Pros:</strong></div><ul class="detail-text">' + "".join([f'<li>{esc(p)}</li>' for p in pros]) + '</ul>'
        if cons:
            content += '<div style="margin-bottom:0.5rem"><strong style="color:#f85149">Cons:</strong></div><ul class="detail-text">' + "".join([f'<li>{esc(c)}</li>' for c in cons]) + '</ul>'
        other_sections += f'<div class="detail-section"><div class="detail-section-title">Pros & Cons</div>{content}</div>'

    # Variants
    variants = item.get("variants", [])
    if variants:
        rows = ""
        for v in variants:
            rows += f'<div class="detail-stat"><span class="detail-stat-label">{esc(v.get("name",""))}</span><span class="detail-stat-value">{v.get("cannons","")} cannons · {esc(v.get("notes",""))}</span></div>'
        other_sections += f'<div class="detail-section"><div class="detail-section-title">Variants</div><div class="detail-stats">{rows}</div></div>'

    # Notes
    notes = item.get("notes", "")
    if notes:
        other_sections += f'<div class="detail-section"><div class="detail-section-title">Notes</div><p class="detail-text">{esc(notes)}</p></div>'

    jsonld_html = build_jsonld(item, name, item_id, desc, icon, category_label, category_href)

    # NOTE: noindex 策略详见 should_noindex(),覆盖 placeholder/无搜索价值的 misc/超短描述
    # 这三类页面 Google 都会判 thin content,不如主动表态不索引,
    # 让爬虫预算花在 ~640 个有内容的 item 页上。
    if should_noindex(item):
        robots_meta = '<meta name="robots" content="noindex, follow">'
    else:
        robots_meta = '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">'

    # 数据驱动的反向链区块:Used-in / Set parts
    enrichment_html = render_used_in_section(item) + render_set_parts_section(item)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(name)} — Windrose Database | Windrose Guides</title>
<meta name="description" content="{esc(name)} in Windrose. View stats, crafting recipe, locations, and related items.">
{robots_meta}
<link rel="canonical" href="{item_url(item_id)}">
<link rel="stylesheet" href="{css_prefix}css/style.css">
<link rel="stylesheet" href="{css_prefix}database/db-style.css">
{jsonld_html}
</head>
<body>
{header_html("database")}

<div class="detail-wrap">
    <div class="detail-breadcrumbs">
        <a href="/database/">Database</a> / <a href="{category_href}">{category_label}</a> / {esc(name)}
    </div>

    <!-- 双栏主体 -->
    <div class="detail-two-col">
        <!-- ========== 左栏：物品信息 ========== -->
        <div class="detail-left">
            <!-- 物品图片 -->
            <div class="detail-item-image">
                {icon_html}
            </div>

            <!-- 物品基础信息 -->
            <div class="detail-item-info">
                <div class="item-label">物品</div>
                <h1 class="item-name">{esc(name)}{conf_html}</h1>
                <div class="item-type-row">
                    <span>{esc(subtype)}</span>
                    <span class="item-rarity-badge {rarity_cls}">{rarity_label}</span>
                </div>

                {stat_grid_html}
            </div>

            {overview_html}
        </div>

        <!-- ========== 右栏：制作与其他信息 ========== -->
        <div class="detail-right">
            {crafting_html}
            {other_sections}
            {enrichment_html}

            <a href="{category_href}" class="detail-back">← Back to {category_label}</a>
        </div>
    </div>
</div>

<script>
document.querySelector('.hamburger').addEventListener('click',function(){{this.classList.toggle('open');document.querySelector('.nav-links').classList.toggle('open');}});
</script>
</body></html>"""


def write_detail(item_id, content):
    """写入详情页"""
    item_id = normalize_item_id(item_id)
    path = os.path.join(PROJECT, "database", "items", item_id, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ── 分类到面包屑的映射 ──────────────────────────────────
CATEGORY_MAP = {
    "melee-weapon": ("Weapons", "/database/weapons/"),
    "range-weapon": ("Weapons", "/database/weapons/"),
    "ammo": ("Weapons", "/database/weapons/"),
    "tool": ("Weapons", "/database/weapons/"),
    "armor": ("Equipment", "/database/armor/"),
    "ring": ("Equipment", "/database/armor/"),
    "necklace": ("Equipment", "/database/armor/"),
    "backpack": ("Equipment", "/database/armor/"),
    "resource": ("Resources", "/database/resources/"),
    "metal": ("Resources", "/database/resources/"),
    "food": ("Resources", "/database/resources/"),
    "alchemy": ("Resources", "/database/resources/"),
    "medicine": ("Resources", "/database/resources/"),
    "ship-weapon": ("Ships", "/database/ships/"),
    "ship-hull-mod": ("Ships", "/database/ships/"),
    "ship-combat-order": ("Ships", "/database/ships/"),
    "misc": ("Database", "/database/"),
    "default": ("Database", "/database/"),
}

count = 0
generated_ids = set()

# ── 加载 Item Stats ──────────────────────────────────
ITEM_STATS = {}
stats_path = os.path.join(PROJECT, "data/item-stats.json")
if os.path.exists(stats_path):
    with open(stats_path, encoding="utf-8") as f:
        ITEM_STATS = json.load(f)
    print(f"  加载 item-stats.json ({len(ITEM_STATS)} 条)")

# ── 阶段 1: 收集所有 item 到一个 (item, label, href) 列表 ──
# 必须先收齐全部 item 才能建反向索引(detail_page 依赖 USED_IN/ARMOR_SET_PARTS 全局)
ALL_TO_GENERATE = []  # list of (item, label, href)
_seen_ids = set()  # 临时去重,与下方 generated_ids 保持等价

def _add_collect(item, label, href):
    iid = item.get("id")
    if not iid or iid in _seen_ids:
        return
    _seen_ids.add(iid)
    ALL_TO_GENERATE.append((item, label, href))

# scraped_items_v2 优先(950 个高质量数据)
scraped_path = os.path.join(PROJECT, "data/scraped_items_v2.json")
if os.path.exists(scraped_path):
    with open(scraped_path, encoding="utf-8") as f:
        scraped_data = json.load(f)
    for item in scraped_data.get("items", []):
        cat = item.get("category", "misc")
        label, href = CATEGORY_MAP.get(cat, ("Database", "/database/"))
        _add_collect(item, label, href)

# bosses + ships
with open(os.path.join(PROJECT, "data/bosses.json"), encoding="utf-8") as f:
    bosses_data = json.load(f)
with open(os.path.join(PROJECT, "data/ships.json"), encoding="utf-8") as f:
    ships_data = json.load(f)
for item in bosses_data.get("items", []):
    if item.get("id") not in _seen_ids:
        item["data_type"] = "boss"
        _add_collect(item, "Bosses", "/database/bosses/")
for ship in ships_data.get("ships", []):
    if ship.get("id") not in _seen_ids:
        ship["data_type"] = "ship"
        _add_collect(ship, "Ships", "/database/ships/")

# weapons(补漏)
_weapons_path = os.path.join(PROJECT, "data/weapons.json")
if os.path.exists(_weapons_path):
    with open(_weapons_path, encoding="utf-8") as f:
        _weapons_data = json.load(f)
    _weapons_items = _weapons_data.get("items", _weapons_data)
    if isinstance(_weapons_items, dict):
        _weapons_items = list(_weapons_items.values())
    for item in _weapons_items:
        if isinstance(item, dict) and item.get("id") not in _seen_ids:
            cat = item.get("category", "misc")
            label, href = CATEGORY_MAP.get(cat, ("Database", "/database/"))
            _add_collect(item, label, href)

# resources(补漏)
_res_path = os.path.join(PROJECT, "data/resources.json")
if os.path.exists(_res_path):
    with open(_res_path, encoding="utf-8") as f:
        _res_data = json.load(f)
    for item in _res_data.get("items", []) + _res_data.get("resources", []):
        if isinstance(item, dict) and item.get("id") not in _seen_ids:
            cat = item.get("category", "resource")
            label, href = CATEGORY_MAP.get(cat, ("Resources", "/database/resources/"))
            _add_collect(item, label, href)

# recipes(补漏): 旧版本曾留下 recipe item 详情页。继续生成它们，避免
# sitemap/canonical 使用历史 HTML。
_recipes_path = os.path.join(PROJECT, "data/recipes.json")
if os.path.exists(_recipes_path):
    with open(_recipes_path, encoding="utf-8") as f:
        _recipes_data = json.load(f)
    for item in _recipes_data.get("items", []):
        if isinstance(item, dict) and normalize_item_id(item.get("id", "")) not in _seen_ids:
            item["id"] = normalize_item_id(item["id"])
            _add_collect(item, "Crafting", "/database/crafting/")

# ── 阶段 2: 用收齐的列表建反向索引 ──
build_indexes([it for it, _, _ in ALL_TO_GENERATE])
print(f"  built indexes: USED_IN coverage={len(USED_IN)} materials, "
      f"ARMOR_SET_PARTS={len(ARMOR_SET_PARTS)} (set,variant) groups")

# ── 阶段 3: 用索引生成所有详情页 ──
noindex_count = 0
for item, label, href in ALL_TO_GENERATE:
    if should_noindex(item):
        noindex_count += 1
    write_detail(item["id"], detail_page(item, label, href))
    generated_ids.add(item["id"])
    count += 1

print(f"✅ Generated {count} detail pages in database/items/ ({noindex_count} noindex)")
