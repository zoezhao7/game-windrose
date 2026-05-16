"""审计所有页面的导航栏链接，找出不一致的模式"""
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
results = {}

for dirpath, dirs, files in os.walk(ROOT):
    for f in files:
        if f == "index.html":
            fp = os.path.join(dirpath, f)
            with open(fp, encoding="utf-8") as fh:
                content = fh.read()
            m = re.search(r"nav-links.*?</ul>", content, re.DOTALL)
            if m:
                hrefs = re.findall(r'href="(/[^"]+?)"', m.group())
                key = "|".join(hrefs)
                rel = os.path.relpath(fp, ROOT)
                if key not in results:
                    results[key] = []
                results[key].append(rel)

for i, (k, pages) in enumerate(results.items()):
    links = k.split("|")
    print(f"--- Pattern {i+1} ({len(pages)} pages) ---")
    print(f"Links: {links}")
    for p in pages:
        print(f"  {p}")
    print()
