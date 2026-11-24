from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row

from .models import Cliente, Cobro, Factura

# UD4.4.d Organizar por columnas sirve para que los formularios de billing
# se vean organizados en columnas en la página,
# tiene relación con Boostrap que divide cada fila en 12 columnas
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # UD4.4.d
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-md-3'),
                Column('apellidos', css_class='col-md-6'),
                Column('nif', css_class='col-md-3'),
            ),
            Row(Column('email', css_class='col-12')),
        )

#UD4.3.b
class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # UD4.4.d
        self.helper.layout = Layout(
            Row(Column('cliente', css_class='col-12')),
            Row(
                Column('numero', css_class='col-md-4'),
                Column('fecha', css_class='col-md-4'),
                Column('total', css_class='col-md-4'),
            ),
            Row(Column('concepto', css_class='col-12')),
        )

    #uso del metodo clean
    def clean(self):
        cleaned_data = super().clean()
        total = cleaned_data.get('total')

        if total is not None and total <= 0:
            self.add_error(
                'total',
                'El importe de la factura debe ser mayor que 0.',
            )

        return cleaned_data


class CobroForm(forms.ModelForm):
    class Meta:
        model = Cobro
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # UD4.4.d
        self.helper.layout = Layout(
            Row(Column('factura', css_class='col-12')),
            Row(
                Column('fecha', css_class='col-md-6'),
                Column('importe', css_class='col-md-6'),
            ),
        )

    #uso del metodo clean otra vez
    def clean(self):
        cleaned_data = super().clean()
        importe = cleaned_data.get('importe')

        if importe is not None and importe <= 0:
            self.add_error(
                'importe',
                'El importe del cobro debe ser mayor que 0.',
            )

        return cleaned_data
