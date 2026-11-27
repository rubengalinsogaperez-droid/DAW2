from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from common import views as common_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", common_views.HomeView.as_view(), name="home"),
    path("panel/", common_views.PanelView.as_view(), name="panel"),

    # Cada aplicación define sus rutas; aquí se conectan con el proyecto.
    path("core/", include("core.urls")),
    path("", include("billing.urls")),
    #Ruta para usuarios la cual esta referenciada a urls de usuarios
    path("usuarios/", include("usuarios.urls")),
        
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)