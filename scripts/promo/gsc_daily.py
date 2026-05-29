"""
GSC 日报 — 拉取 Google Search Console 当日 / 近 7 天搜索表现，输出 markdown 日报。

用法：
  python scripts/promo/gsc_daily.py
  python scripts/promo/gsc_daily.py --days 7

凭证（任选其一）：
  1) scripts/promo/.secrets.json 内：
       GSC_OAUTH_CLIENT_ID, GSC_OAUTH_CLIENT_SECRET, GSC_OAUTH_REFRESH_TOKEN, GSC_SITE_URL
  2) 环境变量同名

如何拿 refresh_token（一次性人工操作）：
  - 在 https://console.cloud.google.com/ 创建一个 OAuth Desktop 客户端
  - 在 https://developers.google.com/oauthplayground 用自己的客户端凭证授权 scope:
        https://www.googleapis.com/auth/webmasters.readonly
  - 复制 refresh_token 到 .secrets.json

GSC API 文档：
  https://developers.google.com/webmaster-tools/v1/searchanalytics/query
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta

from _common import (
    get_logger,
    get_secret,
    md_table,
    report_path,
    write_report,
)

logger = get_logger("gsc_daily")

TOKEN_URL = "https://oauth2.googleapis.com/token"
API_BASE = "https://searchconsole.googleapis.com/webmasters/v3"


def get_access_token() -> str:
    cid = get_secret("GSC_OAUTH_CLIENT_ID")
    cs = get_secret("GSC_OAUTH_CLIENT_SECRET")
    rt = get_secret("GSC_OAUTH_REFRESH_TOKEN")
    if not (cid and cs and rt):
        raise SystemExit(
            "缺少 GSC_OAUTH_CLIENT_ID / GSC_OAUTH_CLIENT_SECRET / GSC_OAUTH_REFRESH_TOKEN。\n"
            "见脚本头部注释如何获取。"
        )
    body = urllib.parse.urlencode(
        {
            "client_id": cid,
            "client_secret": cs,
            "refresh_token": rt,
            "grant_type": "refresh_token",
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        TOKEN_URL,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data["access_token"]


def query(
    site: str,
    token: str,
    start: str,
    end: str,
    dimensions: list[str],
    row_limit: int = 1000,
) -> list[dict]:
    url = f"{API_BASE}/sites/{urllib.parse.quote(site, safe='')}/searchAnalytics/query"
    payload = {
        "startDate": start,
        "endDate": end,
        "dimensions": dimensions,
        "rowLimit": row_limit,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data.get("rows", [])


def fmt_pct(x: float) -> str:
    return f"{x * 100:.2f}%"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7, help="近多少天的窗口（默认 7）")
    ap.add_argument(
        "--site",
        default=get_secret("GSC_SITE_URL", "sc-domain:windrosewiki.games"),
    )
    args = ap.parse_args()

    # GSC 数据有 1-2 天延迟，所以 endDate 用昨天
    end = (date.today() - timedelta(days=2)).isoformat()
    start = (date.today() - timedelta(days=2 + args.days - 1)).isoformat()
    logger.info("site=%s, %s → %s", args.site, start, end)

    token = get_access_token()

    by_query = query(args.site, token, start, end, ["query"], row_limit=200)
    by_page = query(args.site, token, start, end, ["page"], row_limit=200)
    by_country = query(args.site, token, start, end, ["country"], row_limit=20)
    by_device = query(args.site, token, start, end, ["device"], row_limit=10)

    total_clicks = sum(r.get("clicks", 0) for r in by_query)
    total_impr = sum(r.get("impressions", 0) for r in by_query)
    avg_ctr = (total_clicks / total_impr) if total_impr else 0.0

    # 按曝光排序，找"高曝光低点击"
    by_query_sorted = sorted(by_query, key=lambda r: -r.get("impressions", 0))
    zero_click_high_impr = [
        r
        for r in by_query_sorted
        if r.get("impressions", 0) >= 30 and r.get("clicks", 0) == 0
    ][:30]

    top_clicks = sorted(by_query, key=lambda r: -r.get("clicks", 0))[:20]
    top_pages = sorted(by_page, key=lambda r: -r.get("clicks", 0))[:20]

    today = datetime.now().strftime("%Y-%m-%d")
    lines: list[str] = []
    lines.append(f"# GSC 日报 — {today}")
    lines.append("")
    lines.append(f"站点：`{args.site}`")
    lines.append(f"窗口：{start} → {end}（共 {args.days} 天）")
    lines.append("")
    lines.append("## 总览")
    lines.append("")
    lines.append(
        md_table(
            ["指标", "值"],
            [
                ["总点击", f"{total_clicks}"],
                ["总曝光", f"{total_impr}"],
                ["平均 CTR", fmt_pct(avg_ctr)],
                ["不同 query 数", f"{len(by_query)}"],
                ["不同 page 数", f"{len(by_page)}"],
            ],
        )
    )
    lines.append("")

    lines.append("## 🔝 Top 20 关键词（按点击）")
    lines.append("")
    lines.append(
        md_table(
            ["query", "clicks", "impr", "ctr", "position"],
            [
                [
                    r["keys"][0],
                    str(r.get("clicks", 0)),
                    str(r.get("impressions", 0)),
                    fmt_pct(r.get("ctr", 0)),
                    f"{r.get('position', 0):.1f}",
                ]
                for r in top_clicks
            ],
        )
    )
    lines.append("")

    lines.append("## ⚠️ 高曝光但 0 点击的关键词（最值得改写 title/meta）")
    lines.append("")
    if zero_click_high_impr:
        lines.append(
            md_table(
                ["query", "impr", "ctr", "position"],
                [
                    [
                        r["keys"][0],
                        str(r.get("impressions", 0)),
                        fmt_pct(r.get("ctr", 0)),
                        f"{r.get('position', 0):.1f}",
                    ]
                    for r in zero_click_high_impr
                ],
            )
        )
    else:
        lines.append("_没有曝光 ≥30 且 0 点击的关键词，CTR 表现良好。_")
    lines.append("")

    lines.append("## 🔝 Top 20 落地页（按点击）")
    lines.append("")
    lines.append(
        md_table(
            ["page", "clicks", "impr", "ctr", "position"],
            [
                [
                    r["keys"][0],
                    str(r.get("clicks", 0)),
                    str(r.get("impressions", 0)),
                    fmt_pct(r.get("ctr", 0)),
                    f"{r.get('position', 0):.1f}",
                ]
                for r in top_pages
            ],
        )
    )
    lines.append("")

    if by_country:
        lines.append("## 国家分布（Top 10）")
        lines.append("")
        lines.append(
            md_table(
                ["country", "clicks", "impr", "ctr"],
                [
                    [
                        r["keys"][0],
                        str(r.get("clicks", 0)),
                        str(r.get("impressions", 0)),
                        fmt_pct(r.get("ctr", 0)),
                    ]
                    for r in sorted(by_country, key=lambda r: -r.get("clicks", 0))[:10]
                ],
            )
        )
        lines.append("")

    if by_device:
        lines.append("## 设备分布")
        lines.append("")
        lines.append(
            md_table(
                ["device", "clicks", "impr", "ctr"],
                [
                    [
                        r["keys"][0],
                        str(r.get("clicks", 0)),
                        str(r.get("impressions", 0)),
                        fmt_pct(r.get("ctr", 0)),
                    ]
                    for r in by_device
                ],
            )
        )
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("行动建议：")
    lines.append("- 高曝光 0 点击的 query → 立刻改写对应页 title 和 meta description")
    lines.append("- 排名 11–20 的 query → 内链补强 + FAQ 锚点，争取冲到第一页")
    lines.append("- 新出现的长尾词 → 考虑建独立页或扩写现有页对应章节")

    out = report_path("daily", "gsc")
    write_report(out, "\n".join(lines))
    logger.info("已写入 %s", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
