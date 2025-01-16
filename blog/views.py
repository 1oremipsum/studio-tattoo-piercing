from django.core.paginator import Paginator
from sitesetup.models import SiteSetup
from blog.models import Post

from django.shortcuts import render

PER_PAGE = 9

def index(request):
    context = {
        'site_title': 'Studio Tattoo & Piercing'
    }
    return render(request, 'blog/pages/index.html', context)


def home_blog(request):
    posts =  (Post.objects
              .filter(is_published=True)
              .order_by('-pk'))
    
    page_obj = pagination(request, posts)

    title = SiteSetup.objects.all().first().title

    context = {
        'site_title': title,
        'page_obj': page_obj
    }

    return render(request, 'blog/pages/blog.html', context)


def gallery(request):
    return render(request, 'blog/pages/gallery.html')


def post(request):

    context = {
        'site_title': 'Studio Tattoo & Piercing | Post',
        # 'page_obj': page_obj
    }

    return render(request, 'blog/pages/post.html', context)


def pagination(request, objs):
    paginator = Paginator(objs, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj