"""
分析竞品页面的完整 DOM 结构，找出所有需要采集的字段的精确位置。
"""
import requests
from bs4 import BeautifulSoup
import json
import re

BASE_URL = 'https://windrosewiki.org'

# 选三个典型页面：武器(有多级制作)、弹药(简单制作)、资源(无制作)
test_urls = [
    '/database/items/eid-melee-weapon-saber-blank-base',  # Saber - 武器，有 Tier 1/2/3
    '/database/items/aid-ammo-firearm-projectile-stone-bullet-t01',  # Stone Bullet - 弹药
    '/database/items/did-resource-wood-t01',  # Wood - 资源
]

for url in test_urls:
    full_url = BASE_URL + url
    res = requests.get(full_url, timeout=15)
    soup = BeautifulSoup(res.text, 'html.parser')

    print(f"\n{'='*80}")
    print(f"URL: {url}")
    print(f"{'='*80}")

    # 1. 名称
    h1 = soup.find('h1')
    print(f"\n[名称] {h1.text.strip() if h1 else 'MISSING'}")

    # 2. 顶部徽章（分类、稀有度）
    # 找到 h1 后面紧跟的 flex 容器
    badge_container = soup.find('div', class_=lambda c: c and 'flex' in c and 'gap-2' in c and 'flex-wrap' in c)
    if badge_container:
        badges = badge_container.find_all('span', recursive=False)
        if not badges:
            badges = badge_container.find_all('span')
        print(f"[徽章] {[b.text.strip() for b in badges]}")
    else:
        print("[徽章] MISSING - 尝试其他选择器")
        # 尝试更宽泛的查找
        all_flex = soup.find_all('div', class_=lambda c: c and 'flex' in c)
        for div in all_flex[:5]:
            spans = div.find_all('span', recursive=False)
            if spans and len(spans) >= 2:
                print(f"  候选: {[s.text.strip() for s in spans[:5]]}")

    # 3. 概述
    overview_h2 = soup.find(lambda tag: tag.name == 'h2' and 'Overview' in tag.text)
    if overview_h2:
        p = overview_h2.find_next_sibling('p')
        print(f"[概述] {p.text.strip()[:100] if p else 'MISSING'}...")
    else:
        print("[概述] MISSING")

    # 4. 主图片
    item_name = h1.text.strip() if h1 else ''
    img = soup.find('img', alt=item_name)
    if img:
        print(f"[主图片] src={img.get('src', 'N/A')}, alt={img.get('alt', 'N/A')}")
    else:
        # 尝试找到 flex-1 内的 img
        flex1 = soup.find('div', class_='flex-1')
        if flex1:
            img = flex1.find('img')
            print(f"[主图片-flex1] src={img.get('src', 'N/A') if img else 'N/A'}")
        else:
            print("[主图片] MISSING")

    # 5. 制作 (Crafting) 部分 - 这是重点
    crafting_h2 = soup.find(lambda tag: tag.name == 'h2' and 'Crafting' in tag.text)
    if crafting_h2:
        print(f"\n[制作区域] 找到 Crafting h2")
        
        # 找制作区域的父容器
        crafting_section = crafting_h2.parent
        if crafting_section:
            # 找所有包含 Tier 信息的 div
            tier_divs = crafting_section.find_all('div', class_=lambda c: c and 'flex' in c and 'flex-wrap' in c)
            
            # 找所有 span 标签
            all_spans = crafting_section.find_all('span')
            tier_info = []
            station_info = []
            time_info = []
            for span in all_spans:
                txt = span.text.strip()
                if txt.startswith('Tier'):
                    tier_info.append(txt)
                elif txt.startswith('Station'):
                    station_info.append(txt)
                elif '/min' in txt or txt.endswith('s'):
                    time_info.append(txt)
            
            print(f"  Tier信息: {tier_info}")
            print(f"  Station信息: {station_info}")
            print(f"  Time信息: {time_info}")

            # 找材料 - 通常在一个有链接的容器内
            material_links = crafting_section.find_all('a', href=lambda h: h and '/database/items/' in h)
            for a in material_links:
                mat_img = a.find('img')
                mat_name_span = a.find('span')
                qty_match = re.search(r'×(\d+)', a.text)
                print(f"  材料: name={mat_name_span.text.strip() if mat_name_span else a.text.strip()}, "
                      f"qty={qty_match.group(1) if qty_match else '?'}, "
                      f"icon={mat_img.get('src', 'N/A') if mat_img else 'NO_IMG'}, "
                      f"href={a.get('href', 'N/A')}")

            # 找工作台图标
            station_imgs = crafting_section.find_all('img')
            for si in station_imgs:
                if si.get('alt', '') and si not in [a.find('img') for a in material_links if a.find('img')]:
                    print(f"  工作台图标: src={si.get('src')}, alt={si.get('alt')}")
    else:
        print("\n[制作区域] 无 Crafting 区域")

    # 6. Stats / 属性
    stats_h2 = soup.find(lambda tag: tag.name == 'h2' and 'Stats' in tag.text)
    if stats_h2:
        print(f"\n[属性区域] 找到 Stats h2")
        stats_section = stats_h2.parent
        if stats_section:
            # 找属性行
            rows = stats_section.find_all('div', class_=lambda c: c and 'flex' in c)
            for row in rows[:10]:
                txt = row.text.strip().replace('\n', ' ')
                if txt and len(txt) < 100:
                    print(f"  属性: {txt}")
    else:
        print("\n[属性区域] 无 Stats 区域")

    # 7. 扫描所有 h2 看还有什么区域
    all_h2 = soup.find_all('h2')
    print(f"\n[所有 h2 标题] {[h.text.strip() for h in all_h2]}")

    print()
