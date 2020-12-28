from abc import ABCMeta, abstractmethod
from sqlalchemy import create_engine


class MarketAbstract(metaclass=ABCMeta):
    """各マーケットのための基底クラス"""
    _con_str = 'mysql+mysqldb://python:python123@127.0.0.1/pythondb?charset=utf8&use_unicode=1'
    _con = create_engine(_con_str, echo=False).connect()

    @abstractmethod
    def get_watchlist(self):
        raise NotImplementedError()

    @abstractmethod
    def get_basicinfo(self):
        raise NotImplementedError()

    @abstractmethod
    def get_national_stock_timeline(self):
        raise NotImplementedError()

    @abstractmethod
    def get_national_stock_layers(self):
        raise NotImplementedError()

    @abstractmethod
    def get_daily_top5(self):
        raise NotImplementedError()

    @abstractmethod
    def get_uptrends(self):
        raise NotImplementedError()

    @abstractmethod
    def get_sbi_topics(self):
        raise NotImplementedError()

    @abstractmethod
    def get_industry_stack(self):
        raise NotImplementedError()

    @abstractmethod
    def get_radar_chart_count(self):
        raise NotImplementedError()

    @abstractmethod
    def get_radar_chart_cap(self):
        raise NotImplementedError()

    @abstractmethod
    def get_price_including_tax_fee(self, price_no_fee):
        raise NotImplementedError()
