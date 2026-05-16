"""
阶段3: 工具能力建设
- 全站搜索增强 (search-index 重建)
- 配方查找器增强
- 资源规划器
- 进度检查表增强
"""
import json, os
sys_path = os.path.dirname(__file__)
ROOT = r"F:\aicode\gamedoc"

def load_json(name):
    p = os.path.join(ROOT, "data", name)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json(name, data):
    p = os.path.join(ROOT, "data", name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  ✅ data/{name}")

def write_file(rel, content):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ {rel}")


# === 1. 重建搜索索引 ===
def rebuild_search_index():
    index = []
    # 从 recipes 添加
    recipes = load_json("recipes.json")
    for r in recipes.get("recipes", []):
        mats = ", ".join(f'{m.get("qty",1)}x {m["item"]}' for m in r.get("materials",[]))
        index.append({
            "title": r["name"],
            "description": f'{r["category"].title()} — {mats}. {r.get("tips","")}',
            "url": f'/crafting/',
            "type": "recipe"
        })
    # 从 resources 添加
    resources = load_json("resources.json")
    for r in resources.get("resources", []):
        index.append({
            "title": r["name"],
            "description": f'Resource — {r.get("source","")}. {r.get("tips","")}',
            "url": f'/resources/',
            "type": "resource"
        })
    # 从 ships 添加
    ships = load_json("ships.json")
    for s in ships.get("ships", []):
        index.append({
            "title": s["name"],
            "description": f'{s["size"]} ship — {s.get("best_for","")}',
            "url": f'/ships/',
            "type": "ship"
        })
    # 从 bosses 添加
    bosses = load_json("bosses.json")
    for b in bosses.get("bosses", []):
        index.append({
            "title": b["name"],
            "description": f'Boss — {b.get("location","Unknown location")}',
            "url": '/bosses/',
            "type": "boss"
        })
    # 静态页面
    pages = [
        ("Beginner Guide", "Day 1-10 walkthrough, first tools, base building, combat basics", "/beginner-guide/"),
        ("Strategy Guides", "Deep-dive walkthroughs: mining routes, boss strategies, builds", "/guides/"),
        ("Mining Routes", "Optimized mining routes for Copper, Iron, Clay, Sulfur", "/guides/mining-routes/"),
        ("Boss Progression", "Phase-by-phase boss strategies and progression order", "/guides/boss-progression/"),
        ("Best Early Builds", "Optimal stat allocation for DPS, Tank, Balanced", "/guides/best-early-builds/"),
        ("Crafting Progression", "Efficient crafting order from Day 1 to endgame", "/guides/crafting-progression/"),
        ("Sailing & Navigation", "Wind mechanics, ship types, ocean survival", "/guides/sailing-navigation/"),
        ("Co-op Guide", "Server setup, role specialization, crew coordination", "/guides/coop-multiplayer/"),
        ("Naval Combat", "Ship building, upgrading, and combat tactics", "/guides/ship-building-naval-combat/"),
        ("FAQ", "Top 30+ frequently asked questions about Windrose", "/faq/"),
        ("Crafting Recipes", "All workbench, smelting, alchemy, cooking recipes", "/crafting/"),
        ("Weapons & Armor", "Melee, ranged weapons and armor sets with tier list", "/weapons/"),
        ("Download & Game Info", "Steam page, system requirements, platforms", "/download/"),
        ("Server Guide", "Dedicated server setup, firewall, configuration", "/server-guide/"),
        ("News & Updates", "Latest Windrose patch notes and community news", "/news/"),
        ("Tools & Calculators", "Recipe finder, resource planner, progression checklist", "/tools/"),
    ]
    for title, desc, url in pages:
        index.append({"title": title, "description": desc, "url": url, "type": "page"})

    save_json("search-index.json", index)
    print(f"    Search index: {len(index)} entries")


# === 2. 增强配方查找器 ===
def enhance_recipe_finder():
    """重写配方查找器页面，使用 data/recipes.json 动态加载"""
    html = '''<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Recipe Finder — Windrose Crafting Calculator (2026) | Windrose Guides</title>
<meta name="description" content="Search and filter all Windrose crafting recipes. Find materials, stations, and crafting chains instantly.">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<link rel="canonical" href="https://windrose-guides.com/tools/recipe-finder">
<link rel="stylesheet" href="../../css/style.css">
<meta property="og:title" content="Recipe Finder — Windrose (2026)">
<meta property="og:description" content="Search all Windrose crafting recipes instantly.">
<meta property="og:image" content="https://windrose-guides.com/imgs/og.webp">
</head><body>
<header class="header"><div class="container">
<a href="/" class="logo"><img src="/imgs/logo.png" alt="Windrose Guides Logo" width="32" height="32"> Windrose Guides</a>
<button class="hamburger" aria-label="Toggle navigation" aria-expanded="false"><span></span><span></span><span></span></button>
<nav><ul class="nav-links"><li><a href="/">Home</a></li><li><a href="/beginner-guide">Beginner Guide</a></li><li><a href="/guides">Guides</a></li><li><a href="/crafting">Crafting</a></li><li><a href="/resources">Resources</a></li><li><a href="/bosses">Bosses</a></li><li><a href="/ships">Ships</a></li><li><a href="/weapons">Weapons</a></li><li><a href="/builds">Builds</a></li><li><a href="/faq">FAQ</a></li><li><a href="/news">News</a></li></ul></nav>
</div></header>
<div class="container"><nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li><a href="/tools/">Tools</a></li><li>Recipe Finder</li></ol></nav></div>
<main class="container">
<h1>Recipe Finder — Windrose Crafting Calculator</h1>
<p>Search through all known Windrose crafting recipes. Filter by category, station, or workbench level.</p>

<div style="display:flex;gap:1rem;flex-wrap:wrap;margin:1.5rem 0;">
<input type="text" id="recipeSearch" placeholder="Search recipes..." style="flex:1;min-width:200px;padding:0.8rem 1rem;font-size:1rem;border-radius:8px;border:1px solid var(--border);background:var(--bg-surface);color:var(--text);outline:none;">
<select id="categoryFilter" style="padding:0.8rem;border-radius:8px;border:1px solid var(--border);background:var(--bg-surface);color:var(--text);font-size:0.9rem;">
<option value="">All Categories</option>
<option value="tool">Tools</option>
<option value="weapon">Weapons</option>
<option value="armor">Armor</option>
<option value="structure">Structures</option>
<option value="material">Materials</option>
<option value="consumable">Consumables</option>
<option value="food">Food</option>
<option value="equipment">Equipment</option>
<option value="upgrade">Upgrades</option>
</select>
<select id="stationFilter" style="padding:0.8rem;border-radius:8px;border:1px solid var(--border);background:var(--bg-surface);color:var(--text);font-size:0.9rem;">
<option value="">All Stations</option>
<option value="hand">Hand Craft</option>
<option value="workbench">Workbench</option>
<option value="smelting-furnace">Smelting Furnace</option>
<option value="charcoal-kiln">Charcoal Kiln</option>
<option value="weaponsmith">Weaponsmith</option>
<option value="armor-workshop">Armor Workshop</option>
<option value="cooking-fire">Cooking Fire</option>
<option value="alchemy-table">Alchemy Table</option>
<option value="millstone">Millstone</option>
</select>
</div>

<div id="recipeCount" style="color:var(--text-muted);font-size:0.85rem;margin-bottom:1rem;"></div>
<div id="recipeResults"></div>

<script>
let recipes = [];
fetch("/data/recipes.json")
  .then(r => r.json())
  .then(d => { recipes = d.recipes || []; renderRecipes(); })
  .catch(() => { document.getElementById("recipeResults").innerHTML = "<p>Failed to load recipes.</p>"; });

const search = document.getElementById("recipeSearch");
const catFilter = document.getElementById("categoryFilter");
const staFilter = document.getElementById("stationFilter");
[search, catFilter, staFilter].forEach(el => el.addEventListener("input", renderRecipes));
[catFilter, staFilter].forEach(el => el.addEventListener("change", renderRecipes));

function renderRecipes() {
  const q = search.value.toLowerCase().trim();
  const cat = catFilter.value;
  const sta = staFilter.value;
  const filtered = recipes.filter(r => {
    if (q && !r.name.toLowerCase().includes(q) && !(r.tips||"").toLowerCase().includes(q)) return false;
    if (cat && r.category !== cat) return false;
    if (sta && r.station !== sta) return false;
    return true;
  });
  document.getElementById("recipeCount").textContent = filtered.length + " recipes found";
  const html = filtered.map(r => {
    const mats = (r.materials||[]).map(m => (m.qty||1) + "× " + m.item).join(" + ");
    const qty = r.result_qty ? " ×" + r.result_qty : "";
    return '<div class="card" style="margin-bottom:0.75rem;padding:1rem;">' +
      '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;">' +
      '<strong style="color:var(--accent);font-size:1.05rem;">' + r.name + qty + '</strong>' +
      '<span class="badge badge-' + (r.confidence==="verified"?"uncommon":"rare") + '">' + (r.confidence||"community") + '</span></div>' +
      '<div style="margin:0.5rem 0;font-size:0.88rem;color:var(--text-secondary);">' +
      '<span style="color:var(--text-muted);">Materials:</span> ' + mats + '</div>' +
      '<div style="font-size:0.82rem;color:var(--text-muted);">' +
      (r.station==="hand"?"Hand Craft":r.station) + (r.station_level?" Lv"+r.station_level:"") +
      ' · ' + r.category +
      (r.tips ? ' · <em>' + r.tips + '</em>' : '') + '</div></div>';
  }).join("");
  document.getElementById("recipeResults").innerHTML = html || '<p style="color:var(--text-muted);">No recipes match your filters.</p>';
}
</script>
</main>
<footer class="footer"><div class="container"><div class="footer-grid"><div class="footer-brand"><a href="/" class="footer-logo"><img src="/imgs/logo.png" alt="Windrose Guides Logo" width="28" height="28"> Windrose Guides</a><p>Your complete Windrose guide hub.</p></div><div class="footer-col"><h4>Guides</h4><ul><li><a href="/beginner-guide">Beginner Guide</a></li><li><a href="/guides">Strategy Guides</a></li><li><a href="/builds">Build Guides</a></li><li><a href="/faq">FAQ</a></li></ul></div><div class="footer-col"><h4>Database</h4><ul><li><a href="/crafting">Crafting</a></li><li><a href="/resources">Resources</a></li><li><a href="/bosses">Bosses</a></li><li><a href="/ships">Ships</a></li><li><a href="/weapons">Weapons</a></li></ul></div><div class="footer-col"><h4>Explore</h4><ul><li><a href="/tools">Tools</a></li><li><a href="/news">News</a></li><li><a href="/about">About</a></li></ul></div></div><div class="footer-bottom"><span>&copy; 2026 Windrose Guides.</span><nav><a href="/pages">All Pages</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a></nav></div></div></footer>
<script>(function(){var b=document.querySelector('.hamburger'),n=document.querySelector('.nav-links');if(!b||!n)return;b.addEventListener('click',function(){var o=n.classList.toggle('open');b.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});})();</script>
</body></html>'''
    write_file("tools/recipe-finder/index.html", html)


# === 3. 资源规划器增强 ===
def enhance_resource_planner():
    html = '''<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Resource Planner — Windrose (2026) | Windrose Guides</title>
<meta name="description" content="Plan your resource gathering in Windrose. Select target items and see all required materials.">
<link rel="canonical" href="https://windrose-guides.com/tools/resource-planner">
<link rel="stylesheet" href="../../css/style.css">
</head><body>
<header class="header"><div class="container"><a href="/" class="logo"><img src="/imgs/logo.png" alt="Windrose Guides Logo" width="32" height="32"> Windrose Guides</a>
<button class="hamburger" aria-label="Toggle navigation" aria-expanded="false"><span></span><span></span><span></span></button>
<nav><ul class="nav-links"><li><a href="/">Home</a></li><li><a href="/beginner-guide">Beginner Guide</a></li><li><a href="/guides">Guides</a></li><li><a href="/crafting">Crafting</a></li><li><a href="/resources">Resources</a></li><li><a href="/bosses">Bosses</a></li><li><a href="/ships">Ships</a></li><li><a href="/weapons">Weapons</a></li><li><a href="/builds">Builds</a></li><li><a href="/faq">FAQ</a></li><li><a href="/news">News</a></li></ul></nav></div></header>
<div class="container"><nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li><a href="/tools/">Tools</a></li><li>Resource Planner</li></ol></nav></div>
<main class="container">
<h1>Resource Planner — Windrose</h1>
<p>Select the items you want to craft and see the total materials needed. Check off items as you gather them.</p>

<div style="margin:1.5rem 0;">
<input type="text" id="itemSearch" placeholder="Search items to add..." style="width:100%;padding:0.8rem 1rem;font-size:1rem;border-radius:8px;border:1px solid var(--border);background:var(--bg-surface);color:var(--text);">
<div id="itemSuggestions" style="margin-top:0.5rem;"></div>
</div>

<h2>Selected Items</h2>
<div id="selectedItems" style="margin:1rem 0;"></div>

<h2>Total Materials Needed</h2>
<div id="materialsSummary" style="margin:1rem 0;"></div>

<script>
let recipes=[], selected=[];
fetch("/data/recipes.json").then(r=>r.json()).then(d=>{recipes=d.recipes||[];});
const search=document.getElementById("itemSearch");
const suggestions=document.getElementById("itemSuggestions");

search.addEventListener("input",()=>{
  const q=search.value.toLowerCase().trim();
  if(q.length<2){suggestions.innerHTML="";return;}
  const matches=recipes.filter(r=>r.name.toLowerCase().includes(q)).slice(0,8);
  suggestions.innerHTML=matches.map(r=>
    '<button class="btn" style="margin:0.25rem;padding:0.4rem 0.8rem;font-size:0.85rem;" onclick="addItem(\''+r.id+'\')">+ '+r.name+'</button>'
  ).join("");
});

window.addItem=function(id){
  if(selected.find(s=>s.id===id))return;
  const recipe=recipes.find(r=>r.id===id);
  if(recipe)selected.push({...recipe,qty:1});
  render();
  search.value="";suggestions.innerHTML="";
};
window.removeItem=function(id){selected=selected.filter(s=>s.id!==id);render();};
window.changeQty=function(id,delta){
  const item=selected.find(s=>s.id===id);
  if(item){item.qty=Math.max(1,item.qty+delta);render();}
};

function render(){
  document.getElementById("selectedItems").innerHTML=selected.length?selected.map(s=>
    '<div class="card" style="margin:0.5rem 0;padding:0.75rem;display:flex;justify-content:space-between;align-items:center;">'+
    '<span><strong>'+s.name+'</strong></span>'+
    '<span>'+
    '<button class="btn" style="padding:0.2rem 0.5rem;font-size:0.8rem;" onclick="changeQty(\''+s.id+'\',-1)">−</button>'+
    ' <strong>'+s.qty+'</strong> '+
    '<button class="btn" style="padding:0.2rem 0.5rem;font-size:0.8rem;" onclick="changeQty(\''+s.id+'\',1)">+</button>'+
    ' <button class="btn" style="padding:0.2rem 0.5rem;font-size:0.8rem;color:var(--accent-red);" onclick="removeItem(\''+s.id+'\')">✕</button>'+
    '</span></div>'
  ).join(""):'<p style="color:var(--text-muted);">No items selected. Search above to add items.</p>';

  const totals={};
  selected.forEach(s=>{
    (s.materials||[]).forEach(m=>{
      totals[m.item]=(totals[m.item]||0)+(m.qty||1)*s.qty;
    });
  });
  const entries=Object.entries(totals).sort((a,b)=>b[1]-a[1]);
  document.getElementById("materialsSummary").innerHTML=entries.length?
    '<div class="table-responsive"><table><thead><tr><th>Material</th><th>Quantity</th><th>Gathered?</th></tr></thead><tbody>'+
    entries.map(([name,qty])=>
      '<tr><td><strong>'+name+'</strong></td><td>'+qty+'</td><td><input type="checkbox" style="width:18px;height:18px;"></td></tr>'
    ).join("")+'</tbody></table></div>':
    '<p style="color:var(--text-muted);">Add items above to see material requirements.</p>';
}
render();
</script>
</main>
<footer class="footer"><div class="container"><div class="footer-bottom"><span>&copy; 2026 Windrose Guides.</span><nav><a href="/pages">All Pages</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a></nav></div></div></footer>
<script>(function(){var b=document.querySelector('.hamburger'),n=document.querySelector('.nav-links');if(!b||!n)return;b.addEventListener('click',function(){var o=n.classList.toggle('open');b.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});})();</script>
</body></html>'''
    write_file("tools/resource-planner/index.html", html)


# === 4. 进度检查表增强 ===
def enhance_checklist():
    html = '''<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Progression Checklist — Windrose (2026) | Windrose Guides</title>
<meta name="description" content="Track your Windrose progression with this interactive checklist. Saves progress in your browser.">
<link rel="canonical" href="https://windrose-guides.com/tools/progression-checklist">
<link rel="stylesheet" href="../../css/style.css">
</head><body>
<header class="header"><div class="container"><a href="/" class="logo"><img src="/imgs/logo.png" alt="Windrose Guides Logo" width="32" height="32"> Windrose Guides</a>
<button class="hamburger" aria-label="Toggle navigation" aria-expanded="false"><span></span><span></span><span></span></button>
<nav><ul class="nav-links"><li><a href="/">Home</a></li><li><a href="/beginner-guide">Beginner Guide</a></li><li><a href="/guides">Guides</a></li><li><a href="/crafting">Crafting</a></li><li><a href="/resources">Resources</a></li><li><a href="/bosses">Bosses</a></li><li><a href="/ships">Ships</a></li><li><a href="/weapons">Weapons</a></li><li><a href="/builds">Builds</a></li><li><a href="/faq">FAQ</a></li><li><a href="/news">News</a></li></ul></nav></div></header>
<div class="container"><nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li><a href="/tools/">Tools</a></li><li>Progression Checklist</li></ol></nav></div>
<main class="container">
<h1>Progression Checklist — Windrose</h1>
<p>Track your game progress! Check items off as you complete them. <strong>Progress saves automatically in your browser.</strong></p>
<div id="progressBar" style="margin:1.5rem 0;background:var(--bg-elevated);border-radius:8px;height:24px;overflow:hidden;border:1px solid var(--border);">
<div id="progressFill" style="height:100%;background:linear-gradient(90deg,var(--accent),#c09340);transition:width 0.3s;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:0.75rem;font-weight:700;color:#0a0e1a;"></div>
</div>
<div id="checklist"></div>
<button class="btn btn-primary" style="margin-top:1.5rem;" onclick="if(confirm('Reset all progress?')){localStorage.removeItem('wr-checklist');location.reload();}">Reset Progress</button>

<script>
const SECTIONS=[
{title:"🏝️ Starting Island",items:[
"Gather 20+ Wood","Gather 15+ Stone","Gather 30+ Plant Fiber","Build Bonfire","Build Workbench",
"Craft Stone Pickaxe","Craft Stone Axe","Build Cooking Fire","Build Tent","Craft Torn Sailcloth Bag",
"Craft 10+ Bandages","Hunt Boars for Rough Hide","Build Armor Workshop (under roof!)","Craft Survivor's Boots"
]},
{title:"⛏️ Mining & Smelting",items:[
"Find Copper Deposit cave (pickaxe icon)","Mine 20+ Poor Copper Ore","Gather 35+ Clay",
"Build Charcoal Kiln","Produce Charcoal","Build Smelting Furnace","Smelt Copper Ingots",
"Craft Copper Pickaxe","Craft Copper Axe"
]},
{title:"⚔️ Combat Readiness",items:[
"Build Weaponsmith Workshop (under roof!)","Craft Saber/Rapier/Club","Learn Perfect Block timing",
"Craft Survivor's Vest + Gloves","Cook food for buffs","Clear first Pirate Camp"
]},
{title:"⛵ First Ship",items:[
"Complete island quest chain","Receive free Ketch","Sail to second island","Place Fast Travel Bell at base",
"Craft Fast Travel Bell (10 Copper Ingot + 3 Rope)"
]},
{title:"🗺️ Foothills Progression",items:[
"Reach Foothills region","Set up temporary outpost","Mine Iron Ore","Smelt Foothills Iron Ingots",
"Build Sawhorse (Workbench Lv2)","Craft Sailor Backpack","Craft Iron Pickaxe",
"Mine Sulfur","Build Millstone","Craft Gunpowder","Craft Flintlock Pistol"
]},
{title:"💀 Boss Progression",items:[
"Defeat Thomas Richards (Boss 1)","Defeat Israel Hands (Boss 2)","Defeat High Priestess (Boss 3)",
"Defeat Ghost Captain (Boss 4)"
]},
{title:"🔧 Advanced",items:[
"Build Toolbox (Workbench Lv3)","Craft Bosun Backpack","Craft Cutlass","Craft Musket",
"Upgrade to Brigantine","Explore all known biomes","Craft Health + Stamina Potions"
]}
];

let saved=JSON.parse(localStorage.getItem("wr-checklist")||"{}");
function render(){
  let total=0,checked=0;
  let html="";
  SECTIONS.forEach((sec,si)=>{
    html+='<section style="margin:1.5rem 0;"><h2>'+sec.title+'</h2>';
    sec.items.forEach((item,ii)=>{
      const key=si+"-"+ii;
      const done=saved[key]||false;
      total++;if(done)checked++;
      html+='<label style="display:flex;align-items:center;gap:0.75rem;padding:0.6rem 0.75rem;margin:0.25rem 0;background:var(--bg-elevated);border-radius:6px;cursor:pointer;border:1px solid '+(done?'var(--border-accent)':'var(--border)')+';transition:all 0.2s;" onmouseover="this.style.borderColor=\'var(--border-accent)\'" onmouseout="this.style.borderColor=\''+(done?'var(--border-accent)':'var(--border)')+'\'">'+
      '<input type="checkbox" '+(done?"checked":"")+' onchange="toggle(\''+key+'\')" style="width:18px;height:18px;accent-color:var(--accent);">'+
      '<span style="'+(done?'text-decoration:line-through;color:var(--text-muted);':'color:var(--text);')+'">'+item+'</span></label>';
    });
    html+='</section>';
  });
  document.getElementById("checklist").innerHTML=html;
  const pct=total?Math.round(checked/total*100):0;
  document.getElementById("progressFill").style.width=pct+"%";
  document.getElementById("progressFill").textContent=pct+"% Complete ("+checked+"/"+total+")";
}
window.toggle=function(key){saved[key]=!saved[key];localStorage.setItem("wr-checklist",JSON.stringify(saved));render();};
render();
</script>
</main>
<footer class="footer"><div class="container"><div class="footer-bottom"><span>&copy; 2026 Windrose Guides.</span><nav><a href="/pages">All Pages</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a></nav></div></div></footer>
<script>(function(){var b=document.querySelector('.hamburger'),n=document.querySelector('.nav-links');if(!b||!n)return;b.addEventListener('click',function(){var o=n.classList.toggle('open');b.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});})();</script>
</body></html>'''
    write_file("tools/progression-checklist/index.html", html)


if __name__ == "__main__":
    print("=== Phase 3: Tool Enhancement ===")
    rebuild_search_index()
    enhance_recipe_finder()
    enhance_resource_planner()
    enhance_checklist()
    print("\nPhase 3 complete!")
