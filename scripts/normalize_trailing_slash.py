"""一次性批量修复：把所有指向本站的目录型 URL 加上尾斜杠。

背景：Cloudflare Pages 把 /foo 强制 308 → /foo/，但全站 HTML 的 canonical、
og:url、hreflang、JSON-LD 中的 url/item/@id/mainEntityOfPage、以及 sitemap.xml
的 <loc>、xhtml:link href 之前用的都是无尾斜杠形式，与服务器实际响应不一致，
导致 Google Search Console 出现 1400+ "Discovered – currently not indexed"。

此脚本扫描全站 .html 与 sitemap.xml，统一改写为带尾斜杠形式。

规则：
- 只动 https://windrosewiki.games 开头的 URL。
- 跳过根 URL "https://windrosewiki.games/"（已带斜杠）。
- 跳过路径最后一段含 "." 的 URL（认为是文件，如 /imgs/og.webp）。
- 跳过本身已带尾斜杠的 URL。
- 含查询串 "?"：跳过（站内目前无此类 URL，避免误改）。
- 含 fragment "#"：在路径部分做规范化，保留 fragment（用于 JSON-LD @id）。

使用：
    python scripts/normalize_trailing_slash.py            # 默认 dry-run，仅打印计数
    python scripts/normalize_trailing_slash.py --apply    # 真正写回文件
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://windrosewiki.games"

# 跳过的目录：脚本/构建/Git/docs/skills 等
SKIP_DIRS = {".git", "scripts", "docs", "skills", "node_modules", "__pycache__",
             ".claude", "templates"}


def needs_slash(url: str) -> bool:
    """判断一个 https://windrosewiki.games/... URL 是否需要补尾斜杠。"""
    if not url.startswith(SITE):
        return False
    rest = url[len(SITE):]
    if not rest or rest == "/":
        return False  # 根 URL 已带斜杠
    if "?" in rest:
        return False  # 站内目前无带 query 的 canonical/sitemap URL，避免误改
    # 拆 fragment（JSON-LD @id 常见，如 /news#webpage）
    path, _, _ = rest.partition("#")
    if not path or path.endswith("/"):
        return False
    last = path.rsplit("/", 1)[-1]
    if "." in last:
        return False  # 文件 URL（如 /sitemap.xml, /imgs/og.webp）
    return True


def add_slash(url: str) -> str:
    """在路径部分末尾加 /，保留 fragment。"""
    if not needs_slash(url):
        return url
    base, sep, frag = url.partition("#")
    return base + "/" + (sep + frag if sep else "")


# 正则：抓所有带 https://windrosewiki.games 开头的 URL，被引号、>、< 等包围
# 注意：URL 路径里可以含撇号（如 .../crow's-nest/），所以 ' 不能作分隔符
URL_RE = re.compile(r'https://windrosewiki\.games[^\s"<>]*?(?=[\s"<>]|$)')


def rewrite_text(text: str) -> tuple[str, int]:
    """对整段文本里所有匹配 URL 做加斜杠改写。返回 (新文本, 改写次数)。"""
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        url = m.group(0)
        # 去掉可能尾随的 XML/HTML 控制字符（>、/>、" 等已被 URL_RE 排除，但保险起见）
        # 例如 sitemap 里 "<loc>https://...</loc>" — 正则不会吃进 "<"，没问题
        new = add_slash(url)
        if new != url:
            count += 1
        return new

    new_text = URL_RE.sub(repl, text)
    return new_text, count


def should_visit(path: Path) -> bool:
    parts = set(path.parts)
    if parts & SKIP_DIRS:
        return False
    return True


def iter_targets():
    yield ROOT / "sitemap.xml"
    for p in ROOT.rglob("*.html"):
        if should_visit(p.relative_to(ROOT)):
            yield p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="实际写回文件；不加则 dry-run")
    args = ap.parse_args()

    total_files = 0
    total_changes = 0
    changed_files = 0
    for path in iter_targets():
        if not path.exists():
            continue
        total_files += 1
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"SKIP (encoding): {path}", file=sys.stderr)
            continue
        new_text, n = rewrite_text(text)
        if n == 0:
            continue
        changed_files += 1
        total_changes += n
        if args.apply:
            path.write_text(new_text, encoding="utf-8")
            print(f"[fix +{n}] {path.relative_to(ROOT)}")
        else:
            print(f"[would-fix +{n}] {path.relative_to(ROOT)}")

    mode = "applied" if args.apply else "dry-run"
    print(f"\n{mode}: {changed_files}/{total_files} files, {total_changes} URLs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
