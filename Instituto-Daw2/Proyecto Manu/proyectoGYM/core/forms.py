from django.forms import inlineformset_factory

from .models import EjercicioRutina, Rutina, SerieEjercicioRutina


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
