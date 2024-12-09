from django.db import models

# Tabla Customer
class Customer(models.Model):
    customer_id = models.SmallIntegerField(primary_key=True)
    store_id = models.ForeignKey('Store', on_delete=models.CASCADE)  # Muchos a 1 con Store
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=50)
    address_id = models.SmallIntegerField()
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField()
    last_update = models.DateTimeField()
    customer_id_old = models.SmallIntegerField(null=True, blank=True)  # Campo adicional (ejemplo de backup ID)
    segment = models.CharField(max_length=45, null=True, blank=True)  # Asumiendo que es un segmento de cliente

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Tabla Rental
class Rental(models.Model):
    rental_id = models.AutoField(primary_key=True)
    rental_date = models.DateTimeField()
    inventory_id = models.ForeignKey('Inventory', on_delete=models.CASCADE)  # Muchos a 1 con Inventory
    customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE)  # 1 a muchos con Customer
    return_date = models.DateTimeField(null=True, blank=True)
    staff_id = models.SmallIntegerField()
    last_update = models.DateTimeField()

    def __str__(self):
        return f"Rental {self.rental_id}"

# Tabla Store
class Store(models.Model):
    store_id = models.SmallIntegerField(primary_key=True)
    manager_staff_id = models.SmallIntegerField()
    address_id = models.SmallIntegerField()
    last_update = models.DateTimeField()

    def __str__(self):
        return f"Store {self.store_id}"

# Tabla Inventory
class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    film_id = models.ForeignKey('Film', on_delete=models.CASCADE)  # Muchos a 1 con Film
    store_id = models.ForeignKey('Store', on_delete=models.CASCADE)  # 1 a muchos con Store
    last_update = models.DateTimeField()

    def __str__(self):
        return f"Inventory {self.inventory_id}"

# Tabla Film
class Film(models.Model):
    film_id = models.SmallIntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_year = models.IntegerField()
    language_id = models.SmallIntegerField()
    original_language_id = models.SmallIntegerField(null=True, blank=True)
    rental_duration = models.DecimalField(max_digits=4, decimal_places=2)
    rental_rate = models.DecimalField(max_digits=5, decimal_places=2)
    length = models.SmallIntegerField()
    replacement_cost = models.DecimalField(max_digits=5, decimal_places=2)
    num_voted_users = models.IntegerField()  # Cantidad de votos de usuarios
    rating = models.CharField(max_length=10)  # Clasificación de la película, asumiendo que es un texto corto
    special_features = models.TextField()
    last_update = models.DateTimeField()

    def __str__(self):
        return self.title
