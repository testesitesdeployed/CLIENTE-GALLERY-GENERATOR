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


# galleries/views.py

def gallery_detail(request, gallery_id):
    gallery = get_object_or_404(Gallery, pk=gallery_id)

    # 1. Se a galeria NÃO for protegida, libera o acesso direto
    if not gallery.is_protected:
        context = {'gallery': gallery}
        return render(request, 'galleries/gallery_detail.html', context)

    # 2. Se o usuário está enviando a senha agora (Método POST)
    if request.method == 'POST':
        submitted_password = request.POST.get('password')

        # Verifica a senha (usando o método seguro que criamos antes)
        if submitted_password and gallery.check_gallery_password(submitted_password):
            # Senha CORRETA: Mostra a galeria
            # Nota: Nós NÃO estamos mais salvando na sessão (request.session)
            context = {'gallery': gallery}
            return render(request, 'galleries/gallery_detail.html', context)
        else:
            # Senha INCORRETA: Mostra erro
            context = {
                'gallery': gallery,
                'error': 'Senha incorreta. Tente novamente.'
            }
            return render(request, 'galleries/gallery_password_prompt.html', context)

    # 3. Se for qualquer outro acesso (GET), pede a senha.
    # Removemos a verificação de sessão aqui. Toda vez que carregar a URL, pede senha.
    context = {'gallery': gallery}
    return render(request, 'galleries/gallery_password_prompt.html', context)

