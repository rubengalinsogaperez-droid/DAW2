from django.urls import path

from . import views


# Rutas de clientes
urlpatterns = [
    path("cliente_list/", views.ClienteListView.as_view(), name="cliente_list"),
    path(
        "cliente_detail/<int:pk>/",
        views.ClienteDetailView.as_view(),
        name="cliente_detail",
    ),
    path("cliente_create/", views.ClienteCreateView.as_view(), name="cliente_create"),
    path(
        "cliente_update/<int:pk>/",
        views.ClienteUpdateView.as_view(),
        name="cliente_update",
    ),
    path(
        "cliente_delete/<int:pk>/",
        views.ClienteDeleteView.as_view(),
        name="cliente_delete",
    ),

    # Rutas de facturas
    path("factura_list/", views.FacturaListView.as_view(), name="factura_list"),
    path(
        "factura_detail/<int:pk>/",
        views.FacturaDetailView.as_view(),
        name="factura_detail",
    ),
    path("factura_create/", views.FacturaCreateView.as_view(), name="factura_create"),
    path(
        "factura_update/<int:pk>/",
        views.FacturaUpdateView.as_view(),
        name="factura_update",
    ),
    path(
        "factura_delete/<int:pk>/",
        views.FacturaDeleteView.as_view(),
        name="factura_delete",
    ),

    # Rutas de cobros
    path("cobro_list/", views.CobroListView.as_view(), name="cobro_list"),
    path(
        "cobro_detail/<int:pk>/",
        views.CobroDetailView.as_view(),
        name="cobro_detail",
    ),
    path("cobro_create/", views.CobroCreateView.as_view(), name="cobro_create"),
    path(
        "cobro_update/<int:pk>/",
        views.CobroUpdateView.as_view(),
        name="cobro_update",
    ),
    path(
        "cobro_delete/<int:pk>/",
        views.CobroDeleteView.as_view(),
        name="cobro_delete",
    ),
]
