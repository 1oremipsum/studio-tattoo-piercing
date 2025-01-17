from sitesetup.models import SiteSetup
from blog.models import Post

from utils.pagination.model import pagination
from django.shortcuts import render


def index(request):
    context = {
        'site_title': 'Studio Tattoo & Piercing'
    }
    return render(request, 'blog/pages/index.html', context)


def home_blog(request):
    posts =  Post.objects.get_published()
    
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
