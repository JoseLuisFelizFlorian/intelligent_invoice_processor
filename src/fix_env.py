import os

# --- Definimos el contenido exacto con las rutas del entorno ---

CONTENT_ENV = r"""# Configuración de Variables de Entorno
# -------------------------------------

# Ruta al ejecutable de Tesseract 
TESSERACT_CMD="C:/Program Files/Tesseract-OCR/tesseract.exe"

# Ruta a la carpeta BIN de Poppler
POPPLER_PATH="C:/Program Files/poppler-25.12.0/Library/bin"
"""

# Obtener la ruta de la carpeta raíz 
BASE_DIR= os.getcwd()
ENV_PATH = os.path.join(BASE_DIR, '.env')

print(f"Intentando crear .env en: {ENV_PATH}\n")

try:
    with open(ENV_PATH, 'w', encoding='utf-8') as f:
        f.write(CONTENT_ENV)

    print("¡ÉXITO! Archivo .env creado correctamente.\n")

except Exception as e:
    print(f"ERROR al crear archivo: {e}")

# Verificación inmediata: ¿Existe el archivo?
if os.path.exists(ENV_PATH):
    print("Verificación: El sistema confirma que el archivo EXISTE.\n")
else:
    print("Verificación: El archivo sigue invisible.")