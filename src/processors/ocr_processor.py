import os
import sys
import logging
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from dotenv import load_dotenv

# Configuración del logger para este módulo específico
logger = logging.getLogger(__name__)

class OCRProcessor:
    """
    Clase encargada de la extracción de texto (OCR) desde archivos de imagen y PDF.
    
    Utiliza:
    - Tesseract: Para el reconocimiento óptico de caracteres.
    - PDF2Image: Para rasterizar PDFs (convertirlos a imagen) antes del OCR.
    """
    
    def __init__(self):
        """
        Constructor de la clase.
        Carga las configuraciones del entorno y verifica las dependencias externas.
        
        Raises:
            ValueError: Si las rutas de Tesseract o Poppler no están en el archivo .env.
        """
        load_dotenv() # Carga variables del archivo .env
        
        # Configuración de Tesseract (Motor OCR)
        self.tesseract_cmd = os.getenv('TESSERACT_CMD')
        if not self.tesseract_cmd:
            raise ValueError("[ERROR CRITICO] La variable TESSERACT_CMD no está definida en .env")
        
        # Limpieza de rutas para evitar errores en Windows (comillas dobles o simples)
        self.tesseract_cmd = self.tesseract_cmd.strip('"').strip("'")
        
        # Inyección de la ruta en la librería
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd

        # Configuración de Poppler (Herramienta para procesar PDFs)
        self.poppler_path = os.getenv('POPPLER_PATH')
        if not self.poppler_path:
            raise ValueError("[ERROR CRITICO] La variable POPPLER_PATH no está definida en .env")
            
        self.poppler_path = self.poppler_path.strip('"').strip("'")

    def extract_text(self, file_path: str) -> str:
        """
        Método principal para extraer texto. Detecta el tipo de archivo y delega 
        la tarea al método correspondiente.
        
        Args:
            file_path (str): Ruta absoluta o relativa del archivo a procesar.
            
        Returns:
            str: El texto extraído limpio. Devuelve cadena vacía si hay error.
        """
        # Validación básica de existencia
        if not os.path.exists(file_path):
            logger.error(f"[ERROR] Archivo no encontrado en la ruta: {file_path}")
            return ""

        # Obtener extensión del archivo en minúsculas (ej: .pdf, .jpg)
        ext = os.path.splitext(file_path)[1].lower()
        logger.info(f"[PROCESANDO] Iniciando lectura de archivo: {os.path.basename(file_path)}")

        try:
            if ext in ['.jpg', '.jpeg', '.png']:
                return self._process_image(file_path)
            elif ext == '.pdf':
                return self._process_pdf(file_path)
            else:
                logger.warning(f"[ADVERTENCIA] Formato no soportado para OCR: {ext}")
                return ""
        except Exception as e:
            # Captura general para evitar que el programa principal se detenga
            logger.error(f"[ERROR] Fallo durante la extracción en {file_path}: {e}")
            return ""

    def _process_image(self, image_path: str) -> str:
        """
        Lógica interna para procesar imágenes estáticas.
        """
        try:
            # Cargar imagen en memoria
            img = Image.open(image_path)
            # Ejecutar OCR configurado para español ('spa')
            text = pytesseract.image_to_string(img, lang='spa')
            return text
        except Exception as e:
            logger.error(f"[ERROR] Fallo interno en OCR de imagen: {e}")
            raise e

    def _process_pdf(self, pdf_path: str) -> str:
        """
        Lógica interna para procesar documentos PDF.
        Convierte cada página del PDF a una imagen temporal y luego aplica OCR.
        """
        try:
            # Convertir PDF a lista de objetos imagen
            pages = convert_from_path(pdf_path, poppler_path=self.poppler_path)
            full_text = []

            # Iterar sobre cada página
            for i, page in enumerate(pages):
                logger.info(f"[INFO] Leyendo página {i+1} de {len(pages)}...")
                text = pytesseract.image_to_string(page, lang='spa')
                full_text.append(text)
            
            # Unir todo el texto con saltos de línea
            return "\n".join(full_text)
        except Exception as e:
            logger.error(f"[ERROR] Fallo interno en OCR de PDF: {e}")
            raise e