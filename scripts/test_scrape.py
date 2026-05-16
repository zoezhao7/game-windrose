import requests
from bs4 import BeautifulSoup
res = requests.get('https://windrosewiki.org/database/items/eid-melee-weapon-saber-blank-base')
soup = BeautifulSoup(res.text, 'html.parser')
name = soup.find('h1')
level = soup.find(string=lambda t: t and 'Level' in t)
print('Name:', name.text if name else None)
print('Level:', level.parent.text if level and level.parent else None)
badges = soup.select('.flex.gap-2.flex-wrap span')
print('Badges:', [b.text for b in badges])
img = soup.find('img')
print('Image:', img['src'] if img else None)
