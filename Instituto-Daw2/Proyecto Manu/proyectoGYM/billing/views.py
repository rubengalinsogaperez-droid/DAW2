from django.contrib import messages
#esto sirve para controlar y poner mensajes por pantalla 
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
#reverse para que los que necesitan id o pk como cliente update
#para el paginado
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

class ClienteCreateView(CreateView):
    model = Cliente
    template_name = 'base_create_update.html'
    fields = ['nombre', 'apellidos', 'nif', 'email']
    extra_context = {'entity_name': 'cliente', 
                     'list_url_name': 'cliente_list'
                     }
    #esto le indica a que objetos de la tabla toma
    #y si bien devuelve con get_succes url el cual
    #como necesita el pk esta formado de la siguiente manera
    def get_success_url(self):
        return reverse('cliente_update', kwargs={'pk': self.object.pk})


class ClienteUpdateView(UpdateView):
    model = Cliente
    template_name = 'base_create_update.html'
    fields = ['nombre', 'apellidos', 'nif', 'email']
    extra_context = {'entity_name': 'cliente', 'list_url_name': 'cliente_list'}
    def get_success_url(self):
        return reverse('cliente_update', kwargs={'pk': self.object.pk})

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'base_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')
    extra_context = {'list_url_name': 'cliente_list'}

    #como si tiene facturas asociadas da un errro kilometrico y no queremos que el usuario 
    #vea eso vamos a controlarlo (Sacado de copilot)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        #si existe una factura asociada al usuario envia un mensaje y redirije a cliente detail
        if self.object.factura_set.exists():
            messages.warning(
                request,
                'No se puede borrar este cliente porque tiene facturas asociadas.',
            )
            return redirect('cliente_detail', pk=self.object.pk)
        #En caso contrario sigue por chill por su lao sin entrar en el if 
        return super().post(request, *args, **kwargs)


class FacturaCreateView(CreateView):
    model = Factura
    template_name = 'base_create_update.html'
    fields = ['cliente', 'numero', 'concepto', 'fecha', 'total']
    extra_context = {'entity_name': 'factura', 'list_url_name': 'factura_list'}

    def get_success_url(self):
        return reverse('factura_update', kwargs={'pk': self.object.pk})


class FacturaUpdateView(UpdateView):
    model = Factura
    template_name = 'base_create_update.html'
    fields = ['cliente', 'numero', 'concepto', 'fecha', 'total']
    extra_context = {'entity_name': 'factura', 'list_url_name': 'factura_list'}

    def get_success_url(self):
        return reverse('factura_update', kwargs={'pk': self.object.pk})


class FacturaDeleteView(DeleteView):
    model = Factura
    template_name = 'base_confirm_delete.html'
    success_url = reverse_lazy('factura_list')
    extra_context = {'list_url_name': 'factura_list'}

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.cobro_set.exists():
            messages.warning(
                request,
                'No se puede borrar esta factura porque tiene cobros asociados.',
            )
            return redirect('factura_detail', pk=self.object.pk)
        return super().post(request, *args, **kwargs)


class CobroCreateView(CreateView):
    model = Cobro
    template_name = 'base_create_update.html'
    fields = ['factura', 'fecha', 'importe']
    extra_context = {'entity_name': 'cobro', 'list_url_name': 'cobro_list'}

    def get_success_url(self):
        return reverse('cobro_update', kwargs={'pk': self.object.pk})


class CobroUpdateView(UpdateView):
    model = Cobro
    template_name = 'base_create_update.html'
    fields = ['factura', 'fecha', 'importe']
    extra_context = {'entity_name': 'cobro', 'list_url_name': 'cobro_list'}

    def get_success_url(self):
        return reverse('cobro_update', kwargs={'pk': self.object.pk})


class CobroDeleteView(DeleteView):
    model = Cobro
    template_name = 'base_confirm_delete.html'
    success_url = reverse_lazy('cobro_list')
    # Indica a la plantilla compartida a qué listado volver si se cancela.
    extra_context = {'list_url_name': 'cobro_list'}

    #UD4.2.a 