# Función para limpiar y transformar datos
def clean_data(df):
    df = df.drop_nulls()  # Eliminar filas con valores nulos
    df = df.unique()  # Eliminar duplicados
    return df

def transform_data(extracted_data):
    transformed_data = {}
    for key, df in extracted_data.items():
        transformed_data[key] = clean_data(df)
    return transformed_data

if __name__ == "__main__":
    from Film2.backend.appETL.Extraccion import extract_data
    extracted_data = extract_data()
    transformed_data = transform_data(extracted_data)
    print("Transformación de datos completada.")
