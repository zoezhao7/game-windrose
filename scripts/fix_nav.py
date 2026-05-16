"""
批量统一所有页面的导航栏链接。
标准导航与 templates.py 一致。
"""
import os
import re
import sys
sys.path.insert(0, os.path.dirname(__file__))
from templates import NAV_ITEMS

ROOT = os.path.join(os.path.dirname(__file__), "..")

# 转换 (label, href) → (href, label)，不含 Home（build_nav_html 单独加）
STANDARD_NAV_ITEMS = [(href, label) for label, href in NAV_ITEMS if href != "/"]

def build_nav_html(active_href=None, indent="", is_inline=False):
    """生成标准化导航 HTML"""
    items = []
    home_li = '<li><a href="/">Home</a></li>'
    items.append(home_li)
    for href, label in STANDARD_NAV_ITEMS:
        if active_href and href == active_href:
            items.append(f'<li><a href="{href}" class="active">{label}</a></li>')
        else:
            items.append(f'<li><a href="{href}">{label}</a></li>')
    if is_inline:
        return "".join(items)
    else:
        sep = "\n" + indent
        return sep.join(items)

def detect_active(content, filepath):
    """检测当前页面在导航中的 active 链接"""
    rel = os.path.relpath(filepath, ROOT).replace("\\", "/")
    # 直接匹配已有的 active 标记
    m = re.search(r'class="active"[^>]*href="(/[^"]*)"', content)
    if not m:
        m = re.search(r'href="(/[^"]*)"[^>]*class="active"', content)
    if m:
        active = m.group(1).rstrip("/")
        # 只保留标准菜单中的项
        for href, _ in STANDARD_NAV_ITEMS:
            if active == href or active == href + "/":
                return href
    # 基于路径推断
    for href, _ in STANDARD_NAV_ITEMS:
        clean = href.lstrip("/")
        if rel.startswith(clean + "/") or rel.startswith(clean + "\\"):
            return href
    return None

def fix_nav(filepath):
    """修复单个文件的导航栏"""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # 匹配导航列表区域
    # 模式1: 多行格式 <ul class="nav-links">.....</ul>
    # 模式2: 内联格式 <ul class="nav-links"><li>...</li>...</ul>
    pattern = re.compile(
        r'(<ul\s+class="nav-links"[^>]*>)\s*(.*?)\s*(</ul>)',
        re.DOTALL
    )
    m = pattern.search(content)
    if not m:
        return False

    active = detect_active(content, filepath)

    # 检测缩进风格
    old_nav = m.group(0)
    # 是否是内联模式（整个 nav 在几行内）
    lines = old_nav.split("\n")
    is_inline = len(lines) <= 3

    if is_inline:
        nav_items = build_nav_html(active, "", is_inline=True)
        new_nav = f'<ul class="nav-links">{nav_items}</ul>'
    else:
        # 检测缩进
        indent_match = re.search(r'\n(\s+)<li>', old_nav)
        indent = indent_match.group(1) if indent_match else "                "
        nav_items = build_nav_html(active, indent, is_inline=False)
        new_nav = f'<ul class="nav-links">\n{indent}{nav_items}\n{indent[:-4] if len(indent) >= 4 else indent}</ul>'

    new_content = content[:m.start()] + new_nav + content[m.end():]

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

count = 0
for dirpath, dirs, files in os.walk(ROOT):
    # 跳过 docs, scripts, data 等非页面目录
    rel_dir = os.path.relpath(dirpath, ROOT)
    if rel_dir.startswith(("docs", "scripts", "data", "css", "js", "imgs", ".git", "node_modules")):
        continue
    for f in files:
        if f == "index.html":
            fp = os.path.join(dirpath, f)
            if fix_nav(fp):
                rel = os.path.relpath(fp, ROOT)
                print(f"  Fixed: {rel}")
                count += 1

print(f"\nTotal fixed: {count} files")
