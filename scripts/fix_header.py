"""
批量替换所有 HTML 页面的顶部导航栏

解决问题：导航项过多导致在 1100px 容器内换行。
方案：
  1. 统一 header HTML 结构
  2. 缩短 "Beginner Guide" 为 "Beginner"
  3. 移除 Crafting（已被 Database 覆盖）
  4. 保持每个页面原有的 active 状态
  5. 配合 CSS 修改（container 扩至 1320px, 更紧凑间距）

使用方式:
  python scripts/fix_header.py          # dry-run 模式（默认），仅统计
  python scripts/fix_header.py --apply  # 真正执行替换
"""

import os
import re
import sys
from pathlib import Path

# NOTE: 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# NOTE: 需要跳过的目录
SKIP_DIRS = {".git", "node_modules", "__pycache__", "scripts", "data", "docs"}

# NOTE: 根据页面路径判断哪个导航项应该是 active
ACTIVE_MAP = {
    "/": "Home",
    "/index.html": "Home",
    "/beginner-guide": "Beginner",
    "/database": "Database",
    "/bosses": "Bosses",
    "/ships": "Ships",
    "/crafting": "Crafting",
    "/guides": "Guides",
    "/tools": "Tools",
    "/news": "News",
    "/search": "Search",
    "/builds": "Guides",
    "/weapons": "Database",
    "/resources": "Database",
    "/skills": "Database",
    "/server-guide": "Guides",
    "/download": "Home",
    "/faq": "Guides",
    "/building": "Crafting",
}


def detectActivePage(filePath: str) -> str:
    """
    根据文件路径推断当前页面对应的导航高亮项。
    使用最长前缀匹配确保子路径正确匹配父级导航。
    """
    relPath = os.path.relpath(filePath, PROJECT_ROOT).replace("\\", "/")

    # 去掉 index.html 后缀
    if relPath.endswith("/index.html"):
        relPath = relPath[:-len("index.html")]
    elif relPath == "index.html":
        return "Home"

    # 标准化为 /xxx/ 格式
    urlPath = "/" + relPath.rstrip("/")

    # 最长前缀匹配
    bestMatch = ""
    bestActive = ""
    for prefix, active in ACTIVE_MAP.items():
        if urlPath.startswith(prefix) and len(prefix) > len(bestMatch):
            bestMatch = prefix
            bestActive = active

    return bestActive if bestActive else ""


def buildNewHeader(activePage: str) -> str:
    """
    生成新的 header HTML 片段。
    导航项列表经过精简，避免在宽屏幕上换行。
    """
    navItems = [
        ("/", "Home"),
        ("/beginner-guide", "Beginner"),
        ("/database", "Database"),
        ("/bosses", "Bosses"),
        ("/ships", "Ships"),
        ("/crafting", "Crafting"),
        ("/guides", "Guides"),
        ("/tools", "Tools"),
        ("/news", "News"),
        ("/search", "Search 🔍"),
    ]

    navLi = []
    for href, label in navItems:
        # 判断 active 状态
        cleanLabel = label.replace(" 🔍", "")
        if cleanLabel == activePage:
            navLi.append(
                f'<li><a href="{href}" class="active">{label}</a></li>'
            )
        else:
            navLi.append(f'<li><a href="{href}">{label}</a></li>')

    navLinksHtml = "".join(navLi)

    # NOTE: 统一的 header 结构，包含 hamburger 和 nav 标签
    header = (
        '<header class="header">\n'
        '    <div class="container">\n'
        '        <a href="/" class="logo" aria-label="Windrose Guides Home">'
        '<img src="/imgs/logo.png" alt="Windrose Guides Logo" width="32" height="32">'
        " Windrose Guides</a>\n"
        '        <button class="hamburger" aria-label="Toggle navigation menu" '
        'aria-expanded="false"><span></span><span></span><span></span></button>\n'
        '        <nav aria-label="Primary">\n'
        f'            <ul class="nav-links">{navLinksHtml}</ul>\n'
        "        </nav>\n"
        "    </div>\n"
        "</header>"
    )
    return header


# NOTE: 正则匹配现有的 <header class="header"> 到 </header> 之间的全部内容
# 使用 DOTALL 模式匹配跨行内容
HEADER_PATTERN = re.compile(
    r'<header\s+class="header"[\s\S]*?</header>',
    re.IGNORECASE,
)


def processFile(filePath: str, apply: bool) -> bool:
    """
    处理单个 HTML 文件：检测并替换 header。
    返回 True 表示该文件需要/已经被修改。
    """
    try:
        with open(filePath, "r", encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError) as e:
        print(f"  SKIP (read error): {filePath} — {e}")
        return False

    match = HEADER_PATTERN.search(content)
    if not match:
        return False

    activePage = detectActivePage(filePath)
    newHeader = buildNewHeader(activePage)

    oldHeader = match.group(0)

    # 如果已经完全一致，跳过
    # NOTE: 标准化比较，忽略空白差异
    if normalizeWhitespace(oldHeader) == normalizeWhitespace(newHeader):
        return False

    if apply:
        newContent = content[:match.start()] + newHeader + content[match.end():]
        with open(filePath, "w", encoding="utf-8") as f:
            f.write(newContent)

    return True


def normalizeWhitespace(text: str) -> str:
    """标准化空白用于比较"""
    return re.sub(r"\s+", " ", text).strip()


def main():
    apply = "--apply" in sys.argv
    mode = "APPLY" if apply else "DRY-RUN"
    print(f"=== Header 批量替换脚本 ({mode}) ===\n")

    totalFiles = 0
    changedFiles = 0
    skippedDirs = 0

    for root, dirs, files in os.walk(PROJECT_ROOT):
        # 跳过不需要扫描的目录
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for fileName in files:
            if not fileName.endswith(".html"):
                continue

            filePath = os.path.join(root, fileName)
            totalFiles += 1

            changed = processFile(filePath, apply)
            if changed:
                changedFiles += 1
                relPath = os.path.relpath(filePath, PROJECT_ROOT)
                activePage = detectActivePage(filePath)
                action = "UPDATED" if apply else "WOULD UPDATE"
                print(f"  {action}: {relPath} (active={activePage})")

    print(f"\n--- 统计 ---")
    print(f"扫描 HTML 文件: {totalFiles}")
    print(f"需要修改的文件: {changedFiles}")

    if not apply and changedFiles > 0:
        print(f"\n使用 --apply 参数执行实际替换：")
        print(f"  python scripts/fix_header.py --apply")


if __name__ == "__main__":
    main()
