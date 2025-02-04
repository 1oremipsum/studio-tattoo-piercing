from django.contrib import admin
from .models import Portfolio, Image, ImageCategory

@admin.register(ImageCategory)
class ImageCategory(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'id', 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('name',),
    }

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = 'id', 'description', 'category', 'portfolio', 'is_published',
    list_display_links = 'id',
    search_fields = 'id', 'description', 'category', 'portfolio',
    list_filter = 'category', 'is_published',
    list_editable = 'is_published',
    autocomplete_fields = 'category',
    ordering = '-id',
    list_per_page = 15

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = 'id','name', 'description', 'author',
    list_display_links = 'id','name',
    search_fields = 'id', 'name', 'author',
    list_per_page = 10
    ordering = '-id',
    inlines = [ImageInline]
