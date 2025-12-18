import sys
import os

# Ajuste de path para importaciones
sys.path.append(os.getcwd())

from src.processors.parser import InvoiceParser

def test_parser_logic():
    print("========================================")
    print("[PRUEBA] INICIO DE VALIDACION DE PARSER")
    print("========================================\n")

    parser = InvoiceParser()

    # --- CASO DE PRUEBA: Texto Real ---
    print("[TEST 1] Probando con texto de factura real...")
    
    mock_text = """
    RESTORAN WAN SHENG
    002043319-W
    No.2, Jalan Temenggung 19/9,
    Seksyen 9, Bandar Mahkota Cheras,
    43200 Cheras, Selangor
    GST REG NO: 001335787520

    Tax Invoice

    INV No.: 1201504 Cashier: Thandar
    Date : 20-06-2018 1: 1 45

    Description. My D price Total TA

    Teh (B)
    Cham (B)

    1x 2.10 2.10 ZRL
    2X 2.10 4.20 ¿RL
    1x 2,50 2.50 ZRL

    Nescafe (B)

    Take Away
    4 x 0,20 0. .B0 ¿RL
    Total TY: 8
    Total (Excluding GST): 9.60
    Total e of ST); 9.60
    TOTAL 9. 60
    CASH 9, 60
    391 NATY ANOUNE(AM) Tax(RM)
    RL (9 0%) 9.60 0.00
    """
    
    result = parser.extract_data(mock_text)
    print(f"Resultado Obtenido: {result}")
    
    # Validaciones: Esperamos 9.60 de total y el ID correcto
    wait_total = 9.60
    wait_tax_id = '001335787520'

    check_total = (result['total'] == wait_total)
    check_tax = (result['tax_id'] == wait_tax_id)
    
    if check_total and check_tax:
        print("\n[EXITO] El parser extrajo correctamente Total (9.60) y Tax ID.")
    else:
        print(f"\n[FALLO]   Datos incorrectos.")
        print(f"Esperado -> Total: {wait_total}, ID: {wait_tax_id}")
        print(f"Recibido -> Total: {result['total']}, ID: {result['tax_id']}")

    print("\n========================================")
    print("[FIN] VALIDACION COMPLETADA")

if __name__ == "__main__":
    test_parser_logic()