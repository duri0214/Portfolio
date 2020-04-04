"""docstring"""
from django import forms

class WatchelistForm(forms.Form):
    """ウォッチリスト登録時の入力フォームです"""

    buy_symbol = forms.CharField(
        label='シンボル(銘柄)',
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'buy_symbol',
            'placeholder':'英数字のみ入力可能です',
            'pattern':'^[A-Z0-9]+$'})
    )

    buy_date = forms.DateTimeField(
        label='購入日',
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=['%Y-%m-%d']
    )

    buy_cost = forms.CharField(
        label='@単価(1ドン)',
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'buy_cost',
            'placeholder':'数字のみ入力可能です',
            'pattern':'^[0-9]+$'})
    )

    buy_stocks = forms.CharField(
        label='株数',
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'buy_stocks',
            'placeholder':'数字のみ入力可能です',
            'pattern':'^[0-9]+$'})
    )

    buy_bikou = forms.CharField(
        label='備考',
        required=False,
        widget=forms.TextInput(attrs={
            'id': 'buy_bikou'})
    )
