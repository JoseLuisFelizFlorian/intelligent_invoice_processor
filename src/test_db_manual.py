import sys
import os

# Ajuste de path
sys.path.append(os.getcwd())

from src.db.manager import DatabaseManager

def test_database():
    print("========================================")
    print("[PRUEBA] INICIO DE VALIDACION DE BASE DE DATOS")
    print("========================================\n")

    # Inicializar el Manager
    print("Inicializando Base de Datos...")
    db = DatabaseManager()

    # Datos simulados (Como si vinieran del Parser)
    mock_data = {
        'vendor': 'PRUEBA UNITARIA S.A.',
        'tax_id': '999999999',
        'total': 150.75,
        'date': '25-12-2025'
    }
    filename_mock = "factura_test_001.pdf"

    # Intentar guardar
    print(f"Intentando guardar datos: {mock_data}...")
    db.save_invoice(mock_data, filename_mock)

    # Verificación física
    db_file = os.path.join(os.getcwd(), 'data', 'database', 'invoices.db')
    if os.path.exists(db_file):
        print(f"\n[EXITO] El archivo de base de datos existe: {db_file}")
        print("Puedes abrir este archivo con 'DB Browser for SQLite' para ver los datos.")
    else:
        print(f"\n[FALLO] No se encontró el archivo .db")

    print("\n========================================")
    print("[FIN] VALIDACION COMPLETADA")

if __name__ == "__main__":
    test_database()