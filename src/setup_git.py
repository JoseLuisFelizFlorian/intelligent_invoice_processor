import os

folders = [
    "data/01_raw",
    "data/02_processed",
    "data/03_errors",
    "data/database",
    "logs"
]

for folder in folders:
    # Crear ruta completa
    path = os.path.join(os.getcwd(), folder)
    # Crear carpeta si no existe
    os.makedirs(path, exist_ok=True)
    # Crear archivo .gitkeep
    with open(os.path.join(path, ".gitkeep"), "w") as f:
        pass # Crear archivo vacío
    print(f" .gitkeep creado en: {folder}")