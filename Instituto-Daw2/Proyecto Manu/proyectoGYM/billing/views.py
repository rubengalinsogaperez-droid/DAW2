#esto sirve para controlar y poner mensajes por pantalla 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
#reverse para que los que necesitan id o pk como cliente update
#para el paginado
from common.mixins import DeleteViewDependencyMixin
from common.mixins import CreateUpdateContextMixin
from billing.mixins import CobroMixin
from billing.models import Cliente, Factura, Cobro



class ClienteListView(ListView):
    model = Cliente
    template_name = 'cliente_list.html'
    paginate_by = 10


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'cliente_detail.html'


class FacturaListView(ListView):
    model = Factura
    template_name = 'factura_list.html'
    paginate_by = 10


class FacturaDetailView(DetailView):
    model = Factura
    template_name = 'factura_detail.html'


class CobroListView(ListView):
    model = Cobro
    template_name = 'cobro_list.html'
    paginate_by = 10


class CobroDetailView(DetailView):
    model = Cobro
    template_name = 'cobro_detail.html'


#UD4.2.a Inicio

class ClienteCreateView(CreateUpdateContextMixin, CreateView):
    model = Cliente
    template_name = 'base_create_update.html'
    fields = ['nombre', 'apellidos', 'nif', 'email']
    # UD4.2.c / UD4.2.d: El mixin añade estos atributos al contexto.
    titulo_creacion = 'Crear cliente'
    titulo_actualizacion = None
    url_borrado = None
    extra_context = {'entity_name': 'cliente', 
                     'list_url_name': 'cliente_list'
                     }
    #esto le indica a que objetos de la tabla toma
    #y si bien devuelve con get_succes url el cual
    #como necesita el pk esta formado de la siguiente manera
    def get_success_url(self):
        return reverse('cliente_update', kwargs={'pk': self.object.pk})


class ClienteUpdateView(CreateUpdateContextMixin, UpdateView):
    model = Cliente
    template_name = 'base_create_update.html'
    fields = ['nombre', 'apellidos', 'nif', 'email']
    # UD4.2.c / UD4.2.d: El mixin añade estos atributos al contexto.
    titulo_creacion = None
    titulo_actualizacion = 'Actualizar cliente'
    url_borrado = 'cliente_delete'
    extra_context = {
        'entity_name': 'cliente',
        'list_url_name': 'cliente_list',
    }
    def get_success_url(self):
        return reverse('cliente_update', kwargs={'pk': self.object.pk})

class ClienteDeleteView(DeleteViewDependencyMixin, DeleteView):
    model = Cliente
    template_name = 'base_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')
    dependency_relations = ('factura_set',)
    # UD4.2.e: Título y mensaje para la plantilla común de borrado.
    extra_context = {
        'list_url_name': 'cliente_list',
        'titulo': 'Eliminar cliente',
        'mensaje_confirmación': (
            '¿Seguro que quieres eliminar este cliente? '
            'Esta acción no se puede deshacer.'
        ),
    }

class FacturaCreateView(CreateUpdateContextMixin, CreateView):
    model = Factura
    template_name = 'base_create_update.html'
    fields = ['cliente', 'numero', 'concepto', 'fecha', 'total']
    # UD4.2.c / UD4.2.d: El mixin añade estos atributos al contexto.
    titulo_creacion = 'Crear factura'
    titulo_actualizacion = None
    url_borrado = None
    extra_context = {
        'entity_name': 'factura',
        'list_url_name': 'factura_list',
    }

    def get_success_url(self):
        return reverse('factura_update', kwargs={'pk': self.object.pk})


class FacturaUpdateView(CreateUpdateContextMixin, UpdateView):
    model = Factura
    template_name = 'base_create_update.html'
    fields = ['cliente', 'numero', 'concepto', 'fecha', 'total']
    # UD4.2.c / UD4.2.d: El mixin añade estos atributos al contexto.
    titulo_creacion = None
    titulo_actualizacion = 'Actualizar factura'
    url_borrado = 'factura_delete'
    extra_context = {
        'entity_name': 'factura',
        'list_url_name': 'factura_list',
    }

    def get_success_url(self):
        return reverse('factura_update', kwargs={'pk': self.object.pk})


class FacturaDeleteView(DeleteViewDependencyMixin, DeleteView):
    model = Factura
    template_name = 'base_confirm_delete.html'
    success_url = reverse_lazy('factura_list')
    dependency_relations = ('cobro_set',)
    # UD4.2.e: Título y mensaje para la plantilla común de borrado.
    extra_context = {
        'list_url_name': 'factura_list',
        'titulo': 'Eliminar factura',
        'mensaje_confirmación': (
            '¿Seguro que quieres eliminar esta factura? '
            'Esta acción no se puede deshacer.'
        ),
    }

class CobroCreateView(CobroMixin, CreateUpdateContextMixin, CreateView):
    model = Cobro
    template_name = 'base_create_update.html'
    fields = ['factura', 'fecha', 'importe']
    # UD4.2.c / UD4.2.d: El mixin añade estos atributos al contexto.
    titulo_creacion = 'Crear cobro'
    titulo_actualizacion = None
    url_borrado = None
    extra_context = {
        'entity_name': 'cobro',
        'list_url_name': 'cobro_list',
    }

    def get_success_url(self):
        return reverse('cobro_update', kwargs={'pk': self.object.pk})


class CobroUpdateView(CobroMixin, CreateUpdateContextMixin, UpdateView):
    model = Cobro
    template_name = 'base_create_update.html'
    fields = ['factura', 'fecha', 'importe']
    # UD4.2.c / UD4.2.d: El mixin añade estos atributos al contexto.
    titulo_creacion = None
    titulo_actualizacion = 'Actualizar cobro'
    url_borrado = 'cobro_delete'
    extra_context = {
        'entity_name': 'cobro',
        'list_url_name': 'cobro_list',
    }

    def get_success_url(self):
        return reverse('cobro_update', kwargs={'pk': self.object.pk})


class CobroDeleteView(DeleteViewDependencyMixin, DeleteView):
    model = Cobro
    template_name = 'base_confirm_delete.html'
    success_url = reverse_lazy('cobro_list')
    # Indica a la plantilla compartida a qué listado volver si se cancela.
    # UD4.2.e: Título y mensaje para la plantilla común de borrado.
    extra_context = {
        'list_url_name': 'cobro_list',
        'titulo': 'Eliminar cobro',
        'mensaje_confirmación': (
            '¿Seguro que quieres eliminar este cobro? '
            'Esta acción no se puede deshacer.'
        ),
    }

    #UD4.2.a 