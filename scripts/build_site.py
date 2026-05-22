from pathlib import Path
import datetime
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
SITE = "https://windrose-guides.com"
TODAY = datetime.date.today().isoformat()


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_data_files():
    errors = []
    for path in sorted(DATA_DIR.glob("*.json")):
        try:
            data = load_json(path)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
            continue

        if path.name in ("schema-template.json", "search-index.json"):
            continue

        if isinstance(data, dict) and "items" in data:
            items = data["items"]
            data_type = data.get("type", "")
        elif isinstance(data, list):
            items = data
            data_type = ""
        else:
            continue

        for index, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"{path.relative_to(ROOT)}[{index}]: item must be an object")
                continue
            if data_type == "page_snapshot_collection":
                required_fields = ("id", "title", "h1", "source_file", "extracted_at")
            else:
                required_fields = ("id", "slug", "name", "status", "confidence")
            for field in required_fields:
                if field == "slug" and item.get(field) == "":
                    continue
                if not item.get(field):
                    errors.append(f"{path.relative_to(ROOT)}[{index}]: missing {field}")
            if "sources" in item and not isinstance(item["sources"], list):
                errors.append(f"{path.relative_to(ROOT)}[{index}]: sources must be a list")
    return errors


def html_slug(path):
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return ""
    if rel.endswith("/index.html"):
        return rel[:-len("/index.html")]
    return rel[:-len(".html")]


def update_sitemap():
    urls = []
    for html_file in ROOT.rglob("*.html"):
        if any(part in {".git", "docs", "scripts", "skills"} for part in html_file.parts):
            continue
        slug = html_slug(html_file)
        if slug == "404":
            continue
        priority = "0.6"
        if slug == "":
            priority = "1.0"
        elif slug in {"beginner-guide", "crafting/workbench", "resources/copper", "tools", "tools/recipe-finder", "tools/progression-checklist"}:
            priority = "0.9"
        elif slug.split("/")[0] in {"crafting", "resources", "bosses", "ships", "weapons", "builds", "server-guide"}:
            priority = "0.8"
        elif slug.startswith("database/items/"):
            priority = "0.7"
        elif slug.startswith("news/") and slug != "news":
            priority = "0.7"
        # NOTE: 新闻页和新闻详情页使用 daily，保持 Google 抓取频率
        changefreq = "daily" if slug.startswith("news") else "weekly"
        urls.append((slug, priority, changefreq))

    urls.sort(key=lambda item: (item[0].count("/"), item[0]))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for slug, priority, changefreq in urls:
        loc = f"{SITE}/" if slug == "" else f"{SITE}/{slug}"
        lines.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(urls)


def run_builders():
    scripts_to_run = [
        "seo_iteration.py",
        "collect_item_stats.py",
        "gen_database_pages.py",
        "gen_detail_pages.py",
        "gen_news_pages.py",
        "gen_home_pages.py",
        "gen_section_stubs.py",
    ]
    for script_name in scripts_to_run:
        script_path = ROOT / "scripts" / script_name
        if script_path.exists():
            print(f"Running {script_name}...")
            subprocess.run([sys.executable, str(script_path)], cwd=ROOT, check=True)


def main():
    errors = validate_data_files()
    if errors:
        print("Data validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    run_builders()
    # NOTE: sitemap 由 seo_iteration.py 生成（含 hreflang 多语言替代链接），
    # 不在此处覆写以避免丢失 hreflang。
    print("Data validation passed.")
    print("Note: build_site.py now delegates to seo_iteration, gen_database_pages, and gen_detail_pages.")


if __name__ == "__main__":
    main()
