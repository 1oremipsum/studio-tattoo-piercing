from django.db import models

from django.contrib.auth.models import User

from utils.randomization.models import slugify_new
from django.utils import timezone

class Portfolio(models.Model):
    class Meta:
        verbose_name = 'Portfólio'
        verbose_name_plural = 'Portfólios'

    name = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='author',
        verbose_name='Autor'
    )

    def __str__(self):
        return self.name


class ImageCategory(models.Model):
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=255,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 4)
        return super().save(*args, **kwargs)


    def __str__(self) -> str:
        return self.name


class Image(models.Model):
    class Meta:
        verbose_name = 'Imagem'
        verbose_name_plural = 'Imagens'

    description = models.CharField(
        max_length=65, blank=True, null=True
    )
    image = models.ImageField(
        upload_to='gallery/%Y/%m/',
        verbose_name='Imagem',
        blank=False
    )
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE,
        related_name='portfolio'
    )
    category = models.ForeignKey(
        ImageCategory, on_delete=models.CASCADE,
        related_name='category'
    )
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado '
            'para a imagem ser exibida publicamente.'
        ), verbose_name='Publicar'
    )

    def __str__(self):
        return self.description or f"Imagem {self.id}"

