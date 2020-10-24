"""docstring"""
from django import forms
from .models import Articles, WatchList


class WatchlistForm(forms.ModelForm):
    """ウォッチリスト登録時の入力フォームです"""

    class Meta:
        model = WatchList
        fields = ('symbol', 'bought_day', 'stocks_price', 'stocks_count')
        exclude = ('already_has',)


class ArticleForm(forms.ModelForm):
    """CardForm"""

    class Meta:
        model = Articles
        fields = ("title", "note")
