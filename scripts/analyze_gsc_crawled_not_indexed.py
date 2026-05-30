"""分析 GSC 'Crawled - currently not indexed' 列表里的 URL 模式。

输出:
- 按类型分桶,统计每桶 URL 数
- 列出最可疑的 slash/no-slash 重复对(确认上一 commit 修复的必要性)
- 列出每桶代表 URL,后续抓样
"""
from __future__ import annotations
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "reports" / "gsc_crawled_not_indexed_2026-05-30.txt"

LANGS = {"en", "de", "es", "fr", "pt", "zh"}


def load_urls() -> list[str]:
    urls = []
    for line in SRC.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        url = line.split("\t")[0]
        if url.startswith("http"):
            urls.append(url)
    return urls


def parse(url: str) -> tuple[str, str, str]:
    """返回 (lang, top_section, full_path)。lang='en' 表示根目录。"""
    path = url.replace("https://windrosewiki.games", "").strip("/")
    parts = path.split("/") if path else []
    if parts and parts[0] in LANGS - {"en"}:
        lang = parts[0]
        rest = parts[1:]
    else:
        lang = "en"
        rest = parts
    top = rest[0] if rest else "(root)"
    return lang, top, path


def bucket(url: str) -> str:
    """把 URL 归到一个粗粒度类型桶。"""
    p = url.replace("https://windrosewiki.games", "").strip("/")
    parts = p.split("/") if p else []
    if parts and parts[0] in LANGS - {"en"}:
        lang_prefix = True
        parts = parts[1:]
    else:
        lang_prefix = False

    if not parts:
        return "root(home)"
    top = parts[0]

    # database/items/{id} 是详情页
    if top == "database" and len(parts) >= 3 and parts[1] == "items":
        return "database/items (item detail)"
    if top == "database" and len(parts) == 2:
        return "database hub category (e.g. /database/bosses)"
    if top == "database" and len(parts) >= 3:
        return "database sub-section (e.g. /database/ships/hull-modules)"
    if top == "bosses" and len(parts) == 2:
        return "bosses/{slug} (boss page)"
    if top == "ships" and len(parts) == 2:
        return "ships/{slug} (ship page)"
    if top == "guides" and len(parts) == 2:
        return "guides/{slug} (guide article)"
    if top == "guides" and len(parts) == 1:
        return "guides/ (hub)"
    if top == "crafting" and len(parts) == 2:
        return "crafting/{slug} (station)"
    if top == "resources" and len(parts) == 2:
        return "resources/{slug} (resource)"
    if top == "weapons" and len(parts) == 2:
        return "weapons/{cat} (weapons subpage)"
    if top in {"builds", "tools", "download", "server-guide", "faq",
              "beginner-guide", "privacy"}:
        return f"{top}/ (section/standalone)"
    if top == "bosses" and len(parts) == 1:
        return "bosses/ (hub)"
    return f"other ({top})"


def main():
    urls = load_urls()
    print(f"# 总 URL 数: {len(urls)}\n")

    # 1) 按 bucket 分类
    by_bucket = Counter(bucket(u) for u in urls)
    print("## 按页面类型分布\n")
    for b, n in by_bucket.most_common():
        print(f"  {n:>4}  {b}")
    print()

    # 2) 按语言分类
    by_lang = Counter()
    for u in urls:
        lang, _, _ = parse(u)
        by_lang[lang] += 1
    print("## 按语言分布\n")
    for lang, n in by_lang.most_common():
        print(f"  {n:>4}  {lang}")
    print()

    # 3) Slash 重复对检测
    norm_to_variants = defaultdict(set)
    for u in urls:
        canonical = u.rstrip("/")
        norm_to_variants[canonical].add(u)
    dups = {k: v for k, v in norm_to_variants.items() if len(v) > 1}
    print(f"## Slash 重复对: 共 {len(dups)} 组(同一页被同时以带/不带尾斜杠抓取)\n")
    for k, vs in list(dups.items())[:10]:
        for v in sorted(vs):
            print(f"  {v}")
        print()

    # 4) 抽样代表 URL（每个 bucket 取前 3 个）
    print("## 每类代表 URL(用于后续抓样)\n")
    by_bucket_examples = defaultdict(list)
    for u in urls:
        by_bucket_examples[bucket(u)].append(u)
    for b in sorted(by_bucket_examples, key=lambda x: -by_bucket.get(x, 0)):
        print(f"### {b}  (n={by_bucket[b]})")
        for u in by_bucket_examples[b][:3]:
            print(f"  {u}")
        print()


if __name__ == "__main__":
    main()
