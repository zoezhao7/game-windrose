"""Strip the brand suffix from JSON-LD WebPage.name and Article.headline on
all bosses-hub pages so they don't display ` | Windrose Wiki` inside Schema.org.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HUB_TITLES = {
    "bosses/index.html":     "All 4 Windrose Bosses (2026): Order, Drops & Strategies",
    "de/bosses/index.html":  "Alle 4 Windrose-Bosse (2026): Reihenfolge, Drops & Strategien",
    "es/bosses/index.html":  "Los 4 jefes de Windrose (2026): orden, botines y estrategias",
    "fr/bosses/index.html":  "Les 4 boss de Windrose (2026) : ordre, butins & stratégies",
    "pt/bosses/index.html":  "Os 4 chefes de Windrose (2026): ordem, drops e estratégias",
    "zh/bosses/index.html":  "Windrose 全部 4 个 Boss（2026）：顺序、掉落与攻略",
}

def jesc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')

for rel, clean in HUB_TITLES.items():
    p = ROOT / rel
    html = p.read_text(encoding="utf-8")
    orig = html
    html = re.sub(
        r'("@type"\s*:\s*"WebPage"[^{}]*?"name"\s*:\s*")[^"]*(")',
        lambda m: m.group(1) + jesc(clean) + m.group(2),
        html, count=1, flags=re.DOTALL,
    )
    html = re.sub(
        r'("@type"\s*:\s*"Article"[^{}]*?"headline"\s*:\s*")[^"]*(")',
        lambda m: m.group(1) + jesc(clean) + m.group(2),
        html, count=1, flags=re.DOTALL,
    )
    if html != orig:
        p.write_text(html, encoding="utf-8")
        print(f"  ✓ {rel}")
    else:
        print(f"  no-op {rel}")
