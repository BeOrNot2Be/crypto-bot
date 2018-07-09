from requests import get
import json


def get_currency_rarte(cc='bitcoin', c='USD'):
    with open('calculations/dict.json', 'r+') as f:
        data = dict(json.loads(f.read()))
    url = f"https://api.coinmarketcap.com/v2/ticker/{data[cc]}/?convert={c}"
    request = get(url).json()
    quotes = request['data']['quotes'][f'{c}']
    price = quotes['price']
    percent_change_1h = quotes['percent_change_1h']
    if percent_change_1h > 0:
        arrow = '\U0001F4C8'
    else:
        arrow = '\U0001F4C9'
    return f'{cc}: {price}\n{percent_change_1h}{arrow}'


def get_currencies_rarte(cc=['bitcoin', 'ethereum', 'litecoin'], c='USD'):

    with open('calculations/dict.json', 'r+') as f:
        data = dict(json.loads(f.read()))

    answer = []
    url = f"https://api.coinmarketcap.com/v2/ticker/?convert={c}"
    request = get(url).json()

    for i in cc:
        quotes = request['data'][str(data[i])]['quotes'][f'{c}']
        price = quotes['price']
        percent_change_1h = quotes['percent_change_1h']
        if percent_change_1h > 0:
            arrow = '\U0001F4C8'
        else:
            arrow = '\U0001F4C9'

        answer.append(f'{i}: {price}\n{percent_change_1h}{arrow}')
    return answer


def calculation(how_mach=1.00, cc='bitcoin', c='USD'):

    with open('calculations/dict.json', 'r+') as f:
        data = dict(json.loads(f.read()))

    url = f"https://api.coinmarketcap.com/v2/ticker/{data[cc]}/?convert={c}"
    request = get(url).json()
    quotes = request['data']['quotes'][f'{c}']
    price = quotes['price']
    if c == 'USD':
        currency = ''
    else:
        currency = f'({c})'
    return f'{currency}{how_mach * price}'
