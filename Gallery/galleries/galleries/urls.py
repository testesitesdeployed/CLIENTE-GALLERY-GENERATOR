# galleries/urls.py (ARQUIVO NOVO)
from django.urls import path
from . import views # Importa as views (lógica) que criaremos a seguir

urlpatterns = [
    # path('', ...): A URL raiz (nossa página inicial)
    # views.gallery_list: A função de "view" que será chamada
    # name='gallery_list': Um apelido que usaremos para criar links
    path('', views.gallery_list, name='gallery_list'),
    
    # '<int:gallery_id>/': Um padrão de URL. 
    # <int:gallery_id> captura um número inteiro da URL (ex: /5/)
    # e o passa para a view como uma variável chamada 'gallery_id'.
    path('<int:gallery_id>/', views.gallery_detail, name='gallery_detail'),
]