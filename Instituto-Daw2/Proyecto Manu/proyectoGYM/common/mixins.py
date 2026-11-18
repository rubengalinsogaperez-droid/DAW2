from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseRedirect

#notas para mi Manu ignora esto pliz:Lo ves en la herencia de cada vista: por ejemplo, 
# en core/views.py:42, UsuarioListView está decla
# rada como class UsuarioListView(OrderingListViewMixin, ListView). 
# Eso significa que usa primero el mixin y luego ListView.
class CreateUpdateContextMixin:
    titulo_creacion = None
    titulo_actualizacion = None
    url_borrado = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # UD4.2.d: Expone los atributos de la vista como variables de plantilla.
        context.update({
            'titulo_creacion': self.titulo_creacion,
            'titulo_actualizacion': self.titulo_actualizacion,
            'url_borrado': self.url_borrado,
        })
        return context

#UD4.4.a
class CreateUpdateSuccessMessageMixin:
    def form_valid(self, form):
        response = super().form_valid(form)
        self.add_success_message()
        return response

    def add_success_message(self, obj=None):
        if obj is None:
            obj = self.object
        messages.success(
            self.request,
            f'Se ha guardado correctamente: {obj}',
        )


#UD4.2.i

class OrderingListViewMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.GET.get('ordering')

        if ordering == 'asc':
            return queryset.order_by('pk')
        if ordering == 'desc':
            return queryset.order_by('-pk')
        #si no es pedido devuelve la queryset (lista de registros de django volvera a mostrar la pagina )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordering = self.request.GET.get('ordering')
        context['ordering'] = ordering if ordering in ('asc', 'desc') else None
        return context


#UD4.2.h MIXIN DE VALIDACION
class UsuarioMetricValidationMixin:
    def form_invalid(self, form):
        if 'altura' in form.errors or 'peso' in form.errors:
            messages.error(
                self.request,
                'No se ha podido guardar el usuario. Corrige los campos marcados.',
            )
        return super().form_invalid(form)


#UD4.2.f
class DeleteViewDependencyMixin:
    dependency_relations = ()

    def form_valid(self, form):
        has_dependencies = any(
            getattr(self.object, relation).exists()
            for relation in self.dependency_relations
        )
        if has_dependencies:
            return self.show_dependency_error()

        try:
            return super().form_valid(form)
        except ProtectedError:
            return self.show_dependency_error()

    def show_dependency_error(self):
        messages.error(
            self.request,
            f'Existen dependencias para el objeto {self.object}. '
            'Elimine antes dichas dependencias',
        )
        return HttpResponseRedirect(self.get_success_url())
