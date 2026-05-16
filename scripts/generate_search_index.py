import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

def main():
    DATA_DIR.mkdir(exist_ok=True)
    index = []
    
    for html_file in sorted(ROOT.rglob("*.html")):
        if any(part in {".git", "docs", "scripts", "skills", "css", "data"} for part in html_file.parts):
            continue
            
        rel = html_file.relative_to(ROOT).as_posix()
        if rel == "index.html":
            url = "/"
        elif rel.endswith("/index.html"):
            url = "/" + rel[:-len("index.html")]
        else:
            url = "/" + rel
            
        soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "html.parser")
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else "No Title"
        
        desc_tag = soup.find("meta", attrs={"name": "description"})
        desc = desc_tag.get("content", "").strip() if desc_tag else ""
        
        # Make the title cleaner by removing the suffix
        clean_title = title.split(" | ")[0]
        
        index.append({
            "url": url,
            "title": clean_title,
            "description": desc
        })
        
    out_path = DATA_DIR / "search-index.json"
    out_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Generated search index with {len(index)} pages at {out_path.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
