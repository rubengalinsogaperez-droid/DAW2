from django.contrib import admin
from .models import Cliente, Factura, Cobro

#UD3.4.b
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = list_display_links = ("nombre", "apellidos", "nif", "email")
    list_filter = ("nif",)
    search_fields = ("nombre", "apellidos", "nif", "email")
    preserve_filters = True


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = list_display_links = ("numero", "fecha", "total")
    list_filter = ("cliente",)
    search_fields = ("numero", "cliente__nombre", "cliente__apellidos")
    preserve_filters = True


@admin.register(Cobro)
class CobroAdmin(admin.ModelAdmin):
    list_display = list_display_links = ("numero_factura", "fecha", "importe")
    list_filter = ("factura__cliente",)
    search_fields = (
        "factura__numero",
        "factura__cliente__nombre",
        "factura__cliente__apellidos",
    )
    preserve_filters = True

    @admin.display(description="N.º factura", ordering="factura__numero")
    def numero_factura(self, obj):
        return obj.factura.numero
