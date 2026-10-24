from django.db import models
from django.utils.timezone import now

#Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length = 250, verbose_name='Nombre', null=False, blank=False)

class Proyecto(models.Model):
    categorias = models.ManyToManyField(Categoria, verbose_name='Categoría',related_name="proyectos")
    titulo = models.CharField(max_length = 250, verbose_name='Título', null=False, blank=False)
    descripcion = models.TextField(verbose_name='Descripción', null=False, blank=False)
    year = models.IntegerField(verbose_name='Año', null=False, blank=False)
    fecha_creacion = models.DateTimeField(verbose_name='Fecha creación', default=now)
    imagen = models.ImageField(verbose_name = 'Imagen', null=True, blank=True)

#ESTO ES PARA EL MARTS 

# class Perfil(models.Model):
#     usuario = models.OneToOneField(User, verbose_name='Usuario', on_delete=models.CASCADE)
#     peso = models.FloatField(verbose_name='Peso', null=Fakllse, blank=False)
#     altura = models.FloatField(verbose_name='Altura', null=False, blank=False)
#     objetivo = models.TextField(verbose_name='Objetivo', null=False, blank=False)
   
# class Rutina(models.Model):
#     usuario = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.CASCADE, related_name="rutinas")
#     nombre = models.CharField(max_length = 250, verbose_name='Nombre', null=False, blank=False)
#     descripcion = models.TextField(verbose_name='Descripción', null=False, blank=False)
#     fecha_creacion = models.DateTimeField(verbose_name='Fecha creación', default=now)
#     imagen = models.ImageField(verbose_name = 'Imagen', null=True, blank=True)

# class categoriaRutina(models.Model):
#     nombre = models.CharField(max_length = 250, verbose_name='Nombre', null=False, blank=False)
#     descripcion = models.TextField(verbose_name='Descripción', null=False, blank=False)

# class Ejercicio(models.Model):
#     categorias = models.ForeignKey(categoriaRutina, verbose_name='Categoría',related_name="ejercicios", on_delete=models.CASCADE)
#     nombre = models.CharField(max_length = 250, verbose_name='Nombre', null=False, blank=False)
#     descripcion = models.TextField(verbose_name='Descripción', null=False, blank=False)
#     fecha_creacion = models.DateTimeField(verbose_name='Fecha creación', default=now)
#     imagen = models.ImageField(verbose_name = 'Imagen', null=True, blank=True)

# class RutinaEjercicio(models.Model):
#     rutina = models.ForeignKey(Rutina, verbose_name='Rutina', on_delete=models.CASCADE, related_name="ejercicios")
#     ejercicio = models.ForeignKey(Ejercicio, verbose_name='Ejercicio', on_delete=models.CASCADE, related_name="rutinas")
#     series = models.IntegerField(verbose_name='Series', null=False, blank=False)
#     repeticiones = models.IntegerField(verbose_name='Repeticiones', null=False, blank=False)
#     descanso = models.IntegerField(verbose_name='Descanso (segundos)', null=False, blank=False)
