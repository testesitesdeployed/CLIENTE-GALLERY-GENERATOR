from django.db import models
# --- NOVA IMPORTAÇÃO ---
from django.contrib.auth.hashers import make_password, check_password

class Gallery(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    password = models.CharField(
        max_length=128, 
        blank=True, 
        null=True, 
        help_text="Deixe em branco para uma galeria pública."
    )

    # --- NOVO MÉTODO (save) ---
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para garantir que a senha seja hasheada.
        """
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2$')):
            # Se a senha existe e NÃO parece já estar hasheada, hasheie.
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs) # Chama o método save original

    def __str__(self):
        return self.title

    @property
    def is_protected(self):
        return bool(self.password)
    
    # --- NOVO MÉTODO (check_password) ---
    # Adicionamos um helper no modelo para facilitar a vida na view
    def check_gallery_password(self, raw_password):
        """
        Verifica a senha pura contra a senha hasheada no banco.
        """
        if not self.password: # Se não houver senha, falha
            return False
        return check_password(raw_password, self.password)

    @property
    def get_cover_image(self):
        first_photo = self.photos.first() 
        if first_photo:
            return first_photo.image.url
        return None

class Photo(models.Model):
    # ... (sem mudanças aqui)
    gallery = models.ForeignKey(
        Gallery, 
        on_delete=models.CASCADE, 
        related_name='photos'
    )
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name