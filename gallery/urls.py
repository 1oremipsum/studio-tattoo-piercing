from django.urls import path

from gallery.views import ImagesListView

app_name = 'gallery'

urlpatterns = [
    path('', ImagesListView.as_view(), name='home_gallery'),
]