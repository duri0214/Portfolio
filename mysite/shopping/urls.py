"""urls.py"""
from django.urls import path
from .views import IndexView, DetailView

app_name = 'shp'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('detail/<int:pk>', DetailView.as_view(), name='detail')
]
