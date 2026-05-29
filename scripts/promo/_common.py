"""
推广脚本公共工具

约定：
  - 报告统一写到 reports/{daily,weekly,monthly}/YYYY-MM-DD-<name>.md
  - 凭证从环境变量或 scripts/promo/.secrets.json 读取（gitignore）
  - 所有脚本的日志走 stderr，结果文件路径打印到 stdout，便于 pipeline
"""

from __future__ import annotations

import json
import logging
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "reports"
SECRETS_FILE = Path(__file__).resolve().parent / ".secrets.json"

UA = "WindroseWikiPromoBot/1.0 (+https://windrosewiki.games)"


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stderr,
    )
    return logging.getLogger(name)


def load_secrets() -> dict[str, Any]:
    """先尝试 .secrets.json，再退回到环境变量。"""
    if SECRETS_FILE.exists():
        try:
            return json.loads(SECRETS_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def get_secret(key: str, default: str | None = None) -> str | None:
    """key 大小写敏感；优先 .secrets.json，再环境变量。"""
    s = load_secrets()
    if key in s:
        return str(s[key])
    return os.environ.get(key, default)


def report_path(kind: str, name: str, ext: str = "md") -> Path:
    """
    kind: daily / weekly / monthly
    name: e.g. "reddit", "gsc", "steam"
    返回: reports/<kind>/YYYY-MM-DD-<name>.<ext>
    """
    today = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")
    out_dir = REPORTS / kind
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / f"{today}-{name}.{ext}"


def http_get_json(url: str, timeout: int = 20, headers: dict[str, str] | None = None) -> Any:
    h = {"User-Agent": UA, "Accept": "application/json"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def http_get_text(url: str, timeout: int = 20, headers: dict[str, str] | None = None) -> str:
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def write_report(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    print(str(path))  # stdout: 让调用方知道生成了哪个文件


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    """生成简单 markdown 表格。单元格内 | 会被替换成 \\| ，换行被替换成空格。"""
    def safe(s: str) -> str:
        return str(s).replace("|", "\\|").replace("\n", " ").strip()

    out = ["| " + " | ".join(safe(h) for h in headers) + " |"]
    out.append("|" + "|".join("---" for _ in headers) + "|")
    for row in rows:
        out.append("| " + " | ".join(safe(c) for c in row) + " |")
    return "\n".join(out)
