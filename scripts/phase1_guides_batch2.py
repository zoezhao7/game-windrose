"""阶段1: 生成4篇深度攻略 - crafting, sailing, coop, naval"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from phase1_guides_hub import page_wrapper, write_page

def crafting_progression():
    body = """
<h1>Crafting Progression Path — Windrose (2026)</h1>
<p>Knowing <strong>what to craft and when</strong> separates efficient players from those stuck grinding. This guide maps the optimal crafting order from Day 1 to endgame.</p>
<div class="quick-stats">
<div class="stat"><div class="stat-label">Workbench Levels</div><div class="stat-value">3 Tiers</div></div>
<div class="stat"><div class="stat-label">Stations</div><div class="stat-value">6+ Types</div></div>
<div class="stat"><div class="stat-label">Recipes</div><div class="stat-value">100+</div></div>
</div>

<section><h2>1. Crafting Station Build Order</h2>
<div class="table-responsive"><table><caption>Optimal Station Progression</caption>
<thead><tr><th>Order</th><th>Station</th><th>Materials</th><th>Unlocks</th></tr></thead><tbody>
<tr><td>1</td><td><strong>Bonfire</strong></td><td>5 Wood</td><td>Light, warmth, Ash production</td></tr>
<tr><td>2</td><td><strong>Workbench Lv1</strong></td><td>5 Wood</td><td>Basic tools, rope, fabric</td></tr>
<tr><td>3</td><td><strong>Cooking Fire</strong></td><td>3 Wood + 3 Stone</td><td>Cooked food for buffs</td></tr>
<tr><td>4</td><td><strong>Charcoal Kiln</strong></td><td>25 Wood + 20 Clay</td><td>Charcoal for smelting</td></tr>
<tr><td>5</td><td><strong>Smelting Furnace</strong></td><td>15 Clay + 30 Stone</td><td>Metal ingots</td></tr>
<tr><td>6</td><td><strong>Armor Workshop</strong></td><td>Rough Hide</td><td>Armor crafting (needs roof!)</td></tr>
<tr><td>7</td><td><strong>Weaponsmith</strong></td><td>10 Wood + 5 Copper Ingot</td><td>Melee weapons (needs roof!)</td></tr>
</tbody></table></div></section>

<section><h2>2. Workbench Upgrade Path</h2>
<h3>Lv1 → Lv2: Build a Sawhorse</h3>
<p><strong>20 Wood + 10 Copper Ingot</strong> — Place near Workbench within Bonfire radius.</p>
<h3>Lv2 → Lv3: Build a Toolbox</h3>
<p><strong>10 Wood + 20 Nails + 5 Foothills Iron Ingot</strong> — Place near Workbench.</p>
<div class="update-note"><strong>Key:</strong> Some recipes only appear after picking up their materials for the first time.</div></section>

<section><h2>3. Priority Crafting Checklist</h2>
<h3>First Hour</h3><ul>
<li>✅ Stone Pickaxe (3 Stone + 3 Wood)</li>
<li>✅ Torn Sailcloth Bag (2 Coarse Fabric + 1 Rope)</li>
<li>✅ Bandages ×10 (1 Coarse Fabric each)</li>
<li>✅ Tent (4 Wood + 10 Plant Fiber)</li></ul>
<h3>Hours 2-5</h3><ul>
<li>✅ Charcoal Kiln → Smelting Furnace</li>
<li>✅ Copper Pickaxe, Copper Axe</li>
<li>✅ Armor Workshop + first armor</li>
<li>✅ Weaponsmith + Saber/Rapier</li></ul>
<h3>Hours 5-15</h3><ul>
<li>✅ Sawhorse (Workbench Lv2)</li>
<li>✅ Sailor Backpack</li>
<li>✅ Fast Travel Bell</li>
<li>✅ Iron-tier gear after reaching Foothills</li></ul></section>

<section id="faq"><h2>FAQ</h2>
<details><summary>What should I craft first?</summary><div class="faq-answer"><p>Bonfire → Workbench → Stone Pickaxe → Torn Sailcloth Bag → Bandages → Cooking Fire → Tent.</p></div></details>
<details><summary>Why can't I see certain recipes?</summary><div class="faq-answer"><p>Some recipes require you to <strong>pick up the material first</strong>. Explore and collect new resources to unlock hidden recipes.</p></div></details>
</section>

<aside class="related-guides"><h2>Related</h2><ul>
<li><a href="/crafting/">Full Crafting Database</a></li>
<li><a href="/crafting/workbench/">Workbench Recipes Lv1-3</a></li>
<li><a href="/guides/mining-routes/">Mining Routes</a></li>
<li><a href="/beginner-guide/">Beginner Guide</a></li>
</ul></aside>"""
    return page_wrapper(
        "Crafting Progression Path — Windrose (2026) | Windrose Guides",
        "Optimal crafting order from Day 1 to endgame in Windrose. Station build order, workbench upgrades, priority checklist.",
        "https://windrosewiki.games/guides/crafting-progression", "../../css/style.css",
        [("Home","/"),("Guides","/guides/"),("Crafting Progression",None)], body, "/guides")

def sailing_navigation():
    body = """
<h1>Sailing &amp; Navigation Mastery — Windrose (2026)</h1>
<p>The open sea is both your highway and your battlefield in Windrose. Master sailing mechanics to travel efficiently and survive naval encounters.</p>
<div class="quick-stats">
<div class="stat"><div class="stat-label">Ship Types</div><div class="stat-value">3 + Variants</div></div>
<div class="stat"><div class="stat-label">Max Crew</div><div class="stat-value">Up to 10</div></div>
<div class="stat"><div class="stat-label">Sea Shanties</div><div class="stat-value">Yes!</div></div>
</div>

<section><h2>1. Wind &amp; Sailing Basics</h2><ul>
<li><strong>Wind direction matters</strong> — Sailing with the wind is fastest; against it is very slow</li>
<li><strong>Adjust sails</strong> to catch wind optimally</li>
<li><strong>Watch the wind indicator</strong> on screen</li>
<li><strong>Zigzag (tacking)</strong> when sailing into headwinds</li>
</ul></section>

<section><h2>2. Ship Types</h2>
<div class="table-responsive"><table>
<thead><tr><th>Ship</th><th>Size</th><th>Speed</th><th>Cannons</th><th>Best For</th></tr></thead><tbody>
<tr><td><strong>Ketch</strong></td><td>Small</td><td>Fast</td><td>Few</td><td>Solo / exploration</td></tr>
<tr><td><strong>Brigantine</strong></td><td>Medium</td><td>Moderate</td><td>Medium</td><td>Balanced / 2-4 players</td></tr>
<tr><td><strong>Frigate</strong></td><td>Large</td><td>Slow</td><td>Many</td><td>Naval combat / groups</td></tr>
</tbody></table></div>
<p>Each ship has <strong>3 variants</strong>: Stock, Brethren, and Blackbeard — with different cannon/cargo capacities.</p></section>

<section><h2>3. Navigation Tips</h2><ul>
<li><strong>Mark your base</strong> on the map before sailing — it's easy to get lost</li>
<li><strong>Explore coastlines first</strong> before venturing into open water</li>
<li><strong>Keep repair materials</strong> on the ship (Wood, Nails)</li>
<li><strong>Anchor near shore</strong> — don't leave your ship in deep water</li>
<li><strong>Sea Shanties</strong> provide crew buffs — play them!</li>
</ul></section>

<section><h2>4. Ocean Encounters</h2>
<p>The sea is dangerous. You may encounter:</p><ul>
<li><strong>Pirate ships</strong> — Naval combat or flee</li>
<li><strong>Storms</strong> — Reduce visibility and damage your ship</li>
<li><strong>Sea creatures</strong> — Some attack ships</li>
</ul>
<p>Always carry <strong>bandages, food, and ship repair mats</strong> when sailing.</p></section>

<section id="faq"><h2>FAQ</h2>
<details><summary>How do I get my first ship?</summary><div class="faq-answer"><p>Complete the starting island quest chain: build Weaponsmith → craft melee weapon → receive free ship.</p></div></details>
<details><summary>Can my ship sink permanently?</summary><div class="faq-answer"><p>Ships can be destroyed but can be rebuilt. Keep repair materials on hand.</p></div></details>
</section>

<aside class="related-guides"><h2>Related</h2><ul>
<li><a href="/ships/">Ship Database</a></li>
<li><a href="/guides/ship-building-naval-combat/">Naval Combat Guide</a></li>
<li><a href="/guides/coop-multiplayer/">Co-op Guide</a></li>
</ul></aside>"""
    return page_wrapper(
        "Sailing & Navigation Mastery — Windrose (2026) | Windrose Guides",
        "Wind mechanics, ship types, navigation tips, and ocean survival in Windrose.",
        "https://windrosewiki.games/guides/sailing-navigation", "../../css/style.css",
        [("Home","/"),("Guides","/guides/"),("Sailing & Navigation",None)], body, "/guides")

def coop_multiplayer():
    body = """
<h1>Co-op &amp; Multiplayer Guide — Windrose (2026)</h1>
<p>Windrose supports <strong>up to 10 players</strong> (recommended 2-4). This guide covers everything from server setup to crew coordination during boss fights and naval combat.</p>
<div class="quick-stats">
<div class="stat"><div class="stat-label">Max Players</div><div class="stat-value">10</div></div>
<div class="stat"><div class="stat-label">Recommended</div><div class="stat-value">2-4</div></div>
<div class="stat"><div class="stat-label">Server</div><div class="stat-value">Dedicated Available</div></div>
</div>

<section><h2>1. Server Setup Options</h2><ul>
<li><strong>Host & Play</strong> — One player hosts, others join. Simplest setup</li>
<li><strong>Dedicated Server</strong> — Runs 24/7, players join anytime. See <a href="/server-guide/">Server Guide</a></li>
<li><strong>5-8 players</strong> may see performance issues</li>
<li><strong>10 players</strong> is experimental</li>
</ul></section>

<section><h2>2. Role Specialization</h2>
<div class="table-responsive"><table>
<thead><tr><th>Role</th><th>Focus</th><th>Build</th></tr></thead><tbody>
<tr><td><strong>Tank</strong></td><td>Draw aggro, block</td><td>Constitution + Heavy Armor</td></tr>
<tr><td><strong>DPS</strong></td><td>Damage dealing</td><td>Strength + Light Armor</td></tr>
<tr><td><strong>Gatherer</strong></td><td>Resource farming</td><td>Stamina + Carry capacity</td></tr>
<tr><td><strong>Builder</strong></td><td>Base/ship construction</td><td>Flexible</td></tr>
</tbody></table></div></section>

<section><h2>3. Naval Combat Crew Roles</h2><ul>
<li><strong>Captain</strong> — Steering, navigation, calling targets</li>
<li><strong>Gunner(s)</strong> — Manning cannons, timing shots</li>
<li><strong>Boarder</strong> — Jumping to enemy ships for melee</li>
<li><strong>Repair crew</strong> — Patching holes during combat</li>
</ul></section>

<section><h2>4. Co-op Boss Tips</h2><ul>
<li><strong>Tank draws aggro</strong>, DPS attacks from behind</li>
<li><strong>Stagger healing</strong> — Don't all heal at once</li>
<li>Boss HP may scale with player count (needs verification)</li>
<li><strong>Revive downed allies</strong> before they bleed out</li>
</ul></section>

<section><h2>5. Shared Progression</h2><ul>
<li>Resources in shared chests are accessible to all</li>
<li>XP is individual — clear POIs together for mutual benefit</li>
<li>Builds can be dismantled by any crew member</li>
<li><strong>Designate a shared storage area</strong> at your main base</li>
</ul></section>

<aside class="related-guides"><h2>Related</h2><ul>
<li><a href="/server-guide/">Dedicated Server Guide</a></li>
<li><a href="/guides/boss-progression/">Boss Strategies</a></li>
<li><a href="/guides/ship-building-naval-combat/">Naval Combat</a></li>
<li><a href="/builds/">Build Configurations</a></li>
</ul></aside>"""
    return page_wrapper(
        "Co-op & Multiplayer Guide — Windrose (2026) | Windrose Guides",
        "Server setup, role specialization, crew coordination, and co-op tips for Windrose multiplayer.",
        "https://windrosewiki.games/guides/coop-multiplayer", "../../css/style.css",
        [("Home","/"),("Guides","/guides/"),("Co-op Guide",None)], body, "/guides")

def naval_combat():
    body = """
<h1>Ship Building &amp; Naval Combat — Windrose (2026)</h1>
<p>Ships are your lifeline in Windrose. This guide covers everything from building your first vessel to dominating naval battles.</p>
<div class="quick-stats">
<div class="stat"><div class="stat-label">Ships</div><div class="stat-value">3 Types</div></div>
<div class="stat"><div class="stat-label">Variants</div><div class="stat-value">3 Each</div></div>
<div class="stat"><div class="stat-label">Combat</div><div class="stat-value">Cannons + Boarding</div></div>
</div>

<section><h2>1. Ship Acquisition</h2>
<p>Your <strong>first ship is free</strong> — complete the starting island quest chain. Subsequent ships are purchased from the <strong>Wharf</strong> using Piastres and require specific Reputation levels.</p>
<div class="table-responsive"><table>
<thead><tr><th>Ship</th><th>Unlock</th><th>Cost</th></tr></thead><tbody>
<tr><td><strong>Ketch</strong></td><td>Quest reward</td><td>Free</td></tr>
<tr><td><strong>Brigantine</strong></td><td>Reputation Lv2</td><td>Piastres (varies)</td></tr>
<tr><td><strong>Frigate</strong></td><td>Reputation Lv3+</td><td>Piastres (expensive)</td></tr>
</tbody></table></div></section>

<section><h2>2. Ship Customization</h2><ul>
<li><strong>Cannons</strong> — Place on gun ports, different types available</li>
<li><strong>Cargo hold</strong> — Upgrade capacity for longer voyages</li>
<li><strong>Sails</strong> — Affect speed and maneuverability</li>
<li><strong>Hull upgrades</strong> — More HP for combat</li>
<li><strong>Crew stations</strong> — Hire NPC crew members</li>
</ul></section>

<section><h2>3. Naval Combat Tactics</h2>
<h3>Engagement</h3><ol>
<li>Approach enemy ships at an <strong>angle</strong> — broadside for max cannon fire</li>
<li>Fire cannons in <strong>volleys</strong> — time shots to hit the hull</li>
<li>After weakening, <strong>board</strong> the enemy ship for melee combat</li>
<li><strong>Repair during lulls</strong> — carry Wood and Nails</li>
</ol>
<h3>Defensive Tips</h3><ul>
<li><strong>Don't fight near shore</strong> — getting beached is deadly</li>
<li><strong>Turn your bow</strong> toward attackers to minimize target area</li>
<li><strong>Flee downwind</strong> — you're faster with the wind</li>
<li>Keep <strong>repair materials</strong> in quick slots</li>
</ul></section>

<section><h2>4. Ship Repair</h2>
<p>Ships take damage from combat and storms. Always carry:</p><ul>
<li><strong>Wood</strong> — Basic hull repair</li>
<li><strong>Nails</strong> — Structural repair</li>
<li><strong>Planks</strong> — Emergency patching</li>
</ul></section>

<section id="faq"><h2>FAQ</h2>
<details><summary>Can I have multiple ships?</summary><div class="faq-answer"><p>You can own multiple ships but can only sail one at a time. Others remain docked.</p></div></details>
<details><summary>What happens if my ship is destroyed?</summary><div class="faq-answer"><p>You can rebuild at the Wharf. Items in ship cargo may be lost. Keep valuables in base storage.</p></div></details>
</section>

<aside class="related-guides"><h2>Related</h2><ul>
<li><a href="/ships/">Ship Database — All Stats</a></li>
<li><a href="/guides/sailing-navigation/">Sailing & Navigation</a></li>
<li><a href="/guides/coop-multiplayer/">Co-op Crew Roles</a></li>
<li><a href="/weapons/">Weapons for Boarding</a></li>
</ul></aside>"""
    return page_wrapper(
        "Ship Building & Naval Combat — Windrose (2026) | Windrose Guides",
        "Complete guide to building, upgrading, and fighting with ships in Windrose. Cannon placement, boarding, fleet management.",
        "https://windrosewiki.games/guides/ship-building-naval-combat", "../../css/style.css",
        [("Home","/"),("Guides","/guides/"),("Naval Combat",None)], body, "/guides")

if __name__ == "__main__":
    print("=== Phase 1 Batch 2: 4 Guide Articles ===")
    write_page("guides/crafting-progression/index.html", crafting_progression())
    write_page("guides/sailing-navigation/index.html", sailing_navigation())
    write_page("guides/coop-multiplayer/index.html", coop_multiplayer())
    write_page("guides/ship-building-naval-combat/index.html", naval_combat())
    print("Done! 4 guides generated.")
