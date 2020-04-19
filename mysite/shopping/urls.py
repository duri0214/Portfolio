"""urls.py"""
from django.urls import path
from .views import IndexView, DetailView, UploadSingleView, UploadBulkView

app_name = 'shp'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('detail/<int:pk>', DetailView.as_view(), name='detail'),
    path('regist/single/', UploadSingleView.as_view(), name='regist_single'),
    path('regist/bulk/', UploadBulkView.as_view(), name='regist_bulk'),
    path('edit/', IndexView.as_view(), name='edit_data')
]
