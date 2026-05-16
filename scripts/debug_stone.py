"""Debug Stone Bullet crafting parse"""
import sys
sys.path.insert(0, '.')
from scripts.scrape_competitor import fetch_page, parse_crafting_from_flight_data, BASE_URL
from bs4 import BeautifulSoup

url = f"{BASE_URL}/database/items/aid-ammo-firearm-projectile-stone-bullet-t01"
html = fetch_page(url)
soup = BeautifulSoup(html, 'html.parser')
scripts = soup.find_all('script')

result = parse_crafting_from_flight_data(scripts)
print(f"Result: {result}")
print(f"Station: {result.get('station', 'NONE')}")
print(f"Tiers: {result.get('tiers', [])}")
