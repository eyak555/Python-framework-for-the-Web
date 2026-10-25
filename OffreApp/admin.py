import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from .models import Offre


class Prix(admin.SimpleListFilter):
    title = 'prix'
    parameter_name = 'prix'

    def lookups(self, request, model_admin):
        return [
            ('moins_100', 'Moins de 100'),
            ('100_1000', 'Entre 100 et 1000'),
            ('1000_10000', 'Entre 1000 et 10000'),
            ('plus_10000', 'Plus de 10000'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'moins_100':
            return queryset.filter(prix__lt=100)
        elif self.value() == '100_1000':
            return queryset.filter(prix__gte=100, prix__lte=1000)
        elif self.value() == '1000_10000':
            return queryset.filter(prix__gte=1000, prix__lte=10000)
        elif self.value() == 'plus_10000':
            return queryset.filter(prix__gt=10000)
        return queryset


@admin.action(description="Exporter la sélection en CSV")
def exporter_offres_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="offres.csv"'
    writer = csv.writer(response)
    writer.writerow(['reference_expedition', 'transporteur', 'prix', 'statut'])
    for offre in queryset.select_related('expedition', 'Entreprise'):
        writer.writerow([
            offre.expedition.reference,
            offre.Entreprise.raison_sociale,
            offre.prix,
            offre.status
        ])
    return response


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    autocomplete_fields = ('expedition', 'Entreprise', 'Vehicule')
    list_display = ('prix', 'delai_jours', 'statut_colore', 'Entreprise', 'Vehicule', 'expedition')
    search_fields = ('expedition__reference', 'Entreprise__raison_sociale')
    list_filter = ('status', 'Entreprise', 'Vehicule', 'expedition', Prix)
    ordering = ('-created_at',)
    date_hierarchy = 'date_proposition'
    actions = [exporter_offres_csv]
    readonly_fields = ('statut_colore', 'date_proposition', 'created_at', 'updated_at')

    fieldsets = (
        ("Détails de l'offre", {
            'fields': ('expedition', 'Entreprise', 'Vehicule')
        }),
        ('Conditions', {
            'fields': ('prix', 'delai_jours')
        }),
        ('Suivi', {
            'fields': ('statut_colore', 'date_proposition', 'created_at', 'updated_at')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('prix', 'delai_jours', 'status', 'Entreprise', 'Vehicule', 'expedition')
        }),
    )

    @admin.display(description='Statut')
    def statut_colore(self, obj):
        couleurs = {
            'en_attente': '#F0AD4E',
            'acceptee': '#5CB85C',
            'refusee': '#D9534F',
        }
        return format_html(
            '<span style="color:white;background:{};padding:3px 8px;border-radius:4px;">{}</span>',
            couleurs.get(obj.status, '#999'),
            obj.get_status_display(),
        )

    def get_readonly_fields(self, request, obj=None):
        base = list(super().get_readonly_fields(request, obj))
        if obj and obj.status == 'acceptee':
            return base + ['prix', 'delai_jours']
        return base
