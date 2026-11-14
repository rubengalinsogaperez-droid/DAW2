from django.shortcuts import render
from django.views.generic import ListView, DetailView
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
