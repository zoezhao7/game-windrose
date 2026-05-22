"""One-off translation script: bosses/index.html (EN) -> es/bosses/index.html (ES).

Reads the source English page, replaces head metadata, header/footer, and
hand-translates body content to neutral Latin American Spanish.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from templates import header_html, footer_html, HAMBURGER_JS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "bosses" / "index.html"
DST = ROOT / "es" / "bosses" / "index.html"

LANG = "es"
HLANG = "es"
LOCALE_OG = "es_ES"
PATH_SLUG = "bosses"  # used in canonical & hreflang

src = SRC.read_text(encoding="utf-8")

# --- 1. Localized header/footer ------------------------------------------------
header_es = header_html("bosses", LANG, current_path="/bosses")
footer_es = footer_html(LANG)

# Replace original <header class="header">...</header>
src = re.sub(
    r'<header class="header">[\s\S]*?</header>',
    header_es,
    src,
    count=1,
)
src = re.sub(
    r'<footer class="footer">[\s\S]*?</footer>',
    footer_es,
    src,
    count=1,
)
# Replace the original inline hamburger script with HAMBURGER_JS
src = re.sub(
    r"<script>document\.querySelector\('\.hamburger'\)[\s\S]*?</script>",
    HAMBURGER_JS,
    src,
    count=1,
)

# --- 2. <html lang> ------------------------------------------------------------
src = src.replace('<html lang="en">', f'<html lang="{HLANG}">', 1)

# --- 3. CSS path: ../css/style.css -> ../../css/style.css ---------------------
src = src.replace(
    '<link rel="stylesheet" href="../css/style.css">',
    '<link rel="stylesheet" href="../../css/style.css">',
    1,
)

# --- 4. Head metadata replacement ---------------------------------------------
# title
src = src.replace(
    "<title>Windrose Bosses: All Boss Guides, Strategies & Drops (2026) | Windrose Guides</title>",
    "<title>Jefes de Windrose: guías, estrategias y botín (2026) | Windrose Guides</title>",
    1,
)

# meta description
src = src.replace(
    '<meta name="description" content="Complete Windrose boss guide covering all story arena bosses and optional encounters. Strategies, recommended gear, drops, and phase breakdowns for Thomas Richards, Israel Hands, High Priestess, and Ghost Captain.">',
    '<meta name="description" content="Guía completa de los jefes de Windrose: todos los jefes de arena de la historia y los encuentros opcionales. Estrategias, equipo recomendado, botín y análisis por fases de Thomas Richards, Israel Hands, High Priestess y Ghost Captain.">',
    1,
)

# canonical + hreflang block (insert hreflangs after canonical)
old_canonical_block = '<link rel="canonical" href="https://windrose-guides.com/bosses">'
new_canonical_block = (
    f'<link rel="canonical" href="https://windrose-guides.com/{LANG}/{PATH_SLUG}">\n'
    '    <link rel="alternate" hreflang="en" href="https://windrose-guides.com/bosses">\n'
    '    <link rel="alternate" hreflang="es" href="https://windrose-guides.com/es/bosses">\n'
    '    <link rel="alternate" hreflang="pt-BR" href="https://windrose-guides.com/pt/bosses">\n'
    '    <link rel="alternate" hreflang="de" href="https://windrose-guides.com/de/bosses">\n'
    '    <link rel="alternate" hreflang="fr" href="https://windrose-guides.com/fr/bosses">\n'
    '    <link rel="alternate" hreflang="zh-CN" href="https://windrose-guides.com/zh/bosses">\n'
    '    <link rel="alternate" hreflang="x-default" href="https://windrose-guides.com/bosses">'
)
src = src.replace(old_canonical_block, new_canonical_block, 1)

# og:url + og:locale (add og:locale right after og:url)
src = src.replace(
    '<meta property="og:url" content="https://windrose-guides.com/bosses">',
    f'<meta property="og:url" content="https://windrose-guides.com/{LANG}/{PATH_SLUG}">\n'
    f'    <meta property="og:locale" content="{LOCALE_OG}">',
    1,
)

# og:title / og:description / twitter
src = src.replace(
    '<meta property="og:title" content="Windrose Bosses: All Boss Guides, Strategies & Drops (2026)">',
    '<meta property="og:title" content="Jefes de Windrose: guías, estrategias y botín (2026)">',
    1,
)
src = src.replace(
    '<meta property="og:description" content="Complete Windrose boss guide covering all story arena bosses and optional encounters. Strategies, recommended gear, drops, and phase breakdowns.">',
    '<meta property="og:description" content="Guía completa de los jefes de Windrose: todos los jefes de arena de la historia y los encuentros opcionales. Estrategias, equipo recomendado, botín y análisis por fases.">',
    1,
)
src = src.replace(
    '<meta name="twitter:title" content="Windrose Bosses: All Boss Guides (2026)">',
    '<meta name="twitter:title" content="Jefes de Windrose: todas las guías de jefes (2026)">',
    1,
)
src = src.replace(
    '<meta name="twitter:description" content="Complete Windrose boss guide covering all story arena bosses and optional encounters.">',
    '<meta name="twitter:description" content="Guía completa de los jefes de Windrose: todos los jefes de arena de la historia y los encuentros opcionales.">',
    1,
)

# --- 5. JSON-LD ---------------------------------------------------------------
# Update WebSite / Organization @id stays (org/website graph nodes are shared
# canonical IDs across the site, so we leave them). Update WebPage @id, url,
# name, description; BreadcrumbList; Article headline; FAQ Q&A.
src = src.replace(
    '"@id": "https://windrose-guides.com/bosses#webpage",\n                "url": "https://windrose-guides.com/bosses",\n                "name": "Windrose Bosses: All Boss Guides, Strategies & Drops (2026)",\n                "description": "Complete Windrose boss guide covering all story arena bosses and optional encounters.",',
    '"@id": "https://windrose-guides.com/es/bosses#webpage",\n                "url": "https://windrose-guides.com/es/bosses",\n                "name": "Jefes de Windrose: guías, estrategias y botín (2026)",\n                "description": "Guía completa de los jefes de Windrose: todos los jefes de arena de la historia y los encuentros opcionales.",\n                "inLanguage": "es",',
    1,
)
src = src.replace(
    '"breadcrumb": {"@id": "https://windrose-guides.com/bosses#breadcrumb"}',
    '"breadcrumb": {"@id": "https://windrose-guides.com/es/bosses#breadcrumb"}',
    1,
)
src = src.replace(
    '"@id": "https://windrose-guides.com/bosses#breadcrumb",\n                "itemListElement": [\n                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://windrose-guides.com/"},\n                    {"@type": "ListItem", "position": 2, "name": "Bosses"}\n                ]',
    '"@id": "https://windrose-guides.com/es/bosses#breadcrumb",\n                "itemListElement": [\n                    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://windrose-guides.com/es/"},\n                    {"@type": "ListItem", "position": 2, "name": "Jefes"}\n                ]',
    1,
)
src = src.replace(
    '"headline": "Windrose Bosses: All Boss Guides (2026)",',
    '"headline": "Jefes de Windrose: todas las guías de jefes (2026)",',
    1,
)

# FAQ entries
src = src.replace(
    '"name": "How many bosses are in Windrose?",\n                        "acceptedAnswer": {"@type": "Answer", "text": "Current Early Access content includes 3 confirmed story arena bosses (Thomas Richards, Israel Hands, High Priestess) and 1 optional dungeon encounter (Ghost Captain). More bosses are expected as development continues."}',
    '"name": "¿Cuántos jefes hay en Windrose?",\n                        "acceptedAnswer": {"@type": "Answer", "text": "El contenido actual de Early Access incluye 3 jefes de arena de la historia confirmados (Thomas Richards, Israel Hands, High Priestess) y 1 encuentro opcional de mazmorra (Ghost Captain). Se esperan más jefes a medida que avance el desarrollo."}',
    1,
)
src = src.replace(
    '"name": "What is the boss order in Windrose?",\n                        "acceptedAnswer": {"@type": "Answer", "text": "The progression order is: Thomas Richards (Coastal Jungle, Lv 5-6) → Israel Hands (Foothills, Lv 8-10) → High Priestess (Cursed Swamps, Lv 12-15). Ghost Captain is optional and can be fought around Lv 10-12."}',
    '"name": "¿Cuál es el orden de los jefes en Windrose?",\n                        "acceptedAnswer": {"@type": "Answer", "text": "El orden de progresión es: Thomas Richards (Coastal Jungle, Lv 5-6) → Israel Hands (Foothills, Lv 8-10) → High Priestess (Cursed Swamps, Lv 12-15). Ghost Captain es opcional y se puede enfrentar alrededor del Lv 10-12."}',
    1,
)
src = src.replace(
    '"name": "Can I fight bosses in co-op?",\n                        "acceptedAnswer": {"@type": "Answer", "text": "Yes! Windrose supports 1-8 player co-op. Bosses scale with player count, but having teammates to split aggro makes fights significantly easier."}',
    '"name": "¿Puedo enfrentar a los jefes en co-op?",\n                        "acceptedAnswer": {"@type": "Answer", "text": "¡Sí! Windrose admite co-op para 1-8 jugadores. Los jefes escalan con la cantidad de jugadores, pero contar con compañeros para dividir el aggro hace que las peleas sean mucho más fáciles."}',
    1,
)

# --- 6. Breadcrumb nav --------------------------------------------------------
src = src.replace(
    '<nav class="breadcrumb" aria-label="Breadcrumb">\n        <div class="container">\n            <ol>\n                <li><a href="/">Home</a></li>\n                <li aria-current="page">Bosses</li>\n            </ol>\n        </div>\n    </nav>',
    '<nav class="breadcrumb" aria-label="Ruta de navegación">\n        <div class="container">\n            <ol>\n                <li><a href="/es/">Inicio</a></li>\n                <li aria-current="page">Jefes</li>\n            </ol>\n        </div>\n    </nav>',
    1,
)

# --- 7. Body content ----------------------------------------------------------
# Hero
src = src.replace(
    "<h1>Windrose Boss Guide: All Bosses, Strategies & Drops</h1>",
    "<h1>Guía de jefes de Windrose: todos los jefes, estrategias y botín</h1>",
    1,
)
src = src.replace(
    '<p class="hero-subtitle">Master every boss encounter in Windrose — from the Coastal Jungle to the Cursed Swamps. Strategies, recommended gear, phase breakdowns, and verified drop tables.</p>',
    '<p class="hero-subtitle">Domina cada encuentro contra jefes en Windrose, desde la Coastal Jungle hasta los Cursed Swamps. Estrategias, equipo recomendado, análisis por fases y tablas de botín verificadas.</p>',
    1,
)

# Quick stats
src = src.replace(
    '<div class="stat"><div class="stat-label">Story Bosses</div><div class="stat-value">3 Confirmed</div></div>',
    '<div class="stat"><div class="stat-label">Jefes de la Historia</div><div class="stat-value">3 Confirmados</div></div>',
    1,
)
src = src.replace(
    '<div class="stat"><div class="stat-label">Optional Encounters</div><div class="stat-value">1+ Known</div></div>',
    '<div class="stat"><div class="stat-label">Encuentros Opcionales</div><div class="stat-value">1+ Conocido</div></div>',
    1,
)
src = src.replace(
    '<div class="stat"><div class="stat-label">Data Status</div><div class="stat-value">Early Access Tracker</div></div>',
    '<div class="stat"><div class="stat-label">Estado de los Datos</div><div class="stat-value">Seguimiento de Early Access</div></div>',
    1,
)

# Section headings + intro
src = src.replace(
    "<h2>Boss Progression Order</h2>",
    "<h2>Orden de progresión de los jefes</h2>",
    1,
)
src = src.replace(
    "<p>Windrose features a linear boss progression tied to biome advancement. Defeat each story boss to unlock the next biome and crafting tier.</p>",
    "<p>Windrose ofrece una progresión lineal de jefes vinculada al avance por biomas. Derrota a cada jefe de la historia para desbloquear el siguiente bioma y el siguiente nivel de fabricación.</p>",
    1,
)

# Boss progression steps
src = src.replace(
    "<span>Coastal Jungle · Lv 5-6</span>",
    "<span>Coastal Jungle · Lv 5-6</span>",
    1,
)
# (the three spans for Lv lines remain unchanged — biomes/levels already in glossary form)

src = src.replace("<h2>All Boss Encounters</h2>", "<h2>Todos los encuentros con jefes</h2>", 1)

# Thomas Richards card
src = src.replace(
    '<a href="/bosses/thomas-richards/" class="boss-card" id="boss-thomas-richards">',
    '<a href="/es/bosses/thomas-richards/" class="boss-card" id="boss-thomas-richards">',
    1,
)
src = src.replace(
    '<span class="boss-card-badge badge-story">Story Boss #1</span>',
    '<span class="boss-card-badge badge-story">Jefe de la historia #1</span>',
    1,
)
src = src.replace(
    'alt="Thomas Richards - Windrose Boss"',
    'alt="Thomas Richards — jefe de Windrose"',
    1,
)
src = src.replace(
    "<p>The first story arena boss. A brutal melee fighter with explosive grenades and an unblockable grab attack. Defeat him to unlock the Foothills biome.</p>",
    "<p>El primer jefe de arena de la historia. Un brutal combatiente cuerpo a cuerpo con granadas explosivas y un agarre imbloqueable. Derrótalo para desbloquear el bioma Foothills.</p>",
    1,
)

# Israel Hands card
src = src.replace(
    '<a href="/bosses/israel-hands/" class="boss-card" id="boss-israel-hands">',
    '<a href="/es/bosses/israel-hands/" class="boss-card" id="boss-israel-hands">',
    1,
)
src = src.replace(
    '<span class="boss-card-badge badge-story">Story Boss #2</span>',
    '<span class="boss-card-badge badge-story">Jefe de la historia #2</span>',
    1,
)
src = src.replace(
    'alt="Israel Hands - Windrose Boss"',
    'alt="Israel Hands — jefe de Windrose"',
    1,
)
src = src.replace(
    '<p>The second arena boss encountered via "Needle in a Haystack" questline. Drops the legendary Soul Eater greatsword and Charon\'s Obol.</p>',
    '<p>El segundo jefe de arena, al que se llega a través de la misión "Needle in a Haystack". Suelta la legendaria mandoble Soul Eater y el Charon\'s Obol.</p>',
    1,
)

# High Priestess card
src = src.replace(
    '<a href="/bosses/high-priestess/" class="boss-card" id="boss-high-priestess">',
    '<a href="/es/bosses/high-priestess/" class="boss-card" id="boss-high-priestess">',
    1,
)
src = src.replace(
    '<span class="boss-card-badge badge-story">Story Boss #3</span>',
    '<span class="boss-card-badge badge-story">Jefe de la historia #3</span>',
    1,
)
src = src.replace(
    'alt="High Priestess - Windrose Boss"',
    'alt="High Priestess — jefe de Windrose"',
    1,
)
src = src.replace(
    "<p>The final story boss in current Early Access content. A challenging late-game encounter in the Cursed Swamps biome. Drops Charon's Obol.</p>",
    "<p>El jefe final de la historia en el contenido actual de Early Access. Un desafiante encuentro de fase avanzada en el bioma Cursed Swamps. Suelta Charon's Obol.</p>",
    1,
)

# Ghost Captain card
src = src.replace(
    '<a href="/bosses/ghost-captain/" class="boss-card" id="boss-ghost-captain">',
    '<a href="/es/bosses/ghost-captain/" class="boss-card" id="boss-ghost-captain">',
    1,
)
src = src.replace(
    '<span class="boss-card-badge badge-optional">Optional</span>',
    '<span class="boss-card-badge badge-optional">Opcional</span>',
    1,
)
src = src.replace(
    'alt="Ghost Captain - Windrose Boss"',
    'alt="Ghost Captain — jefe de Windrose"',
    1,
)
src = src.replace(
    "<span><span class=\"meta-icon\">📍</span> Temple Dungeon</span>",
    "<span><span class=\"meta-icon\">📍</span> Mazmorra del Temple</span>",
    1,
)
src = src.replace(
    "<p>An optional major dungeon encounter found in the Temple route. Rewards the Soul Eater greatsword for players seeking extra loot.</p>",
    "<p>Un encuentro opcional de mazmorra principal que se encuentra en la ruta del Temple. Recompensa con la mandoble Soul Eater a los jugadores que buscan botín adicional.</p>",
    1,
)

# Charon's Obols card
src = src.replace(
    '<span class="boss-card-badge badge-unconfirmed">Needs Verification</span>',
    '<span class="boss-card-badge badge-unconfirmed">Por verificar</span>',
    1,
)
src = src.replace(
    'alt="Charon\'s Obols - Unverified"',
    'alt="Charon\'s Obols — sin verificar"',
    1,
)
src = src.replace(
    '<span><span class="meta-icon">📍</span> Unknown</span>',
    '<span><span class="meta-icon">📍</span> Desconocido</span>',
    1,
)
src = src.replace(
    '<span><span class="meta-icon">❓</span> Unconfirmed</span>',
    '<span><span class="meta-icon">❓</span> Sin confirmar</span>',
    1,
)
src = src.replace(
    "<p>Legacy page from older data. Cross-checked wiki sources suggest Charon's Obol is a reward item, not a boss. Kept for tracking until verified in-game.</p>",
    "<p>Página heredada de datos antiguos. Al cruzar fuentes de wiki se sugiere que Charon's Obol es un objeto de recompensa, no un jefe. Se mantiene para seguimiento hasta verificarlo en el juego.</p>",
    1,
)

# "View Full Strategy" CTA appears multiple times -> use replace_all-style global
src = src.replace(
    '<span class="boss-card-cta">View Full Strategy →</span>',
    '<span class="boss-card-cta">Ver estrategia completa →</span>',
)

# --- 8. Boss Preparation section ----------------------------------------------
src = src.replace(
    "<h2>General Boss Preparation</h2>",
    "<h2>Preparación general contra jefes</h2>",
    1,
)
src = src.replace(
    "<p>Every boss in Windrose rewards preparation. Here's a universal checklist before entering any boss arena:</p>",
    "<p>Cada jefe de Windrose recompensa la preparación. Aquí tienes una lista universal antes de entrar a cualquier arena de jefe:</p>",
    1,
)
src = src.replace(
    "<caption>Boss Preparation Checklist</caption>",
    "<caption>Lista de verificación de preparación contra jefes</caption>",
    1,
)
src = src.replace(
    '<th scope="col">Category</th>',
    '<th scope="col">Categoría</th>',
    1,
)
src = src.replace(
    '<th scope="col">Recommendation</th>',
    '<th scope="col">Recomendación</th>',
    1,
)
src = src.replace(
    '<th scope="col">Why It Matters</th>',
    '<th scope="col">Por qué importa</th>',
    1,
)

# Row 1: Food Buffs
src = src.replace(
    "<td><strong>Food Buffs</strong></td>",
    "<td><strong>Buffs de comida</strong></td>",
    1,
)
src = src.replace(
    "<td>Bacon and Eggs, Coconut Milk, or best available meal</td>",
    "<td>Bacon and Eggs, Coconut Milk o la mejor comida disponible</td>",
    1,
)
src = src.replace(
    "<td>Increases max HP and stamina recovery during the fight</td>",
    "<td>Aumenta el HP máximo y la recuperación de stamina durante el combate</td>",
    1,
)

# Row 2: Healing
src = src.replace(
    "<td><strong>Healing</strong></td>",
    "<td><strong>Curación</strong></td>",
    1,
)
src = src.replace(
    "<td>10-15 Bandages minimum, potions if available</td>",
    "<td>10-15 Bandages como mínimo, pociones si están disponibles</td>",
    1,
)
src = src.replace(
    "<td>Boss fights are long; running out of healing means a wipe</td>",
    "<td>Las peleas contra jefes son largas; quedarse sin curación significa morir</td>",
    1,
)

# Row 3: Rested Buff
src = src.replace(
    "<td><strong>Rested Buff</strong></td>",
    "<td><strong>Buff de Descanso</strong></td>",
    1,
)
src = src.replace(
    "<td>Sleep at your Bonfire before traveling to the boss</td>",
    "<td>Duerme junto a tu Bonfire antes de viajar hacia el jefe</td>",
    1,
)
src = src.replace(
    "<td>Provides passive stat boost that stacks with food</td>",
    "<td>Otorga un aumento pasivo de estadísticas que se acumula con la comida</td>",
    1,
)

# Row 4: Gear Level
src = src.replace(
    "<td><strong>Gear Level</strong></td>",
    "<td><strong>Nivel de equipo</strong></td>",
    1,
)
src = src.replace(
    "<td>Match or exceed the boss's recommended level</td>",
    "<td>Iguala o supera el nivel recomendado del jefe</td>",
    1,
)
src = src.replace(
    "<td>Under-leveled gear leads to low damage and high incoming damage</td>",
    "<td>El equipo de nivel bajo provoca poco daño infligido y mucho daño recibido</td>",
    1,
)

# Row 5: Ranged Option
src = src.replace(
    "<td><strong>Ranged Option</strong></td>",
    "<td><strong>Opción a distancia</strong></td>",
    1,
)
src = src.replace(
    "<td>Bring a Blunderbuss or Musket with 20+ bullets</td>",
    "<td>Lleva un Blunderbuss o Musket con más de 20 balas</td>",
    1,
)
src = src.replace(
    "<td>Ranged pressure is safe damage; especially useful for kiting</td>",
    "<td>La presión a distancia es daño seguro; muy útil para hacer kiting</td>",
    1,
)

# Row 6: Repair Kits
src = src.replace(
    "<td><strong>Repair Kits</strong></td>",
    "<td><strong>Kits de reparación</strong></td>",
    1,
)
src = src.replace(
    "<td>2-3 Repair Kits or Combat Repair Kits</td>",
    "<td>2-3 Repair Kits o Combat Repair Kits</td>",
    1,
)
src = src.replace(
    "<td>Weapons and armor degrade during long fights</td>",
    "<td>Las armas y la armadura se desgastan durante las peleas largas</td>",
    1,
)

# --- 9. Boss Drops Quick Reference -------------------------------------------
src = src.replace(
    "<h2>Boss Drops Quick Reference</h2>",
    "<h2>Referencia rápida de botín de jefes</h2>",
    1,
)
src = src.replace(
    "<caption>Known Boss Drops (Community-Sourced)</caption>",
    "<caption>Botín conocido de jefes (fuente comunitaria)</caption>",
    1,
)
src = src.replace(
    '<th scope="col">Boss</th>',
    '<th scope="col">Jefe</th>',
    1,
)
src = src.replace(
    '<th scope="col">Notable Drops</th>',
    '<th scope="col">Botín destacado</th>',
    1,
)
src = src.replace(
    '<th scope="col">Unlocks</th>',
    '<th scope="col">Desbloquea</th>',
    1,
)
src = src.replace(
    '<th scope="col">Data Confidence</th>',
    '<th scope="col">Confianza de los datos</th>',
    1,
)

# Drops table rows - rewrite links to /es/ and translate descriptions
src = src.replace(
    '<td><a href="/bosses/thomas-richards/">Thomas Richards</a></td>\n                            <td>50 XP, Thomas Richards\' Journal, Seafood Platter, Silver Ingot</td>\n                            <td>Foothills biome, iron-tier progression</td>\n                            <td>Community</td>',
    '<td><a href="/es/bosses/thomas-richards/">Thomas Richards</a></td>\n                            <td>50 XP, Thomas Richards\' Journal, Seafood Platter, Silver Ingot</td>\n                            <td>Bioma Foothills, progresión de nivel hierro</td>\n                            <td>Comunidad</td>',
    1,
)
src = src.replace(
    '<td><a href="/bosses/israel-hands/">Israel Hands</a></td>\n                            <td>Soul Eater greatsword, 30 Undead Essence, Charon\'s Obol</td>\n                            <td>Cursed Swamps, next story gate</td>\n                            <td>Community</td>',
    '<td><a href="/es/bosses/israel-hands/">Israel Hands</a></td>\n                            <td>Mandoble Soul Eater, 30 Undead Essence, Charon\'s Obol</td>\n                            <td>Cursed Swamps, siguiente puerta de la historia</td>\n                            <td>Comunidad</td>',
    1,
)
src = src.replace(
    '<td><a href="/bosses/high-priestess/">High Priestess</a></td>\n                            <td>Charon\'s Obol</td>\n                            <td>End of current main story (Chapter 1)</td>\n                            <td>Community</td>',
    '<td><a href="/es/bosses/high-priestess/">High Priestess</a></td>\n                            <td>Charon\'s Obol</td>\n                            <td>Final de la historia principal actual (Capítulo 1)</td>\n                            <td>Comunidad</td>',
    1,
)
src = src.replace(
    '<td><a href="/bosses/ghost-captain/">Ghost Captain</a></td>\n                            <td>Soul Eater greatsword</td>\n                            <td>Optional loot route</td>\n                            <td>Community</td>',
    '<td><a href="/es/bosses/ghost-captain/">Ghost Captain</a></td>\n                            <td>Mandoble Soul Eater</td>\n                            <td>Ruta de botín opcional</td>\n                            <td>Comunidad</td>',
    1,
)

# Data note
src = src.replace(
    '<p class="update-note"><strong>Data note:</strong> Windrose is in Early Access (v0.10.0.5.120). Boss drops and mechanics can change with patches. All data on this page is community-sourced and will be updated as official information becomes available.</p>',
    '<p class="update-note"><strong>Nota sobre los datos:</strong> Windrose está en Early Access (v0.10.0.5.120). El botín y las mecánicas de los jefes pueden cambiar con los parches. Todos los datos de esta página provienen de la comunidad y se actualizarán a medida que aparezca información oficial.</p>',
    1,
)

# --- 10. FAQ section ----------------------------------------------------------
src = src.replace(
    "<h2>Frequently Asked Questions</h2>",
    "<h2>Preguntas frecuentes</h2>",
    1,
)
src = src.replace(
    "<summary>How many bosses are in Windrose?</summary>",
    "<summary>¿Cuántos jefes hay en Windrose?</summary>",
    1,
)
src = src.replace(
    '<div class="faq-answer"><p>Current Early Access content includes 3 confirmed story arena bosses (Thomas Richards, Israel Hands, High Priestess) and 1 optional dungeon encounter (Ghost Captain). More bosses are expected as development continues.</p></div>',
    '<div class="faq-answer"><p>El contenido actual de Early Access incluye 3 jefes de arena de la historia confirmados (Thomas Richards, Israel Hands, High Priestess) y 1 encuentro opcional de mazmorra (Ghost Captain). Se esperan más jefes a medida que avance el desarrollo.</p></div>',
    1,
)
src = src.replace(
    "<summary>What is the boss order in Windrose?</summary>",
    "<summary>¿Cuál es el orden de los jefes en Windrose?</summary>",
    1,
)
src = src.replace(
    '<div class="faq-answer"><p>The progression order is: Thomas Richards (Coastal Jungle, Lv 5-6) → Israel Hands (Foothills, Lv 8-10) → High Priestess (Cursed Swamps, Lv 12-15). Ghost Captain is optional and can be fought around Lv 10-12.</p></div>',
    '<div class="faq-answer"><p>El orden de progresión es: Thomas Richards (Coastal Jungle, Lv 5-6) → Israel Hands (Foothills, Lv 8-10) → High Priestess (Cursed Swamps, Lv 12-15). Ghost Captain es opcional y se puede enfrentar alrededor del Lv 10-12.</p></div>',
    1,
)
src = src.replace(
    "<summary>Can I fight bosses in co-op?</summary>",
    "<summary>¿Puedo enfrentar a los jefes en co-op?</summary>",
    1,
)
src = src.replace(
    '<div class="faq-answer"><p>Yes! Windrose supports 1-8 player co-op. Bosses scale with player count, but having teammates to split aggro makes fights significantly easier.</p></div>',
    '<div class="faq-answer"><p>¡Sí! Windrose admite co-op para 1-8 jugadores. Los jefes escalan con la cantidad de jugadores, pero contar con compañeros para dividir el aggro hace que las peleas sean mucho más fáciles.</p></div>',
    1,
)
src = src.replace(
    "<summary>Are all boss drops confirmed?</summary>",
    "<summary>¿Está confirmado todo el botín de los jefes?</summary>",
    1,
)
src = src.replace(
    '<div class="faq-answer"><p>No. Early Access data can change, so exact drops should be rechecked after patches and marked with source confidence. We mark all unverified data as "Community" sourced.</p></div>',
    '<div class="faq-answer"><p>No. Los datos de Early Access pueden cambiar, así que el botín exacto debe revisarse después de cada parche y marcarse con su nivel de confianza. Marcamos todos los datos no verificados como provenientes de la "Comunidad".</p></div>',
    1,
)
src = src.replace(
    "<summary>What's the best weapon for boss fights?</summary>",
    "<summary>¿Cuál es la mejor arma para las peleas contra jefes?</summary>",
    1,
)
src = src.replace(
    '<div class="faq-answer"><p>A Saber for melee (fast combos) combined with a Blunderbuss for ranged kiting is generally the most effective combination. The Soul Eater greatsword becomes available after defeating Israel Hands or Ghost Captain.</p></div>',
    '<div class="faq-answer"><p>Un Saber para el cuerpo a cuerpo (combos rápidos) combinado con un Blunderbuss para el kiting a distancia suele ser la combinación más efectiva. La mandoble Soul Eater queda disponible tras derrotar a Israel Hands o a Ghost Captain.</p></div>',
    1,
)

# --- 11. Related Guides aside -------------------------------------------------
src = src.replace(
    "<h2>Related Guides</h2>",
    "<h2>Guías relacionadas</h2>",
    1,
)
src = src.replace(
    '<li><a href="/guides/boss-progression/">Boss Progression & Strategy Guide</a></li>',
    '<li><a href="/es/guides/boss-progression/">Guía de progresión y estrategia de jefes</a></li>',
    1,
)
src = src.replace(
    '<li><a href="/beginner-guide/">Beginner Guide — Day 1-10</a></li>',
    '<li><a href="/es/beginner-guide/">Guía para principiantes — Días 1-10</a></li>',
    1,
)
src = src.replace(
    '<li><a href="/crafting/workbench/">Workbench Recipes Lv1-3</a></li>',
    '<li><a href="/es/crafting/workbench/">Recetas de Workbench Lv1-3</a></li>',
    1,
)
src = src.replace(
    '<li><a href="/guides/best-early-builds/">Best Early-Game Builds</a></li>',
    '<li><a href="/es/guides/best-early-builds/">Mejores builds del juego temprano</a></li>',
    1,
)
src = src.replace(
    '<li><a href="/database/bosses/">Database: Boss List</a></li>',
    '<li><a href="/es/database/bosses/">Base de datos: Lista de jefes</a></li>',
    1,
)

# --- Write output -------------------------------------------------------------
DST.parent.mkdir(parents=True, exist_ok=True)
DST.write_text(src, encoding="utf-8")
print(f"Wrote {DST} ({len(src)} bytes)")
