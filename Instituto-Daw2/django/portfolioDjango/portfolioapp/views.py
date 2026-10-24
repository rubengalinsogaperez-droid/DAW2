from urllib import request

from django.shortcuts import render
from django.shortcuts import render
from django.template import context # Para FBV
from .models import Proyecto
def home_view(request):
 proyectos = Proyecto.objects.all()
 context={'proyectos': proyectos}
 return render(request, 'portfolio/home.html', context)

from django.views.generic import TemplateView # Para CBV
from .models import Proyecto
class HomeView(TemplateView):
    template_name = 'portfolio/home.html'
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        cat_id = kwargs.get('cat_id')
        context['proyectos'] = Proyecto.objects.filter(categorias__id=cat_id) if cat_id else Proyecto.objects.all()
    
        return context


def contacto_view(request):
    context = {
        'nombre_apellidos': 'Ruben Galinsoga fbv',
    }
    return render(request,'portfolio/contacto.html',context) 

class ContactoView(TemplateView):
    template_name = 'portfolio/contacto.html'

#esto inyextara en contacto.html el nombre y apellidos de la persona que se quiere mostrar
    def get_context_data(self, *args, **kwargs):
        context = super(ContactoView, self).get_context_data(**kwargs)
        context['nombre_apellidos'] = 'Ruben Galinsoga cbv'
        return context
    

