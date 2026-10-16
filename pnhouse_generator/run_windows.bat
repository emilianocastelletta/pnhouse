@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python non trovato. Installa Python 3 da python.org selezionando "Add Python to PATH".
  pause
  exit /b 1
)
if not exist .venv py -3 -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install reportlab pillow
python generate_pnhouse_guides.py
if errorlevel 1 (
  echo.
  echo Generazione non completata. Leggi il messaggio sopra.
  pause
  exit /b 1
)
echo.
echo PDF creati nella cartella output_pdf.
pause
