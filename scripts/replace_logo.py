"""
批量将所有 HTML 文件中的锚点字符 ⚓ logo 替换为 <img> 标签。
处理两种场景：
1. header .logo — 将 ⚓ 替换为 <img src="/imgs/logo.png">
2. footer .footer-logo — 同样替换
"""
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGO_IMG_HEADER = '<img src="/imgs/logo.png" alt="Windrose Guides Logo" width="32" height="32">'
LOGO_IMG_FOOTER = '<img src="/imgs/logo.png" alt="Windrose Guides Logo" width="28" height="28">'

# NOTE: 中文版页面使用不同的站点名称
LOGO_IMG_HEADER_ZH = '<img src="/imgs/logo.png" alt="Windrose 攻略 Logo" width="32" height="32">'
LOGO_IMG_FOOTER_ZH = '<img src="/imgs/logo.png" alt="Windrose 攻略 Logo" width="28" height="28">'

count = 0

for html_file in ROOT.rglob("*.html"):
    # 跳过 node_modules 等无关目录
    if "node_modules" in str(html_file):
        continue

    text = html_file.read_text(encoding="utf-8")
    original = text

    # --- header logo ---
    # 匹配: <a href="..." class="logo" ...>⚓ Windrose Guides</a>
    # 也匹配: <a href="..." class="logo">⚓ Windrose Guides</a>
    text = re.sub(
        r'(<a\s+href="[^"]*"\s+class="logo"[^>]*>)\s*⚓\s*(Windrose Guides)\s*(</a>)',
        rf'\1{LOGO_IMG_HEADER} \2\3',
        text,
    )
    # 中文版 header
    text = re.sub(
        r'(<a\s+href="[^"]*"\s+class="logo"[^>]*>)\s*⚓\s*(Windrose 攻略)\s*(</a>)',
        rf'\1{LOGO_IMG_HEADER_ZH} \2\3',
        text,
    )

    # --- footer logo ---
    # 匹配: <a href="..." class="footer-logo">⚓ Windrose Guides</a>
    text = re.sub(
        r'(<a\s+href="[^"]*"\s+class="footer-logo"[^>]*>)\s*⚓\s*(Windrose Guides)\s*(</a>)',
        rf'\1{LOGO_IMG_FOOTER} \2\3',
        text,
    )
    # 中文版 footer
    text = re.sub(
        r'(<a\s+href="[^"]*"\s+class="footer-logo"[^>]*>)\s*⚓\s*(Windrose 攻略)\s*(</a>)',
        rf'\1{LOGO_IMG_FOOTER_ZH} \2\3',
        text,
    )

    # --- 处理已经没有 ⚓ 但 logo 链接中还没有 img 标签的情况 ---
    # 匹配: <a href="..." class="logo" ...>Windrose Guides</a> (无 img)
    text = re.sub(
        r'(<a\s+href="[^"]*"\s+class="logo"[^>]*>)\s*(?!<img)(Windrose Guides)\s*(</a>)',
        rf'\1{LOGO_IMG_HEADER} \2\3',
        text,
    )

    if text != original:
        html_file.write_text(text, encoding="utf-8")
        count += 1

print(f"已更新 {count} 个 HTML 文件")
