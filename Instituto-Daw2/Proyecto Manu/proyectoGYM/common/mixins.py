from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseRedirect


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
