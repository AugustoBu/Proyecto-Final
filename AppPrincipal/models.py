from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta

class Post(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Título del Post"
    )
    subtitle = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Subtítulo del Post"
    )
    body = models.TextField(verbose_name="Contenido del Post")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Autor"
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
        verbose_name="Imagen del Post"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']  
        
    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%d/%m/%Y')}"

    @property
    def short_body(self):
        """Devuelve una versión corta del contenido (primeros 100 caracteres)."""
        return f"{self.body[:100]}..." if len(self.body) > 100 else self.body

    @property
    def is_recent(self):
        """Determina si el post es reciente (creado en los últimos 7 días)."""
        return self.created_at >= timezone.now() - timedelta(days=7)