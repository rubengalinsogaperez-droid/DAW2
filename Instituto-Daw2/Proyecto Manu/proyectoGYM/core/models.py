from django.db import models



#Esto van a ser las dtablas de mi proyecto, cosa que luego usaremos en otros lados 
# importandolos caso como puede ser el de admin.py
#(^///^)
class Usuario(models.Model):
    nickname = models.CharField(max_length=12, primary_key=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    altura = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    objetivo = models.CharField(max_length=50)

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        #UD3.4.e
        ordering = ['nickname'] #Esto nos sirve para ordenar y ver que ver primero, en este caso es por nickame pero se podria por feha en  alguno otro
        #UD3.4.f
        

    
class Ejercicio(models.Model):
    nombre = models.CharField(max_length=25, primary_key=True)
    imagen = models.ImageField(upload_to='ejercicios/', null=True, blank=True)
    descripcion = models.CharField(max_length=100)
    mayor_peso = models.IntegerField(null=True, blank=True)
    objetivo = models.CharField(max_length=50)

    class Meta:
        verbose_name = "ejercicio"
        verbose_name_plural = "ejercicios"
        #UD3.4.e
        ordering = ['nombre']
        #UD3.4.f
        

    def __str__(self):
        return self.nombre

    
class Rutina(models.Model):
    nombre = models.CharField(max_length=25, primary_key=True)

    class Meta:
        verbose_name = "rutina"
        verbose_name_plural = "rutinas"
        #UD3.4.e
        ordering = ['nombre']
        #UD3.4.f

    def __str__(self):
        return self.nombre


class EjercicioRutina(models.Model):
    rutina = models.ForeignKey(
        Rutina,
        on_delete=models.CASCADE,
        related_name='ejercicios_rutina'
    )
    ejercicio = models.ForeignKey(
        Ejercicio,
        on_delete=models.CASCADE,
        related_name='rutinas_asociadas'
    )
    tiempo = models.DurationField(null=True, blank=True)

    class Meta:
        verbose_name = "ejercicio de rutina"
        verbose_name_plural = "ejercicios de rutina"
        #UD3.4.e
        ordering = ['rutina__nombre', 'ejercicio__nombre']
        #UD3.4.f

    def __str__(self):
        return f"{self.rutina.nombre} - {self.ejercicio.nombre}"
    #UD3.3.b

class SerieEjercicioRutina(models.Model):
    ejercicio_rutina = models.ForeignKey(
        EjercicioRutina,
        on_delete=models.CASCADE,
        related_name='series'
    )
    numero = models.PositiveIntegerField(null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    repeticiones = models.PositiveIntegerField()

    class Meta:
        verbose_name = "serie de ejercicio de rutina"
        verbose_name_plural = "series de ejercicio de rutina"
        ordering = [
            'ejercicio_rutina__rutina__nombre',
            'ejercicio_rutina__ejercicio__nombre',
            'numero',
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['ejercicio_rutina', 'numero'],
                name='uniq_serie_por_ejercicio',
            ),
        ]

    def save(self, *args, **kwargs):
        if self.pk is None and self.numero is None:
            ultima_serie = self.ejercicio_rutina.series.aggregate(
                numero_maximo=models.Max('numero')
            )['numero_maximo']
            self.numero = (ultima_serie or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Serie {self.numero}: {self.ejercicio_rutina} "
            f"({self.repeticiones} repeticiones, {self.peso} kg)"
        )
    #UD3.3.b


class Entrenamiento(models.Model):
    usuario = models.ForeignKey(
    Usuario,
    on_delete=models.CASCADE,
    related_name='entrenamientos'
    )
    rutina = models.ForeignKey(
    Rutina,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='entrenamientos'
    )
    fecha = models.DateField()
    notas = models.CharField(max_length=250, blank=True)

    class Meta:
        verbose_name = "entrenamiento"
        verbose_name_plural = "entrenamientos"
        #Esto nos sirve para que te muestre si es un ejercicio "entrenamiento" si es uno o "entrenamientos" si son varios, en el panel de administración de Django
        #UD3.4.e
        ordering = ['-fecha', 'usuario__nickname', 'rutina__nombre']
        #UD3.4.f

    def __str__(self):
        rutina_nombre = self.rutina.nombre if self.rutina else 'Rutina eliminada'
        return f"{self.usuario.nickname} - {rutina_nombre} - {self.fecha}"
    #UD3.3.b
class UsuarioRutina(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='usuarios_rutinas'
    )
    rutina = models.ForeignKey(
        Rutina,
        on_delete=models.CASCADE,
        related_name='usuarios_rutinas'
    )

    class Meta:
        unique_together = (('usuario', 'rutina'),) 
        #UD3.3.c
        verbose_name = "rutina de usuario"
        verbose_name_plural = "rutinas de usuario"
        #UD3.4.e
        ordering = ['usuario__nickname', 'rutina__nombre']
        #UD3.4.f

    def __str__(self):
        return f"{self.usuario.nickname} - {self.rutina.nombre}"
    #UD3.3.b