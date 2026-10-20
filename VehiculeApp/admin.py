from django.contrib import admin
from .models import Vehicule
# Register your models here.
@admin.register(Vehicule)

class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'type_vehicule', 'disponibilite')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('identification', {
            'fields': ('immatriculation', 'type_vehicule', 'capacite', 'description')
        }),
        ('statut et rattachement', {
            'fields': ('disponibilite', 'Entreprise')
        }),

        ('horodatage', {
            'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)
        })
    )
