from gallery.models import Image, ImageCategory
from django.views.generic.list import ListView
from django.db.models.query import QuerySet
from sitesetup.models import SiteSetup
from typing import Any

from django.shortcuts import get_object_or_404

PER_PAGE = 20

class ImagesListView(ListView):
    model = Image
    template_name = 'gallery/pages/gallery.html'
    context_object_name = 'images_objs'
    paginate_by = PER_PAGE
    
    def get_queryset(self):
        return Image.objects.get_published().get_order_desc()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_objs'] = ImageCategory.objects.all()
        context['site_title'] = get_object_or_404(SiteSetup, id=3).title
        return context


class ImageCategoryView(ImagesListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_title'] = (
            f'{self.object_list[0].category.name} | {get_object_or_404(SiteSetup, id=3).title}'
        )
        return context
    
