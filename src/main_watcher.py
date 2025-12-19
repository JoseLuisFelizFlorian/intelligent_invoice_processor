import sys
import time
import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- IMPORTACIÓN DE MOTORES Y BD (OCR, Parser, Database) ---
try:
    from src.processors.ocr_processor import OCRProcessor
    from src.processors.parser import InvoiceParser
    from src.db.manager import DatabaseManager
except ImportError:
    # Solución para rutas si se ejecuta el script directamente desde src/
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from src.processors.ocr_processor import OCRProcessor
    from src.processors.parser import InvoiceParser
    from src.db.manager import DatabaseManager


# --- CONFIGURACIÓN DE LOGGING ---
# Se establece un sistema de trazabilidad para registrar eventos tanto en archivo como en consola.
logging.basicConfig(
    level=logging.INFO, # Nivel mínimo de severidad para capturar mensajes.
    format='%(asctime)s - %(levelname)s - %(message)s', # Estructura del mensaje: Tiempo - Nivel - Mensaje.
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("logs/watcher.log", encoding='utf-8'), # Persistencia de logs en disco.
        logging.StreamHandler(sys.stdout)        # Salida visual en la terminal.
    ]
)

logger = logging.getLogger(__name__)

# --- CONFIGURACIÓN DE RUTAS ---
# Definición de rutas absolutas para asegurar que el script localice correctamente los directorios.
BASE_DIR = os.getcwd()
WATCHER_LOG_DIR = os.path.join(BASE_DIR, "data", "01_raw")

class InvoiceHandler(FileSystemEventHandler):
    """
    Controlador de eventos personalizado. Hereda de FileSystemEventHandler para 
    sobreescribir los métodos que reaccionan a cambios en el sistema de archivos.
    Orquesta la detección, lectura (OCR), interpretación (Parser) y persistencia (BD).
    """

    def __init__(self):
        """
        Constructor: Inicializa los motores de procesamiento (OCR, Parser y BD) al arrancar.
        Esto evita recargar modelos con cada archivo nuevo.
        """
        logger.info("[SISTEMA] Inicializando motores de procesamiento...")
        try:
            # Iniciar Motor OCR (Tesseract)
            self.ocr = OCRProcessor()

            # Iniciar Motor de Parsing (Regex)
            self.parser = InvoiceParser()
            
            # Iniciar Gestor de Base de Datos (SQLite)
            self.db = DatabaseManager()

            logger.info("[OK] Sistema listo: OCR + Parser + DB conectados.")
        except Exception as e:
            logger.critical(f"[ERROR CRITICO] No se pudo iniciar el procesamiento: {e}")
            sys.exit(1)

    def on_created(self, event):
        """
        Callback que se dispara automáticamente cuando el sistema operativo detecta 
        la creación de un nuevo recurso en la ruta monitoreada.
        """
        if event.is_directory:
            return

        filename = event.src_path
        
        # Validación de extensión: Solo procesa archivos con formato de factura (PDF o imagen).
        if filename.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg')):
            logger.info(f"------------------------------------------------")
            logger.info(f"[DETECTADO] Nuevo archivo: {os.path.basename(filename)}")
            
            # ---------------------------------------------------------
            # ÁREA DE INTEGRACIÓN: Pipeline de Procesamiento (OCR -> Parser -> BD)
            # Este bloque actúa como punto de entrada para el procesamiento
            # de la Extracción, Transformación y Carga de datos (ETL).
            # ---------------------------------------------------------

            try:
                # Extracción de Texto (OCR)
                logger.info("[PROCESANDO] Extrayendo texto con Tesseract...")
                raw_texto = self.ocr.extract_text(filename)
                
                if not raw_texto:
                    logger.warning("[ADVERTENCIA] El OCR no devolvió texto (Imagen vacía o ilegible).")
                    return

                # Interpretación de Datos (Parsing)
                logger.info("[ANALIZANDO] Ejecutando Parser (Extracción de Datos)...")
                structured_data = self.parser.extract_data(raw_texto)
                
                # Visualización en Log
                logger.info("[EXITO] Datos Estructurados Obtenidos:")
                logger.info(f"   > PROVEEDOR : {structured_data.get('vendor')}")
                logger.info(f"   > FECHA     : {structured_data.get('date')}")
                logger.info(f"   > TAX ID    : {structured_data.get('tax_id')}")
                logger.info(f"   > TOTAL     : {structured_data.get('total')}")

                # Persistencia (Base de Datos)
                logger.info("[ALMACENANDO] Guardando registro en Base de Datos...")
                
                # Limpiamos el nombre del archivo para guardarlo solo como referencia
                clean_filename = os.path.basename(filename)
                self.db.save_invoice(structured_data, clean_filename)

            except Exception as e:
                logger.error(f"[ERROR] Falló el pipeline de procesamiento: {e}")
            
            logger.info(f"------------------------------------------------")
            
        else:
            # Uso de nivel DEBUG para evitar saturar el log principal con archivos no deseados.
            logger.debug(f"[IGNORADO] Formato no soportado: {filename}")

def start_watcher():
    """
    Orquestador del servicio de monitoreo. Configura el Observer y gestiona 
    el ciclo de vida del proceso principal.
    """
    # Verificación de integridad: Evita que el script falle si la carpeta objetivo no existe.
    if not os.path.exists(WATCHER_LOG_DIR):
        logger.error(f"[ERROR] La carpeta no existe: {WATCHER_LOG_DIR}")
        return

    event_handler = InvoiceHandler()
    observer = Observer() # El Observer es el hilo que vigila los cambios del sistema operativo.
    
    # Programación del monitoreo: (Manejador, Ruta, No recursivo para evitar subcarpetas).
    observer.schedule(event_handler, WATCHER_LOG_DIR, recursive=False)
    
    observer.start() # Inicia el hilo del observador en segundo plano.
    logger.info(f"[SISTEMA INICIADO] Monitoreando carpeta: {WATCHER_LOG_DIR}")
    logger.info("Presiona Ctrl+C para detener.")

    try:
        # Bucle de espera infinito para mantener el script vivo mientras el hilo Observer trabaja.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Captura la interrupción del teclado (Ctrl+C) para un apagado controlado de los hilos.
        observer.stop()
        logger.info("[DETENIDO] Sistema parado por el usuario.")
    
    observer.join() # Bloquea el script hasta que el hilo del observador termine su limpieza.

if __name__ == "__main__":
    # Punto de entrada estándar para la ejecución del script.
    start_watcher()
