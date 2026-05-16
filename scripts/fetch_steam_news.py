"""
Steam News 自动获取脚本 — Windrose Guides
用法: python scripts/fetch_steam_news.py

从 Steam Web API 获取 Windrose 最新新闻并更新 data/news.json
"""
import json
import os
import logging
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Windrose Steam App ID
STEAM_APP_ID = "3041230"
STEAM_NEWS_URL = f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid={STEAM_APP_ID}&count=10&maxlength=500&format=json"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS_JSON = os.path.join(ROOT, "data", "news.json")


def fetch_steam_news() -> list[dict]:
    """从 Steam API 获取最新新闻"""
    try:
        req = Request(STEAM_NEWS_URL, headers={"User-Agent": "WindroseGuides/1.0"})
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        items = data.get("appnews", {}).get("newsitems", [])
        results = []
        for item in items:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "date": datetime.fromtimestamp(item.get("date", 0)).strftime("%Y-%m-%d"),
                "author": item.get("author", ""),
                "feed_label": item.get("feedlabel", ""),
                "contents_snippet": item.get("contents", "")[:300],
                "source": "steam_api",
                "confidence": "official",
                "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })
        logger.info(f"Fetched {len(results)} news items from Steam API")
        return results
    except URLError as e:
        logger.error(f"Failed to fetch Steam news: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []


def update_news_json(new_items: list[dict]) -> None:
    """更新 data/news.json，合并新闻并去重"""
    existing = {"lastUpdated": "", "items": []}
    if os.path.exists(NEWS_JSON):
        with open(NEWS_JSON, "r", encoding="utf-8") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                pass

    existing_urls = {item.get("url") for item in existing.get("items", [])}
    added = 0
    for item in new_items:
        if item["url"] not in existing_urls:
            existing.setdefault("items", []).insert(0, item)
            added += 1

    existing["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")
    existing["total"] = len(existing.get("items", []))

    with open(NEWS_JSON, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    logger.info(f"Added {added} new items. Total: {existing['total']}")


if __name__ == "__main__":
    logger.info("Fetching Windrose news from Steam API...")
    items = fetch_steam_news()
    if items:
        update_news_json(items)
        logger.info("News update complete!")
    else:
        logger.warning("No news fetched. Check network or Steam API availability.")
