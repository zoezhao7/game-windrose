"""校验各语言翻译产出与英文源是否 1:1。

检查项：
1) HAND_PAGES 每个 slug 在 {lang}/{slug}/index.html 是否存在
2) 文件首行是否为 <!DOCTYPE html>
3) <html lang="..."> 是否匹配语言代码
4) <title>/<meta description>/h1 是否存在
5) 与 en 源文件大小比例不应过低（疑似空壳）

输出：每语言 PASS/FAIL 计数，列出问题文件。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from translate_with_deepseek import HAND_PAGES, LANG_HTML_ATTR  # noqa: E402

LANGS = ["zh", "es", "de", "pt", "fr"]


def page_path(lang: str, slug: str) -> Path:
    if lang == "en":
        return ROOT / slug / "index.html"
    return ROOT / lang / slug / "index.html"


def en_path(slug: str) -> Path:
    return ROOT / slug / "index.html"


def check_one(lang: str, slug: str) -> list[str]:
    issues: list[str] = []
    p = page_path(lang, slug)
    if not p.exists():
        issues.append("MISSING_FILE")
        return issues
    raw = p.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    head = text[:200].lstrip("﻿").lstrip()
    if not head.lower().startswith("<!doctype html"):
        issues.append("NO_DOCTYPE")
    expected_lang_attr = LANG_HTML_ATTR[lang]
    if f'lang="{expected_lang_attr}"' not in text and f"lang='{expected_lang_attr}'" not in text:
        issues.append(f"WRONG_HTML_LANG(want={expected_lang_attr})")
    if "<title>" not in text:
        issues.append("NO_TITLE")
    if 'name="description"' not in text:
        issues.append("NO_META_DESC")
    if "<h1" not in text:
        issues.append("NO_H1")

    # Body size sanity vs en source
    en_p = en_path(slug)
    if en_p.exists():
        en_size = en_p.stat().st_size
        ratio = len(raw) / max(en_size, 1)
        if ratio < 0.4:
            issues.append(f"TOO_SMALL(ratio={ratio:.2f})")
    return issues


def main() -> int:
    summary: dict[str, dict] = {}
    rc = 0
    for lang in LANGS:
        passed = 0
        failed: list[tuple[str, list[str]]] = []
        for slug in HAND_PAGES:
            issues = check_one(lang, slug)
            if issues:
                failed.append((slug, issues))
            else:
                passed += 1
        summary[lang] = {"pass": passed, "fail": len(failed), "issues": failed}
        if failed:
            rc = 1

    print("=" * 70)
    print(f"{'LANG':<6} {'PASS':>5} {'FAIL':>5}   TOTAL={len(HAND_PAGES)}")
    print("=" * 70)
    for lang in LANGS:
        s = summary[lang]
        print(f"{lang:<6} {s['pass']:>5} {s['fail']:>5}")
    print()
    for lang in LANGS:
        s = summary[lang]
        if not s["issues"]:
            continue
        print(f"--- {lang} issues ---")
        for slug, issues in s["issues"]:
            print(f"  {slug}: {', '.join(issues)}")
        print()
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
