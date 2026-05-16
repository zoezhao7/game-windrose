"""
Windrose 全量数据采集爬虫 v2。
从竞品 windrosewiki.org 采集所有物品的完整数据，包括：
- 名称、分类、稀有度
- 概述描述
- 物品主图标（下载到本地）
- 多级制作配方（Tier, Station Lv, 制作时间, 材料名/数量/图标）
- 所有材料图标（下载到本地）

数据结构与编码说明：
竞品使用 Next.js，制作数据嵌入在 <script> 标签的 flight data 中，
格式为 self.__next_f.push([1, "..."]) 的转义 JSON 字符串。
"""
import os
import json
import re
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from urllib.parse import urljoin
from pathlib import Path
import time
import threading

ROOT = Path(__file__).resolve().parents[1]
IMGS_DIR = ROOT / 'imgs' / 'database' / 'items'
IMGS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR = ROOT / 'data'

BASE_URL = 'https://windrosewiki.org'

# 用于线程安全的图片下载计数
img_lock = threading.Lock()
img_downloaded = 0
img_skipped = 0
img_failed = 0


def fetch_page(url):
    """获取页面 HTML，带重试"""
    for attempt in range(3):
        try:
            res = requests.get(url, timeout=15)
            res.raise_for_status()
            return res.text
        except Exception as e:
            if attempt < 2:
                time.sleep(1)
            else:
                print(f"  [ERROR] 获取失败 {url}: {e}")
                return None


def download_image(img_url, filename):
    """
    下载图片到本地。
    返回本地路径（相对于站点根目录）。
    如果已存在则跳过下载。
    """
    global img_downloaded, img_skipped, img_failed
    if not img_url:
        return ""
    if not img_url.startswith('http'):
        img_url = urljoin(BASE_URL, img_url)

    img_path = IMGS_DIR / filename
    if img_path.exists() and img_path.stat().st_size > 100:
        with img_lock:
            img_skipped += 1
        return f"/imgs/database/items/{filename}"

    try:
        res = requests.get(img_url, timeout=10)
        res.raise_for_status()
        with open(img_path, 'wb') as f:
            f.write(res.content)
        with img_lock:
            img_downloaded += 1
        return f"/imgs/database/items/{filename}"
    except Exception as e:
        with img_lock:
            img_failed += 1
        return ""


def parse_crafting_from_flight_data(scripts):
    """
    从 Next.js flight data 的 <script> 标签中解析制作配方。
    支持两种格式：
    1. 多级制作（含 "Tier " 标签，如武器 Tier 1/2/3）
    2. 单级制作（无 Tier 标签，只有工作台 + 材料，如弹药/食物）

    返回字典:
    - station: 工作台名称
    - station_icon_url: 工作台图标 URL
    - tiers: [{tier_num, station_lv, time, materials: [{name, amount, icon_url, href, item_id}]}]
    """
    # 收集所有 flight data 脚本内容
    all_flight = []
    for script in scripts:
        content = script.string or ''
        if '__next_f' in content:
            all_flight.append(content)

    if not all_flight:
        return {}

    full_text = "\n".join(all_flight)

    # 反转义 Next.js flight data
    # 移除所有 JSON 转义用的反斜杠字符（ord=92）
    BACKSLASH = chr(92)
    text = full_text.replace(BACKSLASH, '')

    result = {"station": "", "station_icon_url": "", "tiers": []}

    # 提取工作台信息（所有物品通用）
    # 格式: "title":"Click to view Workbench" ... "src":"/windrose-data/images/xxx.webp"
    station_match = re.search(
        r'"title":"Click to view ([^"]+)"[^}]*?"children":\["\$","span"[^}]*?"children":\[\["\$","img"[^}]*?"src":"(/windrose-data/images/[^"]+)"[^}]*?\],[^]]*?"children":"(\1)"',
        text
    )
    if not station_match:
        # 更宽泛的工作台匹配：找 /database/stations/ 链接
        station_link = re.search(
            r'"href":"/database/stations/([^"]+)"[^}]*?"title":"Click to view ([^"]+)"',
            text
        )
        if station_link:
            result["station"] = station_link.group(2)

        # 找工作台图标（通常在 stations 链接附近，40x40 的图片）
        station_img = re.search(
            r'"href":"/database/stations/[^"]*".*?"src":"(/windrose-data/images/[^"]+)".*?"width":40',
            text
        )
        if station_img:
            result["station_icon_url"] = station_img.group(1)

    # === 方式1：多级制作（有 "Tier " 标签）===
    if '["Tier ",' in text:
        tier_splits = re.split(r'\["Tier ",', text)

        for segment in tier_splits[1:]:
            tier_data = {"tier_num": None, "station_lv": None, "time": "", "materials": []}

            # Tier 数字
            tier_match = re.match(r'(\d+)', segment)
            if tier_match:
                tier_data["tier_num"] = int(tier_match.group(1))

            # Station Lv
            station_match = re.search(r'\["Station Lv ",(\d+)\]', segment)
            if station_match:
                tier_data["station_lv"] = int(station_match.group(1))

            # 制作时间
            time_match = re.search(r'"children":"(\d+s \(\d+/min\))"', segment)
            if time_match:
                tier_data["time"] = time_match.group(1)

            # 材料
            _extract_materials(segment, tier_data)

            if tier_data["tier_num"] is not None:
                result["tiers"].append(tier_data)

    # === 方式2：单级制作（无 Tier 标签，但有材料链接）===
    if not result["tiers"]:
        # 在合并后的全文中直接找材料链接（只匹配 /database/items/ 的链接，不匹配 /database/stations/）
        tier_data = {"tier_num": 1, "station_lv": 1, "time": "", "materials": []}

        # 找制作时间
        time_match = re.search(r'"children":"(\d+s \(\d+/min\))"', text)
        if time_match:
            tier_data["time"] = time_match.group(1)

        _extract_materials(text, tier_data)

        if tier_data["materials"]:
            result["tiers"].append(tier_data)

    return result if result["tiers"] else {}


def _extract_materials(text_segment, tier_data):
    """从文本片段中提取材料信息"""
    # NOTE: 实际 flight data 中 href 在 title 之前
    mat_pattern = r'"href":"(/database/items/[^"]+)"[^}]*?"title":"Click to view ([^"]+)"'
    mat_matches = list(re.finditer(mat_pattern, text_segment))

    mat_img_pattern = r'"src":"(/windrose-data/images/[^"]+)"'
    mat_imgs = re.findall(mat_img_pattern, text_segment)

    qty_pattern = r'\["×",(\d+)\]'
    qtys = re.findall(qty_pattern, text_segment)

    for j, mat_match in enumerate(mat_matches):
        mat_href = mat_match.group(1)
        mat_name = mat_match.group(2)
        mat_icon = mat_imgs[j] if j < len(mat_imgs) else ""
        mat_qty = int(qtys[j]) if j < len(qtys) else 1

        tier_data["materials"].append({
            "name": mat_name,
            "amount": mat_qty,
            "icon_url": mat_icon,
            "href": mat_href,
            "item_id": mat_href.split('/')[-1]
        })


def parse_item(html, item_id, url):
    """解析物品页面，提取所有字段"""
    if not html:
        return None
    soup = BeautifulSoup(html, 'html.parser')

    # 1. 名称
    name_tag = soup.find('h1')
    if not name_tag:
        return None
    name = name_tag.text.strip()

    # 2. 分类 & 稀有度（从徽章提取）
    badges = soup.select('.flex.gap-2.flex-wrap span')
    category = badges[0].text.strip() if len(badges) > 0 else "Unknown"
    rarity = badges[1].text.strip() if len(badges) > 1 else "Common"

    # 3. 概述（收集 Overview h2 后面的所有 p 和 blockquote）
    overview_parts = []
    overview_h2 = soup.find(lambda tag: tag.name == 'h2' and 'Overview' in tag.text)
    if overview_h2:
        next_tag = overview_h2.find_next_sibling()
        while next_tag and next_tag.name in ('p', 'blockquote'):
            text = next_tag.get_text(strip=True)
            if text:
                overview_parts.append(text)
            next_tag = next_tag.find_next_sibling()
    overview = "\n\n".join(overview_parts)

    # 3b. 属性数值（Attack / Level 从 dl.grid 解析）
    item_level = None
    item_attack = None
    stats_dl = soup.select_one('dl.grid.grid-cols-2')
    if stats_dl:
        for div in stats_dl.find_all('div', recursive=False):
            dt = div.find('dt')
            dd = div.find('dd')
            if dt and dd:
                label = dt.get_text(strip=True).lower()
                value = dd.get_text(strip=True)
                if label == 'level':
                    try:
                        item_level = int(value)
                    except ValueError:
                        pass
                elif label == 'attack':
                    try:
                        item_attack = int(value)
                    except ValueError:
                        pass

    # 4. 主图片
    img_tag = soup.find('img', alt=name)
    if not img_tag:
        flex1_imgs = soup.select('div.flex-1 img')
        img_tag = flex1_imgs[0] if flex1_imgs else None

    img_src = img_tag.get('src', '') if img_tag else ''
    icon_filename = f"{item_id}.webp"
    icon_path = download_image(img_src, icon_filename)

    # 5. 制作配方（从 flight data 解析）
    scripts = soup.find_all('script')
    crafting_raw = parse_crafting_from_flight_data(scripts)

    # 下载工作台图标
    station_icon_path = ""
    if crafting_raw.get("station_icon_url"):
        station_filename = crafting_raw.get("station", "station").lower().replace(" ", "-") + ".webp"
        station_icon_path = download_image(crafting_raw["station_icon_url"], station_filename)

    # 下载材料图标并构建最终 crafting 数据
    crafting = {}
    if crafting_raw.get("tiers"):
        crafting = {
            "station": crafting_raw.get("station", ""),
            "station_icon": station_icon_path,
            "tiers": []
        }
        for tier in crafting_raw["tiers"]:
            # 下载材料图标
            final_materials = []
            for mat in tier["materials"]:
                mat_icon_path = ""
                if mat.get("icon_url"):
                    mat_filename = f"{mat['item_id']}.webp"
                    mat_icon_path = download_image(mat["icon_url"], mat_filename)
                final_materials.append({
                    "name": mat["name"],
                    "amount": mat["amount"],
                    "icon": mat_icon_path,
                    "item_id": mat["item_id"]
                })

            tier_entry = {
                "level": tier["tier_num"],
                "name": f"Tier {tier['tier_num']}",
                "station": f"Station Lv {tier['station_lv']}" if tier["station_lv"] else "",
                "time": tier["time"],
                "materials": final_materials
            }
            crafting["tiers"].append(tier_entry)

    # 6. 构建完整的物品数据
    return {
        "id": item_id,
        "slug": url.replace('/database/items/', ''),
        "name": name,
        "category": category.lower().replace(' ', '-'),
        "tier": rarity.lower(),
        "level": item_level,
        "attack": item_attack,
        "description": overview,
        "icon": icon_path,
        "crafting": crafting,
        "status": "verified",
        "confidence": "verified"
    }


def main():
    global img_downloaded, img_skipped, img_failed

    print("=" * 60)
    print("Windrose 全量数据采集 v2")
    print("=" * 60)

    # 获取物品列表
    print("\n[1/3] 获取物品索引页...")
    html = fetch_page(f"{BASE_URL}/database/items/all")
    if not html:
        print("致命错误：无法获取索引页")
        return

    soup = BeautifulSoup(html, 'html.parser')
    item_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if any(prefix in href for prefix in ['eid-', 'did-', 'aid-', 'cid-']):
            if href not in item_links:
                item_links.append(href)

    total = len(item_links)
    print(f"  找到 {total} 个物品链接")

    # 逐批采集（每批 10 个并发，避免被封）
    print(f"\n[2/3] 开始采集 {total} 个物品...")
    results = []
    errors = []
    batch_size = 10

    for batch_start in range(0, total, batch_size):
        batch_end = min(batch_start + batch_size, total)
        batch_urls = item_links[batch_start:batch_end]

        with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
            future_to_url = {
                executor.submit(fetch_page, f"{BASE_URL}{url}"): url
                for url in batch_urls
            }
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                item_id = url.split('/')[-1]
                try:
                    page_html = future.result()
                    item_data = parse_item(page_html, item_id, url)
                    if item_data:
                        results.append(item_data)
                    else:
                        errors.append(f"{url}: 解析失败")
                except Exception as exc:
                    errors.append(f"{url}: {exc}")

        # 进度报告
        done = min(batch_end, total)
        pct = done / total * 100
        crafting_count = sum(1 for r in results if r.get('crafting', {}).get('tiers'))
        print(f"  进度: {done}/{total} ({pct:.0f}%) | 成功: {len(results)} | 有制作配方: {crafting_count} | 图片: +{img_downloaded} 跳过{img_skipped} 失败{img_failed}")

    # 保存结果
    print(f"\n[3/3] 保存数据...")
    output_path = DATA_DIR / 'scraped_items_v2.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"items": results}, f, indent=2, ensure_ascii=False)

    # 最终报告
    print(f"\n{'=' * 60}")
    print(f"采集完成报告")
    print(f"{'=' * 60}")
    print(f"总物品数: {total}")
    print(f"成功采集: {len(results)}")
    print(f"采集失败: {len(errors)}")
    print(f"有制作配方: {sum(1 for r in results if r.get('crafting', {}).get('tiers'))}")
    print(f"有描述: {sum(1 for r in results if r.get('description'))}")
    print(f"有图标: {sum(1 for r in results if r.get('icon'))}")
    print(f"图片下载: 新增{img_downloaded} 跳过{img_skipped} 失败{img_failed}")
    print(f"数据保存至: {output_path}")

    if errors:
        print(f"\n失败列表 (前 20 个):")
        for e in errors[:20]:
            print(f"  {e}")


if __name__ == '__main__':
    main()
