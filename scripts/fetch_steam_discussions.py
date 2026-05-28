"""
Steam Community Discussions 抓取模块（用于新闻聚合）

抓取 Windrose 论坛的 General Discussions 列表，筛选高价值帖（pinned / 高回复数 /
开发者发帖），转换为 news.json schema 的"社区讨论"条目，跳转到 Steam 原贴。

重要约束（出于 SEO 与 Spam 政策考虑）：
  - 不爬取帖子正文，只用列表页元信息生成简短摘要
  - 详情页明确标注「Community Discussion」，并 nofollow 指向原帖
  - 单次抓取限 max_items 条，避免社区噪音淹没正式新闻

NOTE: 本模块不修改任何文件，仅返回标准化条目列表。
"""

from __future__ import annotations

import html
import logging
import re
from datetime import datetime, timezone
from urllib.error import URLError
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)

STEAM_APP_ID = "3041230"
LIST_URL = f"https://steamcommunity.com/app/{STEAM_APP_ID}/discussions/"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

DEFAULT_MAX_ITEMS = 3
MIN_REPLIES_NORMAL = 15

# NOTE: 必须用非贪婪 + DOTALL，因为每个 forum_topic 块跨多行
ROW_RE = re.compile(
    r'<div[^>]*class="forum_topic[^"]*?"[^>]*data-gidforumtopic="(?P<gid>\d+)"'
    r'(?P<head>[^>]*?)>'
    r'(?P<body>.*?)'
    r'<div\s+style="clear:\s*both;"></div>\s*</div>',
    re.DOTALL,
)
TOPIC_NAME_RE = re.compile(
    r'<div class="forum_topic_name[^"]*?">\s*'
    r'(?:<span class="forum_topic_label[^"]*">([^<]+)</span>)?'
    r'\s*([^<]+?)\s*</div>',
    re.DOTALL,
)
OP_RE = re.compile(r'<div class="forum_topic_op">\s*(.+?)\s*</div>', re.DOTALL)
REPLY_RE = re.compile(r'<div class="forum_topic_reply_count">.*?(\d+)\s*</div>', re.DOTALL)
URL_RE = re.compile(r'<a class="forum_topic_overlay"\s+href="([^"]+)"\s*>\s*</a>', re.DOTALL)
LASTPOST_RE = re.compile(r'data-timestamp="(\d+)"')


def fetch_steam_discussions(max_items: int = DEFAULT_MAX_ITEMS) -> list[dict]:
    logger.info("正在抓取 Steam Discussions: %s", LIST_URL)
    try:
        req = Request(
            LIST_URL,
            headers={"User-Agent": USER_AGENT, "Accept-Language": "en"},
        )
        with urlopen(req, timeout=30) as resp:
            text = resp.read().decode("utf-8", "replace")
    except URLError as e:
        logger.error("Steam Discussions 请求失败: %s", e)
        return []

    rows = list(_parse_rows(text))
    logger.info("解析到 %d 个讨论帖", len(rows))

    qualified = [r for r in rows if _is_qualified(r)]
    logger.info("通过质量筛选: %d 条", len(qualified))

    qualified.sort(key=lambda r: (not r["pinned"], -r["replies"]))

    results = []
    for row in qualified[:max_items]:
        parsed = _to_news_item(row)
        if parsed:
            results.append(parsed)

    logger.info("Steam Discussions 输出 %d 条新闻条目", len(results))
    return results


def _parse_rows(text: str):
    for m in ROW_RE.finditer(text):
        gid = m.group("gid")
        head = m.group("head") or ""
        body = m.group("body") or ""

        url_m = URL_RE.search(body)
        name_m = TOPIC_NAME_RE.search(body)
        op_m = OP_RE.search(body)
        rep_m = REPLY_RE.search(body)
        ts_m = LASTPOST_RE.search(body)

        if not (url_m and name_m and op_m):
            continue

        label = (name_m.group(1) or "").strip()
        title = html.unescape(name_m.group(2)).strip()
        op = html.unescape(op_m.group(1)).strip()
        replies = int(rep_m.group(1)) if rep_m else 0
        last_ts = int(ts_m.group(1)) if ts_m else 0

        # NOTE: head 里携带的 class 决定置顶 / 公告
        pinned = "sticky" in head or "PINNED" in label.upper()
        announcement = "announcement" in head.lower() or "ANNOUNCEMENT" in label.upper()

        yield {
            "gid": gid,
            "url": url_m.group(1).strip(),
            "title": title,
            "op": op,
            "replies": replies,
            "last_ts": last_ts,
            "label": label,
            "pinned": pinned,
            "announcement": announcement,
        }


def _is_qualified(row: dict) -> bool:
    """质量过滤：只放行公告/置顶/高回复帖。"""
    if row["announcement"] or row["pinned"]:
        return True
    if row["replies"] >= MIN_REPLIES_NORMAL:
        return True
    return False


def _to_news_item(row: dict) -> dict | None:
    title = row["title"]
    if not title:
        return None

    slug_base = _slugify(title)
    if not slug_base:
        return None

    if row["last_ts"]:
        dt = datetime.fromtimestamp(row["last_ts"], tz=timezone.utc)
    else:
        dt = datetime.now(tz=timezone.utc)
    date_str = dt.strftime("%Y-%m-%d")

    badge = "Pinned thread" if row["pinned"] else (
        "Official announcement" if row["announcement"] else "Active discussion"
    )

    summary = (
        f'{badge} on the Windrose Steam forum by {row["op"]}, '
        f'with {row["replies"]} replies. Read the full discussion on Steam.'
    )

    content_html = (
        f'<p><strong>{badge}</strong> on the official Windrose '
        f'<a href="{LIST_URL}" rel="nofollow noopener" target="_blank">Steam Community Hub</a>.</p>'
        f'<ul>'
        f'<li><strong>Original poster:</strong> {html.escape(row["op"])}</li>'
        f'<li><strong>Replies so far:</strong> {row["replies"]}</li>'
        f'</ul>'
        f'<p>This index entry links to the discussion as a community signal '
        f'for what Windrose players are talking about right now. We do not '
        f'reproduce the thread content here — please read it on Steam:</p>'
        f'<p><a href="{row["url"]}" rel="nofollow noopener" target="_blank">'
        f'Open the thread on Steam Community →</a></p>'
    )

    return {
        "id": f"steamdisc-{row['gid']}",
        "slug": f"news/{slug_base}",
        "name": title,
        "title": title,
        "status": "published",
        "confidence": "community",
        "last_verified": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
        "category": "community",
        "author": row["op"],
        "date": date_str,
        "has_detail_page": True,
        "summary": summary,
        "content": content_html,
        "guide_impact": "",
        "tags": ["community", "steam-discussions"],
        "related_pages": [],
        "source": "steam_discussions",
        "source_feed": "Steam Community Hub",
        "sources": [
            {
                "title": "Windrose Steam Community Discussions",
                "url": row["url"],
                "type": "community",
            }
        ],
        "notes": (
            f"Auto-fetched from Steam Discussions list page "
            f"(replies={row['replies']}, pinned={row['pinned']})"
        ),
    }


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")[:80]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    items = fetch_steam_discussions(max_items=10)
    print(f"\nFetched {len(items)} items:")
    for it in items:
        print(f"  {it['date']}  {it['id']}  [{it['source']}]  {it['title'][:60]}")
