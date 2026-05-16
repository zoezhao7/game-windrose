"""快速检查当前项目状态"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. scraped_items.json
with open(os.path.join(ROOT, 'data', 'scraped_items.json'), 'r', encoding='utf-8') as f:
    scraped = json.load(f)
print(f"scraped_items.json: {len(scraped['items'])} 条")

# 2. 详情页数量
detail_dir = os.path.join(ROOT, 'database', 'items')
page_count = 0
for d in os.listdir(detail_dir):
    idx = os.path.join(detail_dir, d, 'index.html')
    if os.path.exists(idx):
        page_count += 1
print(f"已生成详情页: {page_count} 个")

# 3. 图片数量
img_dir = os.path.join(ROOT, 'imgs', 'database', 'items')
imgs = [f for f in os.listdir(img_dir) if f.endswith('.webp')]
print(f"已下载图片: {len(imgs)} 个")

# 4. 抽查 saber 页面
saber_path = os.path.join(detail_dir, 'saber', 'index.html')
with open(saber_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("\n=== saber 页面检查 ===")
checks = [
    ("真实图标", "saber.webp" in content),
    ("Level显示", "Level" in content and "stat-value" in content),
    ("Uncommon", "Uncommon" in content),
    ("真实概述", "simple saber" in content),
    ("Crafting面板", "crafting-premium" in content),
    ("材料图标", "copper-ingot.webp" in content),
    ("工作台图标", "weaponsmith.webp" in content),
    ("制作时间", "1s (60/min)" in content),
]
for name, ok in checks:
    print(f"  {name}: {'OK' if ok else 'FAIL'}")
