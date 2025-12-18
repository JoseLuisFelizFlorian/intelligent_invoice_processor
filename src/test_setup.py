import os
import pytesseract
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# --- PRUEBA DE TESSERACT OCR Y POPPLER (HERRAMIENTAS PDF) ---
def run_diagnostics():
    print("==========================================")
    print("  INICIANDO DIAGNÓSTICO DEL SISTEMA")
    print("==========================================\n")

    # --- PRUEBA: TESSERACT OCR ---
    print("Probando Tesseract OCR...")
    
    tesseract_cmd = os.getenv("TESSERACT_CMD")
    if not tesseract_cmd:
        print("ERROR: No se encontró TESSERACT_CMD en el archivo .env\n")
        return

    # Configurar pytesseract con la ruta del .exe
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    try:
        # Intentamos obtener la versión y los idiomas instalados
        version = pytesseract.get_tesseract_version()
        langs = pytesseract.get_languages()
        print(f"¡Tesseract encontrado! Versión: {version}\n")
        print(f"Idiomas instalados: {langs}\n")
        
        if 'spa' not in langs:
            print("ADVERTENCIA: NO se detectó el paquete de idioma 'spa' (Español)\n.")
            print("Por favor, verifica que 'spa.traineddata' exista en tu carpeta tessdata.\n")
        else:
            print("Paquete de idioma español detectado.")

    except Exception as e:
        print(f"ERROR: No se pudo ejecutar Tesseract. Detalles: {e}\n")
        print(f"Verifica si la ruta '{tesseract_cmd}' es correcta.\n")

    print("\n------------------------------------------\n")

    # --- PRUEBA: POPPLER (HERRAMIENTAS PDF) ---
    print("Probando Poppler (Procesamiento de PDF)...\n")
    
    poppler_path = os.getenv("POPPLER_PATH")
    if not poppler_path:
        print("ERROR: No se encontró POPPLER_PATH en el archivo .env\n")
        return

    # Verificar si la carpeta existe
    if os.path.exists(poppler_path):
        print(f"El directorio de Poppler existe: {poppler_path}\n")
       
        # Verificar si existe el ejecutable clave
        exe_path = os.path.join(poppler_path, "pdftoppm.exe")
        if os.path.exists(exe_path):
             print("Ejecutable 'pdftoppm.exe' encontrado.\n")
        else:
             print("ERROR: No se encontró 'pdftoppm.exe' en esa carpeta.\n")
    else:
        print(f"ERROR: El directorio no existe: {poppler_path}\n")

    print("\n==========================================")
    print("  DIAGNÓSTICO COMPLETADO")
    print("==========================================")

if __name__ == "__main__":
    run_diagnostics()
