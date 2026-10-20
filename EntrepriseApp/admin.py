from django.contrib import admin
from .models import Entreprise, utilisateur
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

@admin.register(utilisateur)
class UserAdmin(DjangoUserAdmin):
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


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('raison_sociale', 'matricule_fiscale', 'type_entreprise', 'gerant')
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