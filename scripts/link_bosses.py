import os
import shutil

PROJECT_DIR = r"f:\aicode\gamedoc"
BOSSES_DIR = os.path.join(PROJECT_DIR, "bosses")

def setup_boss_page(src_dir, target_dir_name, old_name, new_name):
    target_dir = os.path.join(BOSSES_DIR, target_dir_name)
    if not os.path.exists(target_dir):
        if os.path.exists(os.path.join(BOSSES_DIR, src_dir)):
            shutil.copytree(os.path.join(BOSSES_DIR, src_dir), target_dir)
        else:
            print(f"Source dir {src_dir} not found for {new_name}")
            return
            
    # Update content
    idx_path = os.path.join(target_dir, "index.html")
    if os.path.exists(idx_path):
        with open(idx_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace occurrences of old boss details with new
        content = content.replace(old_name, new_name)
        content = content.replace(old_name.lower(), new_name.lower())
        content = content.replace("boss-01", target_dir_name)
        content = content.replace("boss-02", target_dir_name)
        content = content.replace("Second Boss", new_name)
        content = content.replace("First Boss", new_name)
        
        with open(idx_path, "w", encoding="utf-8") as f:
            f.write(content)

print("1. Creating specific boss directories and pages...")
setup_boss_page("boss-01", "thomas-richards", "First Boss", "Thomas Richards")
setup_boss_page("boss-02", "israel-hands", "Second Boss", "Israel Hands")
setup_boss_page("israel-hands", "high-priestess", "Israel Hands", "High Priestess")
setup_boss_page("israel-hands", "ghost-captain", "Israel Hands", "Ghost Captain")

# Clean up old boss-01 and boss-02 if they were successfully copied
if os.path.exists(os.path.join(BOSSES_DIR, "thomas-richards")) and os.path.exists(os.path.join(BOSSES_DIR, "boss-01")):
    shutil.rmtree(os.path.join(BOSSES_DIR, "boss-01"))
if os.path.exists(os.path.join(BOSSES_DIR, "israel-hands")) and os.path.exists(os.path.join(BOSSES_DIR, "boss-02")):
    shutil.rmtree(os.path.join(BOSSES_DIR, "boss-02"))

print("\n2. Updating bosses/index.html to include links...")
bosses_idx = os.path.join(BOSSES_DIR, "index.html")
with open(bosses_idx, "r", encoding="utf-8") as f:
    html = f.read()

# Wrap boss names in anchor tags
replacements = {
    'Thomas Richards</td>': '<a href="/bosses/thomas-richards">Thomas Richards</a></td>',
    'Israel Hands</td>': '<a href="/bosses/israel-hands">Israel Hands</a></td>',
    'High Priestess</td>': '<a href="/bosses/high-priestess">High Priestess</a></td>',
    'Ghost Captain</td>': '<a href="/bosses/ghost-captain">Ghost Captain</a></td>',
    "Charon's Obols</td>": '<a href="/bosses/charons-obols">Charon\'s Obols</a></td>'
}

for old, new in replacements.items():
    if new not in html:
        html = html.replace(old, new)

with open(bosses_idx, "w", encoding="utf-8") as f:
    f.write(html)

print("Done. All bosses are now clickable.")
