"""
指定銘柄のチャートをpngで取得します
top5のチャートをpngで取得します
step1: 1企業あたり毎日1明細しかないものを group集計する
step2: pandasでtop5を抽出し、top5テーブルにinsertしたあとにスクレイピング
step3: 傾斜を出して、uptrendを抽出
"""
import os
import shutil
import time
import urllib.request
import datetime
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

def scraping(mkt, symbol, outfolder):
    """
    url先の <div id="chart_search_left"> の <img> を取得する。
    1つ処理するごとに4秒ほど休むのは、スクレイピングルールです。
    """
    dic = {"HOSE": 'hcm', "HNX": 'hn'}
    url = 'https://www.viet-kabu.com/{0}/{1}.html'.format(dic[mkt], symbol)
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'lxml')
    tag_img = soup.find(id='chart_search_left').find('img')
    if tag_img:
        urllib.request.urlretrieve(tag_img['src'], outfolder + '/{0}.png'.format(symbol))
        print(symbol)
    time.sleep(4)

# mysql
CON_STR = 'mysql+mysqldb://python:python123@127.0.0.1/pythondb?charset=utf8&use_unicode=1'
CON = create_engine(CON_STR, echo=False).connect()

# chart1: watchlist
print('watch list')
# delete old files
OUTFOLDER = os.path.dirname(os.path.abspath(__file__))
OUTFOLDER = OUTFOLDER + '/mysite/vietnam_research/static/vietnam_research/chart'
shutil.rmtree(OUTFOLDER)
os.mkdir(OUTFOLDER)
# sql
SYMBOLS = pd.read_sql_query(
    '''
    SELECT DISTINCT
        i.market_code, w.symbol
    FROM vietnam_research_industry i INNER JOIN vietnam_research_watchlist w
    ON i.symbol = w.symbol;
    '''
    , CON)
for i, row in SYMBOLS.iterrows():
    scraping(row['market_code'], row['symbol'], OUTFOLDER)

# chart2: top 5 by industry
print('\n' + 'top 5')
# sql
CON.execute('DELETE FROM vietnam_research_dailytop5')
AGG = pd.read_sql_query(
    '''
    SELECT
          CONCAT(c.industry_class, '|', i.industry1) AS ind_name
        , i.market_code
        , i.symbol
        , AVG(i.trade_price_of_a_day) AS trade_price_of_a_day
        , AVG(i.per) AS per
    FROM (vietnam_research_industry i INNER JOIN vietnam_research_indclass c
        ON i.industry1 = c.industry1) INNER JOIN vietnam_research_sbi s
        ON i.market_code = s.market_code AND i.symbol = s.symbol
    GROUP BY ind_name, i.market_code, i.symbol
    HAVING per >1;
    '''
    , CON)
# criteria
CRITERIA = []
CRITERIA.append({"by": ['trade_price_of_a_day', 'per'], "order": False})
CRITERIA.append({"by": ['ind_name', 'trade_price_of_a_day', 'per'], "order": [True, False, False]})
# Sort descending and get top 5
AGG = AGG.sort_values(by=CRITERIA[0]["by"], ascending=CRITERIA[0]["order"])
AGG = AGG.groupby('ind_name').head()
# Sort descending and insert table
AGG = AGG.sort_values(by=CRITERIA[1]["by"], ascending=CRITERIA[1]["order"])
AGG.to_sql('vietnam_research_dailytop5', CON, if_exists='append', index=None)
# scraping from top 5 list
for i, row in AGG.iterrows():
    scraping(row['market_code'], row['symbol'], OUTFOLDER)

# chart3: uptrend by industry
print('\n' + 'uptrend')
# delete old files
OUTFOLDER = os.path.dirname(os.path.abspath(__file__))
OUTFOLDER = OUTFOLDER + '/mysite/vietnam_research/static/vietnam_research/chart_uptrend'
shutil.rmtree(OUTFOLDER)
os.mkdir(OUTFOLDER)
# sql
CON.execute('DELETE FROM vietnam_research_dailyuptrends')
AGG = pd.read_sql_query(
    '''
    SELECT
          CONCAT(c.industry_class, '|', i.industry1) AS ind_name
        , i.market_code
        , i.symbol
        , i.pub_date
        , i.closing_price
    FROM (vietnam_research_industry i INNER JOIN vietnam_research_indclass c
        ON i.industry1 = c.industry1) INNER JOIN vietnam_research_sbi s
        ON i.market_code = s.market_code AND i.symbol = s.symbol
    ORDER BY ind_name, i.symbol, i.pub_date;
    '''
    , CON)
IND_NAMES = []
MARKET_CODES = []
SYMBOLS = []
PRICE_OLDESTS = []
PRICE_LATESTS = []
PRICE_DELTAS = []
for key, values in AGG.groupby('symbol'):
    days = [14, 7, 3]
    # plot: closing_price
    plt.clf()
    plt.plot(range(len(values)), values['closing_price'], "ro")
    plt.ylabel('closing_price')
    plt.grid()
    slope_inner = []
    price_inner = []
    score = 0
    for i in range(len(days)):
        values_inner = values[-days[i]:]
        x_scale = range(len(values_inner))
        A = np.array([x_scale, np.ones(len(x_scale))]).T
        slope, intercept = np.linalg.lstsq(A, values_inner['closing_price'], rcond=-1)[0]
        slope_inner.append(slope)
        # scoring
        if slope > 0:
            score += 1
        # plot: overwrite fitted line
        x_offset = len(values) - days[i]
        x_scale_shifted = range(x_offset, days[i] + x_offset)
        plt.plot(x_scale_shifted, (slope * x_scale + intercept), "g--")
    if score == len(days):
        # save png: w640, h480
        outpath = OUTFOLDER + '/{0}.png'.format(key)
        plt.savefig(outpath)
        # resize png: w250, h200
        Image.open(outpath).resize((250, 200), Image.LANCZOS).save(outpath)
        # stack param
        IND_NAMES.append(values['ind_name'].head(1).iloc[0])
        MARKET_CODES.append(values['market_code'].head(1).iloc[0])
        SYMBOLS.append(key)
        price_inner.append(values.tail(max(days))['closing_price'].head(1).iloc[0])
        price_inner.append(values.tail(max(days))['closing_price'].tail(1).iloc[0])
        price_inner.append(round(price_inner[1] - price_inner[0], 2))
        PRICE_OLDESTS.append(price_inner[0])
        PRICE_LATESTS.append(price_inner[1])
        PRICE_DELTAS.append(price_inner[2])
    print(key, slope_inner, score, price_inner)

AGG = pd.DataFrame({
    'ind_name': IND_NAMES,
    'market_code': MARKET_CODES,
    'symbol': SYMBOLS,
    'stocks_price_oldest': PRICE_OLDESTS,
    'stocks_price_latest': PRICE_LATESTS,
    'stocks_price_delta': PRICE_DELTAS
})
AGG = AGG.sort_values(['ind_name', 'stocks_price_delta'], ascending=['True', 'False'])
AGG.to_sql('vietnam_research_dailyuptrends', CON, if_exists='append', index=None)

# log
with open(os.path.dirname(os.path.abspath(__file__)) + '/result.log', mode='a') as f:
    f.write('\n' + datetime.datetime.now().strftime("%Y/%m/%d %a %H:%M:%S ") + 'stock_chart.py')

# Output
print('Congrats!')
time.sleep(2)
