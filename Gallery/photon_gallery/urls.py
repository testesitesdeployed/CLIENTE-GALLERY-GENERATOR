# photon_gallery/urls.py
from django.contrib import admin
# Adicione 'include' à importação
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Esta linha diz: "Para qualquer URL que comece com '', 
    # consulte o arquivo 'galleries.urls' para obter mais instruções"
    path('', include('galleries.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)