from django.db import models
from django.utils.timezone import now
from portfolioapp.models import Proyecto

class NotificaProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
    fecha = models.DateTimeField(default=now)
    notificado = models.BooleanField(default=False)
