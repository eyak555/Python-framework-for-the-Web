from django.contrib import admin, messages
from django.utils import timezone
from django.utils.html import format_html
from .models import Expedition
from OffreApp.models import Offre


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


class OffreInline(admin.StackedInline):
    model = Offre
    extra = 0
    fk_name = 'expedition'
    readonly_fields = ('Entreprise', 'Vehicule', 'prix', 'delai_jours', 'status')
    show_change_link = True
    can_delete = False


@admin.action(description="Clôturer les expéditions sélectionnées")
def cloturer_expeditions(modeladmin, request, queryset):
    en_cours_qs = queryset.filter(status='en_cours')
    count = 0
    for expedition in en_cours_qs:
        expedition.status = 'terminee'
        expedition.full_clean()
        expedition.save()
        count += 1

    if count > 0:
        modeladmin.message_user(
            request,
            f"{count} expédition(s) clôturée(s) avec succès.",
            messages.SUCCESS
        )
    else:
        modeladmin.message_user(
            request,
            "Aucune expédition au statut 'en_cours' parmi la sélection.",
            messages.WARNING
        )


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'ville_depart', 'ville_arrivee', 'poids',
                    'date_souhaitee', 'status', 'statut_colore', 'entreprise')
    list_editable = ('status',)
    search_fields = ('reference', 'entreprise__raison_sociale')
    list_filter = ('status', 'entreprise', EnRetardFilter)
    ordering = ('-created_at',)
    date_hierarchy = 'date_souhaitee'
    list_per_page = 25
    inlines = [OffreInline]
    actions = [cloturer_expeditions]
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

    @admin.display(description='Statut visuel')
    def statut_colore(self, obj):
        couleurs = {
            'en_attente': '#F0AD4E',
            'publiee': '#0275D8',
            'attribuee': '#5CB85C',
            'en_cours': '#5BC0DE',
            'terminee': '#6C757D',
            'annulee': '#D9534F',
        }
        return format_html(
            '<span style="color:white;background:{};padding:3px 8px;border-radius:4px;">{}</span>',
            couleurs.get(obj.status, '#999'),
            obj.get_status_display(),
        )
