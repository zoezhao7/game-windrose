import os
import shutil
import json

ARTIFACTS_DIR = r"C:\Users\Administrator\.gemini\antigravity\brain\0ab50141-2ba0-4d74-9cf5-84ff009eae30"
PROJECT_DIR = r"f:\aicode\gamedoc"
IMGS_DIR = os.path.join(PROJECT_DIR, "imgs")

IMAGES = {
    "og_home_1778634819630.png": "og_home.png",
    "og_bosses_1778634838479.png": "og_bosses.png",
    "og_ships_1778634852626.png": "og_ships.png",
    "hero_bg_1778634867196.png": "hero_bg.png",
    "og_weapons_1778634892460.png": "og_weapons.png",
    "icon_boss_1778634917295.png": "icon_boss.png",
    "icon_weapon_1778634932802.png": "icon_weapon.png",
    "icon_ship_1778634947378.png": "icon_ship.png"
}

print("1. Copying images...")
os.makedirs(IMGS_DIR, exist_ok=True)
for src_name, dst_name in IMAGES.items():
    src = os.path.join(ARTIFACTS_DIR, src_name)
    dst = os.path.join(IMGS_DIR, dst_name)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied {dst_name}")

print("\n2. Updating OG Images in HTML files...")
OG_MAPPING = {
    "index.html": "og_home.png",
    "zh/index.html": "og_home.png",
    "bosses/index.html": "og_bosses.png",
    "weapons/index.html": "og_weapons.png",
    "ships/index.html": "og_ships.png",
}

for root, dirs, files in os.walk(PROJECT_DIR):
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, PROJECT_DIR).replace("\\", "/")
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            og_img = "og_home.png"
            if rel_path in OG_MAPPING:
                og_img = OG_MAPPING[rel_path]
            elif rel_path.startswith("bosses/"):
                og_img = "og_bosses.png"
            elif rel_path.startswith("ships/"):
                og_img = "og_ships.png"
            elif rel_path.startswith("weapons/"):
                og_img = "og_weapons.png"
            
            content = content.replace("https://windrose-guides.com/imgs/og.webp", f"https://windrose-guides.com/imgs/{og_img}")
            content = content.replace("https://windrose-guides.com/imgs/og-ships.webp", f"https://windrose-guides.com/imgs/{og_img}")
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

print("\n3. Adding Hero Background to homepage...")
index_path = os.path.join(PROJECT_DIR, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index_html = f.read()

if 'class="hero"' in index_html and 'style="background-image' not in index_html:
    index_html = index_html.replace(
        '<section class="hero">', 
        '<section class="hero" style="background-image: linear-gradient(rgba(10, 14, 26, 0.8), rgba(10, 14, 26, 0.9)), url(\'/imgs/hero_bg.png\'); background-size: cover; background-position: center; border-radius: var(--radius); padding: 4rem 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">'
    )
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print("Added hero background to index.html")

print("\n4. Adding Icons to Bosses, Weapons, Ships pages...")
def inject_icon(filepath, header_text, icon_name):
    if not os.path.exists(filepath):
        return
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    
    if icon_name not in html:
        html = html.replace(
            f"<h1>{header_text}</h1>",
            f'<div style="display: flex; align-items: center; gap: 1rem;">\n        <img src="/imgs/{icon_name}" alt="Icon" style="width: 64px; height: 64px; border-radius: 8px; border: 1px solid var(--border);">\n        <h1 style="margin: 0;">{header_text}</h1>\n    </div>'
        )
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Added {icon_name} to {filepath}")

inject_icon(os.path.join(PROJECT_DIR, "bosses", "index.html"), "Windrose Boss Tracker", "icon_boss.png")
inject_icon(os.path.join(PROJECT_DIR, "weapons", "index.html"), "Windrose Weapons Tier List &amp; Armor Guide (2026)", "icon_weapon.png")
inject_icon(os.path.join(PROJECT_DIR, "ships", "index.html"), "Windrose Ships Guide: Ketch, Brigantine &amp; Frigate (2026)", "icon_ship.png")

print("\n5. Updating FAQ HTML with 12 new items...")
faq_path = os.path.join(PROJECT_DIR, "faq", "index.html")
faq_json_path = os.path.join(PROJECT_DIR, "data", "faq-expansion.json")
if os.path.exists(faq_path) and os.path.exists(faq_json_path):
    with open(faq_json_path, "r", encoding="utf-8") as f:
        new_faqs = json.load(f).get("new_items", [])
    
    with open(faq_path, "r", encoding="utf-8") as f:
        faq_html = f.read()
    
    if "How do I get Sulfur" not in faq_html:
        faq_items_html = ""
        current_num = 20
        for q, a in new_faqs:
            current_num += 1
            faq_items_html += f"""
<details>
    <summary>{current_num}. {q}</summary>
    <div class="faq-answer">
        <p>{a}</p>
    </div>
</details>"""
        
        insert_pos = faq_html.find('</section>', faq_html.find('id="faq-list"'))
        if insert_pos != -1:
            faq_html = faq_html[:insert_pos] + faq_items_html + "\n" + faq_html[insert_pos:]
            with open(faq_path, "w", encoding="utf-8") as f:
                f.write(faq_html)
            print("Added 12 new FAQs to faq/index.html")
    else:
        print("FAQs already added.")
