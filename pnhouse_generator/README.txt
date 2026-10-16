PN HOUSE - GENERATORE PDF ANTHROPIC v3 PER WSL

Questa versione corregge l'errore:
  postscript outlines are not supported

Gli OTF Anthropic usano contorni PostScript/CFF, non leggibili direttamente da ReportLab.
Il generatore scarica gli OTF e li converte automaticamente in TTF tramite FontForge,
quindi usa i TTF convertiti nei PDF.

INSTALLAZIONE UNA TANTUM:
  sudo apt update
  sudo apt install -y python3-reportlab python3-pil fontforge

ESECUZIONE:
  cd PN_HOUSE_Generatore_Anthropic_v3
  bash run_wsl.sh

OUTPUT:
  output_pdf/PN_HOUSE_Explore_Guide_IT.pdf
  output_pdf/PN_HOUSE_Explore_Guide_EN.pdf
  output_pdf/PN_HOUSE_Explore_Guide_FR.pdf
  output_pdf/PN_HOUSE_Explore_Guide_ES.pdf
  output_pdf/PN_HOUSE_Explore_Guide_DE.pdf
  output_pdf/PN_HOUSE_Explore_Guide_RU.pdf
