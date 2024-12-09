from django.db.models import Count, Sum
from .models import Rental

def get_rental_report():
    """
    Genera un informe de los alquileres agrupados por cliente.
    """
    try:
        # Obtener datos de alquileres agrupados por cliente
        rental_data = Rental.objects.select_related('customer', 'inventory__film').values(
            'customer__first_name',
            'customer__last_name',
            'customer__email',
            'inventory__film__title',
        ).annotate(
            rental_count=Count('rental_id'),
            total_spent=Sum('rental_rate')  # Si existe un campo de tarifa de alquiler
        )

        # Formatear los datos para el informe
        report = {}
        for entry in rental_data:
            customer_key = f"{entry['customer__first_name']} {entry['customer__last_name']}"
            if customer_key not in report:
                report[customer_key] = {
                    "email": entry["customer__email"],
                    "rentals": [],
                    "total_rentals": 0,
                    "total_spent": 0
                }
            report[customer_key]["rentals"].append({
                "film_title": entry["inventory__film__title"],
                "count": entry["rental_count"]
            })
            report[customer_key]["total_rentals"] += entry["rental_count"]
            report[customer_key]["total_spent"] += entry["total_spent"]

        return report
    except Exception as e:
        raise Exception(f"Error al generar el informe: {str(e)}")
