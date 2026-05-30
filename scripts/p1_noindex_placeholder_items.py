"""一次性脚本: 给所有 description 为 "does not ship a long description in the current mirror"
占位符的 42 个 database/items/{id}/index.html 加 noindex,从 sitemap.xml 移除这些 URL。

策略:
- 这些页面是 thin content + 带"未完成"占位符提示词,Google 会判低质且影响整站质量评估
- noindex,follow 让 Google 不收录该页但仍能爬子链(保住内链权重传递)
- 从 sitemap 移除是为了与 noindex 表态一致(矛盾信号会损害爬虫信任)

使用:
    python scripts/p1_noindex_placeholder_items.py            # dry-run
    python scripts/p1_noindex_placeholder_items.py --apply    # 真正写
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = "does not ship a long description in the current mirror"
ITEMS_DIR = ROOT / "database" / "items"
SITEMAP = ROOT / "sitemap.xml"


def find_placeholder_ids() -> list[str]:
    """从 scraped_items_v2.json 取出所有 description 含 placeholder 的 item id。"""
    src = ROOT / "data" / "scraped_items_v2.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    ids = []
    for it in data.get("items", []):
        if PLACEHOLDER in (it.get("description") or ""):
            ids.append(it["id"])
    return ids


def inject_noindex(html: str) -> tuple[str, bool]:
    """在 <head> 里插入 <meta name="robots" content="noindex, follow">.
    如果已经有 robots meta,替换为 noindex,follow."""
    # 已存在 robots meta?
    if re.search(r'<meta\s+name=["\']robots["\']', html, re.IGNORECASE):
        new = re.sub(
            r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*["\']\s*/?>',
            '<meta name="robots" content="noindex, follow">',
            html,
            count=1,
            flags=re.IGNORECASE,
        )
        return new, new != html
    # 没有则插到 <link rel="canonical"> 前(detail 页有 canonical),退而求其次插到 </head> 前
    inj = '<meta name="robots" content="noindex, follow">\n'
    m = re.search(r'(<link\s+rel=["\']canonical["\'])', html, re.IGNORECASE)
    if m:
        new = html[:m.start()] + inj + html[m.start():]
        return new, True
    new = html.replace("</head>", inj + "</head>", 1)
    return new, new != html


def patch_html_files(ids: list[str], apply: bool) -> tuple[int, int]:
    touched = 0
    missing = 0
    for item_id in ids:
        path = ITEMS_DIR / item_id / "index.html"
        if not path.exists():
            missing += 1
            continue
        text = path.read_text(encoding="utf-8")
        new, changed = inject_noindex(text)
        if not changed:
            continue
        touched += 1
        if apply:
            path.write_text(new, encoding="utf-8")
    return touched, missing


def remove_from_sitemap(ids: set[str], apply: bool) -> int:
    text = SITEMAP.read_text(encoding="utf-8")
    # 匹配整个 <url>...</url> 块,只要 loc 在 ids 中就删
    pattern = re.compile(
        r'\s*<url>\s*<loc>https://windrosewiki\.games/database/items/([^/<]+)/?</loc>.*?</url>',
        re.DOTALL,
    )
    removed = 0
    def repl(m: re.Match) -> str:
        nonlocal removed
        if m.group(1) in ids:
            removed += 1
            return ""
        return m.group(0)
    new = pattern.sub(repl, text)
    if apply and removed:
        SITEMAP.write_text(new, encoding="utf-8")
    return removed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    ids = find_placeholder_ids()
    print(f"placeholder item count: {len(ids)}")
    if not ids:
        print("nothing to do")
        return 0

    touched, missing = patch_html_files(ids, args.apply)
    print(f"HTML files {'patched' if args.apply else 'would patch'}: {touched}, "
          f"missing on disk: {missing}")

    removed = remove_from_sitemap(set(ids), args.apply)
    print(f"sitemap entries {'removed' if args.apply else 'would remove'}: {removed}")

    mode = "applied" if args.apply else "dry-run"
    print(f"\n[{mode}] done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
