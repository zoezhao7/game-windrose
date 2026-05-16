"""
批量在所有 HTML 页面的顶部导航中添加 Crafting 链接。
在 Guides 链接之前插入 Crafting 导航项。
"""
import os
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 需要匹配的旧导航片段（Guides 链接之前没有 Crafting）
OLD_PATTERN = '<li><a href="/guides"'
NEW_INSERT = '<li><a href="/crafting">Crafting</a></li>\n                <li><a href="/guides"'

# 处理中文版的情况
OLD_PATTERN_ZH = '<li><a href="/zh/guides"'
NEW_INSERT_ZH = '<li><a href="/zh/crafting">制作配方</a></li>\n                <li><a href="/zh/guides"'

# 确保不重复插入的检查
ALREADY_EXISTS = 'href="/crafting">Crafting</a>'
ALREADY_EXISTS_ZH = 'href="/zh/crafting"'

count = 0
for html_path in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # 检查是否已有 Crafting 导航链接
    if ALREADY_EXISTS not in content and OLD_PATTERN in content:
        content = content.replace(OLD_PATTERN, NEW_INSERT)
        modified = True

    # 中文版处理
    if ALREADY_EXISTS_ZH not in content and OLD_PATTERN_ZH in content:
        content = content.replace(OLD_PATTERN_ZH, NEW_INSERT_ZH)
        modified = True

    if modified:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Updated: {os.path.relpath(html_path, ROOT)}")

print(f"\nTotal files updated: {count}")
