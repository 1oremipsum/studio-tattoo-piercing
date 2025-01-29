from django.urls import path
from blog.views import (
    PostListView, CreatedByListView, CategoryListView,
    TagListView, SearchListView, PostDetailView, index
)

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('blog/', PostListView.as_view(), name='home_blog'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post'),
    path('created_by/<int:author_id>/', CreatedByListView.as_view(), name='created_by'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category'),
    path('tag/<slug:slug>/', TagListView.as_view(), name='tag'),
    path('search/', SearchListView.as_view(), name='search'),
]