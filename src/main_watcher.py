import sys
import time
import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURACIÓN DE LOGGING ---
# Se establece un sistema de trazabilidad para registrar eventos tanto en archivo como en consola.
logging.basicConfig(
    level=logging.INFO, # Nivel mínimo de severidad para capturar mensajes.
    format='%(asctime)s - %(levelname)s - %(message)s', # Estructura del mensaje: Tiempo - Nivel - Mensaje.
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("logs/watcher.log"), # Persistencia de logs en disco.
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
    """
    
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
            logger.info(f"[DETECTADO] Nuevo archivo: {filename}")
            
            # ---------------------------------------------------------
            # ÁREA DE INTEGRACIÓN: Lógica de Negocio (Pipeline de OCR)
            # Este bloque actúa como punto de entrada para el procesamiento
            # de la Extracción y Transformación de datos.
            # ---------------------------------------------------------

            logger.info("[PROCESANDO] Iniciando tarea simulada...")
            time.sleep(1) # Simulación de latencia de proceso (p. ej. carga de OCR).
            logger.info("[EXITO] Procesamiento finalizado (Simulado).")
            
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
