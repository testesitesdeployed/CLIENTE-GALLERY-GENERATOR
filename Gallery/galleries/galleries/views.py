from django.shortcuts import render, get_object_or_404
# Remova a importação não usada de HttpResponseForbidden
from .models import Gallery, Photo
from django.db.models import Q 

def gallery_list(request):
    # ... (sem mudanças aqui)
    search_query = request.GET.get('q', '') 
    
    if search_query:
        galleries = Gallery.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        ).distinct()
    else:
        galleries = Gallery.objects.all()
        
    context = {
        'galleries': galleries,
        'search_query': search_query 
    }
    return render(request, 'galleries/gallery_list.html', context)


def gallery_detail(request, gallery_id):
    gallery = get_object_or_404(Gallery, pk=gallery_id)

    # Lógica 1: Se a galeria NÃO for protegida
    if not gallery.is_protected:
        context = {'gallery': gallery}
        return render(request, 'galleries/gallery_detail.html', context)

    # Lógica 2: Se for um POST (usuário enviou a senha)
    if request.method == 'POST':
        submitted_password = request.POST.get('password')

        # --- MUDANÇA PRINCIPAL AQUI ---
        # Verificando a senha usando o método hasheado
        if submitted_password and gallery.check_gallery_password(submitted_password):
            # Senha CORRETA.
            
            # (Opcional, mas recomendado) Salvar na sessão que o usuário
            # autenticou nesta galeria, para não pedir de novo.
            request.session[f'gallery_auth_{gallery_id}'] = True
            
            context = {'gallery': gallery}
            return render(request, 'galleries/gallery_detail.html', context)
        else:
            # Senha INCORRETA.
            context = {
                'gallery': gallery,
                'error': 'Senha incorreta. Tente novamente.'
            }
            return render(request, 'galleries/gallery_password_prompt.html', context)

    # Lógica 3: Se for um GET (primeiro acesso)
    
    # (Opcional) Verificar se o usuário já está autenticado na sessão
    if request.session.get(f'gallery_auth_{gallery_id}'):
        context = {'gallery': gallery}
        return render(request, 'galleries/gallery_detail.html', context)
        
    # Se não for POST e não estiver na sessão, pede a senha.
    context = {'gallery': gallery}
    return render(request, 'galleries/gallery_password_prompt.html', context)