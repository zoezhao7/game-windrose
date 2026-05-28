"""
新闻自动更新总入口

一次运行完成：
  1. 从 Steam API 抓取最新新闻
  2. 与现有 data/news.json 合并去重
  3. 重新生成 /news/ 列表页和详情页
  4. 更新首页的「最新动态」区块
  5. 更新 sitemap.xml 中的 lastmod

运行方式：
  python scripts/update_news.py

设计用于 GitHub Actions 每日自动执行。
无新内容时不会产生文件变更，从而避免空 commit。
"""

import json
import logging
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# NOTE: 确保 scripts/ 目录在 Python path 中，以便导入同级模块
sys.path.insert(0, str(Path(__file__).parent))

from fetch_news import fetch_steam_news  # noqa: E402
from fetch_steamdb import fetch_steamdb_patches  # noqa: E402
from fetch_steam_discussions import fetch_steam_discussions  # noqa: E402
from gen_news_pages import main as generate_news_pages  # noqa: E402
from indexnow_submit import submit as indexnow_submit  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
NEWS_FILE = DATA_DIR / "news.json"
INDEX_FILE = ROOT / "index.html"
SITEMAP_FILE = ROOT / "sitemap.xml"


def load_news() -> dict:
    """读取现有 news.json"""
    if NEWS_FILE.exists():
        with NEWS_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {"type": "news_collection", "generated_at": "", "items": []}


def save_news(data: dict) -> None:
    """写入 news.json"""
    data["generated_at"] = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
    with NEWS_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info("已保存 data/news.json (%d 条)", len(data.get("items", [])))


def merge_news(existing_items: list[dict], new_items: list[dict]) -> tuple[list[dict], int]:
    """
    合并新旧新闻条目，按 id 去重，按日期倒序排列

    返回 (合并后的列表, 新增条数)
    """
    seen_ids = {item["id"] for item in existing_items}
    added = 0

    for item in new_items:
        if item["id"] not in seen_ids:
            existing_items.append(item)
            seen_ids.add(item["id"])
            added += 1
            logger.info("新增: %s (%s)", item["title"], item["date"])

    # 按日期倒序
    existing_items.sort(key=lambda x: x.get("date", "0000-00-00"), reverse=True)

    return existing_items, added


def update_homepage_news(items: list[dict], max_items: int = 5) -> bool:
    """
    更新首页 index.html 中的「最新动态」区块

    在 <!-- NEWS_START --> 和 <!-- NEWS_END --> 标记之间注入最新新闻列表。
    如果标记不存在，则在 </main> 前插入整个区块。

    返回是否有变更
    """
    if not INDEX_FILE.exists():
        logger.warning("首页文件不存在: %s", INDEX_FILE)
        return False

    content = INDEX_FILE.read_text(encoding="utf-8")

    # 取最新 N 条新闻
    latest = items[:max_items]
    if not latest:
        return False

    # 生成新闻列表 HTML
    news_html_items = []
    for item in latest:
        title = item.get("title", item.get("name", ""))
        date = item.get("date", "")
        summary = item.get("summary", "")
        slug = item.get("slug", "")
        has_detail = item.get("has_detail_page", False)

        # NOTE: 清理 summary 中残留的 HTML/BBCode 标签，只保留纯文本
        clean_summary = re.sub(r"<[^>]+>", "", summary)
        clean_summary = re.sub(r"&lt;[^&]*&gt;", "", clean_summary)
        clean_summary = re.sub(r"\s+", " ", clean_summary).strip()

        # 格式化日期
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
            date_display = dt.strftime("%b %d, %Y")
        except ValueError:
            date_display = date

        if has_detail and slug.startswith("news/"):
            link = f'<a href="/{slug}">{title}</a>'
        else:
            link = title

        news_html_items.append(
            f'<li><time datetime="{date}">{date_display}</time> — {link}'
            f'<p class="news-summary">{clean_summary[:120]}{"..." if len(clean_summary) > 120 else ""}</p></li>'
        )

    # NOTE: 必须用 .container 包裹，否则在 </main> 前注入会跑到主容器外、左侧顶到视口边
    news_block = (
        '<!-- NEWS_START -->\n'
        '<div class="container">\n'
        '<section id="latest-news">\n'
        '  <h2>Latest News & Updates</h2>\n'
        '  <ul class="news-list">\n'
        '    ' + '\n    '.join(news_html_items) + '\n'
        '  </ul>\n'
        '  <p><a href="/news" class="btn btn-outline">View All News →</a></p>\n'
        '</section>\n'
        '</div>\n'
        '<!-- NEWS_END -->'
    )

    # 尝试替换已有标记
    pattern = re.compile(r"<!-- NEWS_START -->.*?<!-- NEWS_END -->", re.DOTALL)
    if pattern.search(content):
        new_content = pattern.sub(news_block, content)
    else:
        # NOTE: 标记不存在时，在 </main> 前插入新闻区块
        new_content = content.replace("</main>", f"\n{news_block}\n</main>")

    if new_content == content:
        return False

    INDEX_FILE.write_text(new_content, encoding="utf-8")
    logger.info("已更新首页新闻区块 (%d 条)", len(latest))
    return True


def update_sitemap_lastmod() -> None:
    """
    更新 sitemap.xml 中 /news 页面的 lastmod 日期

    NOTE: 只更新 /news 条目的日期，不重建整个 sitemap
    """
    if not SITEMAP_FILE.exists():
        return

    content = SITEMAP_FILE.read_text(encoding="utf-8")
    today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")

    # 匹配 /news 的 lastmod
    # NOTE: 中间夹了 hreflang 标签，所以用 [\s\S]*? 跨行匹配，但限定在同一个 <url> 块内
    pattern = re.compile(
        r"(<loc>https://windrosewiki\.games/news</loc>"
        r"(?:[\s\S]*?))<lastmod>(\d{4}-\d{2}-\d{2})</lastmod>"
    )
    new_content = pattern.sub(rf"\g<1><lastmod>{today}</lastmod>", content)

    if new_content != content:
        SITEMAP_FILE.write_text(new_content, encoding="utf-8")
        logger.info("已更新 sitemap.xml /news lastmod → %s", today)


def fetch_all_sources() -> list[dict]:
    """
    依次调用所有新闻 fetcher，把结果合并到一个列表里。

    单个 fetcher 失败不影响其他源，整体失败也不会中断后续合并/保存流程。
    """
    sources = [
        ("Steam News API", fetch_steam_news, {}),
        ("SteamDB Patchnotes RSS", fetch_steamdb_patches, {}),
        ("Steam Community Discussions", fetch_steam_discussions, {"max_items": 3}),
    ]

    all_items: list[dict] = []
    for name, fn, kwargs in sources:
        try:
            items = fn(**kwargs)
            logger.info("[%s] 返回 %d 条", name, len(items))
            all_items.extend(items)
        except Exception as e:
            logger.warning("[%s] 抓取失败（已跳过）: %r", name, e)

    return all_items


def main() -> None:
    logger.info("=== 开始新闻自动更新 ===")

    # 1. 抓取所有源的新闻
    new_items = fetch_all_sources()
    logger.info("所有数据源合计返回 %d 条", len(new_items))

    # 2. 加载现有数据
    news_data = load_news()
    existing_items = news_data.get("items", [])
    logger.info("现有 news.json 有 %d 条", len(existing_items))

    # 3. 合并去重
    merged, added_count = merge_news(existing_items, new_items)

    if added_count == 0:
        logger.info("没有新增新闻，跳过后续步骤")
        return

    # 4. 保存更新后的 news.json
    news_data["items"] = merged
    save_news(news_data)

    # 5. 重新生成 /news/ 页面
    logger.info("正在重新生成新闻页面...")
    generate_news_pages()

    # 6. 更新首页动态区块
    update_homepage_news(merged)

    # 7. 更新 sitemap
    update_sitemap_lastmod()

    # 8. IndexNow 推送（仅推送本次新增的新闻 URL；首页/news 列表页一并推一下）
    indexnow_urls = ["https://windrosewiki.games/", "https://windrosewiki.games/news"]
    new_ids = {item["id"] for item in new_items}
    for item in merged:
        if item.get("id") in new_ids and item.get("has_detail_page") and item.get("slug", "").startswith("news/"):
            indexnow_urls.append(f"https://windrosewiki.games/{item['slug']}")
    try:
        indexnow_submit(indexnow_urls)
    except Exception as e:  # NOTE: IndexNow 失败不应阻塞新闻发布
        logger.warning("IndexNow 推送失败（已忽略）: %r", e)

    logger.info("=== 新闻更新完成：新增 %d 条 ===", added_count)


if __name__ == "__main__":
    main()
