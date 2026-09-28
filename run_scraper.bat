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

REM Ejecuta el scraper. La salida se guarda en scraper_log.txt
REM y no se muestra en pantalla (silencioso).
".venv\Scripts\python.exe" news_scraper.py > scraper_log.txt 2>&1

REM Comprueba el codigo de salida de Python.
if errorlevel 1 (
    echo [ERROR] El scraper termino con errores. Ver scraper_log.txt
    exit /b 1
)

echo [OK] Scraper ejecutado correctamente. Log: scraper_log.txt
exit /b 0
