from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone
#UD4.4.c HELPER sirve para crear configuracion de crispy para dicho formulario y LAYOUT indica que campos mostrar y de que orden   por ultimo   form_tag = False evita que Crispy genere otra etiqueta <form>, porque la plantilla ya tiene una.
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row


#Importante ruben acuerdate de importar los modelos no seas bobolon
from .models import (
    EjercicioRutina,
    Entrenamiento,
    Ejercicio,
    Rutina,
    SerieEjercicioRutina,
    Usuario,
)
#UD4.3.a

class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #UD4.4.c
        self.helper = FormHelper()
        self.helper.form_tag = False
        #UD4.4.e
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-md-6'),
                Column('objetivo', css_class='col-md-6'),
            ),
            Row(
                Column('descripcion', css_class='col-md-8'),
                Column('mayor_peso', css_class='col-md-4'),
            ),
            Row(Column('imagen', css_class='col-12')),
        )

    def clean(self):
        cleaned_data = super().clean()
        mayor_peso = cleaned_data.get('mayor_peso')

        if mayor_peso is not None and mayor_peso <= 0:
            self.add_error(
                'mayor_peso',
                'El mayor peso debe ser superior a 0 kg.',
            )

        return cleaned_data


class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #UD4.4.c
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    'nombre',
                    css_class='col-md-8 offset-md-2',
                ),
            ),
        )

#UD4.3.c
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #UD4.4.c
        self.helper = FormHelper()
        self.helper.form_tag = False
        #UD4.4.e
        self.helper.layout = Layout(
            Row(
                Column('nickname', css_class='col-md-6'),
                Column('objetivo', css_class='col-md-6'),
            ),
            Row(
                Column('altura', css_class='col-md-6'),
                Column('peso', css_class='col-md-6'),
            ),
            Row(Column('foto_perfil', css_class='col-12')),
        )

    def clean(self):
        cleaned_data = super().clean()
        altura = cleaned_data.get('altura')
        peso = cleaned_data.get('peso')

        if altura is not None and altura <= 0:
            self.add_error('altura', 'La altura debe ser mayor que 0 metros.')
        if peso is not None and peso <= 0:
            self.add_error('peso', 'El peso debe ser mayor que 0 kg.')

        return cleaned_data


class EntrenamientoForm(forms.ModelForm):
    class Meta:
        model = Entrenamiento
        fields = ('usuario', 'rutina', 'fecha', 'notas')
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rutina'].required = True
        #UD4.4.c
        self.helper = FormHelper()
        self.helper.form_tag = False
        #UD4.4.e
        self.helper.layout = Layout(
            Row(
                Column('usuario', css_class='col-md-6'),
                Column('rutina', css_class='col-md-6'),
            ),
            Row(
                Column('fecha', css_class='col-md-4'),
                Column('notas', css_class='col-md-8'),
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')

        if fecha is not None and fecha > timezone.localdate():
            self.add_error(
                'fecha',
                'La fecha del entrenamiento no puede ser futura.',
            )

        return cleaned_data


EjercicioRutinaFormSet = inlineformset_factory(
    Rutina,
    EjercicioRutina,
    fields=('ejercicio', 'tiempo'),
    extra=1,
    can_delete=True,
)

SerieEjercicioRutinaFormSet = inlineformset_factory(
    EjercicioRutina,
    SerieEjercicioRutina,
    fields=('repeticiones', 'peso'),
    extra=1,
    can_delete=True,
)
