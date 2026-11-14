from django.contrib import admin
from .models import (
    Ejercicio,
    EjercicioRutina,
    Entrenamiento,
    Rutina,
    SerieEjercicioRutina,
    Usuario,
    UsuarioRutina,
)
#Esto me trae todos los modelos a admin para poder implementarlos 🥸🤌




#gracias a todo esto puedo meterme en /admin y poder manejar y
#  administrar desde ahi esto es super util por que metes los datos manualmente desde la web 🤩🤩

#UD3.4.a

class EjercicioRutinaInline(admin.TabularInline):
    # Permite añadir ejercicios directamente al editar una rutina.
    model = EjercicioRutina
    extra = 1
    show_change_link = True


class SerieEjercicioRutinaInline(admin.TabularInline):
    # Permite añadir series al ejercicio de una rutina sin editar su número.
    model = SerieEjercicioRutina
    extra = 1
    readonly_fields = ("numero",)


@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    # Muestra, filtra y busca ejercicios por sus datos principales.
    list_display = ("nombre", "objetivo", "mayor_peso")
    search_fields = ("nombre", "objetivo", "descripcion")
    list_filter = ("objetivo",)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # Muestra y permite buscar o filtrar usuarios.
    list_display = ("nickname", "objetivo", "perfil_privado")
    search_fields = ("nickname", "objetivo")
    list_filter = ("perfil_privado", "objetivo")


@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    # Gestiona rutinas y sus ejercicios relacionados desde la misma página.
    list_display = ("nombre",)
    search_fields = ("nombre",)
    inlines = (EjercicioRutinaInline,)


@admin.register(EjercicioRutina)
class EjercicioRutinaAdmin(admin.ModelAdmin):
    # Gestiona los ejercicios de cada rutina y sus series.
    list_display = ("rutina", "ejercicio", "tiempo")
    list_select_related = ("rutina", "ejercicio")
    list_filter = ("rutina",)
    search_fields = ("rutina__nombre", "ejercicio__nombre")
    inlines = (SerieEjercicioRutinaInline,)


@admin.register(Entrenamiento)
class EntrenamientoAdmin(admin.ModelAdmin):
    # Muestra y permite filtrar entrenamientos por fecha y buscar sus datos.
    list_display = ("usuario", "rutina", "fecha")
    list_filter = ("fecha",)
    search_fields = ("usuario__nickname", "rutina__nombre", "notas")


@admin.register(UsuarioRutina)
class UsuarioRutinaAdmin(admin.ModelAdmin):
    # Gestiona las rutinas asignadas a cada usuario.
    list_display = ("usuario", "rutina")
    list_filter = ("rutina",)
    search_fields = ("usuario__nickname", "rutina__nombre")
