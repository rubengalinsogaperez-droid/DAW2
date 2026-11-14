from django.db import models
from django.utils import timezone


class Cliente(models.Model):
    nombre = models.CharField(max_length=256)
    apellidos = models.CharField(max_length=512)
    nif = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        # UD3.4.e
        ordering = ["apellidos", "nombre"]
        # UD3.4.f

    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.nif})"
    #UD3.3.b


class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    numero = models.CharField(max_length=20, verbose_name="N.º factura")
    concepto = models.TextField()
    fecha = models.DateField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "factura"
        verbose_name_plural = "facturas"
        # UD3.4.e
        ordering = ["-fecha", "numero"]
        # UD3.4.f

    def __str__(self):
        return f"Factura {self.numero} - Cliente: {self.cliente.nombre}"
    #UD3.3.b


class Cobro(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.PROTECT)
    fecha = models.DateField(default=timezone.now)
    importe = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "cobro"
        verbose_name_plural = "cobros"
        # UD3.4.e
        ordering = ["-fecha", "factura__numero"]
        # UD3.4.f

    def __str__(self):
        return f"Cobro de {self.importe}€ (Factura {self.factura.numero})"
    #UD3.3.b