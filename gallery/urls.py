from django.urls import path

from gallery.views import ImagesListView, SearchListView

app_name = 'gallery'

urlpatterns = [
    path('', ImagesListView.as_view(), name='home_gallery'),
    path('search/', SearchListView.as_view(), name='search'),
]