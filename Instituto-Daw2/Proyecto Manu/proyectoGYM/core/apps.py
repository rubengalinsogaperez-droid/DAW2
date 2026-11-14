from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'Gestión del gimnasio'#Esto sirve para cambiar el nombre de la app en el panel de administración de Django UD3.4.d