import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import Base, Invoice

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Controlador para manejar la conexión y operaciones con la base de datos SQLite.
    """

    def __init__(self, db_name="invoices.db"):
        # Definimos la ruta en data/database/
        self.db_dir = os.path.join(os.getcwd(), 'data', 'database')
        self.db_path = os.path.join(self.db_dir, db_name)
        
        # URL de conexión para SQLite
        self.engine_url = f"sqlite:///{self.db_path}"
        
        # Crear motor y fábrica de sesiones
        self.engine = create_engine(self.engine_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
        
        # Asegurar que la carpeta existe
        os.makedirs(self.db_dir, exist_ok=True)
        
        # Inicializar tablas
        self._init_db()

    def _init_db(self):
        """Crea las tablas definidas en models.py si no existen."""
        try:
            Base.metadata.create_all(self.engine)
            logger.info(f"[DB] Base de datos conectada en: {self.db_path}")
        except Exception as e:
            logger.critical(f"[DB] Error creando tablas: {e}")

    def save_invoice(self, data: dict, filename: str):
        """
        Guarda un diccionario de datos de factura en la BD.
        """
        session = self.Session()
        try:
            # Creamos el objeto Invoice (Fila de la tabla)
            new_invoice = Invoice(
                filename=filename,
                vendor=data.get('vendor'),
                tax_id=data.get('tax_id'),
                total=data.get('total'),
                invoice_date=data.get('date')
            )
            
            # Insertamos y confirmamos (Commit)
            session.add(new_invoice)
            session.commit()
            logger.info(f"[DB] Factura guardada exitosamente. ID: {new_invoice.id}")
            
        except Exception as e:
            session.rollback() # Deshacer cambios si hay error
            logger.error(f"[DB] Error al guardar en BD: {e}")
        finally:
            session.close() # Importante: Cerrar conexión