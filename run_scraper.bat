@echo off
REM ============================================================
REM  Automatizador del scraper de noticias legales
REM  Activa el entorno virtual .venv y ejecuta news_scraper.py
REM  de forma silenciosa, registrando la salida en un log.
REM ============================================================

REM Cambia al directorio del proyecto (raiz del repo).
cd /d "%~dp0"

REM Configura la ventana para que no aparezca durante la ejecucion.
set PYTHONIOENCODING=utf-8
set PYTHONUNBUFFERED=1

REM Comprueba que el entorno virtual exista.
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] No se encontro el entorno virtual .venv
    echo Ejecuta:  python -m venv .venv
    echo           .venv\Scripts\python.exe -m pip install -r requirements.txt
    exit /b 1
)

REM Crea la carpeta logs\ si no existe.
if not exist "logs\" mkdir "logs"

REM Ejecuta el scraper. Cada ejecucion genera su propio log con fecha,
REM de modo que no se sobrescribe el historial anterior.
REM La fecha se obtiene del propio Python (.venv) en formato ISO
REM AAAA-MM-DD: es independiente de la configuracion regional de
REM Windows, a diferencia de parsear %DATE%.
for /f %%f in ('call ".venv\Scripts\python.exe" -c "import datetime; print(datetime.date.today().isoformat())"') do set FECHA=%%f
if not defined FECHA set FECHA=sin-fecha
set LOG=logs\scraper_%FECHA%.log

".venv\Scripts\python.exe" news_scraper.py > "%LOG%" 2>&1

REM Comprueba el codigo de salida de Python.
if errorlevel 1 (
    echo [ERROR] El scraper termino con errores. Ver "%LOG%"
    exit /b 1
)

echo [OK] Scraper ejecutado correctamente. Log: %LOG%
exit /b 0
