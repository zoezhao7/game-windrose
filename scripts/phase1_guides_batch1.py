"""阶段1: 生成3篇深度攻略 - mining-routes, boss-progression, best-early-builds"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from phase1_guides_hub import page_wrapper, write_page

ROOT = r"F:\aicode\gamedoc"

def mining_routes():
    body = """
<h1>Best Mining Routes in Windrose — Copper, Iron, Clay &amp; Sulfur (2026)</h1>
<p><strong>Mining is the backbone of progression in Windrose.</strong> Every tool upgrade, weapon, and ship component requires refined materials. This guide maps out the most efficient mining routes.</p>
<div class="quick-stats">
<div class="stat"><div class="stat-label">Resources</div><div class="stat-value">6 Types</div></div>
<div class="stat"><div class="stat-label">Biomes</div><div class="stat-value">3 Regions</div></div>
<div class="stat"><div class="stat-label">Run Time</div><div class="stat-value">15-20 min</div></div>
</div>

<section id="prep"><h2>1. Pre-Mining Checklist</h2>
<div class="table-responsive"><table><caption>Mining Loadout</caption>
<thead><tr><th>Item</th><th>Qty</th><th>Why</th></tr></thead><tbody>
<tr><td><strong>Best Pickaxe</strong></td><td>1</td><td>Higher tier = faster mining</td></tr>
<tr><td><strong>Torches</strong></td><td>3-5</td><td>Caves are dark</td></tr>
<tr><td><strong>Bandages</strong></td><td>10+</td><td>Cave enemies ambush you</td></tr>
<tr><td><strong>Food</strong></td><td>5+</td><td>Stack 2 food buffs for HP/stamina</td></tr>
<tr><td><strong>Weapon</strong></td><td>1</td><td>Clear enemies before mining</td></tr>
</tbody></table></div></section>

<section id="copper"><h2>2. Copper Route (Coastal Jungle)</h2>
<p>Copper Deposit Mines are marked with <strong>crossed-pickaxe icons</strong> on the map.</p>
<h3>Optimal Loop</h3><ol>
<li>Check map for pickaxe icons in Coastal Jungle</li>
<li>Clear cave of Drowned enemies first — lure one at a time</li>
<li>Place torches at intersections to prevent getting lost</li>
<li>Mine ALL Poor Copper Ore nodes (8-15 per cave)</li>
<li>Return via Fast Travel Bell</li>
<li>Smelt: <strong>6 Poor Copper Ore + 1 Charcoal = 1 Copper Ingot</strong></li>
</ol>
<h3>Tips</h3><ul>
<li>Ores <strong>respawn</strong> after 2-3 in-game days</li>
<li>Starting island has <strong>3-4 copper caves</strong></li>
<li>Watch for hidden nodes behind pillars</li>
</ul></section>

<section id="clay"><h2>3. Clay Farming (Starting Island)</h2>
<p>Clay is needed for Charcoal Kiln (25 Wood + 20 Clay) and Smelting Furnace (15 Clay + 30 Stone).</p>
<ul>
<li><strong>Riverbanks</strong> — Clay patches along both banks</li>
<li><strong>Coastal flats</strong> — Low beach areas</li>
<li>Mineable with <strong>Stone Pickaxe</strong></li>
<li>Need at least <strong>35 Clay</strong> for Kiln + Furnace</li>
</ul></section>

<section id="iron"><h2>4. Iron Route (Foothills)</h2>
<p>Iron requires <strong>Copper Pickaxe+</strong> and is in the <strong>Foothills</strong> region (ship required).</p>
<ol>
<li>Sail to Foothills island</li>
<li>Set up temporary outpost near deposits</li>
<li>Mine Iron Ore veins (darker, shinier rocks)</li>
<li>Smelt into Foothills Iron Ingots</li>
</ol>
<div class="update-note"><strong>Warning:</strong> Foothills has much tougher enemies. Bring full copper gear.</div></section>

<section id="sulfur"><h2>5. Sulfur &amp; Gunpowder</h2>
<h3>Looting (Early)</h3><ul>
<li><strong>Smuggler's Treasure</strong>: 10 Gunpowder + 4 Rum</li>
<li><strong>Pirate Camps</strong>: Gunpowder drops</li></ul>
<h3>Crafting (Mid-Late)</h3>
<p><strong>10 Sulfur + 20 Ash = 10 Gunpowder</strong> at Millstone. Ash from burning wood; Sulfur from Foothills with Iron Pickaxe.</p></section>

<section id="tips"><h2>6. Efficiency Tips</h2><ul>
<li>Place <strong>Fast Travel Bells</strong> at mining sites (10 Copper Ingot + 3 Rope)</li>
<li>Build temporary outposts near rich deposits</li>
<li>Stack two food buffs before every run</li>
<li>Right-click map to place markers, enable "Show on minimap"</li>
</ul></section>

<section id="faq"><h2>FAQ</h2>
<details><summary>Do mining nodes respawn?</summary><div class="faq-answer"><p>Yes, after 2-3 in-game days. Mark your best spots.</p></div></details>
<details><summary>Can I mine Iron with Stone Pickaxe?</summary><div class="faq-answer"><p><strong>No.</strong> Iron requires Copper Pickaxe minimum.</p></div></details>
</section>

<aside class="related-guides"><h2>Related Guides</h2><ul>
<li><a href="/resources/copper/">Copper Ore Guide</a></li>
<li><a href="/resources/iron/">Iron Ore Guide</a></li>
<li><a href="/resources/gunpowder/">Gunpowder Guide</a></li>
<li><a href="/guides/crafting-progression/">Crafting Progression</a></li>
</ul></aside>"""
    return page_wrapper(
        "Best Mining Routes in Windrose (2026) | Windrose Guides",
        "Optimized mining routes for Copper, Iron, Clay, Sulfur in Windrose.",
        "https://windrose-guides.com/guides/mining-routes", "../../css/style.css",
        [("Home","/"),("Guides","/guides/"),("Mining Routes",None)], body, "/guides")

def boss_progression():
    body = """
<h1>Boss Progression &amp; Strategy Guide — Windrose (2026)</h1>
<p>Windrose features <strong>Soulslite</strong> boss encounters inspired by real historical pirates with supernatural powers. This guide covers the known boss progression order, preparation, and combat strategies.</p>
<div class="quick-stats">
<div class="stat"><div class="stat-label">Known Bosses</div><div class="stat-value">5+</div></div>
<div class="stat"><div class="stat-label">Combat Style</div><div class="stat-value">Soulslite</div></div>
<div class="stat"><div class="stat-label">Status</div><div class="stat-value">Early Access</div></div>
</div>
<div class="update-note"><strong>Early Access:</strong> Boss data is from community sources. Some details may change with patches. Unconfirmed info is marked.</div>

<section id="order"><h2>1. Boss Progression Order</h2>
<div class="table-responsive"><table><caption>Known Boss Encounters</caption>
<thead><tr><th>#</th><th>Boss</th><th>Region</th><th>Rec. Level</th><th>Status</th></tr></thead><tbody>
<tr><td>1</td><td><strong>Thomas Richards</strong></td><td>Coastal Jungle</td><td>~10</td><td>Verified</td></tr>
<tr><td>2</td><td><strong>Israel Hands</strong></td><td>Foothills</td><td>~20</td><td>Community</td></tr>
<tr><td>3</td><td><strong>High Priestess</strong></td><td>Deep Jungle</td><td>~30</td><td>Community</td></tr>
<tr><td>4</td><td><strong>Ghost Captain</strong></td><td>Open Sea</td><td>~35+</td><td>Unconfirmed</td></tr>
<tr><td>5</td><td><strong>Charon's Obols</strong></td><td>Needs verification</td><td>Unknown</td><td>Legacy/Unconfirmed</td></tr>
</tbody></table></div></section>

<section id="general"><h2>2. General Boss Combat Tips</h2>
<ul>
<li><strong>Always eat 2 foods</strong> — Stack two food buffs for max HP/stamina</li>
<li><strong>Learn Perfect Block</strong> — Tap block at exact strike moment for 0 damage + stagger</li>
<li><strong>Dodge > Block</strong> for multi-hit combos — i-frames on Ctrl dodge</li>
<li><strong>Enemies don't regen</strong> — Hit-and-run is valid. Retreat, heal, return</li>
<li><strong>Bring 15+ Bandages</strong> and cooked food</li>
<li><strong>Lock-On (T)</strong> — Enable auto-lock in settings</li>
<li><strong>Safe pattern:</strong> 1-2 hits → dodge back → wait → punish</li>
</ul></section>

<section id="thomas"><h2>3. Thomas Richards (Boss 1)</h2>
<div class="quick-stats">
<div class="stat"><div class="stat-label">Region</div><div class="stat-value">Coastal Jungle</div></div>
<div class="stat"><div class="stat-label">Level</div><div class="stat-value">~10</div></div>
<div class="stat"><div class="stat-label">Confidence</div><div class="stat-value">Verified</div></div>
</div>
<h3>Preparation</h3><ul>
<li>Full Copper weapons and armor</li>
<li>10+ Bandages, 2 food buffs active</li>
<li>Melee weapon with good reach (Saber recommended)</li></ul>
<h3>Strategy</h3>
<p>Thomas Richards is your first real test. He uses sweeping melee attacks with moderate wind-up. The key is patience — wait for his combo to end, then punish with 2-3 hits before dodging away. Perfect Block his overhead slam for a massive counter window.</p>
<h3>Drops</h3><p>Progression unlock + equipment materials. Specific drops need verification.</p></section>

<section id="israel"><h2>4. Israel Hands (Boss 2)</h2>
<div class="quick-stats">
<div class="stat"><div class="stat-label">Region</div><div class="stat-value">Foothills</div></div>
<div class="stat"><div class="stat-label">Level</div><div class="stat-value">~20</div></div>
<div class="stat"><div class="stat-label">Confidence</div><div class="stat-value">Community</div></div>
</div>
<p>Israel Hands is a more aggressive boss with faster attack chains. He punishes passive play. You need to learn his tells and be ready to dodge multiple times in succession.</p>
<h3>Tips</h3><ul>
<li>Upgrade to Iron-tier weapons before attempting</li>
<li>His attack chains are 3-4 hits — don't attack until the full combo ends</li>
<li>Ranged weapons can help chip damage from distance</li>
</ul></section>

<section id="faq"><h2>FAQ</h2>
<details><summary>What order should I fight bosses?</summary><div class="faq-answer"><p>Follow the story progression: Thomas Richards → Israel Hands → High Priestess → later bosses. Each boss gates access to new regions and recipes.</p></div></details>
<details><summary>Can I skip bosses?</summary><div class="faq-answer"><p>Some bosses may be optional, but main progression bosses must be defeated to unlock new areas.</p></div></details>
<details><summary>Do bosses scale with co-op players?</summary><div class="faq-answer"><p>Needs verification. Community reports suggest boss HP increases with more players.</p></div></details>
</section>

<aside class="related-guides"><h2>Related Guides</h2><ul>
<li><a href="/bosses/">Boss Database — All Known Encounters</a></li>
<li><a href="/guides/best-early-builds/">Best Early Builds for Boss Fights</a></li>
<li><a href="/weapons/">Weapons & Armor Database</a></li>
<li><a href="/guides/coop-multiplayer/">Co-op Boss Strategies</a></li>
</ul></aside>"""
    return page_wrapper(
        "Boss Progression & Strategy Guide — Windrose (2026) | Windrose Guides",
        "Phase-by-phase boss strategies, progression order, and combat tips for Windrose.",
        "https://windrose-guides.com/guides/boss-progression", "../../css/style.css",
        [("Home","/"),("Guides","/guides/"),("Boss Progression",None)], body, "/guides")

def best_early_builds():
    body = """
<h1>Best Early-Game Builds in Windrose (2026)</h1>
<p>Your stat and talent choices in the first 20 hours shape your entire Windrose experience. This guide covers optimal early builds for DPS, Tank, and Balanced playstyles, including talent priorities and gear progression.</p>
<div class="quick-stats">
<div class="stat"><div class="stat-label">Builds</div><div class="stat-value">3 Archetypes</div></div>
<div class="stat"><div class="stat-label">Respec</div><div class="stat-value">Free Anytime</div></div>
<div class="stat"><div class="stat-label">Food Buffs</div><div class="stat-value">2 Max Stack</div></div>
</div>

<section id="system"><h2>1. Stat & Talent System Overview</h2>
<p>Press <strong>D</strong> to open Progression/Talents. Key points:</p>
<ul>
<li><strong>Respec is free</strong> — Experiment without fear</li>
<li><strong>Stats</strong> increase base attributes (HP, Stamina, Damage)</li>
<li><strong>Talents</strong> unlock passive bonuses in specialized trees</li>
<li><strong>Food buffs</strong> are the primary way to boost stats — always have 2 active</li>
<li>XP comes from <strong>clearing POIs and quests</strong>, not killing enemies</li>
</ul></section>

<section id="dps"><h2>2. DPS Build — Maximum Damage</h2>
<div class="table-responsive"><table><caption>DPS Build Stats (Level 15)</caption>
<thead><tr><th>Stat</th><th>Priority</th><th>Why</th></tr></thead><tbody>
<tr><td><strong>Strength</strong></td><td>⭐⭐⭐</td><td>Melee damage scaling</td></tr>
<tr><td><strong>Dexterity</strong></td><td>⭐⭐</td><td>Attack speed + ranged damage</td></tr>
<tr><td><strong>Stamina</strong></td><td>⭐⭐</td><td>More attacks per window</td></tr>
<tr><td><strong>Constitution</strong></td><td>⭐</td><td>Minimal — rely on dodging</td></tr>
</tbody></table></div>
<h3>Recommended Gear</h3><ul>
<li><strong>Weapon:</strong> Saber (fast, good reach) or Rapier (highest DPS)</li>
<li><strong>Armor:</strong> Light armor for dodge speed</li>
<li><strong>Food:</strong> Damage-boosting foods</li></ul>
<h3>Playstyle</h3>
<p>Aggressive. Sprint attack → 2-3 light attacks → dodge out. Perfect Block for massive counter windows. Glass cannon — one mistake hurts.</p></section>

<section id="tank"><h2>3. Tank Build — Maximum Survival</h2>
<div class="table-responsive"><table><caption>Tank Build Stats (Level 15)</caption>
<thead><tr><th>Stat</th><th>Priority</th><th>Why</th></tr></thead><tbody>
<tr><td><strong>Constitution</strong></td><td>⭐⭐⭐</td><td>Maximum HP</td></tr>
<tr><td><strong>Stamina</strong></td><td>⭐⭐⭐</td><td>Block more, dodge more</td></tr>
<tr><td><strong>Strength</strong></td><td>⭐⭐</td><td>Moderate damage</td></tr>
<tr><td><strong>Dexterity</strong></td><td>⭐</td><td>Not needed</td></tr>
</tbody></table></div>
<h3>Recommended Gear</h3><ul>
<li><strong>Weapon:</strong> Club (high stagger) or Shield + Sword</li>
<li><strong>Armor:</strong> Heavy armor — maximum defense</li>
<li><strong>Food:</strong> HP and stamina foods</li></ul>
<h3>Playstyle</h3>
<p>Patient. Block → Perfect Block for staggers → heavy attack punish. Best for co-op as you draw aggro while DPS deals damage.</p></section>

<section id="balanced"><h2>4. Balanced Build — Best for Solo</h2>
<p>Split stats evenly between Constitution, Strength, and Stamina. Use medium armor. This is the safest choice for solo play and new players. Invest in <strong>Toughguy tree</strong> talents first for survival, then branch into damage.</p></section>

<section id="talents"><h2>5. Talent Priority</h2>
<div class="table-responsive"><table>
<thead><tr><th>Phase</th><th>Tree</th><th>Focus</th></tr></thead><tbody>
<tr><td>Levels 1-10</td><td><strong>Toughguy</strong></td><td>HP, stamina regen, damage reduction</td></tr>
<tr><td>Levels 10-20</td><td><strong>Your archetype</strong></td><td>DPS or Tank specialization</td></tr>
<tr><td>Levels 20+</td><td><strong>Mix</strong></td><td>Quality of life + combat efficiency</td></tr>
</tbody></table></div></section>

<section id="faq"><h2>FAQ</h2>
<details><summary>Can I respec for free?</summary><div class="faq-answer"><p><strong>Yes!</strong> Respecs are completely free at any time. Experiment freely.</p></div></details>
<details><summary>What's the best solo build?</summary><div class="faq-answer"><p>Balanced build with Toughguy talents. Survival > damage for solo play.</p></div></details>
</section>

<aside class="related-guides"><h2>Related Guides</h2><ul>
<li><a href="/builds/">All Build Configurations</a></li>
<li><a href="/weapons/">Weapons & Armor Database</a></li>
<li><a href="/guides/boss-progression/">Boss Progression Guide</a></li>
<li><a href="/beginner-guide/">Beginner Guide</a></li>
</ul></aside>"""
    return page_wrapper(
        "Best Early-Game Builds in Windrose (2026) | Windrose Guides",
        "Optimal stat allocation, talent priorities, and gear for DPS, Tank, and Balanced builds in Windrose.",
        "https://windrose-guides.com/guides/best-early-builds", "../../css/style.css",
        [("Home","/"),("Guides","/guides/"),("Best Early Builds",None)], body, "/guides")

if __name__ == "__main__":
    print("=== Phase 1 Batch 1: 3 Guide Articles ===")
    write_page("guides/mining-routes/index.html", mining_routes())
    write_page("guides/boss-progression/index.html", boss_progression())
    write_page("guides/best-early-builds/index.html", best_early_builds())
    print("Done! 3 guides generated.")
