import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from appETL.models import Customer, Store

def clean_dict_keys(data):
    """
    Limpia las claves de un diccionario eliminando espacios en blanco adicionales.
    """
    return {key.strip(): value for key, value in data.items()}

def display_data(transformed_data):
    """
    Muestra los datos transformados en la consola antes de cargarlos.
    """
    print("\n--- DATOS TRANSFORMADOS ---")
    for table_name, df in transformed_data.items():
        print(f"\nTabla: {table_name}")
        print(df)  # Mostrar el DataFrame transformado

def load_data(transformed_data):
    """
    Carga los datos transformados en la base de datos.
    """
    # Mostrar los datos transformados
    display_data(transformed_data)

    # Procesar y cargar cada tabla
    if 'customer' not in transformed_data:
        raise KeyError("'customer' no se encuentra en los datos transformados.")

    customers_df = transformed_data['customer']
    total_customers = 0  # Contador para verificar el total de clientes procesados

    for row in customers_df.to_dicts():  # Método recomendado para iterar en Polars
        # Limpiar las claves del diccionario
        row = clean_dict_keys(row)

        # Validar que 'store_id' esté presente
        store_id = row.get('store_id')
        if not store_id:
            print(f"Advertencia: 'store_id' no encontrado para la fila: {row}")
            continue  # Saltar esta fila

        try:
            store = Store.objects.get(store_id=store_id)
        except Store.DoesNotExist:
            print(f"Advertencia: No existe un Store con 'store_id'={store_id}. Fila ignorada.")
            continue  # Saltar esta fila

        # Limpiar valores específicos
        email = row.get('email', '').strip()
        create_date = row.get('create_date', '').strip()

        # Actualizar o crear el cliente
        _, created = Customer.objects.update_or_create(
            customer_id=row['customer_id'],
            defaults={
                'store_id': store,
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': email,
                'address_id': row['address_id'],
                'active': row['active'],
                'create_date': create_date,
                'last_update': timezone.now(),
                'customer_id_old': row.get('customer_id_old', None),
                'segment': row.get('segment', None),
            }
        )
        if created:
            total_customers += 1  # Incrementar el contador solo para nuevos registros

    print(f"Carga de datos de clientes completada. Total de nuevos clientes creados: {total_customers}")

if __name__ == "__main__":
    from Extraccion import extract_data
    from Transformacion import transform_data

    # Extraer los datos
    extracted_data = extract_data()

    # Transformar los datos
    transformed_data = transform_data(extracted_data)

    # Mostrar y cargar los datos
    load_data(transformed_data)
