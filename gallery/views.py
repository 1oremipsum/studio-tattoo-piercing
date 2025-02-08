from django.views.generic.list import ListView
from sitesetup.models import SiteSetup
from gallery.models import Image

PER_PAGE = 20

def gallery_title():
    return SiteSetup.objects.get(id=3).title


def get_images():
    return Image.objects.all()


class ImagesListView(ListView):
    model = Image
    template_name = 'gallery/pages/gallery.html'
    context_object_name = 'images_objs'
    ordering = '-pk',
    paginate_by = PER_PAGE
    queryset = get_images()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'site_title': gallery_title()})
        return context

