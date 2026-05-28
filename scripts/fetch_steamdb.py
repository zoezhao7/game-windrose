"""
SteamDB Patchnotes RSS 抓取模块

从 SteamDB 的公开 Patchnotes RSS 拉取 Windrose 补丁记录，标准化为 news.json schema。

用途：
  - Steam News API 偶尔会漏掉一些小补丁（dev 没发公告但客户端确实更新了）
  - SteamDB 监控 Steam depot 变更，理论上覆盖更全

NOTE: 本模块不修改任何文件，仅返回标准化条目列表。
"""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.error import URLError
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

logger = logging.getLogger(__name__)

STEAM_APP_ID = "3041230"
RSS_URL = f"https://steamdb.info/api/PatchnotesRSS/?appid={STEAM_APP_ID}"
USER_AGENT = "WindroseWikiBot/1.0 (+https://windrosewiki.games)"

MAX_ITEMS = 15


def fetch_steamdb_patches(count: int = MAX_ITEMS) -> list[dict]:
    logger.info("正在抓取 SteamDB RSS: %s", RSS_URL)
    try:
        req = Request(RSS_URL, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=30) as resp:
            xml_bytes = resp.read()
    except URLError as e:
        logger.error("SteamDB RSS 请求失败: %s", e)
        return []

    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        logger.error("SteamDB RSS XML 解析失败: %s", e)
        return []

    channel = root.find("channel")
    if channel is None:
        return []

    results: list[dict] = []
    for item in channel.findall("item")[:count]:
        parsed = _parse_item(item)
        if parsed:
            results.append(parsed)

    logger.info("从 SteamDB 获取到 %d 条补丁记录", len(results))
    return results


def _parse_item(item: ET.Element) -> dict | None:
    title = (item.findtext("title") or "").strip()
    link = (item.findtext("link") or "").strip()
    guid = (item.findtext("guid") or "").strip()
    description = (item.findtext("description") or "").strip()
    pub_date_raw = (item.findtext("pubDate") or "").strip()

    if not title or not link:
        return None

    try:
        dt = parsedate_to_datetime(pub_date_raw).astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None

    date_str = dt.strftime("%Y-%m-%d")
    build_id = _extract_build_id(guid, link, title)
    item_id = f"steamdb-{build_id}" if build_id else f"steamdb-{date_str}"
    slug_base = _slugify(title)
    if not slug_base:
        return None

    summary = description or f"SteamDB build record for {title}."
    content_html = (
        f'<p>{summary}</p>'
        f'<p>This patch was detected by SteamDB by monitoring the game\'s Steam depot. '
        f'For the official changelog, check the linked patch notes thread on Steam.</p>'
        f'<p><a href="{link}" rel="nofollow noopener" target="_blank">'
        f'View build details on SteamDB →</a></p>'
    )

    return {
        "id": item_id,
        "slug": f"news/{slug_base}",
        "name": title,
        "title": title,
        "status": "published",
        "confidence": "verified",
        "last_verified": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
        "category": "patch_notes",
        "author": "SteamDB",
        "date": date_str,
        "has_detail_page": True,
        "summary": summary,
        "content": content_html,
        "guide_impact": "",
        "tags": ["patch-notes", "steamdb"],
        "related_pages": [],
        "source": "steamdb",
        "source_feed": "SteamDB Patchnotes",
        "sources": [
            {
                "title": "SteamDB Patch Notes",
                "url": link,
                "type": "third_party",
            }
        ],
        "notes": f"Auto-fetched from SteamDB RSS (build: {build_id or 'n/a'})",
    }


def _extract_build_id(guid: str, link: str, title: str) -> str:
    m = re.search(r"build#?(\d+)", guid)
    if m:
        return m.group(1)
    m = re.search(r"/patchnotes/(\d+)", link)
    if m:
        return m.group(1)
    return ""


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")[:80]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    items = fetch_steamdb_patches()
    print(f"\nFetched {len(items)} items:")
    for it in items:
        print(f"  {it['date']}  {it['id']}  {it['title'][:70]}")
