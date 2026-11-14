from urllib import request

from django.shortcuts import render
from django.shortcuts import render
from django.template import context # Para FBV
from .models import Proyecto
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic import TemplateView # Para CBV
from django.urls import reverse_lazy
from .mixins import ProyectoMixin
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from notificaciones.models import NotificaProyecto






def home_view(request):
 proyectos = Proyecto.objects.all()
 context={'proyectos': proyectos}
 return render(request, 'portfolio/home.html', context)


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
    
class ProyectoCreateView( CreateView):
    model = Proyecto
    success_message = "Proyecto creado exitosamente"
    fields = ['titulo', 'descripcion', 'fecha_creacion', 'year', 'categorias', 'imagen']

    def form_valid(self, form):
        
        
        if form.instance.fecha_creacion < timezone.now():
            print("La fecha/hora del proyecto no puede ser anterior a la actual.")
            messages.error(self.request, "La fecha/hora del proyecto no puede ser anterior a la actual.")
            return super(ProyectoCreateView, self).form_invalid(form)
        else:
            proyecto = form.save()
            NotificaProyecto.objects.create(proyecto=proyecto)
            return super(ProyectoCreateView, self).form_valid(form)



class ProyectoUpdateView(ProyectoMixin, UpdateView):
    # model = Proyecto
    # fields = ['titulo', 'descripcion', 'fecha_creacion', 'year', 'categorias', 'imagen']
    success_url = reverse_lazy('home')
    success_message = "Proyecto actualizado exitosamente"
    def get_success_message(self, cleaned_data):
        return "Proyecto '{}' actualizado exitosamente".format(str(self.object))
    

class ProyectoDeleteView(DeleteView):
 model = Proyecto
 success_url = reverse_lazy('home')




class ProyectoCreateView(SuccessMessageMixin, CreateView):
 model = Proyecto
 fields = ['titulo', 'descripcion', 'fecha_creacion', 'year', 'categorias', 'imagen']
 success_message = "Proyecto creado exitosamente"
 def get_success_url(self):
    object = self.object
    return reverse_lazy('proyecto_update', kwargs={'pk': object.id}) 


class ProyectoUpdateView(SuccessMessageMixin, UpdateView):
 model = Proyecto
 fields = ['titulo', 'descripcion', 'fecha_creacion', 'year', 'categorias', 'imagen']
 success_message = "Proyecto editado exitosamente"


class ProyectoCreateView(ProyectoMixin, CreateView):
    success_message = "Proyecto creado exitosamente"

class ProyectoUpdateView(ProyectoMixin, UpdateView):
    success_message = "Proyecto actualizado exitosamente"