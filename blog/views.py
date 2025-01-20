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


def created_by(request, author_id):
    posts =  Post.objects.get_published().filter(created_by__pk=author_id)
    page_obj = pagination(request, posts)
    title = SiteSetup.objects.all().first().title

    context = {
        'site_title': title,
        'page_obj': page_obj
    }

    return render(request, 'blog/pages/blog.html', context)


def category(request, slug):
    posts =  Post.objects.get_published().filter(category__slug=slug)
    page_obj = pagination(request, posts)
    title = SiteSetup.objects.all().first().title

    context = {
        'site_title': title,
        'page_obj': page_obj
    }

    return render(request, 'blog/pages/blog.html', context)


def post(request, slug):
    post =  Post.objects.get_published().filter(slug=slug).first()
    title = SiteSetup.objects.all().first().title

    context = {
        'site_title': f"{post.title} - {title}",
        'post': post,
    }

    return render(request, 'blog/pages/post.html', context)


def gallery(request):
    return render(request, 'blog/pages/gallery.html')
