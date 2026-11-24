from django.urls import path

from .views import (
    CreateOffre,
    DeleteOffre,
    DetailOffre,
    ListOffre,
    UpdateOffre,
)


urlpatterns = [
    path('', ListOffre.as_view(), name='offre-list'),
    path('create/', CreateOffre.as_view(), name='offre-create'),
    path('<int:pk>/', DetailOffre.as_view(), name='offre-detail'),
    path('<int:pk>/update/', UpdateOffre.as_view(), name='offre-update'),
    path('<int:pk>/delete/', DeleteOffre.as_view(), name='offre-delete'),
]
