"""urls.py"""
from django.urls import path
from . import views

app_name = 'shp'
urlpatterns = [
    path('', views.index, name='index'),
]