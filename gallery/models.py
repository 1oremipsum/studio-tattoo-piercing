from django.db import models

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from utils.randomization.models import slugify_new
from utils.resizing.images import resize_image


class ImageQuerySet(models.QuerySet):
    def get_published(self):
        return self.filter(is_published=True)

    def get_order_desc(self):
        return self.order_by('-id')


class ImageManager(models.Manager):
    def get_queryset(self):
        return ImageQuerySet(self.model, using=self._db)

    def get_published(self):
        return self.get_queryset().get_published()

    def get_order_desc(self):
        return self.get_queryset().get_order_desc()


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
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
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


class ImageArtStyle(models.Model):
    class Meta:
        verbose_name = 'Estilo de Arte'
        verbose_name_plural = 'Estilos de Arte'

    name = models.CharField(
        max_length=100, verbose_name='Nome'
    )
    slug = models.SlugField(
        unique=True, default=None,
        null=True, blank=True, max_length=100,
    )
    category = models.ForeignKey(
        ImageCategory, on_delete=models.CASCADE,
        related_name='ImageArtStyleCategory'
    )
    description = models.TextField(verbose_name='Descrição')

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

    objects = ImageManager()

    description = models.CharField(
        max_length=85, blank=True, null=True
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
    style = models.ManyToManyField(
        ImageArtStyle, blank=True, verbose_name='Estilo(s)'
    )

    def clean(self):
        clean = super().clean()
        for style in self.style.all():
            if style.category.name != self.category.name:
                raise ValidationError(
                    f'O estilo "{style.name}" (da categoria: {style.category.name})'
                    f'não pode ser associado a uma imagem de categoria "{self.category.name}"'
                )
        return clean

    def save(self, *args, **kwargs):
        current_image_name = str(self.image.name)
        super_save = super().save(*args, **kwargs)
        image_changed = False

        if self.image:
            image_changed = current_image_name != self.image.name

        if image_changed:
            resize_image(self.image, 960, True, 85)

        return super_save

    def __str__(self):
        return self.description or f"Imagem {self.id}"
