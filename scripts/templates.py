"""共享 HTML 模板片段，供各生成脚本导入复用。"""
import html as html_mod

NAV_ITEMS = [
    ("Home", "/"),
    ("Beginner Guide", "/beginner-guide"),
    ("Database", "/database"),
    ("Bosses", "/bosses"),
    ("Ships", "/ships"),
    ("Guides", "/guides"),
    ("Tools", "/tools"),
    ("News", "/news"),
    ("Search \U0001f50d", "/search"),
]


def header_html(active=""):
    items = []
    for label, href in NAV_ITEMS:
        is_active = False
        if active:
            if href == active:
                is_active = True
            elif href != "/" and active.startswith(href.strip("/")):
                is_active = True
        cls = ' class="active"' if is_active else ""
        current = ' aria-current="page"' if is_active else ""
        items.append(
            f'<li><a href="{href}"{cls}{current}>{html_mod.escape(label)}</a></li>'
        )
    nav = "".join(items)
    return (
        '<header class="header"><div class="container">'
        '<a href="/" class="logo" aria-label="Windrose Guides Home"><img src="/imgs/logo.png" alt="Windrose Guides Logo" width="32" height="32"> Windrose Guides</a>'
        '<button class="hamburger" aria-label="Toggle navigation menu" aria-expanded="false">'
        '<span></span><span></span><span></span></button>'
        '<nav aria-label="Primary"><ul class="nav-links">'
        + nav +
        "</ul></nav></div></header>"
    )