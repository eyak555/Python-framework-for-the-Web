from django.urls import path

from .views import (
    CreateVehicule,
    DeleteVehicule,
    DetailVehicule,
    ListVehicule,
    UpdateVehicule,
)


urlpatterns = [
    path('', ListVehicule.as_view(), name='vehicule-list'),
    path('listclass/', ListVehicule.as_view(), name='vehicule-listclass'),
    path('create/', CreateVehicule.as_view(), name='vehicule-create'),
    path('createclass/', CreateVehicule.as_view(), name='vehicule-createclass'),
    path('<int:pk>/', DetailVehicule.as_view(), name='vehicule-detail'),
    path('detailsclass/<int:pk>/', DetailVehicule.as_view(), name='vehicule-detailsclass'),
    path('<int:pk>/update/', UpdateVehicule.as_view(), name='vehicule-update'),
    path('updateclass/<int:pk>/', UpdateVehicule.as_view(), name='vehicule-updateclass'),
    path('<int:pk>/delete/', DeleteVehicule.as_view(), name='vehicule-delete'),
    path('deleteclass/<int:pk>/', DeleteVehicule.as_view(), name='vehicule-deleteclass'),
]
