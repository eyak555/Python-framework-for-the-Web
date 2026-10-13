from django.contrib import admin
from .models import Offre


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('prix', 'delai_jours', 'status', 'Entreprise', 'Vehicule',
                    'expedition')
    readonly_fields = ('date_proposition', 'created_at', 'updated_at')
    fieldsets = (
        ('Proposition', {
            'fields': ('prix', 'delai_jours', 'status')
        }),
        ('Rattachement', {
            'fields': ('Entreprise', 'Vehicule', 'expedition')
        }),
        ('Horodatage', {
            'fields': ('date_proposition', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )