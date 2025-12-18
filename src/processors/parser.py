import re
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class InvoiceParser:
    """
    Clase encargada de transformar texto crudo en datos estructurados 
    utilizando Expresiones Regulares (Regex).
    """

    def __init__(self):
        # Compilamos los patrones al iniciar para mejorar rendimiento
        self._compile_patterns()

    def _compile_patterns(self):
        """Define y compila los patrones regex para cada campo."""
        
        # Patrones de FECHA (Soporta DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD)
        self.date_pattern = re.compile(
            r'(?:Fecha|Date|Time|Emision)[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})', 
            re.IGNORECASE
        )

        # Patrones de TOTAL (Busca números con decimales después de palabras clave)
        self.amount_pattern = re.compile(
            r'(?:Total|Monto|Importe|Amount|Net|Grand Total)[\D]*?(\d{1,3}(?:[,.]\d{3})*(?:[.,]\d{2}))', 
            re.IGNORECASE
        )

        # Patrones de TAX ID (MEJORADO)
        # Soporta variaciones como: "GST REG NO:", "Tax ID:", "RUC:", "NIT No."
        # (?:\s+(?:Reg|No|Num|Number|Id)\.?)* permite palabras intermedias opcionales
        self.tax_id_pattern = re.compile(
            r'(?:RUC|NIT|CUIT|RFC|GST|VAT|Tax ID)(?:\s+(?:Reg|No|Num|Number|Id)\.?)*[:\s\.]*([A-Z0-9\-\.]{8,15})', 
            re.IGNORECASE
        )

    def extract_data(self, text: str) -> Dict[str, Any]:
        """
        Analiza el texto completo y extrae los campos clave.
        """
        if not text:
            return {}

        data = {
            "vendor": self._extract_vendor(text),
            "date": None,
            "total": None,
            "tax_id": None,
            "raw_text": text[:200].replace('\n', ' ') + "..." # Snippet limpio
        }

        # --- Extracción de Fecha ---
        date_match = self.date_pattern.search(text)
        if date_match:
            data["date"] = date_match.group(1)

        # --- Extracción de Total ---
        amount_matches = self.amount_pattern.findall(text)
        if amount_matches:
            # Tomamos el último valor encontrado, asumiendo que es el "Grand Total"
            # Limpiamos comas si es formato americano (1,000.00 -> 1000.00)
            raw_amount = amount_matches[-1].replace(',', '') 
            try:
                data["total"] = float(raw_amount)
            except ValueError:
                logger.warning(f"[PARSER] No se pudo convertir a float: {raw_amount}")

        # --- Extracción de Tax ID ---
        tax_match = self.tax_id_pattern.search(text)
        if tax_match:
            data["tax_id"] = tax_match.group(1)

        logger.info(f"[PARSER] Datos extraídos: {data}")
        return data

    def _extract_vendor(self, text: str) -> str:
        """
        Intenta adivinar el proveedor tomando la primera línea no vacía.
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            return lines[0]
        return "Unknown Vendor"