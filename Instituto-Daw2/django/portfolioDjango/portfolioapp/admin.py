from django.contrib import admin


from django.contrib import admin
from .models import Categoria, Proyecto

class CategoriaAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('nombre',)
    search_fields = ['nombre']
class ProyectoAdmin(admin.ModelAdmin):
    list_display = list_display_links = ('titulo', 'descripcion', 'year')

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Proyecto, ProyectoAdmin)
# Register your models here.
