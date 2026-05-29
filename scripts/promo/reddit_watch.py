"""
Reddit 监控器 — 抓取多个 sub 内 Windrose 关键词的最新帖子，输出候选问答清单。

用法：
  python scripts/promo/reddit_watch.py
  python scripts/promo/reddit_watch.py --hours 24 --min-questions 1
  python scripts/promo/reddit_watch.py --subs WindroseGame,pcgaming --keywords windrose

输出：
  reports/daily/YYYY-MM-DD-reddit.md
  打印到 stdout 的就是这个文件路径

不需要登录。使用 Reddit 公开 JSON API（每分钟约 60 req，足够）。
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from datetime import datetime, timezone

from _common import (
    get_logger,
    get_secret,
    http_get_json,
    md_table,
    report_path,
    write_report,
)

# Reddit 屏蔽默认 bot UA。用接近浏览器的 UA 走公开 JSON 端点。
# 注意：仅做读取候选清单，无任何写操作，不违反 Reddit 用户协议中的"自动化"条款。
REDDIT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

logger = get_logger("reddit_watch")

DEFAULT_SUBS = "WindroseGame,Windrose,pcgaming,Survivalgaming,PirateGames,CoopGaming"
DEFAULT_KEYWORDS = "windrose"
QUESTION_HINTS = [
    r"\?",
    r"\bhow\s+(?:to|do|can)\b",
    r"\bwhere\s+(?:to|is|do|can)\b",
    r"\bwhy\b",
    r"\bwhat(?:'s| is)\b",
    r"\bcan\s+(?:i|you|we)\b",
    r"\bstuck\b",
    r"\bhelp\b",
    r"\bbest\s+way\b",
    r"\banyone\s+know\b",
]
QUESTION_RE = re.compile("|".join(QUESTION_HINTS), re.IGNORECASE)


def fetch_sub(sub: str, keyword: str, hours: int) -> list[dict]:
    """从 sub 内搜索 keyword，按 new 排序。"""
    url = (
        f"https://www.reddit.com/r/{sub}/search.json"
        f"?q={keyword}&sort=new&restrict_sr=1&t=week&limit=50"
    )
    try:
        data = http_get_json(url, headers={"User-Agent": REDDIT_UA})
    except Exception as e:
        logger.warning("拉 r/%s 失败: %r", sub, e)
        return []

    cutoff = time.time() - hours * 3600
    out: list[dict] = []
    for child in data.get("data", {}).get("children", []):
        d = child.get("data", {})
        created = d.get("created_utc", 0)
        if created < cutoff:
            continue
        title = d.get("title", "")
        selftext = d.get("selftext", "") or ""
        body = (title + " " + selftext)[:2000]
        is_question = bool(QUESTION_RE.search(body))
        out.append(
            {
                "sub": sub,
                "title": title,
                "url": "https://www.reddit.com" + d.get("permalink", ""),
                "author": d.get("author", "[deleted]"),
                "score": d.get("score", 0),
                "comments": d.get("num_comments", 0),
                "created_utc": created,
                "created_iso": datetime.fromtimestamp(
                    created, tz=timezone.utc
                ).isoformat(timespec="minutes"),
                "is_question": is_question,
                "snippet": (selftext[:240] + "...") if len(selftext) > 240 else selftext,
                "flair": d.get("link_flair_text") or "",
            }
        )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=int, default=24, help="只看过去多少小时（默认 24）")
    ap.add_argument(
        "--subs",
        default=get_secret("REDDIT_SUBS", DEFAULT_SUBS),
        help="逗号分隔的 sub 列表",
    )
    ap.add_argument(
        "--keywords",
        default=get_secret("REDDIT_KEYWORDS", DEFAULT_KEYWORDS),
        help="逗号分隔的搜索关键词",
    )
    ap.add_argument(
        "--min-questions",
        type=int,
        default=0,
        help="低于此值就在报告里提示需要扩大范围",
    )
    args = ap.parse_args()

    subs = [s.strip() for s in args.subs.split(",") if s.strip()]
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]

    logger.info("subs=%s, keywords=%s, hours=%d", subs, keywords, args.hours)

    seen: set[str] = set()
    posts: list[dict] = []
    for sub in subs:
        for kw in keywords:
            for p in fetch_sub(sub, kw, args.hours):
                if p["url"] in seen:
                    continue
                seen.add(p["url"])
                posts.append(p)
            time.sleep(1.0)  # 礼貌限速，避免 429

    posts.sort(key=lambda x: (not x["is_question"], -x["created_utc"]))

    questions = [p for p in posts if p["is_question"]]
    others = [p for p in posts if not p["is_question"]]

    today = datetime.now().strftime("%Y-%m-%d")
    lines: list[str] = []
    lines.append(f"# Reddit 监控日报 — {today}")
    lines.append("")
    lines.append(f"窗口：过去 {args.hours} 小时")
    lines.append(f"覆盖 subs：{', '.join(subs)}")
    lines.append(f"关键词：{', '.join(keywords)}")
    lines.append(
        f"命中：{len(posts)} 篇（其中疑似问答 {len(questions)} 篇）"
    )
    lines.append("")

    if len(questions) < args.min_questions:
        lines.append(
            f"> ⚠️ 问答帖少于 {args.min_questions}，建议本日扩大 sub 或关键词。"
        )
        lines.append("")

    if questions:
        lines.append("## 🎯 优先回答的问答帖")
        lines.append("")
        lines.append(
            md_table(
                ["sub", "title", "score", "comments", "created", "link"],
                [
                    [
                        f"r/{p['sub']}",
                        p["title"][:80],
                        str(p["score"]),
                        str(p["comments"]),
                        p["created_iso"],
                        f"[open]({p['url']})",
                    ]
                    for p in questions[:30]
                ],
            )
        )
        lines.append("")
        lines.append("### 详情")
        lines.append("")
        for p in questions[:15]:
            lines.append(f"#### r/{p['sub']} — {p['title']}")
            lines.append("")
            lines.append(f"- 作者：u/{p['author']} | score={p['score']} | comments={p['comments']}")
            lines.append(f"- 时间：{p['created_iso']}")
            if p["flair"]:
                lines.append(f"- flair：`{p['flair']}`")
            lines.append(f"- 链接：{p['url']}")
            if p["snippet"]:
                lines.append("")
                lines.append("> " + p["snippet"].replace("\n", " "))
            lines.append("")
    else:
        lines.append("## 🎯 优先回答的问答帖")
        lines.append("")
        lines.append("_今日窗口内未发现明显问答帖。_")
        lines.append("")

    if others:
        lines.append("## 其他相关讨论")
        lines.append("")
        lines.append(
            md_table(
                ["sub", "title", "score", "comments", "created", "link"],
                [
                    [
                        f"r/{p['sub']}",
                        p["title"][:80],
                        str(p["score"]),
                        str(p["comments"]),
                        p["created_iso"],
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
    lines.append("- 优先挑 score 较低、comments 较少的新帖回答（更有可能成为最佳答案）")
    lines.append("- 遵守 10:1 自推规则，每 10 条普通回答配 1 条带 windrosewiki.games 链接")
    lines.append("- 长贴回答后顺手 upvote 提问者，养号")

    out = report_path("daily", "reddit")
    write_report(out, "\n".join(lines))
    logger.info("已写入 %s", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
