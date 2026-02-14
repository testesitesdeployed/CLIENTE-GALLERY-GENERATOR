from django.contrib import admin
from .models import Gallery, Photo

# Classe padrão do Django para adicionar fotos DENTRO da galeria
class PhotoInline(admin.TabularInline):
    model = Photo
    # 'extra' permite que você veja N caixas de upload de uma vez
    extra = 3 

class GalleryAdmin(admin.ModelAdmin):
    # Anexa o 'inline' padrão
    inlines = [PhotoInline]
    
    # Adiciona 'is_protected' à lista para fácil visualização
    list_display = ('title', 'created_at', 'is_protected')
    search_fields = ('title',)
    
    # Organiza os campos de edição, incluindo a nova senha
    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('Segurança', {
            'fields': ('password',),
            'description': 'Deixe a senha em branco para uma galeria pública.'
        }),
    )

# Remove o registro antigo, se houver
try:
    admin.site.unregister(Gallery)
except admin.sites.NotRegistered:
    pass

admin.site.register(Gallery, GalleryAdmin)

# Também registre o modelo Photo para que apareça no admin (opcional)
admin.site.register(Photo)