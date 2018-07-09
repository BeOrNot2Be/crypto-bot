import io
import requests
import datetime
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
from matplotlib.dates import date2num
from matplotlib.dates import (MONDAY, DateFormatter, DayLocator,
                     WeekdayLocator, AutoDateFormatter, AutoDateLocator, HourLocator)
from PIL import Image


def get_histodata(time, time_co, cc, c, aggregate=1):
    answer = []
    url = f'https://min-api.cryptocompare.com/data/histo{time}'\
    f'?fsym={cc}&tsym={c}&limit={time_co}&aggregate={aggregate}&e=CCCAGG'
    data = requests.get(url).json()
    for quotes in data['Data']:
        date = date2num(datetime.datetime.fromtimestamp(quotes['time']))
        answer.append(tuple([date, quotes['open'], quotes['high'],
                             quotes['low'], quotes['close']]))
    return answer


def get_graph(data, dt, cc='BTC', c='USD'):
    fig, ax = plt.subplots(figsize=(10, 5), dpi=400,
         facecolor='royalblue', edgecolor='royalblue')

    candlestick_ohlc(ax, data, colorup='palegreen', colordown='salmon')

    plt.grid(color='cornflowerblue')

    if dt:
        mondays = WeekdayLocator(MONDAY)
        weekFormatter = DateFormatter('%m/%d')

        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_major_formatter(weekFormatter)
    else:
        loc = HourLocator(interval=8)
        formatter = DateFormatter('%d/%H')

        ax.xaxis.set_major_locator(loc)
        ax.xaxis.set_major_formatter(formatter)

    fig.subplots_adjust(left=0.055, top=1.00, right=1.00)
    ax.set_facecolor('royalblue')
    ax.tick_params(color='aliceblue', labelcolor='aliceblue')
    for spine in ax.spines.values():
        spine.set_edgecolor('aliceblue')

    ax.xaxis_date()
    plt.setp(plt.gca().get_xticklabels(),
            rotation=90, horizontalalignment='right')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', facecolor='royalblue', edgecolor='royalblue')
    return buf.getvalue()


def get_cryptocurrency_graph(time='day', time_count='365',
                            cryptocurrency='BTC', currency='USD'):

    if time == 'day':
        datevstime = True
        aggregate = 1
    else:
        datevstime = False
        aggregate = 2
    histodata = get_histodata(time=time, time_co=time_count,
                            cc=cryptocurrency, c=currency, aggregate=aggregate)


    return get_graph(histodata, c=cryptocurrency, cc=currency, dt=datevstime)
