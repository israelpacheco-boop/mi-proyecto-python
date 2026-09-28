# mi-proyecto-python

Estructura base de un proyecto en Python, creada con la ayuda de
[Cline](https://cline.bot) (un asistente de programación con IA).

## Estructura

```
mi-proyecto-python/
├── main.py                 # Verifica que el entorno y las librerias estén listos
├── scraper.py              # Scraper de ejemplo (quotes.toscrape.com -> Excel)
├── news_scraper.py         # Noticias legales (elderecho.com + law360.com -> Excel)
├── run_scraper.bat         # Ejecutor de Windows: activa .venv y lanza el scraper
├── logs/                   # Logs con fecha de cada ejecucion (generado)
├── requirements.txt        # Dependencias del proyecto
├── .gitignore              # Archivos excluidos del control de versiones
└── README.md               # Este archivo
```

## Requisitos

- Python 3.6 o superior
- Git

## Configuracion inicial

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Uso

Verificar que el entorno esta listo:

```bash
.venv\Scripts\python.exe main.py
```

Ejecutar los scrapers:

```bash
.venv\Scripts\python.exe scraper.py
.venv\Scripts\python.exe news_scraper.py
```

Ambos generan un archivo Excel: `resultados_scraping.xlsx` y
`noticias_legales.xlsx` respectivamente.

## Dependencias

| Paquete | Uso |
|---|---|
| `requests` | Peticiones HTTP |
| `beautifulsoup4` | Analisis de HTML (web scraping) |
| `pandas` | Manipulacion de datos tabulares |
| `openpyxl` | Lectura y escritura de archivos Excel |
| `pypdf` | Lectura y escritura de archivos PDF |

Para instalarlas:

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Automatizacion en Windows

El scraper de noticias puede ejecutarse solo, todos los dias a las 8:00 AM,
mediante una tarea programada de Windows.

### 1. El archivo ejecutor

`run_scraper.bat` es un archivo por lotes que:

1. Cambia al directorio del proyecto (`cd /d "%~dp0"`), de modo que funciona
   sin importar desde donde se invoque.
2. Comprueba que el entorno virtual `.venv` exista. Si falta, muestra las
   instrucciones para crearlo y termina con error.
3. Ejecuta `news_scraper.py` con el interprete del entorno virtual,
   redirigiendo toda la salida a `scraper_log.txt`.
4. Propaga el codigo de salida de Python, de modo que quede registrado si la
   ejecucion fue correcta o fallo.

El modo "silencioso" se logra redirigiendo la salida a un archivo de log
en lugar de mostrarla por pantalla.

Para ejecutarlo manualmente:

```bat
run_scraper.bat
```

### 2. La tarea programada

Se creo con el comando:

```bat
schtasks /create /tn "Actualizacion_Noticias_Legales" /tr "C:\Users\israe\Documents\mi-proyecto-python\run_scraper.bat" /sc daily /st 08:00
```

Para consultar su estado:

```bat
schtasks /query /tn "Actualizacion_Noticias_Legales" /fo list /v
```

Campos clave: `Next Run Time` (proxima ejecucion), `Last Run Time` (ultima
ejecucion) y `Last Result` (codigo de salida; `0` significa correcto).

Para ejecutarla al instante, sin esperar a las 8:00:

```bat
schtasks /run /tn "Actualizacion_Noticias_Legales"
```

Para eliminarla:

```bat
schtasks /delete /tn "Actualizacion_Noticias_Legales" /f
```

> **Importante:** la tarea se ejecuta con los permisos del usuario que la creo
> (`israelpacheco-boop`). Si el equipo esta bloqueado o en suspension a las
> 8:00 AM, la ejecucion se omitira. El PC debe estar encendido y con sesion
> iniciada a esa hora.

### 3. Comprobar los registros

Cada ejecucion genera su propio archivo de log con marca de tiempo dentro de
la carpeta `logs/`, con el formato `scraper_AAAA-MM-DD.log`. La carpeta se
crea automaticamente si no existe.

Esto significa que **el log del dia se sobrescribe en cada corrida de ese
dia**, pero los dias anteriores se conservan. Por ejemplo, tras varios dias
la carpeta contendra:

```
logs/
├── scraper_2026-09-28.log
├── scraper_2026-09-29.log
└── scraper_2026-09-30.log
```

Para listar los logs disponibles:

```bat
dir logs
```

Para ver el contenido completo de uno:

```bat
type logs\scraper_2026-09-28.log
```

Para ver solo las ultimas lineas:

```bash
Get-Content logs\scraper_$(Get-Date -Format yyyy-MM-dd).log -Tail 20
```

Buscar errores en el log del dia:

```bash
Select-String -Path logs\*.log -Pattern "ERROR", "REINTENTO"
```

El log incluye el retardo aleatorio aplicado entre peticiones, los reintentos
ante errores HTTP 429, el detalle de la deduplicacion del historico y un
resumen con el total de registros extraidos por cada fuente.

### 4. Historico acumulado de noticias

`noticias_legales.xlsx` no se sobrescribe: acumula el historico.

En cada ejecucion, si el archivo ya existe, el script:

1. Lee el archivo previo con `pandas.read_excel()`.
2. Lo concatena con las noticias recien extraidas.
3. Elimina las filas cuyo titulo ya estaba presente, usando
   `drop_duplicates(subset=["Titulo"], keep="first")`.
4. Guarda de nuevo el conjunto completo.

La deduplicacion se hace por la columna `Titulo` y conserva la primera
aparicion, de modo que cada noticia mantiene la fecha en que fue vista por
primera vez. La columna `Fecha de Extraccion` permite saber de que corrida
procede cada registro.

Los archivos `.xlsx`, `.log` y la carpeta `logs/` estan excluidos en
`.gitignore`: son datos generados, no codigo fuente, y se regeneran ejecutando
los scripts.

## Notas

- `.gitignore` ya está preparado para entornos virtuales (`.venv/`, `env/`),
  cachés de Python (`__pycache__/`), variables de entorno (`.env`),
  configuraciones de IDE y datos generados (`*.xlsx`, `*.log`), de modo que
  esos archivos no se subirán al repositorio por accidente.
- Todo el código de este repositorio se versiona con Git usando la rama
  principal `main`.
- Los scrapers aplican un retardo aleatorio de 2 a 4 segundos entre
  peticiones, y reintentan hasta 3 veces ante un error HTTP 429, para no
  bloquear la IP de origen.

## Licencia

Sin licencia especificada por ahora.
