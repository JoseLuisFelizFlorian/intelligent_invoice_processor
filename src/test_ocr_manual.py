import os
import sys

# Agregamos el directorio raíz al PATH de Python para poder importar los módulos de 'src'
# Esto es necesario porque ejecutamos el script directamente.
sys.path.append(os.getcwd())

from src.processors.ocr_processor import OCRProcessor

def test_ocr():
    print("========================================")
    print("[PRUEBA] INICIO DE DIAGNOSTICO DE OCR")
    print("========================================\n")

    # Inicialización del motor
    try:
        processor = OCRProcessor()
        print("[OK] Motor OCR inicializado correctamente.")
    except Exception as e:
        print(f"[ERROR CRITICO] No se pudo iniciar el motor: {e}")
        return

    # Búsqueda automática de archivos en la carpeta raw
    RAW_PATH = os.path.join("data", "01_raw")
    
    # Listar archivos soportados
    files = [f for f in os.listdir(RAW_PATH) if f.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg'))]

    if not files:
        print(f"[ADVERTENCIA] No hay archivos en {RAW_PATH}.")
        print("Por favor, coloca una factura (PDF o Imagen) para probar.")
        return

    # 3. Procesamiento del primer archivo encontrado
    test_file = os.path.join(RAW_PATH, files[0])
    print(f"[INFO] Archivo seleccionado para la prueba: {files[0]}")
    print("[PROCESANDO] Extrayendo texto (espere un momento)...")

    # Llamada al método real
    text_extracted = processor.extract_text(test_file)

    print("\n--- INICIO DEL TEXTO EXTRAIDO (Muestra parcial) ---")
    # Mostramos solo los primeros 500 caracteres para no saturar la consola
    print(text_extracted[:500])
    print("\n--- FIN DEL TEXTO EXTRAIDO ------------------------")
    
    # Validación simple
    if len(text_extracted) > 10:
        print("[EXITO] La extracción generó texto legible.")
    else:
        print("[ADVERTENCIA] Se extrajo muy poco texto o el resultado está vacío.")

if __name__ == "__main__":
    test_ocr()