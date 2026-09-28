"""Web scraper de ejemplo.

Descarga las citas de quotes.toscrape.com (sitio de pruebas designed
para practicing scraping), extrae el texto, el autor y las etiquetas,
y guarda el resultado en un archivo Excel.

Uso:
    .\\.venv\\Scripts\\python.exe scraper.py
"""

import sys
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

# --- Configuracion --------------------------------------------------------
URL_BASE = "https://quotes.toscrape.com"
ARCHIVO_SALIDA = Path(__file__).parent / "resultados_scraping.xlsx"
MAX_PAGINAS = 3  # 3 paginas x 10 citas = 30 registros
TIMEOUT = 20

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "mi-proyecto-python-scraper/1.0"
    )
}


def obtener_soup(url):
    """Descarga una pagina y devuelve su BeautifulSoup, o None si falla."""
    try:
        respuesta = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        respuesta.raise_for_status()
    except requests.RequestException as error:
        print(f"  [ERROR] No se pudo descargar {url}: {error}")
        return None
    return BeautifulSoup(respuesta.text, "html.parser")


def extraer_citas(soup):
    """Extrae (texto, autor, etiquetas) de cada cita de la pagina."""
    filas = []
    for cita in soup.select("div.quote"):
        texto = cita.select_one("span.text")
        autor = cita.select_one("small.author")
        etiquetas = [
            tag.get_text(strip=True)
            for tag in cita.select("div.tags a.tag")
        ]

        if not texto or not autor:
            continue

        filas.append(
            {
                "Texto": texto.get_text(strip=True).lstrip("\u201c").rstrip("\u201d"),
                "Autor": autor.get_text(strip=True),
                "Etiquetas": ", ".join(etiquetas),
            }
        )
    return filas


def scrapear(max_paginas=MAX_PAGINAS):
    """Recorre las paginas del sitio y devuelve un DataFrame."""
    todas = []

    for numero in range(1, max_paginas + 1):
        url = f"{URL_BASE}/page/{numero}/"
        print(f"Descargando pagina {numero}/{max_paginas}...")

        soup = obtener_soup(url)
        if soup is None:
            break

        filas = extraer_citas(soup)
        if not filas:
            print("  No se encontraron citas; finalizando.")
            break

        todas.extend(filas)
        print(f"  {len(filas)} citas extraidas")

    return pd.DataFrame(todas)


def guardar_excel(df, ruta=ARCHIVO_SALIDA):
    """Guarda el DataFrame en un archivo Excel con openpyxl."""
    df.to_excel(ruta, index=False, engine="openpyxl", sheet_name="Citas")
    return ruta


def main():
    print("=" * 52)
    print(" Scraper de quotes.toscrape.com")
    print("=" * 52)

    df = scrapear()

    if df.empty:
        print("\nNo se obtuvo ningun dato. Abortando.")
        return 1

    print(f"\nTotal de citas extraidas: {len(df)}")
    print("\nPrimeras 3 filas:")
    print(df.head(3).to_string(index=False))

    ruta = guardar_excel(df)
    print(f"\nArchivo generado: {ruta}")
    print(f"Tamano: {ruta.stat().st_size} bytes")
    print("=" * 52)
    return 0


if __name__ == "__main__":
    sys.exit(main())
