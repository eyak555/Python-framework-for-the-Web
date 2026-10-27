from .views import home
from django.urls import path
from .views import welcome
from .views import listExpeditions
from .views import *

"""app_name = 'Expedition'"""

urlpatterns = [
    path('home/', home, name='home'),
    path("welcome/<str:name>/", welcome, 
    name="welcomeFunction"),
    path('list/', listExpeditions, name='list'),
    path('details/<int:pk>/', details, name='details'),
    path('delete/<int:pk>/', delete_expedition, name='delete')
]