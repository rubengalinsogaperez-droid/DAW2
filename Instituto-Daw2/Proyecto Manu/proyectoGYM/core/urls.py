from django.urls import path

from . import views

#UD3.7.b
urlpatterns = [
    # URLs de la app core para consultar usuarios.

    path(
        "usuarios/",
        views.UsuarioListView.as_view(),
        name="usuario_list",
    ),
    path(
        "usuarios/<str:pk>/",
        views.usuario_detail,
        name="usuario_detail",
    ),
    # URLs de la app core para consultar ejercicios.
    path(
        "ejercicios/",
        views.EjercicioListView.as_view(),
        name="ejercicio_list",
    ),
    path(
        "ejercicios/<str:pk>/",
        views.ejercicio_detail,
        name="ejercicio_detail",
    ),
    # URLs de la app core para consultar rutinas.
    path(
        "rutinas/",
        views.RutinaListView.as_view(),
        name="rutina_list",
    ),
    path(
        "rutinas/<str:pk>/",
        views.rutina_detail,
        name="rutina_detail",
    ),
    # URLs de la app core para consultar entrenamientos.
    path(
        "entrenamientos/",
        views.EntrenamientoListView.as_view(),
        name="entrenamiento_list",
    ),
    path(
        "entrenamientos/<int:pk>/",
        views.entrenamiento_detail,
        name="entrenamiento_detail",
    ),
]
