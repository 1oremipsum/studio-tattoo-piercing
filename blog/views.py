from django.contrib.auth.models import User
from sitesetup.models import SiteSetup
from django.http import Http404
from django.db.models import Q
from blog.models import Post

from utils.pagination.model import pagination
from django.shortcuts import render


def blog_title():
    return  SiteSetup.objects.all().first().title


def get_pots():
    return Post.objects.get_published()

# views

def index(request):
    context = {
        'site_title': 'Studio Tattoo & Piercing'
    }
    return render(request, 'blog/pages/index.html', context)


def home_blog(request):
    page_obj = pagination(request, get_pots().order_by('-created_at'))

    context = {
        'site_title': blog_title,
        'page_obj': page_obj
    }

    return render(request, 'blog/pages/blog.html', context)


def created_by(request, author_id):
    posts = get_pots().filter(created_by__pk=author_id).order_by('-created_at')
    page_obj = pagination(request, posts)

    user = User.objects.filter(pk=author_id).first()

    if user is None:
        raise Http404()

    user_full_name = user.username

    if user.first_name:
        user_full_name = f"{user.first_name} {user.last_name}"

    context = {
        'site_title': f"Posts de {user_full_name} - {blog_title()}",
        'page_obj': page_obj
    }

    return render(request, 'blog/pages/blog.html', context)


def category(request, slug):
    posts = get_pots().filter(category__slug=slug).order_by('-created_at')
    page_obj = pagination(request, posts)

    if len(posts) == 0:
        raise Http404()

    context = {
        'site_title': f"Posts da Categoria {page_obj[0].category.name} - {blog_title()}",
        'page_obj': page_obj
    }

    return render(request, 'blog/pages/blog.html', context)


def tag(request, slug):
    posts = get_pots().filter(tags__slug=slug).order_by('-created_at')
    page_obj = pagination(request, posts)

    if len(posts) == 0:
        raise Http404()

    context = {
        'site_title': f"Posts da Tag {page_obj[0].tags.first().name} - {blog_title()}",
        'page_obj': page_obj
    }

    return render(request, 'blog/pages/blog.html', context)


def search(request):
    query = request.GET.get('search', None).strip()
    posts = get_pots().filter(
        Q(title__icontains=query) | Q(excerpt__icontains=query) |
        Q(content__icontains=query)
    )

    page_obj = pagination(request, posts)
    
    if query:
        title = f"Você pesquisou por {query[:20]} - "
        title += blog_title()
    else:
        title = blog_title()

    context = {
        'site_title': title,
        'posts': posts,
        'search_value': query,
        'page_obj': page_obj
    }

    return render(request, 'blog/pages/blog.html', context)


def post(request, slug):
    post_obj = get_pots().filter(slug=slug).first()

    if post_obj is None:
        raise Http404()

    context = {
        'site_title': f"{post_obj.title} - {blog_title()}",
        'post': post_obj,
    }

    return render(request, 'blog/pages/post.html', context)


def gallery(request):
    return render(request, 'blog/pages/gallery.html')
