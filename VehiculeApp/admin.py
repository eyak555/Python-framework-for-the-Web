from django.contrib import admin
from .models import Vehicule

# Register your models here.
@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'type_vehicule', 'disponibilite')
    list_editable = ('disponibilite',)
    search_fields = ('immatriculation', 'Entreprise__raison_sociale')
    list_filter = ('disponibilite', 'type_vehicule', 'status')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('identification', {
            'fields': ('immatriculation', 'type_vehicule', 'capacite', 'description')
        }),
        ('statut et rattachement', {
            'fields': ('disponibilite', 'Entreprise')
        }),
        ('horodatage', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
