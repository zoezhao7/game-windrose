"""
批量将所有页面的 footer 替换为分类式三列布局。
标准 footer 结构：品牌区 + Guides / Database / Explore 三列 + 底部法律链接行。
"""
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")

# 标准 footer HTML（使用绝对路径，所有页面通用）
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


def fix_footer(filepath):
    """替换文件中的 footer"""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # 匹配整个 <footer class="footer">...</footer> 块
    pattern = re.compile(r'<footer\s+class="footer"[^>]*>.*?</footer>', re.DOTALL)
    m = pattern.search(content)
    if not m:
        return False

    old_footer = m.group()
    if "footer-grid" in old_footer:
        # 已经是新格式
        return False

    new_content = content[:m.start()] + STANDARD_FOOTER + content[m.end():]

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False


count = 0
for dirpath, dirs, files in os.walk(ROOT):
    rel_dir = os.path.relpath(dirpath, ROOT)
    if rel_dir.startswith(("docs", "scripts", "data", "css", "js", "imgs", ".git", "node_modules")):
        continue
    for f in files:
        if f == "index.html":
            fp = os.path.join(dirpath, f)
            if fix_footer(fp):
                rel = os.path.relpath(fp, ROOT)
                print(f"  Fixed: {rel}")
                count += 1

print(f"\nTotal fixed: {count} files")
