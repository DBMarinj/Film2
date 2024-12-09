from rest_framework import generics
from .models import Customer, Rental, Store, Inventory, Film
from .serializers import CustomerSerializer, RentalSerializer, StoreSerializer, InventorySerializer, FilmSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.db.models import Count
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .Extraccion import extract_data
from .Transformacion import transform_data
from .Load import load_data

# Vistas para Customer
class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# Vistas para Rental
class RentalListCreateView(generics.ListCreateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

class RentalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

# Vistas para Store
class StoreListCreateView(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class StoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

# Vistas para Inventory
class InventoryListCreateView(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

# Vistas para Film
class FilmListCreateView(generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

class FilmDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

# Vista para extracción de datos
class ExtractDataView(APIView):
    def get(self, request):
        # Extraer los datos
        data = extract_data()

        # Convertir los DataFrames de polars a listas de diccionarios (serializables a JSON)
        json_data = {sheet: df.to_dicts() for sheet, df in data.items()}

        return Response({
            "message": "Extracción completada",
            "data": json_data
        }, status=status.HTTP_200_OK)

# Vista para transformación de datos
class TransformDataView(APIView):
    def get(self, request):
        # Extraer los datos
        extracted_data = extract_data()

        # Transformar los datos
        transformed_data = transform_data(extracted_data)

        # Convertir los DataFrames de Polars a listas de diccionarios
        json_data = {sheet: df.to_dicts() for sheet, df in transformed_data.items()}

        # Retornar la respuesta con los datos transformados
        return Response({
            "message": "Transformación completada",
            "data": json_data
        }, status=status.HTTP_200_OK)

# Vista para carga de datos
class LoadDataView(APIView):
    def get(self, request):
        # Extraer y transformar los datos
        extracted_data = extract_data()
        transformed_data = transform_data(extracted_data)

        # Cargar los datos
        load_data(transformed_data)

        # Obtener los datos cargados de la base de datos
        customers = Customer.objects.all()
        customer_serializer = CustomerSerializer(customers, many=True)

        return Response({
            "message": "Carga completada",
            "data": customer_serializer.data
        }, status=status.HTTP_200_OK)

# Vista para generar informe de alquileres
class RentalReportView(APIView):
    """
    Vista para generar un informe consolidado sobre los alquileres por cliente en formato PDF.
    """
    def get(self, request):
        try:
            # Obtener datos de alquileres agrupados por cliente
            rental_data = Rental.objects.select_related('customer', 'inventory_id__film_id').values(
                'customer_id__first_name',  # Relacionado con customer_id
                'customer_id__last_name',   # Relacionado con customer_id
                'customer_id__email',       # Relacionado con customer_id
                'inventory_id__film_id__title',  # Relacionado con film_id
            ).annotate(
                rental_count=Count('rental_id'),
            )

            # Generar el PDF en memoria
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="informe_alquileres.pdf"'

            c = canvas.Canvas(response, pagesize=letter)

            # Título del informe
            c.setFont("Helvetica-Bold", 14)
            c.drawString(100, 750, "Informe de Alquileres por Cliente")
            c.setFont("Helvetica", 10)
            y_position = 730

            # Agregar los datos al PDF
            for entry in rental_data:
                customer_name = f"{entry['customer_id__first_name']} {entry['customer_id__last_name']}"
                customer_email = entry['customer_id__email']
                rental_count = entry['rental_count']
                film_title = entry["inventory_id__film_id__title"]

                # Escribir los datos en el PDF
                c.drawString(100, y_position, f"Cliente: {customer_name} (Email: {customer_email})")
                y_position -= 15
                c.drawString(100, y_position, f"Película: {film_title} - Alquileres: {rental_count}")
                y_position -= 15
                if y_position < 100:  # Si llegamos al final de la página, creamos una nueva página
                    c.showPage()
                    y_position = 750

            # Finalizar el PDF
            c.showPage()
            c.save()

            return response
        except Exception as e:
            return Response({
                "message": "Error al generar el informe",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
