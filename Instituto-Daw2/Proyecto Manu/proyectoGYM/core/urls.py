from django.urls import path

from . import views

#UD3.7.b
urlpatterns = [
    #UD4.2.B
    # USUARIOS
    path(
        "usuarios/",
        views.UsuarioListView.as_view(),
        name="usuario_list",
    ),
    path(
        "usuarios/crear/",
        views.UsuarioCreateView.as_view(),
        name="usuario_create",
    ),
    path(
        "usuarios/<str:pk>/editar/",
        views.UsuarioUpdateView.as_view(),
        name="usuario_update",
    ),
    path(
        "usuarios/<str:pk>/eliminar/",
        views.UsuarioDeleteView.as_view(),
        name="usuario_delete",
    ),
    path(
        "usuarios/<str:pk>/",
        views.usuario_detail,
        name="usuario_detail",
    ),

    # EJERCICIOS
    path(
        "ejercicios/",
        views.EjercicioListView.as_view(),
        name="ejercicio_list",
    ),
    path(
        "ejercicios/crear/",
        views.EjercicioCreateView.as_view(),
        name="ejercicio_create",
    ),
    path(
        "ejercicios/<str:pk>/editar/",
        views.EjercicioUpdateView.as_view(),
        name="ejercicio_update",
    ),
    path(
        "ejercicios/<str:pk>/eliminar/",
        views.EjercicioDeleteView.as_view(),
        name="ejercicio_delete",
    ),
    path(
        "ejercicios/<str:pk>/",
        views.ejercicio_detail,
        name="ejercicio_detail",
    ),

    # RUTINAS
    path(
        "rutinas/",
        views.RutinaListView.as_view(),
        name="rutina_list",
    ),
    path(
        "rutinas/crear/",
        views.RutinaCreateView.as_view(),
        name="rutina_create",
    ),
    path(
        "rutinas/<str:pk>/editar/",
        views.RutinaUpdateView.as_view(),
        name="rutina_update",
    ),
    path(
        "rutinas/<str:pk>/eliminar/",
        views.RutinaDeleteView.as_view(),
        name="rutina_delete",
    ),
    path(
        "rutinas/<str:pk>/",
        views.rutina_detail,
        name="rutina_detail",
    ),
    path(
        "rutinas/<str:pk>/ejercicios/<int:ejercicio_rutina_pk>/series/",
        views.RutinaSeriesUpdateView.as_view(),
        name="rutina_series_update",
    ),

    # ENTRENAMIENTOS
    path(
        "entrenamientos/",
        views.EntrenamientoListView.as_view(),
        name="entrenamiento_list",
    ),
    path(
        "entrenamientos/crear/",
        views.EntrenamientoCreateView.as_view(),
        name="entrenamiento_create",
    ),
    path(
        "entrenamientos/<int:pk>/",
        views.entrenamiento_detail,
        name="entrenamiento_detail",
    ),
]
