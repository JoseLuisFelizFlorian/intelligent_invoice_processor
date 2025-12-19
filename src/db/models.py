from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

# Clase base de SQLAlchemy
Base = declarative_base()

class Invoice(Base):
    """
    Representación de la tabla 'facturas' en la base de datos.
    """
    __tablename__ = 'facturas'

    # Definición de Columnas
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)     # Nombre del archivo original
    vendor = Column(String, nullable=True)        # Proveedor (ej. Restoran Wan Sheng)
    tax_id = Column(String, nullable=True)        # RUC / NIT
    total = Column(Float, nullable=True)          # Monto total
    invoice_date = Column(String, nullable=True)  # Fecha extraída (como texto)
    
    # Metadatos de auditoría de cuándo se procesó
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Invoice(id={self.id}, vendor='{self.vendor}', total={self.total})>"