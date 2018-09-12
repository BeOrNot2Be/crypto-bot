import json


def get_json_dict(url='calculations/dict.json', id_=True):
    with open('calculations/dict.json', 'r+') as f:
        data = dict(json.loads(f.read()))
    if not id_:
        return data['symbol_name']
    elif id_ != 'all':
        return data
    else:
        return data['name_id']


def get_currency_rate(request, cc='bitcoin', c='USD'):
    quotes = request['data']['quotes'][f'{c}']
    price = quotes['price']
    percent_change_1h = quotes['percent_change_1h']
    if percent_change_1h > 0:
        arrow = '\U0001F4C8'
    else:
        arrow = '\U0001F4C9'
    return f'{cc}: {price}\n{percent_change_1h}{arrow}'


def get_currencies_rate(request, cc=['bitcoin', 'ethereum'], c='USD'):
    answer = []

    for i in cc:
        quotes = request['data'][i]['quotes'][f'{c}']
        price = quotes['price']
        percent_change_1h = quotes['percent_change_1h']
        if percent_change_1h > 0:
            arrow = '\U0001F4C8'
        else:
            arrow = '\U0001F4C9'

        answer.append(f'{cc[i]}: {price}\n{percent_change_1h}{arrow}')
    return answer


def calculation(request, how_mach=1.00, cc='bitcoin', c='USD'):
    quotes = request['data']['quotes'][f'{c}']
    price = quotes['price']

    if c == 'USD':
        currency = ''
    else:
        currency = f'({c})'
    return f'{currency}{how_mach * price}'
