from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('blog', views.home_blog, name='home_blog'),
    path('galeria', views.gallery, name='gallery'),
    path('post', views.post, name='post'),
]