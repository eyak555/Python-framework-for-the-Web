from django.contrib import admin
from django.urls import path
from .models import Entreprise, utilisateur
from VehiculeApp.models import Vehicule
from django.contrib.auth.admin import UserAdmin 
from .views import health_check_view

admin.site.site_header = "transconnect - Administration"
admin.site.site_title = "transconnect"
admin.site.index_title = "tableau de bord"


original_get_urls = admin.site.get_urls

def get_admin_urls():
    custom_urls = [
        path('health-check/', admin.site.admin_view(health_check_view), name='health_check'),
    ]
    return custom_urls + original_get_urls()

admin.site.get_urls = get_admin_urls


@admin.register(utilisateur)
class UserAdmin(UserAdmin):
    list_display = ('user_id', 'username', 'email', 'role', 'is_active', 'is_superuser')
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')
    fieldsets = (
        ('Identification', {
            'fields': ('user_id', 'username', 'first_name', 'last_name', 'email')
        }),
        ('Profil et permissions', {
            'fields': ('telephone', 'role', 'is_active', 'is_staff', 'is_superuser',
                       'groups', 'user_permissions')
        }),
        ('Sécurité', {
            'fields': ('password',)
        }),
        ('Horodatage', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'usable_password', 'email', 'password1', 'password2', 'role')
        }),
    )
    list_filter = ("role", "is_active")


class VehiculeInline(admin.TabularInline):
    model = Vehicule
    fields = ("immatriculation", "type_vehicule", "capacite", "disponibilite")
    extra = 2
    show_change_link = True


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    inlines = [VehiculeInline]
    list_display = ('raison_sociale', 'matricule_fiscale', 'type_entreprise', 'gerant')
    search_fields = ('raison_sociale', 'matricule_fiscale')
    list_filter = ('type_entreprise',)
    ordering = ('raison_sociale',)
    readonly_fields = ('creation_date', 'update_date')
    fieldsets = (
        ('Identification', {
            'fields': ('raison_sociale', 'matricule_fiscale', 'type_entreprise')
        }),
        ('Adresse et gérant', {
            'fields': ('adresse', 'gerant')
        }),
        ('Horodatage', {
            'fields': ('creation_date', 'update_date'),
            'classes': ('collapse',)
        }),
    )
