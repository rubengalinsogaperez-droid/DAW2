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
from .forms import (
    EntrenamientoForm,
    EjercicioRutinaFormSet,
    SerieEjercicioRutinaFormSet,
)
from .models import (
    EjercicioRutina,
    Entrenamiento,
    Ejercicio,
    Rutina,
    SerieEjercicioRutina,
    Usuario,
    UsuarioRutina,
)
from common.mixins import (
    CreateUpdateContextMixin,
    DeleteViewDependencyMixin,
    OrderingListViewMixin,
    UsuarioMetricValidationMixin,
)










class UsuarioListView(OrderingListViewMixin, ListView):
    model = Usuario
    template_name = "usuario_list.html"
    paginate_by = 10


def usuario_detail(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, "usuario_detail.html", {"usuario": usuario})


class EjercicioListView(OrderingListViewMixin, ListView):
    model = Ejercicio
    template_name = "ejercicio_list.html"
    paginate_by = 10


class EjercicioCreateView(CreateUpdateContextMixin, CreateView):
    model = Ejercicio
    template_name = "base_create_update.html"
    fields = ['nombre', 'imagen', 'descripcion', 'mayor_peso', 'objetivo']
    # UD4.2.c / UD4.2.d: El mixin añade estos atributos al contexto.
    titulo_creacion = 'Crear ejercicio'
    titulo_actualizacion = None
    url_borrado = None
    extra_context = {
        'entity_name': 'ejercicio',
        'list_url_name': 'ejercicio_list',
    }
    success_url = reverse_lazy('ejercicio_list')


class EjercicioUpdateView(CreateUpdateContextMixin, UpdateView):
    model = Ejercicio
    template_name = "base_create_update.html"
    fields = ['nombre', 'imagen', 'descripcion', 'mayor_peso', 'objetivo']
    # UD4.2.c / UD4.2.d: El mixin añade estos atributos al contexto.
    titulo_creacion = None
    titulo_actualizacion = 'Actualizar ejercicio'
    url_borrado = 'ejercicio_delete'
    extra_context = {
        'entity_name': 'ejercicio',
        'list_url_name': 'ejercicio_list',
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


class EjercicioDeleteView(DeleteViewDependencyMixin, DeleteView):
    model = Ejercicio
    template_name = 'base_confirm_delete.html'
    success_url = reverse_lazy('ejercicio_list')
    dependency_relations = ('rutinas_asociadas',)
    # UD4.2.e: Título y mensaje para la plantilla común de borrado.
    extra_context = {
        'list_url_name': 'ejercicio_list',
        'titulo': 'Eliminar ejercicio',
        'mensaje_confirmación': (
            '¿Seguro que quieres eliminar este ejercicio? '
            'Esta acción no se puede deshacer.'
        ),
    }

def ejercicio_detail(request, pk):
    ejercicio = get_object_or_404(Ejercicio, pk=pk)
    return render(request, "ejercicio_detail.html", {"ejercicio": ejercicio})


class RutinaListView(OrderingListViewMixin, ListView):
    model = Rutina
    template_name = "rutina_list.html"
    paginate_by = 2


class RutinaCreateView(CreateUpdateContextMixin, CreateView):
    model = Rutina
    template_name = "base_create_update.html"
    fields = ['nombre']
    # UD4.2.c / UD4.2.d: El mixin añade estos atributos al contexto.
    titulo_creacion = 'Crear rutina'
    titulo_actualizacion = None
    url_borrado = None
    extra_context = {
        'entity_name': 'rutina',
        'list_url_name': 'rutina_list',
    }
    success_url = reverse_lazy('rutina_list')


class RutinaUpdateView(CreateUpdateContextMixin, UpdateView):
    model = Rutina
    template_name = "base_create_update.html"
    fields = ['nombre']
    # UD4.2.c / UD4.2.d: El mixin añade estos atributos al contexto.
    titulo_creacion = None
    titulo_actualizacion = 'Actualizar rutina'
    url_borrado = 'rutina_delete'
    extra_context = {
        'entity_name': 'rutina',
        'list_url_name': 'rutina_list',
    }

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


class RutinaDeleteView(DeleteViewDependencyMixin, DeleteView):
    model = Rutina
    template_name = 'base_confirm_delete.html'
    success_url = reverse_lazy('rutina_list')
    dependency_relations = (
        'ejercicios_rutina',
        'entrenamientos',
        'usuarios_rutinas',
    )
    # UD4.2.e: Título y mensaje para la plantilla común de borrado.
    extra_context = {
        'list_url_name': 'rutina_list',
        'titulo': 'Eliminar rutina',
        'mensaje_confirmación': (
            '¿Seguro que quieres eliminar esta rutina? '
            'Esta acción no se puede deshacer.'
        ),
    }


def rutina_detail(request, pk):
    rutina = get_object_or_404(Rutina, pk=pk)
    return render(request, "rutina_detail.html", {"rutina": rutina})


class EntrenamientoListView(OrderingListViewMixin, ListView):
    model = Entrenamiento
    template_name = "entrenamiento_list.html"
    paginate_by = 10
    queryset = Entrenamiento.objects.select_related("usuario", "rutina")


class EntrenamientoCreateView(CreateView):
    model = Entrenamiento
    form_class = EntrenamientoForm
    template_name = "base_create_update.html"
    extra_context = {
        'titulo_creacion': 'Registrar entrenamiento',
        'titulo_actualizacion': None,
        'url_borrado': None,
        'entity_name': 'entrenamiento',
        'list_url_name': 'entrenamiento_list',
    }

    def get_success_url(self):
        return reverse('entrenamiento_detail', kwargs={'pk': self.object.pk})


def entrenamiento_detail(request, pk):
    entrenamiento = get_object_or_404(
        Entrenamiento.objects.select_related('usuario', 'rutina').prefetch_related(
            'rutina__ejercicios_rutina__ejercicio',
            'rutina__ejercicios_rutina__series',
        ),
        pk=pk,
    )
    return render(
        request,
        "entrenamiento_detail.html",
        {"entrenamiento": entrenamiento},
    )

#UD4.2.a Inicio
class UsuarioCreateView(
    #UD4.2.h MIXIN PRIMERAVALIDACION
    UsuarioMetricValidationMixin,
    CreateUpdateContextMixin,
    CreateView,
):
    model = Usuario
    template_name = "base_create_update.html"
    fields = [
        'nickname',
        'foto_perfil',
        'altura',
        'peso',
        'objetivo',
    ]
    # UD4.2.c / UD4.2.d: El mixin añade estos atributos al contexto.
    titulo_creacion = 'Crear usuario'
    titulo_actualizacion = None
    url_borrado = None
    extra_context = {
        'entity_name': 'usuario',
        'list_url_name': 'usuario_list',
    }

    success_url = reverse_lazy('usuario_list')


class UsuarioUpdateView(
    #UD4.2.h MIXIN SEGUNDAVALIDACION
    UsuarioMetricValidationMixin,
    CreateUpdateContextMixin,
    UpdateView,
):
    model = Usuario
    template_name = "base_create_update.html"
    fields = [
        'nickname',
        'foto_perfil',
        'altura',
        'peso',
        'objetivo',
    ]
    # UD4.2.c / UD4.2.d: El mixin añade estos atributos al contexto.
    titulo_creacion = None
    titulo_actualizacion = 'Actualizar usuario'
    url_borrado = 'usuario_delete'
    extra_context = {
        'entity_name': 'usuario',
        'list_url_name': 'usuario_list',
    }

    def get_success_url(self):
        return reverse('usuario_detail', kwargs={'pk': self.object.pk})

class UsuarioDeleteView(DeleteViewDependencyMixin, DeleteView):
    model = Usuario
    template_name = 'base_confirm_delete.html'
    success_url = reverse_lazy('usuario_list')
    dependency_relations = ('entrenamientos', 'usuarios_rutinas')
    # UD4.2.e: Título y mensaje para la plantilla común de borrado.
    extra_context = {
        'list_url_name': 'usuario_list',
        'titulo': 'Eliminar usuario',
        'mensaje_confirmación': (
            '¿Seguro que quieres eliminar este usuario? '
            'Esta acción no se puede deshacer.'
        ),
    }
