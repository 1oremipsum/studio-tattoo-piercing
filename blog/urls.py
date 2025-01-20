from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.home_blog, name='home_blog'),
    path('galeria/', views.gallery, name='gallery'),
    path('post/<slug:slug>/', views.post, name='post'),
    path('created_by/<int:author_id>/', views.created_by, name='created_by'),
    path('category/<slug:slug>/', views.category, name='category'),
]