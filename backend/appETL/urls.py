from django.urls import path
from .views import (
    CustomerListCreateView, CustomerDetailView,
    RentalListCreateView, RentalDetailView,
    StoreListCreateView, StoreDetailView,
    InventoryListCreateView, InventoryDetailView,
    FilmListCreateView, FilmDetailView,
    ExtractDataView, TransformDataView, LoadDataView,
    RentalReportView  # Importamos la nueva vista
)

urlpatterns = [
    # Rutas para Customer
    path('customers/', CustomerListCreateView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),

    # Rutas para Rental
    path('rentals/', RentalListCreateView.as_view(), name='rental-list'),
    path('rentals/<int:pk>/', RentalDetailView.as_view(), name='rental-detail'),

    # Rutas para Store
    path('stores/', StoreListCreateView.as_view(), name='store-list'),
    path('stores/<int:pk>/', StoreDetailView.as_view(), name='store-detail'),

    # Rutas para Inventory
    path('inventory/', InventoryListCreateView.as_view(), name='inventory-list'),
    path('inventory/<int:pk>/', InventoryDetailView.as_view(), name='inventory-detail'),

    # Rutas para Film
    path('films/', FilmListCreateView.as_view(), name='film-list'),
    path('films/<int:pk>/', FilmDetailView.as_view(), name='film-detail'),

    # Rutas para extracción, transformación y carga de datos
    path('extract/', ExtractDataView.as_view(), name='extract-data'),
    path('transform/', TransformDataView.as_view(), name='transform-data'),
    path('load/', LoadDataView.as_view(), name='load-data'),

    # Ruta para el informe de alquileres por cliente
    path('rental-report/', RentalReportView.as_view(), name='rental-report'),  # Nuevo endpoint
]
