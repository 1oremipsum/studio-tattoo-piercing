from django.core.paginator import Paginator
from django.shortcuts import render

posts = list(range(1000))

def index(request):
    return render(request, 'blog/pages/index.html')


def home_blog(request):
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/pages/blog.html', { 'page_obj': page_obj })


def gallery(request):
    return render(request, 'blog/pages/gallery.html')


def post(request):
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/pages/post.html',)
