from django.urls import path

from .views import (
    CreateEntreprise,
    DeleteEntreprise,
    DetailEntreprise,
    ListEntreprise,
    UpdateEntreprise,
)


urlpatterns = [
    path('', ListEntreprise.as_view(), name='entreprise-list'),
    path('create/', CreateEntreprise.as_view(), name='entreprise-create'),
    path('<int:pk>/', DetailEntreprise.as_view(), name='entreprise-detail'),
    path('<int:pk>/update/', UpdateEntreprise.as_view(), name='entreprise-update'),
    path('<int:pk>/delete/', DeleteEntreprise.as_view(), name='entreprise-delete'),
]
