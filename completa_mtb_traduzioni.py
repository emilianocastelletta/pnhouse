#!/usr/bin/env python3
"""Complete MTB card in missing PN HOUSE languages; leave existing cards unchanged."""
from pathlib import Path
from html import escape
import re
import shutil
from datetime import datetime

ROOT = Path(__file__).resolve().parent
URL = 'https://www.komoot.com/it-it/guide/607329/mtb-trails-around-san-gemini'
PADEL = 'https://www.facebook.com/HappyVillageTerni'
DATA = {
    'it': ('MTB', 'Mountain bike a San Gemini', 'Scopri gli itinerari MTB nei dintorni di San Gemini e scegli quello più adatto alla tua esperienza. Verifica tracciato e condizioni prima di partire.', 'Esplora i percorsi su Komoot'),
    'en': ('MTB', 'Mountain biking around San Gemini', 'Explore mountain bike routes around San Gemini and choose one suited to your experience. Check the route and conditions before setting out.', 'Explore routes on Komoot'),
    'fr': ('VTT', 'VTT autour de San Gemini', 'Découvrez les itinéraires VTT autour de San Gemini et choisissez celui qui correspond à votre expérience. Vérifiez le parcours et les conditions avant de partir.', 'Explorer les parcours sur Komoot'),
    'es': ('MTB', 'Bicicleta de montaña en San Gemini', 'Descubre rutas de bicicleta de montaña cerca de San Gemini y elige una adecuada a tu experiencia. Comprueba el recorrido y las condiciones antes de salir.', 'Explorar rutas en Komoot'),
    'ru': ('MTB', 'Горные велосипеды в окрестностях Сан-Джемини', 'Изучите маршруты для горного велосипеда рядом с Сан-Джемини и выберите подходящий по уровню подготовки. Перед поездкой проверьте маршрут и условия.', 'Посмотреть маршруты на Komoot'),
    'de': ('MTB', 'Mountainbiken rund um San Gemini', 'Entdecken Sie MTB-Routen rund um San Gemini und wählen Sie eine Tour passend zu Ihrer Erfahrung. Prüfen Sie Strecke und Bedingungen vor der Fahrt.', 'Routen auf Komoot entdecken'),
}
CARD_RE = re.compile(r'<article\b[^>]*class=["\']card["\'][^>]*>.*?</article>', re.I | re.S)

def main():
    updates = {}
    for lang, (category, title, desc, label) in DATA.items():
        path = ROOT / ('funandactivity.html' if lang == 'it' else f'{lang}/funandactivity.html')
        if not path.is_file():
            raise SystemExit(f'Manca {path}: nessuna modifica eseguita.')
        text = path.read_text(encoding='utf-8')
        cards = list(CARD_RE.finditer(text))
        mtb_cards = [m for m in cards if URL in m.group() or re.search(r'<span class=["\']num["\']>\s*06\s*/', m.group())]
        if mtb_cards:
            if len(mtb_cards) == 1 and URL in mtb_cards[0].group() and len(cards) == 6:
                print(f'{path.relative_to(ROOT)}: MTB già presente, invariato')
                continue
            raise SystemExit(f'{path}: scheda 06 inattesa o duplicata; nessuna modifica eseguita.')
        if len(cards) != 5 or PADEL not in cards[-1].group() or not re.search(r'<span class=["\']num["\']>\s*05\s*/', cards[-1].group()):
            raise SystemExit(f'{path}: la quinta scheda non è Padel; nessuna modifica eseguita.')
        card = ('\n<article class="card"><span class="num">06 / ' + escape(category) + '</span>'
                '<h3>' + escape(title) + '</h3><p>' + escape(desc) + '</p>'
                '<a href="' + URL + '" target="_blank" rel="noopener noreferrer">'
                + escape(label) + ' ↗</a></article>')
        end = cards[-1].end()
        updated = text[:end] + card + text[end:]
        if len(CARD_RE.findall(updated)) != 6 or updated.count(URL) != 1:
            raise SystemExit(f'{path}: controllo finale fallito; nessuna modifica eseguita.')
        updates[path] = updated
    if not updates:
        print('Tutte le sei pagine contengono già MTB: nessuna modifica.'); return
    # Backup outside the repository. Abort if the destination already exists.
    backup = ROOT.parent / ('pnhouse-backup-mtb-traduzioni-' + datetime.now().strftime('%Y%m%d-%H%M%S'))
    if backup.exists(): raise SystemExit(f'Backup già presente: {backup}')
    backup.mkdir()
    for path in updates:
        target = backup / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    for path, text in updates.items():
        path.write_text(text, encoding='utf-8')
        print(f'{path.relative_to(ROOT)}: MTB aggiunta')
    print('Backup:', backup)
    print('Nessun commit o push eseguito.')

if __name__ == '__main__': main()
