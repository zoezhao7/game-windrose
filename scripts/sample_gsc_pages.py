"""对 GSC 'Crawled - not indexed' 列表里每类抽 1-3 个样,实际抓取并量化:
- 正文纯文本长度
- 是否多语言页但正文还是英文(对非英语 lang 页面)
- canonical / robots / hreflang 是否正常
"""
from __future__ import annotations
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

ROOT = Path(__file__).resolve().parents[1]

SAMPLES = {
    "database/items": [
        "https://windrosewiki.games/database/items/did-resource-vinegar-t04/",
        "https://windrosewiki.games/database/items/eid-armor-pikeman-base-head/",
        "https://windrosewiki.games/database/items/eid-necklace-strength-minor/",
        "https://windrosewiki.games/database/items/did-misc-recipe-paper-unlock-cannon-24-cold-barrels-base/",
        "https://windrosewiki.games/database/items/eid-cannon-12-blank-base/",
        "https://windrosewiki.games/database/items/cutlass/",  # 旧风格 id
        "https://windrosewiki.games/database/items/clay/",
    ],
    "bosses/{slug}": [
        "https://windrosewiki.games/bosses/thomas-richards/",
        "https://windrosewiki.games/es/bosses/high-priestess/",
        "https://windrosewiki.games/zh/bosses/charons-obols/",
    ],
    "crafting/{slug}": [
        "https://windrosewiki.games/crafting/cooking/",
        "https://windrosewiki.games/zh/crafting/cooking/",
        "https://windrosewiki.games/de/crafting/alchemy/",
    ],
    "guides/{slug}": [
        "https://windrosewiki.games/guides/coop-multiplayer/",
        "https://windrosewiki.games/guides/secrets/",
        "https://windrosewiki.games/zh/guides/boss-progression/",
    ],
    "ships/{slug}": [
        "https://windrosewiki.games/ships/brigantine/",
        "https://windrosewiki.games/de/ships/sloop/",
        "https://windrosewiki.games/zh/ships/frigate/",
    ],
    "resources/{slug}": [
        "https://windrosewiki.games/es/resources/clay/",
        "https://windrosewiki.games/fr/resources/iron/",
    ],
    "weapons/{cat}": [
        "https://windrosewiki.games/es/weapons/ranged/",
        "https://windrosewiki.games/fr/weapons/armor/",
    ],
    "section hub": [
        "https://windrosewiki.games/builds/",
        "https://windrosewiki.games/guides/",
        "https://windrosewiki.games/pt/tools/",
        "https://windrosewiki.games/zh/bosses/",
    ],
    "database hub category": [
        "https://windrosewiki.games/database/bosses/",
        "https://windrosewiki.games/de/database/bosses/",
    ],
}


class TextExtractor(HTMLParser):
    SKIP = {"script", "style", "noscript", "header", "nav", "footer"}

    def __init__(self):
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0
        self.in_main = False
        self.main_depth = 0
        self.meta = {
            "title": "",
            "canonical": "",
            "robots": "",
            "html_lang": "",
            "hreflang_self": "",
            "h1": "",
        }
        self._in_title = False
        self._in_h1 = False

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag == "html" and "lang" in attrs_d:
            self.meta["html_lang"] = attrs_d["lang"]
        if tag == "title":
            self._in_title = True
        if tag == "h1":
            self._in_h1 = True
        if tag == "link" and attrs_d.get("rel") == "canonical":
            self.meta["canonical"] = attrs_d.get("href", "")
        if tag == "meta" and attrs_d.get("name") == "robots":
            self.meta["robots"] = attrs_d.get("content", "")
        if tag in self.SKIP:
            self.skip_depth += 1
        # 内容区:<main> 或 database 详情用的 <div class="detail-wrap">
        cls = attrs_d.get("class", "")
        is_content_root = (
            tag == "main"
            or (tag == "div" and "detail-wrap" in cls)
            or (tag == "article")
        )
        if is_content_root and not self.in_main:
            self.in_main = True
            self.main_depth = 1
        elif self.in_main and tag != "br":
            self.main_depth += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip_depth > 0:
            self.skip_depth -= 1
        if tag == "title":
            self._in_title = False
        if tag == "h1":
            self._in_h1 = False
        if self.in_main:
            self.main_depth -= 1
            if self.main_depth <= 0:
                self.in_main = False

    def handle_data(self, data):
        if self._in_title:
            self.meta["title"] += data
        if self._in_h1:
            self.meta["h1"] += data
        if self.skip_depth == 0 and self.in_main:
            text = data.strip()
            if text:
                self.parts.append(text)

    def text(self) -> str:
        return " ".join(self.parts)


def fetch(url: str) -> tuple[int, str]:
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    })
    try:
        with urlopen(req, timeout=20) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except URLError as e:
        return 0, f"ERR: {e}"


# 简单 ASCII 比例判定:若一个本应是 zh/de/es/fr/pt 的页面正文 ASCII 比 > 90%,可能正文未翻译
def ascii_ratio(text: str) -> float:
    if not text:
        return 0.0
    return sum(1 for c in text if ord(c) < 128) / len(text)


# 计算 trigram 重复率 - 高表示模板化严重
def trigram_diversity(text: str) -> float:
    tokens = re.findall(r"\w+", text.lower())
    if len(tokens) < 3:
        return 1.0
    trigrams = list(zip(tokens, tokens[1:], tokens[2:]))
    return len(set(trigrams)) / len(trigrams)


def analyze(url: str):
    status, html = fetch(url)
    if status != 200:
        return {"url": url, "status": status, "err": html[:200]}
    p = TextExtractor()
    p.feed(html)
    text = p.text()
    words = re.findall(r"\w+", text)
    return {
        "url": url,
        "status": status,
        "html_lang": p.meta["html_lang"],
        "title_len": len(p.meta["title"].strip()),
        "h1": p.meta["h1"].strip()[:60],
        "canonical": p.meta["canonical"],
        "robots": p.meta["robots"],
        "main_chars": len(text),
        "main_words": len(words),
        "uniq_words": len(set(w.lower() for w in words)),
        "ascii_ratio": round(ascii_ratio(text), 3),
        "trigram_div": round(trigram_diversity(text), 3),
        "preview": text[:200].replace("\n", " "),
    }


def main():
    print(f"{'BUCKET':<28} {'URL':<70} {'LANG':<6} {'CHRS':>5} {'WRDS':>5} {'UNQ':>4} {'ASCII':>6} {'TRGM':>5}")
    for bucket, urls in SAMPLES.items():
        for url in urls:
            r = analyze(url)
            if r.get("err"):
                print(f"{bucket:<28} {url:<70} ERR {r['err'][:60]}")
                continue
            short = url.replace("https://windrosewiki.games", "")
            print(f"{bucket:<28} {short:<70} {r['html_lang']:<6} {r['main_chars']:>5} {r['main_words']:>5} {r['uniq_words']:>4} {r['ascii_ratio']:>6} {r['trigram_div']:>5}")


if __name__ == "__main__":
    main()
