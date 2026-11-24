"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.views.generic import TemplateView
from EntrepriseApp.views import profile, profile_delete, profile_edit, register

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='project-home'),
    path('admin/', admin.site.urls),
    path('entreprise/', include('EntrepriseApp.urls')),
    path('expedition/', include('ExpeditionApp.urls')),
    path('vehicule/', include('VehiculeApp.urls')),
    path('offre/', include('OffreApp.urls')),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', profile_edit, name='profile-edit'),
    path('profile/delete/', profile_delete, name='profile-delete'),
]

