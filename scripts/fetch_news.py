"""
Steam News API 抓取模块

从 Steam Web API 获取 Windrose 最新新闻公告。
返回标准化的新闻条目列表，供 update_news.py 合并到 data/news.json。

NOTE: 本模块不直接修改任何文件，只负责数据获取和格式化。
"""

import html
import logging
import re
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError
import json

logger = logging.getLogger(__name__)

# Windrose Steam App ID
STEAM_APP_ID = "3041230"

# NOTE: 最多抓取的新闻条数，避免首次运行时拉取过多历史数据
MAX_NEWS_COUNT = 20

# NOTE: Steam 摘要最大长度（0 = 全文，这里取前 500 字符作为 summary）
SUMMARY_MAX_LENGTH = 500


def fetch_steam_news(count: int = MAX_NEWS_COUNT) -> list[dict]:
    """
    从 Steam Web API 抓取 Windrose 官方新闻

    返回标准化的新闻条目列表，每条包含：
    - id, slug, title, name, date, summary, content
    - category, author, confidence, sources
    - has_detail_page, status, last_verified
    """
    url = (
        f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/"
        f"?appid={STEAM_APP_ID}&count={count}&maxlength=0&format=json"
    )

    logger.info("正在抓取 Steam News API: %s", url)

    try:
        req = Request(url, headers={"User-Agent": "WindroseGuidesBot/1.0"})
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (URLError, json.JSONDecodeError) as e:
        logger.error("Steam API 请求失败: %s", e)
        return []

    news_items = data.get("appnews", {}).get("newsitems", [])
    if not news_items:
        logger.info("Steam API 返回 0 条新闻")
        return []

    results = []
    for item in news_items:
        # NOTE: 只处理 Steam 官方公告，跳过社区帖子和外部聚合
        feed_type = item.get("feed_type", 0)
        feed_label = item.get("feedlabel", "")

        parsed = _parse_steam_item(item, feed_type, feed_label)
        if parsed:
            results.append(parsed)

    logger.info("从 Steam API 获取到 %d 条有效新闻", len(results))
    return results


def _parse_steam_item(item: dict, feed_type: int, feed_label: str) -> dict | None:
    """
    将单条 Steam 新闻解析为标准化格式

    NOTE: feed_type=1 通常是官方公告，feed_type=0 是社区/外部聚合
    """
    title = item.get("title", "").strip()
    if not title:
        return None

    # 生成 slug
    slug_base = _slugify(title)
    if not slug_base:
        return None

    # 解析日期
    timestamp = item.get("date", 0)
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    date_str = dt.strftime("%Y-%m-%d")

    # 处理正文内容
    raw_content = item.get("contents", "")
    content_html = _steam_bbcode_to_html(raw_content)
    summary = _extract_summary(raw_content)

    # 判断分类
    category = _determine_category(title, feed_label)

    # 判断作者
    author = item.get("author", "Kraken Express")
    if not author:
        author = "Kraken Express"

    steam_url = item.get("url", "")
    gid = item.get("gid", "")

    source = "steam_official" if feed_type == 1 else "steam_media"

    return {
        "id": f"steam-{gid}" if gid else f"steam-{slug_base}",
        "slug": f"news/{slug_base}",
        "name": title,
        "title": title,
        "status": "published",
        "confidence": "official" if source == "steam_official" else "media",
        "last_verified": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d"),
        "category": category,
        "author": author,
        "date": date_str,
        "has_detail_page": True,
        "summary": summary,
        "content": content_html,
        "guide_impact": "",
        "tags": _extract_tags(title, category),
        "related_pages": [],
        "source": source,
        "source_feed": feed_label,
        "sources": [
            {
                "title": "Steam Community Announcements" if source == "steam_official" else feed_label,
                "url": steam_url,
                "type": "official" if source == "steam_official" else "media",
            }
        ],
        "notes": f"Auto-fetched from Steam News API (feed: {feed_label})",
    }


def _slugify(text: str) -> str:
    """将标题转为 URL-safe slug"""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")[:80]


def _steam_bbcode_to_html(text: str) -> str:
    """
    将 Steam BBCode 格式转为 HTML

    NOTE: Steam 公告使用类 BBCode 标记，这里做基础转换。
    复杂格式可能需要后续完善。
    """
    if not text:
        return "<p>Content not available.</p>"

    # 基础 BBCode 转 HTML
    conversions = [
        (r"\[h1\](.*?)\[/h1\]", r"<h3>\1</h3>"),
        (r"\[h2\](.*?)\[/h2\]", r"<h3>\1</h3>"),
        (r"\[h3\](.*?)\[/h3\]", r"<h4>\1</h4>"),
        (r"\[b\](.*?)\[/b\]", r"<strong>\1</strong>"),
        (r"\[i\](.*?)\[/i\]", r"<em>\1</em>"),
        (r"\[u\](.*?)\[/u\]", r"<u>\1</u>"),
        (r"\[strike\](.*?)\[/strike\]", r"<del>\1</del>"),
        (r"\[url=(.*?)\](.*?)\[/url\]", r'<a href="\1" rel="nofollow">\2</a>'),
        (r"\[url\](.*?)\[/url\]", r'<a href="\1" rel="nofollow">\1</a>'),
        (r"\[img\](.*?)\[/img\]", r'<img src="\1" alt="Steam news image" loading="lazy">'),
        (r"\[list\]", "<ul>"),
        (r"\[/list\]", "</ul>"),
        (r"\[olist\]", "<ol>"),
        (r"\[/olist\]", "</ol>"),
        (r"\[\*\](.*?)(?=\[\*\]|\[/list\]|\[/olist\]|$)", r"<li>\1</li>"),
        (r"\[previewyoutube=(.*?)\]\[/previewyoutube\]", r'<p><a href="https://www.youtube.com/watch?v=\1" rel="nofollow">Watch on YouTube →</a></p>'),
    ]

    result = text
    for pattern, replacement in conversions:
        result = re.sub(pattern, replacement, result, flags=re.DOTALL | re.IGNORECASE)

    # 移除剩余未处理的 BBCode 标签
    result = re.sub(r"\[/?[a-zA-Z0-9_=;# ]+\]", "", result)

    # 将连续换行转为段落
    paragraphs = re.split(r"\n\s*\n", result.strip())
    html_parts = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        # 如果已经是 HTML 块级元素，不再包裹
        if re.match(r"^<(h[1-6]|ul|ol|li|div|p|img|table|blockquote)", p):
            html_parts.append(p)
        else:
            # 单行换行转 <br>
            p = p.replace("\n", "<br>")
            html_parts.append(f"<p>{p}</p>")

    return "\n".join(html_parts) if html_parts else "<p>Content not available.</p>"


def _extract_summary(text: str) -> str:
    """从原始内容提取纯文本摘要"""
    # 移除所有 BBCode 标签
    clean = re.sub(r"\[/?[a-zA-Z0-9_=;#\" ]+\]", "", text)
    # NOTE: Steam 内容可能混有 HTML 标签（img、a、br 等），也需要清除
    clean = re.sub(r"<[^>]+>", "", clean)
    # 移除多余空白
    clean = re.sub(r"\s+", " ", clean).strip()
    if len(clean) > SUMMARY_MAX_LENGTH:
        clean = clean[:SUMMARY_MAX_LENGTH].rsplit(" ", 1)[0] + "..."
    return clean


def _determine_category(title: str, feed_label: str) -> str:
    """
    根据标题和来源标签判断新闻分类

    NOTE: 优先匹配标题关键词，然后回退到 feed_label
    """
    title_lower = title.lower()
    if any(kw in title_lower for kw in ["patch", "hotfix", "update", "fix", "version"]):
        return "patch_notes"
    if any(kw in title_lower for kw in ["million", "milestone", "celebrate", "accolade"]):
        return "milestone"
    if any(kw in title_lower for kw in ["preview", "roadmap", "upcoming", "sneak peek"]):
        return "preview"
    if any(kw in title_lower for kw in ["community", "event", "contest"]):
        return "community"
    return "media"


def _extract_tags(title: str, category: str) -> list[str]:
    """从标题和分类中提取标签"""
    tags = [category.replace("_", "-")]
    title_lower = title.lower()
    if "patch" in title_lower or "hotfix" in title_lower:
        tags.append("patch-notes")
    if "server" in title_lower:
        tags.append("server")
    if "bug" in title_lower or "fix" in title_lower:
        tags.append("bug-fix")
    if "performance" in title_lower:
        tags.append("performance")
    return list(set(tags))
