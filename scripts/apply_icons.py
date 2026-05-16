import os
import shutil

ARTIFACTS_DIR = r"C:\Users\Administrator\.gemini\antigravity\brain\0ab50141-2ba0-4d74-9cf5-84ff009eae30"
PROJECT_DIR = r"f:\aicode\gamedoc"
IMGS_DIR = os.path.join(PROJECT_DIR, "imgs")

IMAGES = {
    "thomas_richards_1778636803977.png": "thomas_richards.png",
    "israel_hands_1778636817896.png": "israel_hands.png",
    "high_priestess_1778636833693.png": "high_priestess.png",
    "ghost_captain_1778636859455.png": "ghost_captain.png",
    "ship_ketch_1778636899685.png": "ship_ketch.png",
    "ship_brigantine_1778636913808.png": "ship_brigantine.png",
    "ship_frigate_1778636930393.png": "ship_frigate.png",
    "weapon_musket_1778636947652.png": "weapon_musket.png",
    "weapon_blunderbuss_1778636975393.png": "weapon_blunderbuss.png"
}

print("1. Copying images...")
for src_name, dst_name in IMAGES.items():
    src = os.path.join(ARTIFACTS_DIR, src_name)
    dst = os.path.join(IMGS_DIR, dst_name)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied {dst_name}")

print("\n2. Updating HTML files...")
bosses_path = os.path.join(PROJECT_DIR, "bosses", "index.html")
if os.path.exists(bosses_path):
    with open(bosses_path, "r", encoding="utf-8") as f:
        html = f.read()
    html = html.replace('<td>Thomas Richards</td>', '<td><img src="/imgs/thomas_richards.png" alt="Thomas Richards" style="width: 48px; height: 48px; border-radius: 4px; vertical-align: middle; margin-right: 8px;">Thomas Richards</td>')
    html = html.replace('<td>Israel Hands</td>', '<td><img src="/imgs/israel_hands.png" alt="Israel Hands" style="width: 48px; height: 48px; border-radius: 4px; vertical-align: middle; margin-right: 8px;">Israel Hands</td>')
    html = html.replace('<td>High Priestess</td>', '<td><img src="/imgs/high_priestess.png" alt="High Priestess" style="width: 48px; height: 48px; border-radius: 4px; vertical-align: middle; margin-right: 8px;">High Priestess</td>')
    html = html.replace('<td>Ghost Captain</td>', '<td><img src="/imgs/ghost_captain.png" alt="Ghost Captain" style="width: 48px; height: 48px; border-radius: 4px; vertical-align: middle; margin-right: 8px;">Ghost Captain</td>')
    with open(bosses_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated bosses HTML.")

ships_path = os.path.join(PROJECT_DIR, "ships", "index.html")
if os.path.exists(ships_path):
    with open(ships_path, "r", encoding="utf-8") as f:
        html = f.read()
    html = html.replace('<div class="nav-icon">⛵</div>\n                    <h3>Ketch (Tier 1)</h3>', '<img src="/imgs/ship_ketch.png" alt="Ketch" style="width: 64px; height: 64px; border-radius: 8px; margin-bottom: 0.5rem;">\n                    <h3>Ketch (Tier 1)</h3>')
    html = html.replace('<div class="nav-icon">⛵</div>\n                    <h3>Brigantine (Tier 2)</h3>', '<img src="/imgs/ship_brigantine.png" alt="Brigantine" style="width: 64px; height: 64px; border-radius: 8px; margin-bottom: 0.5rem;">\n                    <h3>Brigantine (Tier 2)</h3>')
    html = html.replace('<div class="nav-icon">🚢</div>\n                    <h3>Frigate (Tier 3)</h3>', '<img src="/imgs/ship_frigate.png" alt="Frigate" style="width: 64px; height: 64px; border-radius: 8px; margin-bottom: 0.5rem;">\n                    <h3>Frigate (Tier 3)</h3>')
    with open(ships_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated ships HTML.")

weapons_path = os.path.join(PROJECT_DIR, "weapons", "index.html")
if os.path.exists(weapons_path):
    with open(weapons_path, "r", encoding="utf-8") as f:
        html = f.read()
    html = html.replace('<span class="tier-item">Rapier of a Thousand Cuts</span>', '<span class="tier-item"><img src="/imgs/icon_weapon.png" style="width:24px; height:24px; vertical-align: middle; margin-right: 4px;">Rapier of a Thousand Cuts</span>')
    html = html.replace('<span class="tier-item">Reliable Musket</span>', '<span class="tier-item"><img src="/imgs/weapon_musket.png" style="width:24px; height:24px; vertical-align: middle; margin-right: 4px;">Reliable Musket</span>')
    html = html.replace('<span class="tier-item">Cutlass</span>', '<span class="tier-item"><img src="/imgs/icon_weapon.png" style="width:24px; height:24px; vertical-align: middle; margin-right: 4px;">Cutlass</span>')
    html = html.replace('<span class="tier-item">Blunderbuss</span>', '<span class="tier-item"><img src="/imgs/weapon_blunderbuss.png" style="width:24px; height:24px; vertical-align: middle; margin-right: 4px;">Blunderbuss</span>')
    with open(weapons_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated weapons HTML.")

print("\nDone.")
