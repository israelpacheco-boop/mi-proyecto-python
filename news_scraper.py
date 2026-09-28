"""Recopilador de noticias del sector legal.

Extrae titulares de dos fuentes publicas y los unifica en un DataFrame:
  1. elderecho.com  - seccion 'Inteligencia Artificial y Derecho'
  2. law360.com     - portada de noticias legales

Uso:
    .\\.venv\\Scripts\\python.exe news_scraper.py

Nota sobre selectores: los titulares de law360.com NO estan en <h1> ni
<h3> (sus <h1> son nombres de marca). Se extraen de los enlaces
<a href="/articles/..."> de la portada. Ver LEEME en el bloque de
comentarios de cada funcion.
"""

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

# --- Configuracion --------------------------------------------------------
URL_ELDERECHO = "https://elderecho.com/inteligencia-artificial-y-derecho"
URL_LAW360 = "https://law360.com"

ARCHIVO_SALIDA = Path(__file__).parent / "noticias_legales.xlsx"
TIMEOUT = 25

# User-Agent explicito: sin el, ambos sitios responden 403.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

COLUMNAS = ["Fuente", "Seccion", "Titulo", "Autor", "Fecha de Extraccion"]


def obtener_soup(url):
    """Descarga una pagina y devuelve su BeautifulSoup, o None si falla."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
    except requests.RequestException as error:
        print(f"  [ERROR] {url} -> {error}")
        return None
    return BeautifulSoup(r.text, "html.parser")


def scrape_elderecho(fecha):
    """Articulos de la seccion de IA y Derecho.

    Selectores verificados sobre el HTML real:
      - div.excerpt  -> contenedor de cada articulo
      - h3           -> titulo
      - p / span     -> autor y fecha dentro del contenedor
    """
    soup = obtener_soup(URL_ELDERECHO)
    if soup is None:
        return []

    filas = []
    for contenedor in soup.select("div.excerpt"):
        titulo_tag = contenedor.select_one("h3")
        if not titulo_tag:
            continue

        # El autor real esta en <address class="author"><span rel="author">.
        autor_tag = contenedor.select_one(
            'address.author span[rel="author"], address.author'
        )
        autor = autor_tag.get_text(strip=True) if autor_tag else ""

        filas.append(
            {
                "Fuente": "elderecho.com",
                "Seccion": "Inteligencia Artificial y Derecho",
                "Titulo": titulo_tag.get_text(strip=True),
                "Autor": autor or "No indicado",
                "Fecha de Extraccion": fecha,
            }
        )
    return filas


def scrape_law360(fecha):
    """Titulares de la portada de law360.com.

    Selectores verificados sobre el HTML real:
      - a[href^="/articles/"] -> enlace al articulo; su texto es el titular
      - h2                    -> nombres de las secciones de la pagina
        (The Practice of Law, Deep News & Analysis, etc.)
    Los autores NO se publican en la portada, solo en la ficha del articulo.
    """
    soup = obtener_soup(URL_LAW360)
    if soup is None:
        return []

    # Subsecciones publicadas como <h2> en la portada.
    subsecciones = [
        h.get_text(" ", strip=True)
        for h in soup.select("h2")
        if h.get_text(" ", strip=True)
    ]

    filas = []
    vistos = set()

    for enlace in soup.select('a[href^="/articles/"]'):
        titulo = enlace.get_text(" ", strip=True)
        # Filtra ruido de navegacion: 'Read Full Article', '(read more)'...
        if not titulo or len(titulo) < 25 or titulo in vistos:
            continue
        if titulo.lower().startswith(("read ", "(read", "sign in", "subscribe")):
            continue

        vistos.add(titulo)
        filas.append(
            {
                "Fuente": "law360.com",
                "Seccion": subsecciones[0] if subsecciones else "Portada",
                "Titulo": titulo,
                "Autor": "No publicado en portada",
                "Fecha de Extraccion": fecha,
            }
        )
    return filas


def main():
    print("=" * 60)
    print(" Recopilador de noticias legales")
    print("=" * 60)

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n[1/2] elderecho.com ...")
    filas_elderecho = scrape_elderecho(fecha)
    print(f"      {len(filas_elderecho)} articulos")

    print("[2/2] law360.com ...")
    filas_law360 = scrape_law360(fecha)
    print(f"      {len(filas_law360)} titulares")

    todas = filas_elderecho + filas_law360

    if not todas:
        print("\nNo se obtuvo ninguna noticia.")
        return 1

    df = pd.DataFrame(todas, columns=COLUMNAS)

    print("\nResumen por fuente:")
    print(df.groupby("Fuente").size().to_string())

    print("\nPrimeras 5 filas:")
    print(df.head(5)[["Fuente", "Seccion", "Titulo"]].to_string(index=False))

    df.to_excel(ARCHIVO_SALIDA, index=False, engine="openpyxl",
                sheet_name="Noticias")
    print(f"\nArchivo generado: {ARCHIVO_SALIDA}")
    print(f"Tamano: {ARCHIVO_SALIDA.stat().st_size} bytes")
    print(f"Total de registros: {len(df)}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
