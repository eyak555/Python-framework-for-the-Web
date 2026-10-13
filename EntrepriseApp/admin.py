from django.contrib import admin
from .models import Entreprise, utilisateur
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'role', 'is_active', 'is_superuser')
    

admin.site.register(Entreprise)
admin.site.register(utilisateur, UserAdmin)