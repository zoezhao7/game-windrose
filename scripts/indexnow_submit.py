"""
IndexNow 提交脚本

用法：
  # 提交一个或多个 URL
  python scripts/indexnow_submit.py https://windrosewiki.games/news/foo https://windrosewiki.games/news/bar

  # 从 stdin 逐行读取（便于 pipeline）
  echo "https://windrosewiki.games/news/foo" | python scripts/indexnow_submit.py -

  # 提交整个 sitemap.xml（首次接入或大批量更新时用，平时不要跑）
  python scripts/indexnow_submit.py --from-sitemap

参数：
  --dry-run   只打印请求体，不真正发送

说明：
  - 单次最多 10000 条 URL（IndexNow 协议上限）
  - 同一站点同一天大批量重复提交可能触发 429
  - 同 host (windrosewiki.games) 的 URL 才会被接受
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HOST = "windrosewiki.games"
KEY = "62eeee17bb84441ea332d93033db687b"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/IndexNow"
SITEMAP = ROOT / "sitemap.xml"
BATCH_SIZE = 10000

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("indexnow")


def normalize_url(u: str) -> str:
    u = u.strip()
    if not u:
        return ""
    if u.startswith("/"):
        u = f"https://{HOST}{u}"
    return u


def filter_for_host(urls: list[str]) -> list[str]:
    keep = []
    dropped = 0
    for u in urls:
        if not u:
            continue
        if f"//{HOST}/" in u or u.rstrip("/").endswith(f"//{HOST}"):
            keep.append(u)
        else:
            dropped += 1
    if dropped:
        logger.warning("丢弃 %d 个非 %s 的 URL", dropped, HOST)
    return keep


def load_from_sitemap() -> list[str]:
    if not SITEMAP.exists():
        logger.error("sitemap.xml 不存在: %s", SITEMAP)
        return []
    text = SITEMAP.read_text(encoding="utf-8")
    return re.findall(r"<loc>([^<]+)</loc>", text)


def submit(urls: list[str], dry_run: bool = False) -> bool:
    if not urls:
        logger.warning("没有要提交的 URL")
        return False

    all_ok = True
    for i in range(0, len(urls), BATCH_SIZE):
        batch = urls[i : i + BATCH_SIZE]
        payload = {
            "host": HOST,
            "key": KEY,
            "keyLocation": KEY_LOCATION,
            "urlList": batch,
        }
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        if dry_run:
            logger.info("[dry-run] 将发送 %d 条到 %s", len(batch), ENDPOINT)
            logger.info("payload preview: %s", body[:400].decode("utf-8", "replace"))
            continue

        req = urllib.request.Request(
            ENDPOINT,
            data=body,
            method="POST",
            headers={"Content-Type": "application/json; charset=utf-8"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                logger.info(
                    "批次 %d/%d: %d 条 → HTTP %d %s",
                    i // BATCH_SIZE + 1,
                    (len(urls) + BATCH_SIZE - 1) // BATCH_SIZE,
                    len(batch),
                    r.status,
                    r.reason,
                )
        except urllib.error.HTTPError as e:
            body_text = e.read().decode("utf-8", "replace")[:500]
            logger.error(
                "批次失败: HTTP %d %s — %s", e.code, e.reason, body_text
            )
            all_ok = False
        except Exception as e:
            logger.error("请求异常: %r", e)
            all_ok = False

    return all_ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="*", help="要提交的 URL；- 表示从 stdin 读")
    ap.add_argument(
        "--from-sitemap",
        action="store_true",
        help="提交 sitemap.xml 中所有 URL（首次接入用）",
    )
    ap.add_argument("--dry-run", action="store_true", help="不真正发送请求")
    args = ap.parse_args()

    urls: list[str] = []
    if args.from_sitemap:
        urls = load_from_sitemap()
        logger.info("从 sitemap 加载 %d 条", len(urls))
    elif args.urls == ["-"]:
        urls = [normalize_url(line) for line in sys.stdin]
    else:
        urls = [normalize_url(u) for u in args.urls]

    urls = filter_for_host([u for u in urls if u])
    logger.info("有效 URL: %d 条", len(urls))

    ok = submit(urls, dry_run=args.dry_run)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
