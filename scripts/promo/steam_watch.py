"""
Steam 社区讨论区抓取器 — Windrose

抓取 Steam Community Hub 的 General Discussions 列表，输出待回答候选清单。

用法：
  python scripts/promo/steam_watch.py
  python scripts/promo/steam_watch.py --pages 2 --hours 48

实现说明：
  - Steam 论坛列表页是 SSR 的，可直接用 HTTP + 正则解析，无需 Playwright
  - 每帖详情懒加载，只在列表无法判断"是否已有答复"时再回源
  - 礼貌限速：每页间隔 2 秒
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import time
from datetime import datetime

from _common import (
    UA,
    get_logger,
    get_secret,
    http_get_text,
    md_table,
    report_path,
    write_report,
)

logger = get_logger("steam_watch")

DEFAULT_APP_ID = "3041230"  # Windrose

# 列表页每条帖子的 HTML 结构（取关键 anchor + 元信息）
ROW_RE = re.compile(
    r'<div class="forum_topic[^"]*"[^>]*>.*?'
    r'<a class="forum_topic_overlay"\s+href="([^"]+)"></a>.*?'
    r'<div class="forum_topic_name[^"]*">([^<]+)</div>.*?'
    r'<div class="forum_topic_op">([^<]+)</div>.*?'
    r'<div class="forum_topic_reply_count">(\d+)</div>'
    r'(?:.*?<div class="forum_topic_lastpost">([^<]*)</div>)?',
    re.DOTALL,
)

QUESTION_RE = re.compile(
    r"\?|\bhow\b|\bwhere\b|\bwhy\b|\bwhat\b|\bcan\s+(?:i|you)\b|"
    r"\bstuck\b|\bhelp\b|\bbug\b|\bcrash\b|\banyone\b",
    re.IGNORECASE,
)


def fetch_list(app_id: str, page: int = 1) -> str:
    # General Discussions（forum_id=0 等价于全部综合，使用默认入口即可）
    if page == 1:
        url = f"https://steamcommunity.com/app/{app_id}/discussions/"
    else:
        url = f"https://steamcommunity.com/app/{app_id}/discussions/?fp={page}"
    logger.info("GET %s", url)
    return http_get_text(url, headers={"User-Agent": UA, "Accept-Language": "en"})


def parse_list(text: str) -> list[dict]:
    out: list[dict] = []
    for m in ROW_RE.finditer(text):
        url = html.unescape(m.group(1)).strip()
        title = html.unescape(m.group(2)).strip()
        op = html.unescape(m.group(3)).strip()
        replies = int(m.group(4))
        last = (m.group(5) or "").strip()
        out.append(
            {
                "url": url,
                "title": title,
                "op": op,
                "replies": replies,
                "last": last,
                "is_question": bool(QUESTION_RE.search(title)),
            }
        )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--app-id",
        default=get_secret("STEAM_APP_ID", DEFAULT_APP_ID),
        help="Steam App ID（默认 Windrose 的 3041230）",
    )
    ap.add_argument("--pages", type=int, default=1, help="抓取列表页数，默认 1")
    ap.add_argument(
        "--max-replies",
        type=int,
        default=3,
        help="只关注回复数 ≤ 此值的帖（更可能是未解决的问题），默认 3",
    )
    args = ap.parse_args()

    posts: list[dict] = []
    seen: set[str] = set()
    for p in range(1, args.pages + 1):
        try:
            text = fetch_list(args.app_id, p)
        except Exception as e:
            logger.warning("拉第 %d 页失败: %r", p, e)
            continue
        rows = parse_list(text)
        logger.info("第 %d 页解析到 %d 条", p, len(rows))
        for r in rows:
            if r["url"] in seen:
                continue
            seen.add(r["url"])
            posts.append(r)
        time.sleep(2.0)

    if not posts:
        logger.warning("没有抓到任何帖子，可能 HTML 结构变化或被反爬")

    questions = [p for p in posts if p["is_question"] and p["replies"] <= args.max_replies]
    answered = [p for p in posts if p["is_question"] and p["replies"] > args.max_replies]
    others = [p for p in posts if not p["is_question"]]

    today = datetime.now().strftime("%Y-%m-%d")
    lines: list[str] = []
    lines.append(f"# Steam 社区监控日报 — {today}")
    lines.append("")
    lines.append(f"App ID：{args.app_id}（Windrose）")
    lines.append(
        f"抓取页数：{args.pages}，命中 {len(posts)} 帖（疑似问答 "
        f"{len(questions) + len(answered)}）"
    )
    lines.append("")

    if questions:
        lines.append("## 🎯 优先回答（疑似问题，回复 ≤ {} 条）".format(args.max_replies))
        lines.append("")
        lines.append(
            md_table(
                ["title", "OP", "replies", "last", "link"],
                [
                    [
                        p["title"][:90],
                        p["op"],
                        str(p["replies"]),
                        p["last"],
                        f"[open]({p['url']})",
                    ]
                    for p in questions[:30]
                ],
            )
        )
        lines.append("")
    else:
        lines.append("## 🎯 优先回答")
        lines.append("")
        lines.append("_本批次未发现低回复问答帖。_")
        lines.append("")

    if answered:
        lines.append("## 已有讨论的问答帖（可补充更优答案）")
        lines.append("")
        lines.append(
            md_table(
                ["title", "OP", "replies", "last", "link"],
                [
                    [
                        p["title"][:90],
                        p["op"],
                        str(p["replies"]),
                        p["last"],
                        f"[open]({p['url']})",
                    ]
                    for p in answered[:20]
                ],
            )
        )
        lines.append("")

    if others:
        lines.append("## 其他讨论")
        lines.append("")
        lines.append(
            md_table(
                ["title", "OP", "replies", "last", "link"],
                [
                    [
                        p["title"][:90],
                        p["op"],
                        str(p["replies"]),
                        p["last"],
                        f"[open]({p['url']})",
                    ]
                    for p in others[:20]
                ],
            )
        )
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("行动建议：")
    lines.append("- 优先回答 replies ≤ 3 的新问题，成为首答可见度最高")
    lines.append("- 单帖最多 1 个 windrosewiki.games 链接，且放在完整答案之后")
    lines.append("- Guides 板块每周一发布新攻略，节奏稳定有助于权重")

    out = report_path("daily", "steam")
    write_report(out, "\n".join(lines))
    logger.info("已写入 %s", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
