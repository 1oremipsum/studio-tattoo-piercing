from gallery.models import Image, ImageCategory, ImageArtStyle
from django.views.generic.list import ListView
from sitesetup.models import SiteSetup
from django.db.models import Q

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
        context['tattoo_category'] = ImageCategory.objects.get(id=1)
        context['piercing_category'] = ImageCategory.objects.get(id=2)
        context['tattoo_styles'] = ImageArtStyle.objects.filter(category=1).order_by('name')
        context['piercing_styles'] = ImageArtStyle.objects.filter(category=2).order_by('name')
        context['site_title'] = get_object_or_404(SiteSetup, id=3).title
        return context

class SearchListView(ImagesListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._search_value = ''
        self._style_slug = ''
        self._category_slug = ''

    def get_title(self):
        if self._search_value:
            query = self._search_value

            query = self._search_value
            base_title = get_object_or_404(SiteSetup, id=3).title
            if query:
                title = f"Você pesquisou por {query[:20]} | "
                title += base_title
        else:
            title = get_object_or_404(SiteSetup, id=3).title

        return title

    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        self._category_slug = request.GET.get('category', '').strip()
        self._style_slug = request.GET.get('style', '').strip()
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if self._search_value == '' and self._style_slug == '' and self._category_slug == '':
            return redirect('gallery:home_gallery')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        
        if self._search_value:
            queryset = queryset.filter(
                Q(description__icontains=self._search_value) | 
                Q(category__name__icontains=self._search_value) | 
                Q(style__name__icontains=self._search_value)
            )

        if self._style_slug:
            style = get_object_or_404(ImageArtStyle, slug=self._style_slug)
            queryset = queryset.filter(style=style)

        if self._category_slug:
            category = get_object_or_404(ImageCategory, slug=self._category_slug)
            queryset = queryset.filter(category=category)

        return queryset
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['site_title'] = self.get_title()
        ctx['search_value'] = self._search_value
        ctx['selected_style'] = self._style_slug
        ctx['selected_category'] = self._category_slug

        return ctx
