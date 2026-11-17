from django import forms
from django.forms import inlineformset_factory

from .models import (
    EjercicioRutina,
    Entrenamiento,
    Rutina,
    SerieEjercicioRutina,
)


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
