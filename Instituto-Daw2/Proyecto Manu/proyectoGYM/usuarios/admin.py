from django.contrib import admin
from .models import MyUser

@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    #list display son las columnas de la lista
    list_display = ("username", "email", "is_staff", "is_active", "create_date", "update_date")
    #podemos buscar por email o username
    search_fields = ("email", "username")
    #filtros laterales
    list_filter = ("is_staff", "is_active")
    #campos que no se pueden editar si no que solo se pueden leer
    readonly_fields = ("create_date", "update_date")