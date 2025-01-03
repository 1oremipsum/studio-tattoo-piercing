from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'), 
    path('galeria', views.gallery, name='gallery'),
    path('post', views.post, name='post'), 
    path('page', views.page, name='page'),
]