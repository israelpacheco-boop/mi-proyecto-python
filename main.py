"""Script de verificacion del entorno de trabajo.

Comprueba que el entorno virtual (.venv) y las librerias de
automatizacion estan correctamente instalados y listos para usar.
"""

import sys
from pathlib import Path

# --- Librerias requeridas -------------------------------------------------
# (nombre del modulo, nombre del paquete en pip, version minima)
LIBRERIAS = [
    ("requests", "requests", "2.31.0"),
    ("bs4", "beautifulsoup4", "4.12.0"),
    ("pandas", "pandas", "2.0.0"),
    ("openpyxl", "openpyxl", "3.1.0"),
    ("pypdf", "pypdf", "4.0.0"),
]


def comparar_versiones(instalada, minima):
    """Compara dos versiones numericas (ej. '2.31.0' vs '4.0.0')."""
    return tuple(map(int, instalada.split(".")[:3])) >= tuple(
        map(int, minima.split(".")[:3])
    )


def verificar_entorno():
    """Verifica cada libreria y devuelve una lista de (paquete, estado, detalle)."""
    resultados = []

    for modulo, paquete, minima in LIBRERIAS:
        try:
            mod = __import__(modulo)
            version = getattr(mod, "__version__", "desconocida")
            suficiente = comparar_versiones(version, minima)
            if suficiente:
                estado = "OK"
                detalle = f"v{version} (min v{minima})"
            else:
                estado = "ADVERTENCIA"
                detalle = f"v{version} es menor que v{minima}"
        except ImportError:
            estado = "ERROR"
            detalle = "no instalado"
        resultados.append((paquete, estado, detalle))

    return resultados


def main():
    print("=" * 52)
    print(" Verificacion del entorno - mi-proyecto-python")
    print("=" * 52)

    # Python y entorno virtual
    print(f"\n[Python]     {sys.version.split()[0]}")
    print(f"[Ejecutable] {sys.executable}")

    raiz = Path(__file__).parent
    if (raiz / ".venv").is_dir():
        print(f"[Entorno]    .venv detectado en {raiz / '.venv'}")
    else:
        print("[Entorno]    ADVERTENCIA: no se encontro la carpeta .venv")

    # Librerias
    print("\nLibrerias:")
    resultados = verificar_entorno()
    for paquete, estado, detalle in resultados:
        print(f"  [{estado:^11}] {paquete:<15} {detalle}")

    # Resumen
    errores = [r for r in resultados if r[1] == "ERROR"]
    advertencias = [r for r in resultados if r[1] == "ADVERTENCIA"]

    print("\n" + "-" * 52)
    if errores:
        print(f" RESULTADO: {len(errores)} libreria(s) con errores.")
        print(" Ejecuta:  pip install -r requirements.txt")
        return 1
    if advertencias:
        print(f" RESULTADO: todo instalado, {len(advertencias)} advertencia(s).")
        return 0

    print(" RESULTADO: entorno listo para automatizacion y scripting.")
    print("=" * 52)
    return 0


if __name__ == "__main__":
    sys.exit(main())
