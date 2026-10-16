#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PY=/usr/bin/python3
missing=()
dpkg -s python3-reportlab >/dev/null 2>&1 || missing+=(python3-reportlab)
dpkg -s python3-pil >/dev/null 2>&1 || missing+=(python3-pil)
dpkg -s fontforge >/dev/null 2>&1 || missing+=(fontforge)
if ((${#missing[@]})); then
  echo "Mancano questi pacchetti Ubuntu: ${missing[*]}"
  echo "Esegui: sudo apt update && sudo apt install -y ${missing[*]}"
  exit 1
fi
"$PY" generate_pnhouse_guides.py
