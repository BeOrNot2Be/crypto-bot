import io
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
from matplotlib.dates import (MONDAY, DateFormatter,
                              WeekdayLocator, HourLocator)


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
    plt.savefig(buf, format='png', facecolor='royalblue',
                edgecolor='royalblue')
    return buf.getvalue()
