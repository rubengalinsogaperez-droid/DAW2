from decimal import Decimal

from django.db.models import Sum

from .models import Cobro

#UD4.2.g
class CobroMixin:
    def form_valid(self, form):
        factura = form.cleaned_data['factura']
        importe = form.cleaned_data['importe']
        cobros = Cobro.objects.filter(factura=factura)

        if self.object is not None:
            cobros = cobros.exclude(pk=self.object.pk)

        importe_acumulado = (
            cobros.aggregate(total=Sum('importe'))['total'] or Decimal('0.00')
        )
        if importe_acumulado + importe > factura.total:
            form.add_error(
                'importe',
                'La suma de los importes de los cobros no puede superar '
                'el importe de la factura.',
            )
            return self.form_invalid(form)

        return super().form_valid(form)
