"""修复使用 <footer> 裸标签的页面，替换为标准分类 footer"""
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")

STANDARD_FOOTER = '''<footer class="footer">
    <div class="container">
        <div class="footer-grid">
            <div class="footer-brand">
                <a href="/" class="footer-logo"><img src="/imgs/logo.png" alt="Windrose Guides Logo" width="28" height="28"> Windrose Guides</a>
                <p>Your complete Windrose wiki, database, and guide hub. Crafting recipes, resource maps, boss strategies, ship builds, and more &mdash; all in one place.</p>
            </div>
            <div class="footer-col">
                <h4>Guides</h4>
                <ul>
                    <li><a href="/beginner-guide">Beginner Guide</a></li>
                    <li><a href="/builds">Build Guides</a></li>
                    <li><a href="/server-guide">Server Guide</a></li>
                    <li><a href="/download">Download</a></li>
                    <li><a href="/faq">FAQ</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>Database</h4>
                <ul>
                    <li><a href="/crafting">Crafting</a></li>
                    <li><a href="/resources">Resources</a></li>
                    <li><a href="/bosses">Bosses</a></li>
                    <li><a href="/ships">Ships</a></li>
                    <li><a href="/weapons">Weapons</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>Explore</h4>
                <ul>
                    <li><a href="/tools">Tools</a></li>
                    <li><a href="/news">News</a></li>
                    <li><a href="/sources">Sources</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <span>&copy; 2026 Windrose Guides. Unofficial fan resource. Not affiliated with Kraken Express or Pocketpair Publishing.</span>
            <nav>
                <a href="/pages">All Pages</a>
                <a href="/privacy">Privacy Policy</a>
                <a href="/terms">Terms of Service</a>
            </nav>
        </div>
    </div>
</footer>'''

count = 0
for dirpath, dirs, files in os.walk(ROOT):
    rel_dir = os.path.relpath(dirpath, ROOT)
    if rel_dir.startswith(("docs", "scripts", "data", "css", "js", "imgs", ".git", "node_modules")):
        continue
    for f in files:
        if f == "index.html":
            fp = os.path.join(dirpath, f)
            with open(fp, encoding="utf-8") as fh:
                content = fh.read()
            if "footer-grid" in content:
                continue
            # 匹配任意 footer 标签
            m = re.search(r"<footer[^>]*>.*?</footer>", content, re.DOTALL)
            if m:
                new_content = content[:m.start()] + STANDARD_FOOTER + content[m.end():]
                with open(fp, "w", encoding="utf-8") as fh:
                    fh.write(new_content)
                rel = os.path.relpath(fp, ROOT)
                print(f"  Fixed: {rel}")
                count += 1

print(f"\nTotal fixed: {count} files")
