from django.urls import path

from gallery.views import ImagesListView, ImageCategoryView, SearchListView

app_name = 'gallery'

urlpatterns = [
    path('', ImagesListView.as_view(), name='home_gallery'),
    path('search/', SearchListView.as_view(), name='search'),
    path('category/<slug:slug>', ImageCategoryView.as_view(), name='img_category'),
]