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

# 列表页结构（截至 2026-05，已不是原来的 name → op → reply_count 顺序）：
#   <a class="forum_topic_overlay" href="URL">  ← 行起点锚
#     <div class="forum_topic_details ...">
#       <div class="forum_topic_reply_count"><img...> N </div>
#       [<div class="forum_topic_award_count">...</div>]
#       [<div class="forum_topic_lastpost" title="..." data-timestamp="TS"> 显示文本 </div>]
#     </div>
#     [<div class="forum_topic_icon" title="This thread is pinned/locked..."><img/></div>]
#     <div class="forum_topic_name ">[<span class="forum_topic_label ...">PINNED:</span>] 标题</div>
#     <div class="forum_topic_op"> 作者 </div>
# 直接对每个 overlay 切片解析比单一大正则稳健得多。
OVERLAY_RE = re.compile(r'<a class="forum_topic_overlay"\s+href="([^"]+)"')
REPLY_RE = re.compile(
    r'class="forum_topic_reply_count"\s*>\s*(?:<img[^>]*>)?\s*(\d+)',
    re.DOTALL,
)
LASTPOST_RE = re.compile(
    r'class="forum_topic_lastpost"([^>]*)>\s*(.*?)\s*</div>',
    re.DOTALL,
)
LASTPOST_TS_RE = re.compile(r'data-timestamp="(\d+)"')
NAME_RE = re.compile(r'class="forum_topic_name[^"]*"\s*>(.*?)</div>', re.DOTALL)
LABEL_SPAN_RE = re.compile(
    r'<span\s+class="forum_topic_label[^"]*"[^>]*>.*?</span>',
    re.DOTALL,
)
OP_RE = re.compile(r'class="forum_topic_op"\s*>\s*(.+?)\s*</div>', re.DOTALL)
ICON_TITLE_RE = re.compile(r'class="forum_topic_icon"\s+title="([^"]+)"')
TAG_RE = re.compile(r'<[^>]+>')

QUESTION_RE = re.compile(
    r"\?|\bhow\b|\bwhere\b|\bwhy\b|\bwhat\b|\bcan\s+(?:i|you)\b|"
    r"\bstuck\b|\bhelp\b|\bbug\b|\bcrash\b|\banyone\b|\bquestion(?:s)?\b",
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


def _strip_html(s: str) -> str:
    s = TAG_RE.sub("", s)
    return html.unescape(re.sub(r"\s+", " ", s)).strip()


def parse_list(text: str) -> list[dict]:
    starts = [(m.start(), m.group(1)) for m in OVERLAY_RE.finditer(text)]
    if not starts:
        return []

    out: list[dict] = []
    for i, (start, raw_url) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else len(text)
        chunk = text[start:end]

        m_name = NAME_RE.search(chunk)
        if not m_name:
            continue
        raw_title = LABEL_SPAN_RE.sub("", m_name.group(1))
        title = _strip_html(raw_title)
        if not title:
            continue

        m_reply = REPLY_RE.search(chunk)
        replies = int(m_reply.group(1)) if m_reply else 0

        m_op = OP_RE.search(chunk)
        op = _strip_html(m_op.group(1)) if m_op else ""

        last = ""
        last_ts: int | None = None
        m_last = LASTPOST_RE.search(chunk)
        if m_last:
            last = _strip_html(m_last.group(2))
            m_ts = LASTPOST_TS_RE.search(m_last.group(1))
            if m_ts:
                last_ts = int(m_ts.group(1))

        icon_title = ""
        m_icon = ICON_TITLE_RE.search(chunk)
        if m_icon:
            icon_title = html.unescape(m_icon.group(1))
        pinned = (
            "pinned" in icon_title.lower()
            or 'class="forum_topic_label sticky_label"' in chunk
        )
        locked = "locked" in icon_title.lower()

        out.append(
            {
                "url": html.unescape(raw_url).strip(),
                "title": title,
                "op": op,
                "replies": replies,
                "last": last,
                "last_ts": last_ts,
                "pinned": pinned,
                "locked": locked,
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

    # 置顶 / 锁帖通常是开发组公告或 FAQ，不需要去回答
    pinned = [p for p in posts if p["pinned"] or p["locked"]]
    active = [p for p in posts if not (p["pinned"] or p["locked"])]

    def _sort_key(p: dict) -> tuple[int, int]:
        # 按最后活动时间倒序（无 ts 排最后）
        ts = p.get("last_ts") or 0
        return (0 if ts else 1, -ts)

    questions = sorted(
        [p for p in active if p["is_question"] and p["replies"] <= args.max_replies],
        key=_sort_key,
    )
    answered = sorted(
        [p for p in active if p["is_question"] and p["replies"] > args.max_replies],
        key=_sort_key,
    )
    others = sorted([p for p in active if not p["is_question"]], key=_sort_key)

    today = datetime.now().strftime("%Y-%m-%d")
    lines: list[str] = []
    lines.append(f"# Steam 社区监控日报 — {today}")
    lines.append("")
    lines.append(f"App ID：{args.app_id}（Windrose）")
    lines.append(
        f"抓取页数：{args.pages}，命中 {len(posts)} 帖"
        f"（活跃 {len(active)}，置顶/锁 {len(pinned)}，"
        f"疑似问答 {len(questions) + len(answered)}）"
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

    if pinned:
        lines.append("## 置顶 / 锁帖（参考用，不要回复）")
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
                    for p in pinned[:10]
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
