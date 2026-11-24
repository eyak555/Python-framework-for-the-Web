from django.urls import path
from django.views.generic.base import RedirectView
from .views import welcome
from .views import listExpeditions
from .views import *

"""app_name = 'Expedition'"""

urlpatterns = [
    path('home/', RedirectView.as_view(pattern_name='project-home'), name='expedition-home'),
    path("welcome/<str:name>/", welcome, 
    name="welcomeFunction"),
    path('list/', listExpeditions, name='list'),
    path('details/<int:pk>/', details, name='details'),
    path('delete/<int:pk>/', delete_expedition, name='delete'),
    path('listclass/', ListExpedition.as_view(), name='listclass'),
    path('detailsclass/<int:pk>/', DetailExpedition.as_view(), name='detailsclass'),
    path('deleteclass/<int:pk>/', DeleteExpedition.as_view(), name='deleteclass'),
    path('createclass/', CreateExpedition.as_view(), name='createclass'),
    path('updateclass/<int:pk>/', UpdateExpedition.as_view(), name='updateclass'),
]