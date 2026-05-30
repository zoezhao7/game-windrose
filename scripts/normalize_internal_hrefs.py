"""一次性脚本:给所有 HTML 文件里的内链(<a href="/foo">)加尾斜杠,
跟 normalize_trailing_slash.py 同质,只是目标是相对路径 href,而不是绝对 URL。

源头(lang_url / templates.NAV_KEYS)其实已经修好了,生成的新页都对。
这个 patcher 修的是历史遗留 HTML 文件 —— 主要是:
- 172 个 /database/items/{old-id}/ 孤儿页(已不在数据源,P2 没覆写)
- 多语言页(P2 只跑 gen_detail_pages,没跑其它 generator)
- news 详情页

规则(跟 needs_slash_url 同语义):
- 只动 href="/foo[/bar]..." 这种以 / 开头的内部绝对路径
- 跳过 href="/" (已是根)
- 跳过 href="/foo/" (已带斜杠)
- 跳过 href="/foo.png" (路径最后一段含 ".",视为文件)
- 跳过 href="/foo?bar" / href="/foo#bar" (有查询/锚)
- 跳过 href="https://..." / href="//..." / href="mailto:..." / href="javascript:..." 等非内部链
- 跳过 相对路径如 href="../foo" 或 href="foo"

使用:
    python scripts/normalize_internal_hrefs.py          # dry-run
    python scripts/normalize_internal_hrefs.py --apply  # 实际写
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "scripts", "docs", "skills", "node_modules", "__pycache__",
             ".claude", "templates"}

# 匹配 href="/something"(双引号或单引号,路径以单个 / 开头但不是 //)
# 注意:用非贪婪 + lookahead 确保不吃进引号本身,允许撇号字符如 crow's-nest
HREF_RE = re.compile(r'''href=(["'])(/[^"'/][^"']*)\1''')


def needs_slash(path: str) -> bool:
    """判断一个 href 值是否需要在末尾补 /。"""
    if not path or path == "/" or path.endswith("/"):
        return False
    if path.startswith("//"):  # protocol-relative URL,不动
        return False
    if "?" in path or "#" in path:
        return False
    # 看路径最后一段是否含 . —— 含 . 视为文件
    last = path.rsplit("/", 1)[-1]
    if "." in last:
        return False
    return True


def rewrite(text: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        quote = m.group(1)
        path = m.group(2)
        if needs_slash(path):
            count += 1
            return f'href={quote}{path}/{quote}'
        return m.group(0)

    new_text = HREF_RE.sub(repl, text)
    return new_text, count


def should_visit(path: Path) -> bool:
    parts = set(path.parts)
    return not (parts & SKIP_DIRS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    total = 0
    changed = 0
    fixes = 0
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT)
        if not should_visit(rel):
            continue
        total += 1
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"SKIP (encoding): {rel}", file=sys.stderr)
            continue
        new_text, n = rewrite(text)
        if n == 0:
            continue
        changed += 1
        fixes += n
        if args.apply:
            p.write_text(new_text, encoding="utf-8")
        if changed <= 8 or changed % 100 == 0:
            print(f"[{'fix' if args.apply else 'would-fix'} +{n}] {rel}")

    mode = "applied" if args.apply else "dry-run"
    print(f"\n{mode}: {changed}/{total} files, {fixes} href fixes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
