"""找出所有缺少新 footer 的 HTML 页面"""
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")

for dirpath, dirs, files in os.walk(ROOT):
    rel_dir = os.path.relpath(dirpath, ROOT)
    if rel_dir.startswith(("docs", "scripts", "data", "css", "js", "imgs", ".git", "node_modules")):
        continue
    for f in files:
        if f == "index.html":
            fp = os.path.join(dirpath, f)
            with open(fp, encoding="utf-8") as fh:
                content = fh.read()
            if "footer-grid" not in content:
                rel = os.path.relpath(fp, ROOT)
                # 检测 footer 类型
                if 'class="footer"' in content:
                    ftype = "old-class"
                elif "<footer>" in content:
                    ftype = "bare-tag"
                else:
                    ftype = "no-footer"
                print(f"  Missing: {rel} ({ftype})")
