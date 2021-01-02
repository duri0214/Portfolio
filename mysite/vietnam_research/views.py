"""子供のurls.pyがこの処理を呼び出します"""
import json
from datetime import datetime

from sqlalchemy import create_engine
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http.response import JsonResponse
from django.db.models import Count, Case, When, IntegerField
import pandas as pd
from .forms import ArticleForm, WatchlistForm, ExchangeForm
from .market_vietnam import MarketVietnam
from .models import WatchList, Likes, Articles
from django.contrib.auth.decorators import login_required


def index(request):
    """いわばhtmlのページ単位の構成物です"""

    # GETだったら MarketVietnam(), nasdaqが選ばれたらMarketNasdaq()
    mkt = MarketVietnam()

    exchanged = {}
    if request.method == 'POST':
        watchlist_form = WatchlistForm(request.POST)
        if watchlist_form.is_valid():
            # watchlist_form data
            buy_symbol = watchlist_form.cleaned_data['buy_symbol']
            buy_date = watchlist_form.cleaned_data['buy_date']
            buy_cost = watchlist_form.cleaned_data['buy_cost']
            buy_stocks = watchlist_form.cleaned_data['buy_stocks']
            buy_bikou = watchlist_form.cleaned_data['buy_bikou']
            # db register
            watchlist = WatchList()
            watchlist.symbol = buy_symbol
            watchlist.already_has = True
            watchlist.bought_day = buy_date
            watchlist.stocks_price = buy_cost
            watchlist.stocks_count = buy_stocks
            watchlist.bikou = buy_bikou
            watchlist.save()
            # redirect
            return redirect('vnm:index')

        # TODO(為替変換): https://docs.microsoft.com/ja-jp/partner/develop/get-foreign-exchange-rates
        # https://www.ceccs.co.jp/archives/blog/%E3%80%90%E3%83%97%E3%83%AA%E3%82%B6%E3%83%B3%E3%82%BF%E3%83%BC%E3%80%91-%E7%AC%AC58%E5%9B%9E%EF%BC%89%E5%85%AC%E9%96%8Bapi%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E8%87%AA%E5%8B%95%E9%80%9A%E8%B2%A8
        exchange_form = ExchangeForm(request.POST)
        if exchange_form.is_valid():
            # exchange_form data
            current_balance = exchange_form.cleaned_data['current_balance']
            unit_price = exchange_form.cleaned_data['unit_price']
            quantity = exchange_form.cleaned_data['quantity']
            # calc
            exchanged['current_balance'] = current_balance
            exchanged['unit_price'] = unit_price
            exchanged['quantity'] = quantity
            exchanged['price_no_fee'] = unit_price * quantity
            exchanged['fee'] = mkt.get_price_including_tax_fee(price_no_fee=exchanged['price_no_fee'])
            exchanged['price_in_fee'] = exchanged['price_no_fee'] + exchanged['fee']
            exchanged['deduction_price'] = exchanged['current_balance'] - exchanged['price_in_fee']

    else:
        exchange_form = ExchangeForm()
        watchlist_form = WatchlistForm()
        watchlist_form.buy_date = datetime.today().strftime("%Y/%m/%d")

    # count by industry, marketcap by industry
    # mysql
    con_str = 'mysql+mysqldb://python:python123@127.0.0.1/pythondb?charset=utf8&use_unicode=1'
    con = create_engine(con_str, echo=False).connect()

    # articlesとlike
    try:
        loginid = get_user_model().objects.values('id').get(email=request.user)['id']
    except get_user_model().DoesNotExist:
        loginid = None
    articles = Articles.objects.annotate(likes_cnt=Count('likes'))
    articles = articles.select_related('user')
    like_list = Likes.objects.filter(user_id=loginid).values('articles_id')
    articles = articles.annotate(
        is_like=Case(
            When(likes__articles_id__in=like_list, then=1), default=0, output_field=IntegerField()
        )
    ).order_by('-created_at')[:3]

    # context
    context = {
        'industry_count': json.dumps(mkt.get_radar_chart_count(), ensure_ascii=False),
        'industry_cap': json.dumps(mkt.get_radar_chart_cap(), ensure_ascii=False),
        'industry_stack': json.dumps(mkt.get_industry_stack(), ensure_ascii=False),
        'vnindex_timeline': json.dumps(mkt.get_national_stock_timeline(), ensure_ascii=False),
        'vnindex_layers': json.dumps(mkt.get_national_stock_layers(), ensure_ascii=False),
        'articles': articles,
        'basicinfo': mkt.get_basicinfo(),
        'watchlist': mkt.get_watchlist(),
        'sbi_topics': mkt.get_sbi_topics(),
        'uptrends': json.dumps(mkt.get_uptrends(), ensure_ascii=False),
        'watchlist_form': watchlist_form,
        'exchange_form': exchange_form,
        'exchanged': exchanged,
    }

    # htmlとして返却します
    return render(request, 'vietnam_research/index.html', context)


@login_required
def likes(request, user_id, article_id):
    """いいねボタンをクリック"""
    if request.method == 'POST':
        print(json.loads(request.body), json.loads(request.body).get('status'))
        query = Likes.objects.filter(user=user_id, articles_id=article_id)
        if query.count() == 0:
            likes_tbl = Likes()
            likes_tbl.articles_id = article_id
            likes_tbl.user_id = user_id
            likes_tbl.save()
        else:
            query.delete()
        # response json
        return JsonResponse({"status": "responded by views.py"})


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """ArticleCreateView"""
    model = Articles
    template_name = "vietnam_research/articles/create.html"
    form_class = ArticleForm
    success_url = reverse_lazy("vnm:index")

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class WatchListRegister(CreateView):
    """WatchListRegister"""
    model = WatchList
    template_name = "vietnam_research/watchlist/register.html"
    form_class = WatchlistForm
    success_url = reverse_lazy("vnm:index")

    def form_valid(self, form):
        form.instance.already_has = 1
        return super().form_valid(form)
