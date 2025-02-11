from gallery.models import Image, ImageCategory
from django.views.generic.list import ListView
from django.db.models.query import QuerySet
from sitesetup.models import SiteSetup
from django.db.models import Q
from typing import Any

from django.shortcuts import get_object_or_404, redirect

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


class SearchListView(ImagesListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._search_value = ''

    def get_title(self):
        q = self._search_value
        base_title = get_object_or_404(SiteSetup, id=3).title
        if q:
            title = f"Você pesquisou por {q[:20]} | "
            title += base_title

        return title

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('gallery:home_gallery')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        q = self._search_value
        return super().get_queryset().filter(
            Q(description__icontains=q) | 
            Q(category__name__icontains=q) | 
            Q(portfolio__name__icontains=q)
        )
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['site_title'] = self.get_title()
        ctx['search_value'] = self._search_value

        return ctx
        
    
