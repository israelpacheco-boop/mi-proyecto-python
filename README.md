# mi-proyecto-python

Estructura base de un proyecto en Python, creada con la ayuda de
[Cline](https://cline.bot) (un asistente de programación con IA).

## Estructura

```
mi-proyecto-python/
├── main.py           # Punto de entrada del programa
├── requirements.txt  # Dependencias del proyecto (vacío por ahora)
├── .gitignore        # Archivos excluidos del control de versiones
└── README.md         # Este archivo
```

## Requisitos

- Python 3.6 o superior
- Git

## Uso

```bash
python main.py
```

Salida esperada:

```
Hola Mundo
```

## Dependencias

Este proyecto no tiene dependencias todavía. Para instalar las que se agreguen
en el futuro:

```bash
pip install -r requirements.txt
```

## Notas

- `.gitignore` ya está preparado para entornos virtuales (`.venv/`, `env/`),
  cachés de Python (`__pycache__/`), variables de entorno (`.env`) y
  configuraciones de IDE, de modo que esos archivos no se subirán al
  repositorio por accidente.
- Todo el código de este repositorio se versiona con Git usando la rama
  principal `main`.

## Licencia

Sin licencia especificada por ahora.
