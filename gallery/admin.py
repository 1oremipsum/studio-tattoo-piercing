from django.contrib import admin
from .models import Portfolio, Image, ImageCategory, ImageArtStyle

@admin.register(ImageCategory)
class ImageCategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'id', 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('name',),
    }

@admin.register(ImageArtStyle)
class ImageArtStyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'category')
    list_display_links = ('id', 'name')
    search_fields = ('id', 'name', 'category')
    list_per_page = 15
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

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field == "style":
            if 'object_id' in request.resolver_match.kwargs:
                image = Image.objects.get(id=request.resolver_match.kwargs['object_id'])
                kwargs["queryset"] = ImageArtStyle.objects.filter(category=image.category)
            else:
                kwargs["queryset"] = ImageArtStyle.objects.none()

        return super().formfield_for_manytomany(db_field, request, **kwargs)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = 'id','name', 'description', 'created_at','author',
    list_display_links = 'id','name',
    search_fields = 'id', 'name', 'author',
    list_per_page = 10
    ordering = '-id',
    readonly_fields = (
        'created_at',
        )
    inlines = [ImageInline]
