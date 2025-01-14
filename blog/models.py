from django.contrib.auth.models import User
from django.db import models

from utils.randomization.models import slugify_new

class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=50, unique=True, 
        default=None, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 4)
        return super().save(*args, **kwargs)


    def __str__(self) -> str:
        return self.name
    
    
class Category(models.Model):
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

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


class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    title = models.CharField(max_length=65, verbose_name='Título')
    slug = models.SlugField(
        unique=True, default="", verbose_name='Slug',
        null=False, blank=True, max_length=255
    )
    excerpt = models.CharField(max_length=150, verbose_name='Trecho')
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisará estar marcado '
            'para o post ser exibido publicamente.'
        ), verbose_name='Publicar'
    )
    content = models.TextField(verbose_name='Conteúdo')
    cover = models.ImageField(
        upload_to='posts/%Y/%m/', blank=True, 
        default='', verbose_name='Imagem de Capa'
    )
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text=(
            'Se marcado, exibirá a capa '
            'no conteúdo do post.'
        ),
        verbose_name='Exibir capa no post'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )

    # user.post_created_by.all
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_created_by',
        verbose_name='Criado por'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Atualizado em'
    )

    # user.post_updated_by.all
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_updated_by',
        verbose_name='Atualizado por'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None, verbose_name='Categoria'
    )
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 4)
        return super().save(*args, **kwargs)
