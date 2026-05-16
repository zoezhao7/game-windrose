import os

PROJECT_DIR = r"f:\aicode\gamedoc"

# 1. Update README.md
readme_path = os.path.join(PROJECT_DIR, "README.md")
with open(readme_path, "r", encoding="utf-8") as f:
    readme_content = f.read()

if "windrose.tools" not in readme_content:
    readme_content += "\n## 竞品参考与数据来源 (Competitors)\n"
    readme_content += "- windrose.tools\n"
    readme_content += "- gaming.tools\n"
    readme_content += "- windrosegame.net\n"
    readme_content += "- windrosewiki.org\n"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

# Boss Data
bosses_data = {
    "thomas-richards": {
        "title": "Thomas Richards Boss Guide: Strategy, Tips & Drops (2026)",
        "content": """
            <h2>Boss Overview</h2>
            <p><strong>Thomas Richards</strong> is the first major boss encounter in Windrose. You face him at the conclusion of the main questline titled <strong>"Revenge is Best Served Cold"</strong> in the Coastal Jungle biome. To access his camp, you must collect four Black Marks from pirate guards located in Blackbear Outposts.</p>
            
            <h2>Preparation Strategy</h2>
            <ul>
                <li><strong>Gear Level:</strong> Upgrade weapons and all 5 pieces of armor to Level 5.</li>
                <li><strong>Buffs:</strong> Consume food like Bacon and Eggs or Coconut Milk with Bananas. Ensure the "Rested" buff is active.</li>
            </ul>

            <h2>Combat Tactics</h2>
            <p>This boss is a significant difficulty spike. He uses a multi-hit melee combo, throws explosive grenades, and has an unblockable grab attack signaled by a red flash.</p>
            <ul>
                <li><strong>Stagger System:</strong> He has a posture bar (shields). Break this using heavy attacks to open a window for free damage.</li>
                <li><strong>Patience is Key:</strong> Do not get greedy. Wait for his combo to end, land 1-2 hits, and retreat.</li>
                <li><strong>Ranged Alternative:</strong> Using a Blunderbuss to kite him and aim for headshots is a highly effective strategy.</li>
            </ul>

            <h2>Drops & Rewards</h2>
            <ul>
                <li>50 Experience Points</li>
                <li>Thomas Richards' Journal</li>
                <li>Seafood Platter</li>
                <li>Silver Ingot</li>
            </ul>
        """
    },
    "israel-hands": {
        "title": "Israel Hands Boss Guide: Strategy & Drops (2026)",
        "content": """
            <h2>Boss Overview</h2>
            <p><strong>Israel Hands</strong> is the second major boss found at the end of the "Needle in a Haystack" quest in the Foothills. His defeat unlocks access to the Cursed Swamps biome and iron-tier crafting schematics.</p>
            
            <h2>Preparation Strategy</h2>
            <ul>
                <li><strong>Gear Level:</strong> Ensure your primary weapon, firearm, and armor are Level 10.</li>
                <li><strong>Weapons:</strong> The <strong>Rapier of a Thousand Cuts</strong> is highly recommended for bleed damage. Firearms help maintain distance.</li>
                <li><strong>Utility:</strong> Place a Tent outside the boss arena as a respawn point.</li>
            </ul>

            <h2>Combat Tactics</h2>
            <p>Israel Hands punishes greedy play with hyper-armor counter-attacks.</p>
            <ul>
                <li><strong>Sword Combos:</strong> Perfect Block his 1-3 hit saber swings to break his poise, then counter with heavy attacks.</li>
                <li><strong>Spectral Charge:</strong> An unblockable attack glowing red. Dodge sideways immediately.</li>
                <li><strong>Soul Barrage:</strong> He floats and rains down souls. Sprint in a wide circle to evade.</li>
                <li><strong>Poison Lunge:</strong> He crouches and dashes. Dodge sideways, never backward.</li>
            </ul>

            <h2>Drops & Rewards</h2>
            <ul>
                <li><strong>Soul Eater:</strong> Epic-tier two-handed greatsword with life-drain.</li>
                <li>Charon's Obol</li>
                <li>30 Undead Essence</li>
                <li>50 Experience Points</li>
            </ul>
        """
    },
    "high-priestess": {
        "title": "High Priestess Boss Guide: Strategy & Weak Points (2026)",
        "content": """
            <h2>Boss Overview</h2>
            <p>The <strong>High Priestess</strong> is a late-game boss in the Cursed Swamps. This fight is a mechanical encounter focused on destroying weak points rather than a pure DPS race.</p>
            
            <h2>Combat Tactics</h2>
            <p>The core loop involves targeting her glowing, yellow pustules on her back and sides.</p>
            <ul>
                <li><strong>Weak Points:</strong> Use shotguns like the Dragon's Breath or pistols like Drake's Double-Barreled Pistol to hit multiple pustules.</li>
                <li><strong>Stagger Window:</strong> Breaking pustules depletes her poise. Once staggered, her mouth opens. <strong>Focus all damage on her mouth</strong> for guaranteed critical strikes.</li>
                <li><strong>Add Management:</strong> She periodically summons Plague Thralls. Kill them quickly.</li>
                <li><strong>Melee Bonus:</strong> Crude weapons, specifically maces and halberds, deal a flat damage bonus against her.</li>
            </ul>

            <h2>Drops & Rewards</h2>
            <ul>
                <li><strong>Charon's Obol</strong> (Required Quest Item)</li>
                <li>10x Tear of Sorrow</li>
            </ul>
        """
    },
    "ghost-captain": {
        "title": "Ghost Captain Boss Guide: Strategy & Drops (2026)",
        "content": """
            <h2>Boss Overview</h2>
            <p>The <strong>Ghost Captain</strong> is a challenging optional boss found within the Temple Dungeon. He represents a significant difficulty spike.</p>
            
            <h2>Preparation Strategy</h2>
            <ul>
                <li><strong>Recommended Level:</strong> 10-12.</li>
                <li><strong>Weapons:</strong> Fast weapons like the <strong>Saber</strong> or <strong>Rapier</strong> are highly recommended to exploit short punish windows safely.</li>
                <li><strong>Supplies:</strong> Bring 15+ portions of high-quality healing food.</li>
            </ul>

            <h2>Combat Tactics</h2>
            <ul>
                <li><strong>Stamina Management:</strong> Avoid exhausting your stamina completely. Being "winded" prevents dodging, which is fatal in this fight.</li>
                <li><strong>Ghostly Combos:</strong> He uses a 3-swing combo followed by a brief pause. Attack 1-2 times during the pause and disengage.</li>
                <li><strong>Grab Attack:</strong> His most dangerous move (telegraphed by a flash), dealing ~50% health damage. Prioritize evasion over parrying for his spectral attacks.</li>
            </ul>

            <h2>Drops & Rewards</h2>
            <ul>
                <li><strong>Soul Eater:</strong> Epic two-handed greatsword with a special life-drain attack (scales with Strength/Vitality).</li>
                <li><strong>Arboris Saber:</strong> Potential rare drop.</li>
            </ul>
        """
    }
}

for boss_id, data in bosses_data.items():
    boss_path = os.path.join(PROJECT_DIR, "bosses", boss_id, "index.html")
    if os.path.exists(boss_path):
        with open(boss_path, "r", encoding="utf-8") as f:
            html = f.read()
        
        # Replace title
        import re
        html = re.sub(r'<title>.*?</title>', f'<title>{data["title"]} | Windrose Guides</title>', html)
        html = re.sub(r'<h1>.*?</h1>', f'<h1>{data["title"]}</h1>', html)
        
        # Replace content area
        # Find the <div class="card"...> up to <h2>FAQ</h2> and replace it
        start_tag = '<div class="card" style="margin:1.5rem 0;text-align:center;padding:2rem;">'
        if start_tag in html:
            start_idx = html.find(start_tag)
            end_idx = html.find('<h2>FAQ</h2>', start_idx)
            if end_idx != -1:
                new_html = html[:start_idx] + data["content"] + "\n            " + html[end_idx:]
                with open(boss_path, "w", encoding="utf-8") as f:
                    f.write(new_html)
                print(f"Updated {boss_id}")
            else:
                print(f"Could not find FAQ section in {boss_id}")
        else:
            print(f"Could not find start tag in {boss_id}")
