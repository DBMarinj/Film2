import os
import django
import polars as pl
from django.utils import timezone

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Ahora puedes importar los modelos
from appETL.models import Customer, Rental, Store, Inventory, Film

# Ruta al archivo Excel
excel_path = r"D:\Desktop\APP_ETL\backend\Films_2.xlsx"

# Cargar los datos de cada pestaña según su orden
films_data = pl.read_excel(excel_path, sheet_id=1)  # Segunda pestaña: film
inventory_data = pl.read_excel(excel_path, sheet_id=2)  # Tercera pestaña: inventory
rentals_data = pl.read_excel(excel_path, sheet_id=3)  # Cuarta pestaña: rental
customers_data = pl.read_excel(excel_path, sheet_id=4)  # Quinta pestaña: customer
stores_data = pl.read_excel(excel_path, sheet_id=5)  # Sexta pestaña: store

# Función para validar y limpiar datos
def clean_data(df):
    df = df.drop_nulls()  # Eliminar filas con valores nulos
    df = df.unique()  # Eliminar duplicados
    return df

# Procesar cada tabla
def process_customers(customers_data):
    customers_data = clean_data(customers_data)
    for row in customers_data.iterrows():
        Customer.objects.update_or_create(
            customer_id=row['customer_id'],
            defaults={
                'store_id': Store.objects.get(store_id=row['store_id']),
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'address_id': row['address_id'],
                'active': row['active'],
                'create_date': row['create_date'],
                'last_update': timezone.now(),
                'customer_id_old': row.get('customer_id_old', None),
                'segment': row.get('segment', None)
            }
        )

def process_rentals(rentals_data):
    rentals_data = clean_data(rentals_data)
    for row in rentals_data.iterrows():
        Rental.objects.update_or_create(
            rental_id=row['rental_id'],
            defaults={
                'rental_date': row['rental_date'],
                'inventory_id': Inventory.objects.get(inventory_id=row['inventory_id']),
                'customer_id': Customer.objects.get(customer_id=row['customer_id']),
                'return_date': row.get('return_date', None),
                'staff_id': row['staff_id'],
                'last_update': timezone.now()
            }
        )

def process_stores(stores_data):
    stores_data = clean_data(stores_data)
    for row in stores_data.iterrows():
        Store.objects.update_or_create(
            store_id=row['store_id'],
            defaults={
                'manager_staff_id': row['manager_staff_id'],
                'address_id': row['address_id'],
                'last_update': timezone.now()
            }
        )

def process_inventory(inventory_data):
    inventory_data = clean_data(inventory_data)
    for row in inventory_data.iterrows():
        Inventory.objects.update_or_create(
            inventory_id=row['inventory_id'],
            defaults={
                'film_id': Film.objects.get(film_id=row['film_id']),
                'store_id': Store.objects.get(store_id=row['store_id']),
                'last_update': timezone.now()
            }
        )

def process_films(films_data):
    films_data = clean_data(films_data)
    for row in films_data.iterrows():
        Film.objects.update_or_create(
            film_id=row['film_id'],
            defaults={
                'title': row['title'],
                'description': row['description'],
                'release_year': row['release_year'],
                'language_id': row['language_id'],
                'original_language_id': row.get('original_language_id', None),
                'rental_duration': row['rental_duration'],
                'rental_rate': row['rental_rate'],
                'length': row['length'],
                'replacement_cost': row['replacement_cost'],
                'num_voted_users': row['num_voted_users'],
                'rating': row['rating'],
                'special_features': row['special_features'],
                'last_update': timezone.now()
            }
        )

# Ejecutar el proceso ETL
def run_etl():
    process_customers(customers_data)
    process_rentals(rentals_data)
    process_stores(stores_data)
    process_inventory(inventory_data)
    process_films(films_data)
    print("ETL process completed successfully.")

# Ejecutar el proceso ETL cuando se llame el script
if __name__ == "__main__":
    run_etl()
