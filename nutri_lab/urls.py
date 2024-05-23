from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .api import api


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('autenticacao.urls')),
    path('', include('plataforma.urls')),
    path('consultas/', include('consultas.urls')),
    path('api/', api.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
