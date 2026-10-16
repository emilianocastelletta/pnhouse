from pathlib import Path
import re

VERSION = "1.2.0"

ROOT = Path(".")

PAGES = {
    "index.html": {
        "title": "Attività & Divertimento",
        "desc": "Padel, tennis, mountain bike, eventi e tante attività per vivere al meglio il territorio di San Gemini e dintorni.",
        "link": "Scopri le attività →",
        "href": "funandactivity.html"
    },
    "en/index.html": {
        "title": "Fun & Activities",
        "desc": "Padel, tennis, mountain biking, events and many activities to enjoy San Gemini and its surroundings.",
        "link": "Discover activities →",
        "href": "../funandactivity.html"
    },
    "fr/index.html": {
        "title": "Activités & Loisirs",
        "desc": "Padel, tennis, VTT, événements et nombreuses activités pour découvrir San Gemini et ses environs.",
        "link": "Découvrir les activités →",
        "href": "../funandactivity.html"
    },
    "es/index.html": {
        "title": "Actividades y Ocio",
        "desc": "Pádel, tenis, ciclismo MTB, eventos y muchas actividades para disfrutar de San Gemini y sus alrededores.",
        "link": "Descubrir actividades →",
        "href": "../funandactivity.html"
    },
    "de/index.html": {
        "title": "Freizeit & Aktivitäten",
        "desc": "Padel, Tennis, Mountainbike, Veranstaltungen und viele weitere Aktivitäten rund um San Gemini.",
        "link": "Aktivitäten entdecken →",
        "href": "../funandactivity.html"
    },
    "ru/index.html": {
        "title": "Развлечения и Активности",
        "desc": "Падел, теннис, горный велосипед, мероприятия и множество развлечений в Сан-Джемини и окрестностях.",
        "link": "Узнать больше →",
        "href": "../funandactivity.html"
    }
}

CARD = """
<a href    <div class="feature-number">03</div>
    <h3>{title}</h3>
    <p>{desc}</p>
    <span class="feature-link">{link}</span>
</a>
"""

RESPONSIVE_BLOCK = """

/* =====================================================
   RELEASE 1.2.0
   ===================================================== */

@media (max-width: 768px) {

    .features-grid {
        grid-template-columns: 1fr !important;
        gap: 1rem;
    }

    .feature-card {
        padding: 1.2rem;
    }

    .feature-number {
        font-size: 1.8rem;
    }

    .feature-card h3 {
        font-size: 1.2rem;
    }

    .feature-card p {
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .feature-link {
        font-size: 0.95rem;
    }
}
"""

def update_version(html):
    html = re.sub(
        r'(\d+\.\d+\.\d+)',
        VERSION,
        html,
        count=1
    )
    return html


for file_path, card in PAGES.items():

    path = ROOT / file_path

    if not path.exists():
        print(f"SKIP {file_path}")
        continue

    html = path.read_text(encoding="utf-8")

    html = update_version(html)

    if card["title"] not in html:

        new_card = CARD.format(**card)

        m = re.search(
            r'(<a[^>]*class="feature-card"[^>]*>.*?</a>\s*</div>)',
            html,
            flags=re.DOTALL
        )

        if m:
            html = html.replace(
                m.group(1),
                m.group(1) + "\n" + new_card
            )

    path.write_text(html, encoding="utf-8")
    print(f"UPDATED {file_path}")

css = ROOT / "assets" / "style.css"

if css.exists():

    content = css.read_text(encoding="utf-8")

    if "RELEASE 1.2.0" not in content:
        content += RESPONSIVE_BLOCK
        css.write_text(content, encoding="utf-8")
        print("UPDATED assets/style.css")

print()
print("========== COMPLETATO ==========")
print("Versione sito aggiornata a 1.2.0")
print("Card Fun & Activity aggiunta")
print("Responsive mobile aggiunto")