from django.urls import path

from gallery.views import ImagesListView, ImageCategoryView, ImageStyleView, SearchListView

app_name = 'gallery'

urlpatterns = [
    path('', ImagesListView.as_view(), name='home_gallery'),
    path('search/', SearchListView.as_view(), name='search'),
    path('style/<slug:slug>', ImageStyleView.as_view(), name='img_style'),
    path('category/<slug:slug>', ImageCategoryView.as_view(), name='img_category'),
]