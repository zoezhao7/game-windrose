import os, re

project = r"F:\aicode\gamedoc"
all_pages = []
for root, dirs, files in os.walk(project):
    for f in files:
        if f == "index.html":
            rel = os.path.relpath(os.path.join(root, f), project).replace("\\", "/")
            url = "/" + rel.replace("/index.html", "/").replace("index.html", "")
            all_pages.append(url)

# Collect links from guides, database, and home
guides_path = os.path.join(project, "guides", "index.html")
db_path = os.path.join(project, "database", "index.html")
home_path = os.path.join(project, "index.html")

linked = set()
for check_file in [guides_path, db_path, home_path]:
    with open(check_file, "r", encoding="utf-8") as fh:
        content = fh.read()
    for m in re.findall(r'href="(/[^"#]+?)"', content):
        url = m.rstrip("/") + "/"
        linked.add(url)

print("=== ALL PAGES ===")
orphaned = []
for p in sorted(all_pages):
    is_linked = any(p.rstrip("/").startswith(l.rstrip("/")) or l.rstrip("/").startswith(p.rstrip("/")) for l in linked)
    status = "OK" if is_linked else "ORPHAN"
    if status == "ORPHAN":
        orphaned.append(p)
    print(f"{status}: {p}")

print(f"\nTotal: {len(all_pages)} pages, {len(orphaned)} orphans")
if orphaned:
    print("\n=== ORPHANED PAGES ===")
    for o in orphaned:
        print(o)
