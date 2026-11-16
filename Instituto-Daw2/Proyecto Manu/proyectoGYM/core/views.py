from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    View,
)
from django.db import transaction
from django.urls import reverse_lazy, reverse
#para el paginado
from .forms import EjercicioRutinaFormSet, SerieEjercicioRutinaFormSet
from .models import (
    EjercicioRutina,
    Entrenamiento,
    Ejercicio,
    Rutina,
    SerieEjercicioRutina,
    Usuario,
    UsuarioRutina,
)
from django.contrib import messages










class UsuarioListView(ListView):
    model = Usuario
    template_name = "usuario_list.html"
    paginate_by = 10


def usuario_detail(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, "usuario_detail.html", {"usuario": usuario})


class EjercicioListView(ListView):
    model = Ejercicio
    template_name = "ejercicio_list.html"
    paginate_by = 10


class EjercicioCreateView(CreateView):
    model = Ejercicio
    template_name = "base_create_update.html"
    fields = ['nombre', 'imagen', 'descripcion', 'mayor_peso', 'objetivo']
    extra_context = {
        'entity_name': 'ejercicio',
        'list_url_name': 'ejercicio_list',
    }
    success_url = reverse_lazy('ejercicio_list')


class EjercicioUpdateView(UpdateView):
    model = Ejercicio
    template_name = "base_create_update.html"
    fields = ['nombre', 'imagen', 'descripcion', 'mayor_peso', 'objetivo']
    extra_context = {
        'entity_name': 'ejercicio',
        'list_url_name': 'ejercicio_list',
        'delete_url_name': 'ejercicio_delete',
    }

    def form_valid(self, form):
        nombre_anterior = self.kwargs['pk']
        if form.cleaned_data['nombre'] == nombre_anterior:
            return super().form_valid(form)

        # Como el nombre es la clave primaria, Django guarda el nombre nuevo
        # como otro registro. Movemos sus relaciones y borramos el anterior.
        with transaction.atomic():
            ejercicio = form.save()
            EjercicioRutina.objects.filter(
                ejercicio_id=nombre_anterior,
            ).update(ejercicio=ejercicio)
            Ejercicio.objects.filter(pk=nombre_anterior).delete()
            self.object = ejercicio

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('ejercicio_detail', kwargs={'pk': self.object.pk})


class EjercicioDeleteView(DeleteView):
    model = Ejercicio
    template_name = 'base_confirm_delete.html'
    success_url = reverse_lazy('ejercicio_list')
    extra_context = {'list_url_name': 'ejercicio_list'}

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.rutinas_asociadas.exists():
            messages.warning(
                request,
                'No se puede eliminar este ejercicio porque pertenece '
                'a una o varias rutinas.',
            )
            return redirect('ejercicio_detail', pk=self.object.pk)
        return super().post(request, *args, **kwargs)


def ejercicio_detail(request, pk):
    ejercicio = get_object_or_404(Ejercicio, pk=pk)
    return render(request, "ejercicio_detail.html", {"ejercicio": ejercicio})


class RutinaListView(ListView):
    model = Rutina
    template_name = "rutina_list.html"
    paginate_by = 2


class RutinaCreateView(CreateView):
    model = Rutina
    template_name = "base_create_update.html"
    fields = ['nombre']
    extra_context = {
        'entity_name': 'rutina',
        'list_url_name': 'rutina_list',
    }
    success_url = reverse_lazy('rutina_list')


class RutinaUpdateView(UpdateView):
    model = Rutina
    template_name = "rutina_update.html"
    fields = ['nombre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'ejercicio_formset' not in context:
            if hasattr(self, '_ejercicio_formset'):
                context['ejercicio_formset'] = self._ejercicio_formset
            else:
                context['ejercicio_formset'] = EjercicioRutinaFormSet(
                    instance=self.object,
                    prefix='ejercicios',
                )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Guarda el nombre original antes de validar, porque el formulario puede cambiarlo en memoria.
        self._original_routine_name = self.object.pk
        # Prepara los ejercicios enviados para esta rutina.
        self._ejercicio_formset = EjercicioRutinaFormSet(
            request.POST,
            instance=self.object,
            prefix='ejercicios',
        )
        # Valida primero los ejercicios mientras siguen asociados a la clave original.
        ejercicio_formset_is_valid = self._ejercicio_formset.is_valid()
        form = self.get_form()
        form_is_valid = form.is_valid()
        # Guarda solo cuando ambos formularios son válidos.
        if form_is_valid and ejercicio_formset_is_valid:
            return self.form_valid(form)

        # Si hay errores, restaura la clave para volver a mostrar la rutina correcta.
        self.object.pk = self._original_routine_name
        return self.form_invalid(form)

    def form_valid(self, form):
        ejercicio_formset = self._ejercicio_formset
        old_name = self._original_routine_name
        new_name = form.cleaned_data['nombre']
        # Mantiene coherentes los cambios relacionados: se confirman todos o ninguno.
        with transaction.atomic():
            if new_name != old_name:
                # El nombre es la clave principal; crea la nueva rutina y mueve sus relaciones.
                rutina = Rutina.objects.create(nombre=new_name)
                EjercicioRutina.objects.filter(rutina_id=old_name).update(
                    rutina=rutina
                )
                Entrenamiento.objects.filter(rutina_id=old_name).update(
                    rutina=rutina
                )
                UsuarioRutina.objects.filter(rutina_id=old_name).update(
                    rutina=rutina
                )
                Rutina.objects.get(pk=old_name).delete()
                self.object = rutina
                # Hace que los ejercicios editados apunten a la rutina con el nombre nuevo.
                ejercicio_formset.instance = rutina
                for ejercicio_form in ejercicio_formset.forms:
                    if ejercicio_form.instance.pk:
                        ejercicio_form.instance.rutina = rutina
            else:
                # Si el nombre no cambia, guarda la misma rutina.
                self.object = form.save()
                ejercicio_formset.instance = self.object

            # Aplica las altas, modificaciones y eliminaciones de ejercicios.
            ejercicio_formset.save()

        # Vuelve al detalle de la rutina guardada.
        return redirect(self.get_success_url())

    def get_success_url(self):
        # Construye la URL con la clave actual de la rutina.
        return reverse('rutina_detail', kwargs={'pk': self.object.pk})


class RutinaSeriesUpdateView(View):
    # Plantilla donde se muestran y editan las series.
    template_name = 'rutina_series_form.html'

    def get_ejercicio_rutina(self):
        # Busca el ejercicio dentro de la rutina indicada en la URL.
        # Si no existe o pertenece a otra rutina, devuelve un 404.
        return get_object_or_404(
            # Carga también la rutina y el ejercicio para evitar consultas adicionales.
            EjercicioRutina.objects.select_related('rutina', 'ejercicio'),
            pk=self.kwargs['ejercicio_rutina_pk'],
            rutina_id=self.kwargs['pk'],
        )

    def render_formset(self, request, ejercicio_rutina, formset):
        # Envía a la plantilla el ejercicio, su rutina y el formulario de series.
        return render(
            request,
            self.template_name,
            {
                'ejercicio_rutina': ejercicio_rutina,
                'rutina': ejercicio_rutina.rutina,
                'formset': formset,
            },
        )

    def get(self, request, *args, **kwargs):
        # Al abrir la página, muestra las series existentes y una fila vacía para añadir otra.
        ejercicio_rutina = self.get_ejercicio_rutina()
        formset = SerieEjercicioRutinaFormSet(
            instance=ejercicio_rutina,
            # Este prefijo identifica los campos del formulario enviados por el navegador.
            prefix='series',
        )
        return self.render_formset(request, ejercicio_rutina, formset)

    def post(self, request, *args, **kwargs):
        # Recupera el mismo ejercicio y asocia al formset los datos enviados.
        ejercicio_rutina = self.get_ejercicio_rutina()
        formset = SerieEjercicioRutinaFormSet(
            request.POST,
            instance=ejercicio_rutina,
            prefix='series',
        )
        if formset.is_valid():
            # Guarda todas las series juntas; si algo falla, se revierten los cambios.
            with transaction.atomic():
                formset.save()
            # Después de guardar, vuelve al detalle de la rutina.
            return redirect('rutina_detail', pk=ejercicio_rutina.rutina_id)
        # Si hay errores, vuelve a mostrar el formulario con los datos y avisos.
        return self.render_formset(request, ejercicio_rutina, formset)


class RutinaDeleteView(DeleteView):
    model = Rutina
    template_name = 'base_confirm_delete.html'
    success_url = reverse_lazy('rutina_list')
    extra_context = {'list_url_name': 'rutina_list'}


def rutina_detail(request, pk):
    rutina = get_object_or_404(Rutina, pk=pk)
    return render(request, "rutina_detail.html", {"rutina": rutina})


class EntrenamientoListView(ListView):
    model = Entrenamiento
    template_name = "entrenamiento_list.html"
    paginate_by = 10
    queryset = Entrenamiento.objects.select_related("usuario", "rutina")


def entrenamiento_detail(request, pk):
    entrenamiento = get_object_or_404(Entrenamiento, pk=pk)
    return render(
        request,
        "entrenamiento_detail.html",
        {"entrenamiento": entrenamiento},
    )

#UD4.2.a Inicio
class UsuarioCreateView(CreateView):
    model = Usuario
    template_name = "base_create_update.html"
    fields = [
        'nickname',
        'foto_perfil',
        'altura',
        'peso',
        'objetivo',
    ]
    extra_context = {
        'entity_name': 'usuario',
        'list_url_name': 'usuario_list',
    }

    success_url = reverse_lazy('usuario_list')


class UsuarioUpdateView(UpdateView):
    model = Usuario
    template_name = "base_create_update.html"
    fields = [
        'nickname',
        'foto_perfil',
        'altura',
        'peso',
        'objetivo',
    ]
    extra_context = {
        'entity_name': 'usuario',
        'list_url_name': 'usuario_list',
        'delete_url_name': 'usuario_delete',
    }

    def get_success_url(self):
        return reverse('usuario_detail', kwargs={'pk': self.object.pk})

class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'base_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')
    extra_context = {'list_url_name': 'usuario_list'}

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (
            self.object.entrenamientos.exists()
            or self.object.usuarios_rutinas.exists()
        ):
            messages.warning(
                request,
                'No se puede eliminar este usuario porque tiene entrenamientos '
                'o rutinas asignadas.',
            )
            return redirect('usuario_detail', pk=self.object.pk)
        return super().post(request, *args, **kwargs)