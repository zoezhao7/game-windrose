from pathlib import Path
from datetime import datetime
import json
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
TODAY = "2026-05-12"


def page_slug(path):
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return ""
    if rel.endswith("/index.html"):
        return rel[:-len("/index.html")]
    return rel[:-len(".html")]


def clean_text(node):
    if not node:
        return ""
    return " ".join(node.get_text(" ", strip=True).split())


def extract_tables(soup):
    tables = []
    for table in soup.find_all("table"):
        caption = clean_text(table.find("caption"))
        headers = [clean_text(th) for th in table.find_all("th")]
        rows = []
        for tr in table.find_all("tr"):
            cells = [clean_text(td) for td in tr.find_all("td")]
            if cells:
                rows.append(cells)
        tables.append({
            "caption": caption,
            "headers": headers,
            "rows": rows
        })
    return tables


def extract_faq(soup):
    faq = []
    for detail in soup.find_all("details"):
        summary = clean_text(detail.find("summary"))
        answer_parts = []
        for child in detail.find_all(["p", "li"]):
            text = clean_text(child)
            if text:
                answer_parts.append(text)
        if summary:
            faq.append({
                "question": summary,
                "answer": " ".join(answer_parts)
            })
    return faq


def extract_links(soup):
    links = []
    for link in soup.find_all("a", href=True):
        text = clean_text(link)
        href = link["href"]
        if text or href:
            links.append({"text": text, "href": href})
    return links


def extract_page(path):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    title = clean_text(soup.find("title"))
    description_tag = soup.find("meta", attrs={"name": "description"})
    description = description_tag.get("content", "") if description_tag else ""
    h1 = clean_text(soup.find("h1"))
    headings = []
    for heading in soup.find_all(["h2", "h3", "h4"]):
        headings.append({
            "level": int(heading.name[1]),
            "text": clean_text(heading)
        })
    slug = page_slug(path)
    return {
        "id": slug or "home",
        "slug": slug,
        "title": title,
        "description": description,
        "h1": h1,
        "headings": headings,
        "tables": extract_tables(soup),
        "faq": extract_faq(soup),
        "links": extract_links(soup),
        "source_file": path.relative_to(ROOT).as_posix(),
        "extracted_at": TODAY
    }


def main():
    DATA_DIR.mkdir(exist_ok=True)
    pages = []
    for html_file in sorted(ROOT.rglob("*.html")):
        if any(part in {".git", "docs", "scripts", "skills"} for part in html_file.parts):
            continue
        pages.append(extract_page(html_file))

    output = {
        "type": "page_snapshot_collection",
        "generated_at": TODAY,
        "purpose": "Snapshot of content already present in HTML files before the project fully migrates to data-driven generation.",
        "items": pages
    }
    out_path = DATA_DIR / "html-content-snapshot.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Extracted {len(pages)} HTML pages to {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
