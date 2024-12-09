import polars as pl
from fastexcel import read_excel

# Ruta al archivo Excel
file_path = r"D:/Desktop/APP_ETL/Film2/backend/Films_2.xlsx"

def extract_data():
    # Lista de las pestañas que se requieren
    required_sheets = ['film', 'inventory', 'rental', 'customer', 'store']

    # Diccionario para almacenar los datos de cada pestaña
    data = {}

    # Cargar los datos de cada pestaña requerida usando `fastexcel`
    workbook = read_excel(file_path)
    
    for sheet in required_sheets:
        # Cargar cada pestaña usando el nombre
        data[sheet] = pl.read_excel(file_path, sheet_name=sheet)
    
    return data

if __name__ == "__main__":
    data = extract_data()
    print("Extracción de datos completada.")
