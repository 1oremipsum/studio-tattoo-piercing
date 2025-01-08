from django.core.paginator import Paginator
from django.shortcuts import render
from sitesetup.models import SiteSetup

posts = list(range(1000))

def index(request):
    context = {
        'site_title': 'Studio Tattoo & Piercing'
    }
    return render(request, 'blog/pages/index.html', context)


def home_blog(request):
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    title = SiteSetup.objects.all().first().title

    context = {
        'site_title': title,
        'page_obj': page_obj
    }

    return render(request, 'blog/pages/blog.html', context)


def gallery(request):
    return render(request, 'blog/pages/gallery.html')


def post(request):
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'site_title': 'Studio Tattoo & Piercing | Post',
        'page_obj': page_obj
    }

    return render(request, 'blog/pages/post.html', context)
