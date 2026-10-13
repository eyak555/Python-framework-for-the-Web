from django.contrib import admin
from .models import Expedition


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'ville_depart', 'ville_arrivee', 'poids',
                    'date_souhaitee', 'status', 'entreprise')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Identification', {
            'fields': ('reference', 'description')
        }),
        ('Itinéraire et chargement', {
            'fields': ('ville_depart', 'ville_arrivee', 'poids', 'date_souhaitee')
        }),
        ('Statut et entreprise', {
            'fields': ('status', 'entreprise')
        }),
        ('Horodatage', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )