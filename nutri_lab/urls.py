from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

#Definir as urls principais e secundarias, que apontam para as urls dos app criados
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('autenticacao.urls')),
    path('', include('plataforma.urls')),
]

#Adiciona ao urlpatterns as váriaveis estaticas de media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)