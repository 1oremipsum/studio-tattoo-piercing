from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from sitesetup.models import SiteSetup
from django.http import Http404
from django.db.models import Q
from blog.models import Post
from typing import Any

from utils.pagination.model import pagination
from django.shortcuts import redirect, render

PER_PAGE = 9

def blog_title():
    return  SiteSetup.objects.all().first().title


def get_post():
    return Post.objects.get_published()

# views here.

class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/blog.html'
    context_object_name = 'posts_objs'
    ordering = '-pk',
    paginate_by = PER_PAGE
    queryset = get_post()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'site_title': blog_title()})
        return context



class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context['user']
        user_full_name = user.username
    
        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
    
        ctx.update({
            'site_title': f"Posts de {user_full_name} - {blog_title()}",
        })
        return ctx
    

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self.kwargs.get('author_id'))
        return qs
    

    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_id')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()
        
        self._temp_context.update({
            'author_id': author_pk,
            'user': user,
        })

        return super().get(request, *args, **kwargs)


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            category__slug=self.kwargs.get('slug')
        )
    

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = (
            f'Posts da Categoria {self.object_list[0].category.name} - {blog_title()}'
        )
        ctx.update({
            'site_title': page_title,
        })

        return ctx


def index(request):
    context = {
        'site_title': 'Studio Tattoo & Piercing'
    }
    return render(request, 'blog/pages/index.html', context)


def tag(request, slug):
    posts = get_post().filter(tags__slug=slug).order_by('-created_at')
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
    posts = get_post().filter(
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
    post_obj = get_post().filter(slug=slug).first()

    if post_obj is None:
        raise Http404()

    context = {
        'site_title': f"{post_obj.title} - {blog_title()}",
        'post': post_obj,
    }

    return render(request, 'blog/pages/post.html', context)


def gallery(request):
    return render(request, 'blog/pages/gallery.html')
