from django.shortcuts import render
from django.views.generic import ListView
#para el paginado


from .models import Entrenamiento, Ejercicio, Rutina, Usuario


class UsuarioListView(ListView):
    model = Usuario
    template_name = "core/usuario_list.html"
    paginate_by = 10


def usuario_detail(request, pk):
    return render(request, "core/usuario_detail.html", {"pk": pk})


class EjercicioListView(ListView):
    model = Ejercicio
    template_name = "core/ejercicio_list.html"
    paginate_by = 10


def ejercicio_detail(request, pk):
    return render(request, "core/ejercicio_detail.html", {"pk": pk})


class RutinaListView(ListView):
    model = Rutina
    template_name = "core/rutina_list.html"
    paginate_by = 2


def rutina_detail(request, pk):
    return render(request, "core/rutina_detail.html", {"pk": pk})


class EntrenamientoListView(ListView):
    model = Entrenamiento
    template_name = "core/entrenamiento_list.html"
    paginate_by = 10
    queryset = Entrenamiento.objects.select_related("usuario", "rutina")


def entrenamiento_detail(request, pk):
    return render(request, "core/entrenamiento_detail.html", {"pk": pk})
