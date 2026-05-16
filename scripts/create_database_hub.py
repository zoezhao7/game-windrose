import os
import re

PROJECT_DIR = r"f:\aicode\gamedoc"

# 1. Create Database Directory and Page
db_dir = os.path.join(PROJECT_DIR, "database")
os.makedirs(db_dir, exist_ok=True)

db_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Windrose Database: Items, Weapons, Mobs & Maps (2026) | Windrose Guides</title>
    <meta name="description" content="The ultimate Windrose database. Search for crafting recipes, weapon stats, armor sets, boss drops, enemies, and resource locations in one place.">
    <link rel="canonical" href="https://windrose-guides.com/database">
    <link rel="stylesheet" href="../css/style.css">
    <style>
        .db-search {
            margin-bottom: 3rem;
            text-align: center;
        }
        .db-search input {
            width: 100%;
            max-width: 600px;
            padding: 1rem 1.5rem;
            font-size: 1.2rem;
            border-radius: 50px;
            border: 2px solid var(--border);
            background: rgba(10, 14, 26, 0.6);
            color: #f8fafc;
            outline: none;
            transition: all var(--transition);
        }
        .db-search input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 15px rgba(212,168,83,0.3);
        }
        .category-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
        }
        .category-card {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1.5rem;
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            transition: all var(--transition);
            text-decoration: none;
        }
        .category-card:hover {
            transform: translateY(-3px);
            border-color: var(--accent);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        .category-icon {
            font-size: 2rem;
            background: rgba(212,168,83,0.1);
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            color: var(--accent);
        }
        .category-info h3 {
            margin: 0 0 0.25rem 0;
            color: #f1f5f9;
        }
        .category-info p {
            margin: 0;
            font-size: 0.85rem;
            color: var(--text-muted);
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <a href="/" class="logo"><img src="/imgs/logo.png" alt="Windrose Guides Logo" width="32" height="32"> Windrose Guides</a>
            <button class="hamburger" aria-label="Toggle menu" aria-expanded="false"><span></span><span></span><span></span></button>
            <ul class="nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="/beginner-guide">Beginner</a></li>
                <li><a href="/database" class="active">Database</a></li>
                <li><a href="/guides">Guides</a></li>
                <li><a href="/tools">Tools</a></li>
                <li><a href="/news">News</a></li>
            </ul>
        </div>
    </header>

    <main>
        <section class="hero" style="background-image: linear-gradient(rgba(10, 14, 26, 0.8), rgba(10, 14, 26, 0.9)), url('/imgs/hero_bg.png'); background-size: cover; background-position: center; border-radius: 0; padding: 5rem 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <div class="container" style="text-align: center;">
                <h1 style="border:none; margin-bottom: 1rem;">Windrose Database Explorer</h1>
                <p class="tagline" style="justify-content: center; margin-bottom: 2rem;">Search items, weapons, bosses, and resources instantly.</p>
                <div class="db-search">
                    <input type="text" placeholder="Search for 'Copper', 'Soul Eater', 'Thomas Richards'..." id="globalSearch">
                </div>
            </div>
        </section>

        <div class="container" style="margin-top: 3rem;">
            <h2>Browse Categories</h2>
            <div class="category-grid">
                <a href="/weapons" class="category-card">
                    <div class="category-icon">⚔️</div>
                    <div class="category-info">
                        <h3>Weapons</h3>
                        <p>Sabers, Muskets, Stats</p>
                    </div>
                </a>
                <a href="/armor" class="category-card">
                    <div class="category-icon">🛡️</div>
                    <div class="category-info">
                        <h3>Armor Sets</h3>
                        <p>Stats & Set Bonuses</p>
                    </div>
                </a>
                <a href="/ships" class="category-card">
                    <div class="category-icon">⛵</div>
                    <div class="category-info">
                        <h3>Ships</h3>
                        <p>Ketch, Brigantine, Frigate</p>
                    </div>
                </a>
                <a href="/bosses" class="category-card">
                    <div class="category-icon">💀</div>
                    <div class="category-info">
                        <h3>Bosses</h3>
                        <p>Mechanics & Loot Tables</p>
                    </div>
                </a>
                <a href="/enemies" class="category-card">
                    <div class="category-icon">🧟</div>
                    <div class="category-info">
                        <h3>Bestiary</h3>
                        <p>Mobs & Elite Encounters</p>
                    </div>
                </a>
                <a href="/crafting" class="category-card">
                    <div class="category-icon">🔨</div>
                    <div class="category-info">
                        <h3>Crafting</h3>
                        <p>Workbench & Smelting</p>
                    </div>
                </a>
                <a href="/cooking" class="category-card">
                    <div class="category-icon">🍖</div>
                    <div class="category-info">
                        <h3>Food & Alchemy</h3>
                        <p>Consumables & Buffs</p>
                    </div>
                </a>
                <a href="/resources" class="category-card">
                    <div class="category-icon">⛏️</div>
                    <div class="category-info">
                        <h3>Resources</h3>
                        <p>Ore, Wood, Materials</p>
                    </div>
                </a>
                <a href="/factions" class="category-card">
                    <div class="category-icon">📜</div>
                    <div class="category-info">
                        <h3>Factions</h3>
                        <p>NPCs & Reputation</p>
                    </div>
                </a>
            </div>
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <a href="/" class="footer-logo"><img src="/imgs/logo.png" alt="Windrose Guides Logo" width="28" height="28"> Windrose Guides</a>
                    <p>Your complete Windrose wiki, database, and guide hub.</p>
                </div>
            </div>
            <div class="footer-bottom">
                <span>&copy; 2026 Windrose Guides. Unofficial fan resource.</span>
                <nav><a href="/privacy">Privacy Policy</a></nav>
            </div>
        </div>
    </footer>
    <script>
        document.querySelector('.hamburger').addEventListener('click',function(){this.classList.toggle('open');document.querySelector('.nav-links').classList.toggle('open');this.setAttribute('aria-expanded',this.classList.contains('open'));});
        // Dummy search functionality placeholder
        document.getElementById('globalSearch').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                alert('Global JSON search feature is currently under construction. Please use the category cards below.');
            }
        });
    </script>
</body>
</html>
"""

with open(os.path.join(db_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(db_html_content)

print("Created /database/index.html")

# 2. Update navigation in all HTML files
def determine_active_class(filepath):
    rel_path = os.path.relpath(filepath, PROJECT_DIR).replace('\\', '/')
    if rel_path == 'index.html' or rel_path == 'zh/index.html':
        return 'home'
    elif rel_path.startswith('beginner-guide'):
        return 'beginner'
    elif rel_path.startswith('database') or rel_path.startswith('bosses') or rel_path.startswith('crafting') or rel_path.startswith('resources') or rel_path.startswith('ships') or rel_path.startswith('weapons'):
        return 'database'
    elif rel_path.startswith('guides') or rel_path.startswith('builds'):
        return 'guides'
    elif rel_path.startswith('tools'):
        return 'tools'
    elif rel_path.startswith('news'):
        return 'news'
    return ''

for root, dirs, files in os.walk(PROJECT_DIR):
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Use regex to find and replace the <ul class="nav-links">...</ul> block
            # This regex looks for <ul class="nav-links"> and anything inside it until </ul>
            pattern = re.compile(r'<ul class="nav-links">.*?</ul>', re.DOTALL)
            
            if pattern.search(content):
                active_category = determine_active_class(filepath)
                
                active_cls = ' class="active"'
                
                new_nav = '<ul class="nav-links">\n'
                new_nav += f'                <li><a href="/"{active_cls if active_category == "home" else ""}>Home</a></li>\n'
                new_nav += f'                <li><a href="/beginner-guide"{active_cls if active_category == "beginner" else ""}>Beginner</a></li>\n'
                new_nav += f'                <li><a href="/database"{active_cls if active_category == "database" else ""}>Database</a></li>\n'
                new_nav += f'                <li><a href="/guides"{active_cls if active_category == "guides" else ""}>Guides</a></li>\n'
                new_nav += f'                <li><a href="/tools"{active_cls if active_category == "tools" else ""}>Tools</a></li>\n'
                new_nav += f'                <li><a href="/news"{active_cls if active_category == "news" else ""}>News</a></li>\n'
                new_nav += '            </ul>'
                
                updated_content = pattern.sub(new_nav, content)
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(updated_content)

print("Updated navigation menu across all HTML files.")
