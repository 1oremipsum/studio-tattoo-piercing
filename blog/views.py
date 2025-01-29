from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from sitesetup.models import SiteSetup
from django.http import Http404
from django.db.models import Q
from blog.models import Post
from typing import Dict, Any

from django.shortcuts import redirect, render

# utils

PER_PAGE = 9

def blog_title():
    return  SiteSetup.objects.all().first().title


def get_post():
    return Post.objects.get_published()

# views

def index(request):
    context = {
        'site_title': 'Studio Tattoo & Piercing'
    }
    return render(request, 'blog/pages/index.html', context)


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
            'site_title': f"Posts de {user_full_name} | {blog_title()}",
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
            f'Posts da Categoria {self.object_list[0].category.name} | {blog_title()}'
        )
        ctx.update({
            'site_title': page_title,
        })

        return ctx


class TagListView(PostListView):
    allow_empty = False

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}
    

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(
            tags__slug=self.kwargs.get('slug')
        )
    

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = (
            f"Posts da Tag {self.object_list[0].tags.first().name} | {blog_title()}"
        )
    
        ctx.update({
            'site_title': page_title,
        })

        return ctx


class SearchListView(PostListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._search_value = ''


    def get_title(self):
        q = self._search_value
        if q:
            title = f"Você pesquisou por {q[:20]} | "
            title += blog_title()
        
        return title


    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)


    def get_queryset(self):
        q = self._search_value
        return super().get_queryset().filter(
            Q(title__icontains=q) | Q(excerpt__icontains=q) |Q(content__icontains=q)
        )


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'site_title': self.get_title(),
            'search_value': self._search_value,
            })

        return ctx
    

    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:home_blog')
        return super().get(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    slug_field = 'slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        post = self.get_object()
        page_title = f"{post.title} | {blog_title()}"
        ctx.update({
            'site_title': page_title,
        })

        return ctx

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

