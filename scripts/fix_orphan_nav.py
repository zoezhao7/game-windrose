"""一次性修复 database/items/ 下残留旧导航的历史页面"""
import os
import re
import sys
sys.path.insert(0, os.path.dirname(__file__))
from templates import header_html

ROOT = os.path.join(os.path.dirname(__file__), "..")

NEW_HEADER = header_html("database")

# 匹配旧版 header 块：<header class="header"><div class="container">...品牌内容...</ul></div></header>
OLD_HEADER_RE = re.compile(
    r'<header class="header"><div class="container">\s*'
    r'<a href="/" class="logo">[^<]*</a>\s*'
    r'<button class="hamburger"[^>]*><span></span><span></span><span></span></button>\s*'
    r'<ul class="nav-links">.*?</ul>\s*'
    r'</div></header>',
    re.DOTALL
)

count = 0
items_dir = os.path.join(ROOT, "database", "items")
for dirpath, dirs, files in os.walk(items_dir):
    for f in files:
        if f == "index.html":
            fp = os.path.join(dirpath, f)
            with open(fp, encoding="utf-8") as fh:
                content = fh.read()
            if "<nav aria-label=" in content:
                continue  # 已经修复过的跳过
            new_content = OLD_HEADER_RE.sub(NEW_HEADER, content, count=1)
            if new_content != content:
                with open(fp, "w", encoding="utf-8") as fh:
                    fh.write(new_content)
                rel = os.path.relpath(fp, ROOT)
                print(f"  Fixed: {rel}")
                count += 1

print(f"\nTotal fixed: {count} files")