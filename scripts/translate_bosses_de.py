# -*- coding: utf-8 -*-
"""One-off script: translate /bosses/index.html to German and write to /de/bosses/index.html.

Follows the rules in scripts/TRANSLATION_GUIDE.md:
- HTML lang -> "de"
- canonical -> /de/bosses
- Adds full hreflang block + og:locale=de_DE
- Replaces header/footer with templates.header_html("bosses","de") / footer_html("de")
- Replaces hamburger script with templates.HAMBURGER_JS
- Rewrites internal links (/X -> /de/X) for paths that have localized versions
- Glossary terms stay English (Windrose, Thomas Richards, Israel Hands, High Priestess,
  Ghost Captain, Charon's Obol, Sloop, Brigantine, Frigate, Foothills,
  Coastal Jungle, Cursed Swamps, Saber, Blunderbuss, Musket, etc.)
- Translates body, meta, JSON-LD into German Du-form
- CSS path stays ../../css/style.css because the file lives two levels deep
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from templates import header_html, footer_html, HAMBURGER_JS  # noqa: E402

DEST = ROOT / "de" / "bosses" / "index.html"


HTML = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Windrose Bosse: Alle Boss-Guides, Strategien & Drops (2026) | Windrose Guides</title>
    <meta name="description" content="Vollständiger Windrose-Boss-Guide mit allen Story-Arena-Bossen und optionalen Begegnungen. Strategien, empfohlene Ausrüstung, Drops und Phasenanalysen für Thomas Richards, Israel Hands, High Priestess und Ghost Captain.">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <link rel="canonical" href="https://windrosewiki.games/de/bosses">
    <link rel="alternate" hreflang="en" href="https://windrosewiki.games/bosses">
    <link rel="alternate" hreflang="es" href="https://windrosewiki.games/es/bosses">
    <link rel="alternate" hreflang="pt-BR" href="https://windrosewiki.games/pt/bosses">
    <link rel="alternate" hreflang="de" href="https://windrosewiki.games/de/bosses">
    <link rel="alternate" hreflang="fr" href="https://windrosewiki.games/fr/bosses">
    <link rel="alternate" hreflang="zh-CN" href="https://windrosewiki.games/zh/bosses">
    <link rel="alternate" hreflang="x-default" href="https://windrosewiki.games/bosses">
    <link rel="stylesheet" href="../../css/style.css">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://windrosewiki.games/de/bosses">
    <meta property="og:title" content="Windrose Bosse: Alle Boss-Guides, Strategien & Drops (2026)">
    <meta property="og:description" content="Vollständiger Windrose-Boss-Guide mit allen Story-Arena-Bossen und optionalen Begegnungen. Strategien, empfohlene Ausrüstung, Drops und Phasenanalysen.">
    <meta property="og:image" content="https://windrosewiki.games/imgs/og_bosses.png">
    <meta property="og:site_name" content="Windrose Guides">
    <meta property="og:locale" content="de_DE">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Windrose Bosse: Alle Boss-Guides (2026)">
    <meta name="twitter:description" content="Vollständiger Windrose-Boss-Guide mit allen Story-Arena-Bossen und optionalen Begegnungen.">
    <meta name="twitter:image" content="https://windrosewiki.games/imgs/og_bosses.png">
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "@id": "https://windrosewiki.games/de/#website",
                "url": "https://windrosewiki.games/de/",
                "name": "Windrose Guides",
                "inLanguage": "de",
                "publisher": {"@id": "https://windrosewiki.games/#org"}
            },
            {
                "@type": "Organization",
                "@id": "https://windrosewiki.games/#org",
                "name": "Windrose Guides",
                "url": "https://windrosewiki.games/"
            },
            {
                "@type": "WebPage",
                "@id": "https://windrosewiki.games/de/bosses#webpage",
                "url": "https://windrosewiki.games/de/bosses",
                "name": "Windrose Bosse: Alle Boss-Guides, Strategien & Drops (2026)",
                "description": "Vollständiger Windrose-Boss-Guide mit allen Story-Arena-Bossen und optionalen Begegnungen.",
                "inLanguage": "de",
                "dateModified": "2026-05-16",
                "isPartOf": {"@id": "https://windrosewiki.games/de/#website"},
                "breadcrumb": {"@id": "https://windrosewiki.games/de/bosses#breadcrumb"}
            },
            {
                "@type": "BreadcrumbList",
                "@id": "https://windrosewiki.games/de/bosses#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Startseite", "item": "https://windrosewiki.games/de/"},
                    {"@type": "ListItem", "position": 2, "name": "Bosse"}
                ]
            },
            {
                "@type": "Article",
                "headline": "Windrose Bosse: Alle Boss-Guides (2026)",
                "inLanguage": "de",
                "datePublished": "2026-05-12",
                "dateModified": "2026-05-16",
                "author": {"@type": "Organization", "name": "Windrose Guides"}
            },
            {
                "@type": "FAQPage",
                "inLanguage": "de",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "Wie viele Bosse gibt es in Windrose?",
                        "acceptedAnswer": {"@type": "Answer", "text": "Die aktuellen Early-Access-Inhalte umfassen 3 bestätigte Story-Arena-Bosse (Thomas Richards, Israel Hands, High Priestess) und 1 optionale Dungeon-Begegnung (Ghost Captain). Weitere Bosse werden im Verlauf der Entwicklung erwartet."}
                    },
                    {
                        "@type": "Question",
                        "name": "Wie ist die Boss-Reihenfolge in Windrose?",
                        "acceptedAnswer": {"@type": "Answer", "text": "Die Fortschrittsreihenfolge lautet: Thomas Richards (Coastal Jungle, Lv 5-6) → Israel Hands (Foothills, Lv 8-10) → High Priestess (Cursed Swamps, Lv 12-15). Ghost Captain ist optional und kann um Lv 10-12 bekämpft werden."}
                    },
                    {
                        "@type": "Question",
                        "name": "Kann ich Bosse im Koop bekämpfen?",
                        "acceptedAnswer": {"@type": "Answer", "text": "Ja! Windrose unterstützt Koop für 1-8 Spieler. Bosse skalieren mit der Spieleranzahl, aber mit Teamkollegen, die Aggro aufteilen, werden die Kämpfe deutlich einfacher."}
                    }
                ]
            }
        ]
    }
    </script>
    <style>
        /* Boss 卡片网格布局 - 为 bosses 页面提供丰富的视觉展示 */
        .boss-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        .boss-card {
            position: relative;
            display: flex;
            flex-direction: column;
            background: var(--card-bg, rgba(15, 23, 42, 0.8));
            border: 1px solid var(--border, rgba(212, 168, 83, 0.15));
            border-radius: var(--radius, 12px);
            overflow: hidden;
            text-decoration: none;
            color: inherit;
            transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        }
        .boss-card:hover {
            transform: translateY(-6px);
            border-color: var(--accent, #d4a853);
            box-shadow: 0 12px 40px rgba(212, 168, 83, 0.2), 0 4px 12px rgba(0,0,0,0.4);
        }
        .boss-card-img {
            width: 100%;
            aspect-ratio: 1 / 1;
            object-fit: cover;
            border-bottom: 2px solid var(--border, rgba(212, 168, 83, 0.15));
            transition: transform 0.4s ease;
        }
        .boss-card:hover .boss-card-img {
            transform: scale(1.05);
        }
        .boss-card-img-wrapper {
            overflow: hidden;
            position: relative;
        }
        .boss-card-badge {
            position: absolute;
            top: 0.75rem;
            right: 0.75rem;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            z-index: 2;
        }
        .badge-story {
            background: rgba(212, 168, 83, 0.9);
            color: #1a1207;
        }
        .badge-optional {
            background: rgba(100, 116, 139, 0.9);
            color: #f1f5f9;
        }
        .badge-unconfirmed {
            background: rgba(239, 68, 68, 0.8);
            color: #fff;
        }
        .boss-card-body {
            padding: 1.25rem;
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        .boss-card-body h3 {
            margin: 0 0 0.5rem 0;
            font-size: 1.2rem;
            color: #f1f5f9;
        }
        .boss-card-meta {
            display: flex;
            gap: 1rem;
            margin-bottom: 0.75rem;
            flex-wrap: wrap;
        }
        .boss-card-meta span {
            font-size: 0.8rem;
            color: var(--text-muted, #94a3b8);
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }
        .boss-card-meta .meta-icon {
            font-size: 0.9rem;
        }
        .boss-card-body p {
            margin: 0;
            font-size: 0.9rem;
            color: var(--text-muted, #94a3b8);
            line-height: 1.5;
            flex: 1;
        }
        .boss-card-cta {
            margin-top: 1rem;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--accent, #d4a853);
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }
        .boss-card:hover .boss-card-cta {
            gap: 0.6rem;
        }
        .boss-progression {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0;
            margin: 2rem 0;
            flex-wrap: wrap;
        }
        .boss-progression-step {
            text-align: center;
            padding: 0.75rem 1.25rem;
            background: var(--card-bg, rgba(15, 23, 42, 0.8));
            border: 1px solid var(--border, rgba(212, 168, 83, 0.15));
            border-radius: var(--radius, 12px);
            min-width: 140px;
        }
        .boss-progression-step strong {
            display: block;
            color: #f1f5f9;
            font-size: 0.9rem;
        }
        .boss-progression-step span {
            font-size: 0.75rem;
            color: var(--text-muted, #94a3b8);
        }
        .boss-progression-arrow {
            font-size: 1.5rem;
            color: var(--accent, #d4a853);
            padding: 0 0.5rem;
        }
        @media (max-width: 600px) {
            .boss-grid {
                grid-template-columns: 1fr;
            }
            .boss-progression {
                flex-direction: column;
                gap: 0.5rem;
            }
            .boss-progression-arrow {
                transform: rotate(90deg);
            }
        }
    </style>
</head>
<body>
__HEADER__

    <nav class="breadcrumb" aria-label="Breadcrumb">
        <div class="container">
            <ol>
                <li><a href="/de/">Startseite</a></li>
                <li aria-current="page">Bosse</li>
            </ol>
        </div>
    </nav>

    <main>
        <section class="page-hero">
            <h1>Windrose Boss-Guide: Alle Bosse, Strategien & Drops</h1>
            <p class="hero-subtitle">Meistere jede Boss-Begegnung in Windrose — vom Coastal Jungle bis zu den Cursed Swamps. Strategien, empfohlene Ausrüstung, Phasenanalysen und verifizierte Drop-Tabellen.</p>
        </section>

        <section class="content-section">
            <div class="container">
                <div class="quick-stats">
                    <div class="stat"><div class="stat-label">Story-Bosse</div><div class="stat-value">3 Bestätigt</div></div>
                    <div class="stat"><div class="stat-label">Optionale Begegnungen</div><div class="stat-value">1+ Bekannt</div></div>
                    <div class="stat"><div class="stat-label">Datenstatus</div><div class="stat-value">Early-Access-Tracker</div></div>
                </div>

                <h2>Boss-Fortschrittsreihenfolge</h2>
                <p>Windrose bietet einen linearen Boss-Fortschritt, der an das Vorankommen durch die Biome gekoppelt ist. Besiege jeden Story-Boss, um das nächste Biom und die nächste Handwerksstufe freizuschalten.</p>

                <div class="boss-progression">
                    <div class="boss-progression-step">
                        <strong>Thomas Richards</strong>
                        <span>Coastal Jungle · Lv 5-6</span>
                    </div>
                    <span class="boss-progression-arrow">→</span>
                    <div class="boss-progression-step">
                        <strong>Israel Hands</strong>
                        <span>Foothills · Lv 8-10</span>
                    </div>
                    <span class="boss-progression-arrow">→</span>
                    <div class="boss-progression-step">
                        <strong>High Priestess</strong>
                        <span>Cursed Swamps · Lv 12-15</span>
                    </div>
                </div>

                <h2>Alle Boss-Begegnungen</h2>

                <div class="boss-grid">
                    <!-- Thomas Richards -->
                    <a href="/de/bosses/thomas-richards/" class="boss-card" id="boss-thomas-richards">
                        <div class="boss-card-img-wrapper">
                            <span class="boss-card-badge badge-story">Story-Boss #1</span>
                            <img src="/imgs/thomas_richards.png" alt="Thomas Richards - Windrose Boss" class="boss-card-img" width="400" height="400" loading="lazy">
                        </div>
                        <div class="boss-card-body">
                            <h3>Thomas Richards</h3>
                            <div class="boss-card-meta">
                                <span><span class="meta-icon">📍</span> Coastal Jungle</span>
                                <span><span class="meta-icon">⚔️</span> Lv 5-6</span>
                            </div>
                            <p>Der erste Story-Arena-Boss. Ein brutaler Nahkampfgegner mit explosiven Granaten und einem unblockbaren Greifangriff. Besiege ihn, um das Foothills-Biom freizuschalten.</p>
                            <span class="boss-card-cta">Vollständige Strategie ansehen →</span>
                        </div>
                    </a>

                    <!-- Israel Hands -->
                    <a href="/de/bosses/israel-hands/" class="boss-card" id="boss-israel-hands">
                        <div class="boss-card-img-wrapper">
                            <span class="boss-card-badge badge-story">Story-Boss #2</span>
                            <img src="/imgs/israel_hands.png" alt="Israel Hands - Windrose Boss" class="boss-card-img" width="400" height="400" loading="lazy">
                        </div>
                        <div class="boss-card-body">
                            <h3>Israel Hands</h3>
                            <div class="boss-card-meta">
                                <span><span class="meta-icon">📍</span> Foothills</span>
                                <span><span class="meta-icon">⚔️</span> Lv 8-10</span>
                            </div>
                            <p>Der zweite Arena-Boss, den du über die Questreihe „Needle in a Haystack“ triffst. Lässt das legendäre Soul-Eater-Großschwert und Charon's Obol fallen.</p>
                            <span class="boss-card-cta">Vollständige Strategie ansehen →</span>
                        </div>
                    </a>

                    <!-- High Priestess -->
                    <a href="/de/bosses/high-priestess/" class="boss-card" id="boss-high-priestess">
                        <div class="boss-card-img-wrapper">
                            <span class="boss-card-badge badge-story">Story-Boss #3</span>
                            <img src="/imgs/high_priestess.png" alt="High Priestess - Windrose Boss" class="boss-card-img" width="400" height="400" loading="lazy">
                        </div>
                        <div class="boss-card-body">
                            <h3>High Priestess</h3>
                            <div class="boss-card-meta">
                                <span><span class="meta-icon">📍</span> Cursed Swamps</span>
                                <span><span class="meta-icon">⚔️</span> Lv 12-15</span>
                            </div>
                            <p>Der letzte Story-Boss in den aktuellen Early-Access-Inhalten. Eine herausfordernde Late-Game-Begegnung im Cursed-Swamps-Biom. Lässt Charon's Obol fallen.</p>
                            <span class="boss-card-cta">Vollständige Strategie ansehen →</span>
                        </div>
                    </a>

                    <!-- Ghost Captain -->
                    <a href="/de/bosses/ghost-captain/" class="boss-card" id="boss-ghost-captain">
                        <div class="boss-card-img-wrapper">
                            <span class="boss-card-badge badge-optional">Optional</span>
                            <img src="/imgs/ghost_captain.png" alt="Ghost Captain - Windrose Boss" class="boss-card-img" width="400" height="400" loading="lazy">
                        </div>
                        <div class="boss-card-body">
                            <h3>Ghost Captain</h3>
                            <div class="boss-card-meta">
                                <span><span class="meta-icon">📍</span> Tempel-Dungeon</span>
                                <span><span class="meta-icon">⚔️</span> Lv 10-12</span>
                            </div>
                            <p>Eine optionale große Dungeon-Begegnung auf der Tempel-Route. Belohnt dich mit dem Soul-Eater-Großschwert für zusätzliche Beute.</p>
                            <span class="boss-card-cta">Vollständige Strategie ansehen →</span>
                        </div>
                    </a>

                    <!-- Charon's Obols -->
                    <div class="boss-card" id="boss-charons-obols" style="opacity: 0.7; cursor: default;">
                        <div class="boss-card-img-wrapper">
                            <span class="boss-card-badge badge-unconfirmed">Verifizierung nötig</span>
                            <img src="/imgs/icon_boss.png" alt="Charon's Obols - Unverifiziert" class="boss-card-img" width="400" height="400" loading="lazy" style="filter: grayscale(60%);">
                        </div>
                        <div class="boss-card-body">
                            <h3>Charon's Obols</h3>
                            <div class="boss-card-meta">
                                <span><span class="meta-icon">📍</span> Unbekannt</span>
                                <span><span class="meta-icon">❓</span> Unbestätigt</span>
                            </div>
                            <p>Altseite aus älteren Daten. Querverweise auf Wiki-Quellen legen nahe, dass Charon's Obol ein Belohnungsgegenstand ist und kein Boss. Wird zur Nachverfolgung beibehalten, bis es im Spiel verifiziert ist.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <h2>Allgemeine Boss-Vorbereitung</h2>
                <p>Jeder Boss in Windrose belohnt gute Vorbereitung. Hier ist eine universelle Checkliste, bevor du eine Boss-Arena betrittst:</p>
                <table>
                    <caption>Boss-Vorbereitungs-Checkliste</caption>
                    <thead>
                        <tr>
                            <th scope="col">Kategorie</th>
                            <th scope="col">Empfehlung</th>
                            <th scope="col">Warum es wichtig ist</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Essens-Buffs</strong></td>
                            <td>Bacon and Eggs, Coconut Milk oder die beste verfügbare Mahlzeit</td>
                            <td>Erhöht die maximalen HP und die Ausdauer-Regeneration während des Kampfes</td>
                        </tr>
                        <tr>
                            <td><strong>Heilung</strong></td>
                            <td>Mindestens 10-15 Bandages, Tränke wenn verfügbar</td>
                            <td>Boss-Kämpfe sind lang; ohne Heilung bedeutet das einen Wipe</td>
                        </tr>
                        <tr>
                            <td><strong>Ausgeruht-Buff</strong></td>
                            <td>Schlafe an deinem Bonfire, bevor du zum Boss reist</td>
                            <td>Bietet einen passiven Statusbonus, der sich mit Essen stapelt</td>
                        </tr>
                        <tr>
                            <td><strong>Ausrüstungsstufe</strong></td>
                            <td>Erreiche oder übertriff die empfohlene Stufe des Bosses</td>
                            <td>Unterlevelte Ausrüstung führt zu wenig Schaden und hohem eingehenden Schaden</td>
                        </tr>
                        <tr>
                            <td><strong>Fernkampf-Option</strong></td>
                            <td>Bringe einen Blunderbuss oder eine Musket mit 20+ Kugeln mit</td>
                            <td>Fernkampfdruck ist sicherer Schaden; besonders nützlich zum Kiten</td>
                        </tr>
                        <tr>
                            <td><strong>Reparatur-Kits</strong></td>
                            <td>2-3 Repair Kits oder Combat Repair Kits</td>
                            <td>Waffen und Rüstung verschleißen während langer Kämpfe</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <h2>Boss-Drops Schnellübersicht</h2>
                <table>
                    <caption>Bekannte Boss-Drops (Community-Quellen)</caption>
                    <thead>
                        <tr>
                            <th scope="col">Boss</th>
                            <th scope="col">Bemerkenswerte Drops</th>
                            <th scope="col">Schaltet frei</th>
                            <th scope="col">Datenkonfidenz</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><a href="/de/bosses/thomas-richards/">Thomas Richards</a></td>
                            <td>50 XP, Thomas Richards' Tagebuch, Seafood Platter, Silver Ingot</td>
                            <td>Foothills-Biom, Iron-Tier-Fortschritt</td>
                            <td>Community</td>
                        </tr>
                        <tr>
                            <td><a href="/de/bosses/israel-hands/">Israel Hands</a></td>
                            <td>Soul-Eater-Großschwert, 30 Undead Essence, Charon's Obol</td>
                            <td>Cursed Swamps, nächstes Story-Tor</td>
                            <td>Community</td>
                        </tr>
                        <tr>
                            <td><a href="/de/bosses/high-priestess/">High Priestess</a></td>
                            <td>Charon's Obol</td>
                            <td>Ende der aktuellen Hauptstory (Kapitel 1)</td>
                            <td>Community</td>
                        </tr>
                        <tr>
                            <td><a href="/de/bosses/ghost-captain/">Ghost Captain</a></td>
                            <td>Soul-Eater-Großschwert</td>
                            <td>Optionale Beuteroute</td>
                            <td>Community</td>
                        </tr>
                    </tbody>
                </table>
                <p class="update-note"><strong>Datenhinweis:</strong> Windrose befindet sich im Early Access (v0.10.0.5.120). Boss-Drops und -Mechaniken können sich mit Patches ändern. Alle Daten auf dieser Seite stammen aus der Community und werden aktualisiert, sobald offizielle Informationen verfügbar sind.</p>
            </div>
        </section>

        <section class="content-section">
            <div class="container">
                <h2>Häufig gestellte Fragen</h2>
                <details>
                    <summary>Wie viele Bosse gibt es in Windrose?</summary>
                    <div class="faq-answer"><p>Die aktuellen Early-Access-Inhalte umfassen 3 bestätigte Story-Arena-Bosse (Thomas Richards, Israel Hands, High Priestess) und 1 optionale Dungeon-Begegnung (Ghost Captain). Weitere Bosse werden im Verlauf der Entwicklung erwartet.</p></div>
                </details>
                <details>
                    <summary>Wie ist die Boss-Reihenfolge in Windrose?</summary>
                    <div class="faq-answer"><p>Die Fortschrittsreihenfolge lautet: Thomas Richards (Coastal Jungle, Lv 5-6) → Israel Hands (Foothills, Lv 8-10) → High Priestess (Cursed Swamps, Lv 12-15). Ghost Captain ist optional und kann um Lv 10-12 bekämpft werden.</p></div>
                </details>
                <details>
                    <summary>Kann ich Bosse im Koop bekämpfen?</summary>
                    <div class="faq-answer"><p>Ja! Windrose unterstützt Koop für 1-8 Spieler. Bosse skalieren mit der Spieleranzahl, aber mit Teamkollegen, die Aggro aufteilen, werden die Kämpfe deutlich einfacher.</p></div>
                </details>
                <details>
                    <summary>Sind alle Boss-Drops bestätigt?</summary>
                    <div class="faq-answer"><p>Nein. Early-Access-Daten können sich ändern, daher sollten exakte Drops nach Patches erneut überprüft und mit Quellen-Konfidenz markiert werden. Wir kennzeichnen alle unverifizierten Daten als „Community"-Quelle.</p></div>
                </details>
                <details>
                    <summary>Was ist die beste Waffe für Boss-Kämpfe?</summary>
                    <div class="faq-answer"><p>Ein Saber für den Nahkampf (schnelle Combos) kombiniert mit einem Blunderbuss zum Fernkampf-Kiten ist im Allgemeinen die effektivste Kombination. Das Soul-Eater-Großschwert wird verfügbar, nachdem du Israel Hands oder Ghost Captain besiegt hast.</p></div>
                </details>
            </div>
        </section>

        <aside class="related-guides">
            <div class="container">
                <h2>Verwandte Leitfäden</h2>
                <ul>
                    <li><a href="/de/guides/boss-progression/">Boss-Fortschritts- & Strategie-Leitfaden</a></li>
                    <li><a href="/de/beginner-guide/">Anfänger-Leitfaden — Tag 1-10</a></li>
                    <li><a href="/de/crafting/workbench/">Workbench-Rezepte Lv1-3</a></li>
                    <li><a href="/de/guides/best-early-builds/">Beste Early-Game-Builds</a></li>
                    <li><a href="/de/database/bosses/">Datenbank: Boss-Liste</a></li>
                </ul>
            </div>
        </aside>
    </main>

__FOOTER__
__HAMBURGER_JS__
</body>
</html>
"""


def main():
    header = header_html("bosses", "de", current_path="/bosses")
    footer = footer_html("de")
    out = (HTML
           .replace("__HEADER__", header)
           .replace("__FOOTER__", footer)
           .replace("__HAMBURGER_JS__", HAMBURGER_JS))
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(out, encoding="utf-8")
    print(f"Wrote {DEST} ({len(out)} bytes)")


if __name__ == "__main__":
    main()
