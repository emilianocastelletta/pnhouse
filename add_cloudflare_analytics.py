from pathlib import Path
import shutil
from datetime import datetime

ROOT = Path(__file__).resolve().parent

TOKEN = "18e69ea9ef414a25a74eef29d0ac1e6f"

CLOUDFLARE_SNIPPET = f"""<!-- Cloudflare Web Analytics -->
<script type='module'
        src='https://static.cloudflareinsights.com/beacon.min.js'
        data-cf-beacon='{{"token": "{TOKEN}"}}'></script>
<!-- End Cloudflare Web Analytics -->"""

BACKUP_DIR = ROOT / f"backup_before_analytics_{datetime.now():%Y%m%d_%H%M%S}"

updated = []
already_present = []
errors = []

html_files = sorted(ROOT.rglob("*.html"))

print("=" * 60)
print("PN HOUSE - Cloudflare Web Analytics")
print("=" * 60)
print(f"File HTML trovati: {len(html_files)}")
print()

for path in html_files:

    # Ignora eventuali backup creati precedentemente
    if any(part.startswith("backup_before_analytics_") for part in path.parts):
        continue

    relative_path = path.relative_to(ROOT)

    try:
        content = path.read_text(encoding="utf-8")

        # Evita l'inserimento doppio
        if TOKEN in content or "data-cf-beacon" in content:
            already_present.append(str(relative_path))
            print(f"[SKIP] {relative_path} - Analytics gia presente")
            continue

        # Verifica che la pagina abbia </body>
        body_position = content.lower().rfind("</body>")

        if body_position == -1:
            errors.append(str(relative_path))
            print(f"[WARN] {relative_path} - tag </body> non trovato")
            continue

        # Crea il backup mantenendo la struttura delle cartelle
        backup_path = BACKUP_DIR / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup_path)

        new_content = (
            content[:body_position].rstrip()
            + "\n\n"
            + CLOUDFLARE_SNIPPET
            + "\n"
            + content[body_position:]
        )

        path.write_text(new_content, encoding="utf-8")

        updated.append(str(relative_path))
        print(f"[OK]   {relative_path}")

    except Exception as exc:
        errors.append(str(relative_path))
        print(f"[ERR]  {relative_path}: {exc}")


print()
print("=" * 60)
print("RIEPILOGO")
print("=" * 60)
print(f"Aggiornati:        {len(updated)}")
print(f"Gia configurati:   {len(already_present)}")
print(f"Errori/avvisi:     {len(errors)}")

if updated:
    print(f"\nBackup creato in:\n{BACKUP_DIR.name}")

if errors:
    print("\nFile da controllare:")
    for item in errors:
        print(f"  - {item}")

print()
print("Operazione completata.")
