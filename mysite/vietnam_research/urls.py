"""docstring"""
from django.urls import path
from . import views

app_name = 'vnm'
urlpatterns = [
    # index.htmlがリクエストされたときは views.index の処理に
    path('', views.index, name='index'),
    # いいね！がリクエストされたときは views.likes の処理に 引数[ユーザID, 記事ID] を渡します
    path('likes/<int:user_id>/<int:article_id>', views.likes, name='likes'),
]
