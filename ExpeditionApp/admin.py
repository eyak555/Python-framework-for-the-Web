from django.contrib import admin
from .models import Expedition
from django.utils import timezone


class EnRetardFilter(admin.SimpleListFilter):
    title = 'En retard'
    parameter_name = 'en_retard'

    def lookups(self, request, model_admin):
        return (
            ('oui', 'Oui'),
            ('non', 'Non'),
        )

    def queryset(self, request, queryset):
        aujourd_hui = timezone.now().date()
        if self.value() == 'oui':
            return queryset.filter(status="publiee", date_souhaitee__lt=aujourd_hui)
        if self.value() == 'non':
            return queryset.exclude(status="publiee", date_souhaitee__lt=aujourd_hui)
        return queryset


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
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('ville_depart', 'ville_arrivee', 'poids', 'date_souhaitee', 'description', 'status', 'entreprise')
        }),
    )
    list_filter = ('status', 'entreprise', EnRetardFilter)