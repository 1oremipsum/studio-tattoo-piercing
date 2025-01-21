from django.db import models
from django.contrib.auth.models import User
from django_summernote.models import AbstractAttachment

from utils.randomization.models import slugify_new
from utils.resizing.images import resize_image
from django.urls import reverse

class PostAttachment(AbstractAttachment):
    class Meta:
        verbose_name = 'Anexo do post'
        verbose_name_plural = 'Anexos dos posts'

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False
    
        if self.file:
            file_changed = current_file_name != self.file.name
        
        if file_changed:
            # 900=Maximum width for file, 70=quality 70%
            resize_image(self.file, 900, True, 70)

        return super_save


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


class PostManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True)


    def get_order_desc(self):
        return self.order_by('-pk')


class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    objects = PostManager()

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


    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:home_blog')
        return reverse('blog:post', args=(self.slug,))


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 4)

        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False
    
        if self.cover:
            cover_changed = current_cover_name != self.cover.name
        
        if cover_changed:
            # 900:Maximum width for cover, 70:quality 70%
            resize_image(self.cover, 900, True, 70)

        return super_save