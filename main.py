import telebot
from telebot import types
import config
import datetime
from requests import get
from calculations.get_rate import (calculation, get_currencies_rate,
                                   get_currency_rate, get_json_dict)
from graph.get_graph import get_graph
# import news func
from news.get_newspaper_image import get_newspaper_image
from news.get_requests_data import (get_bijournal_news,
                                    get_forklog_news, get_coindesk_news)
from translate import Translator
from matplotlib.dates import date2num

bot = telebot.TeleBot(config.TOKEN)

user_dict = {}


def get_request(url):
    return get(url).json()


def get_currencies_list(chat_id):
    currencies = ['bitcoin', 'ethereum', 'litecoin', 'eos',
                  'monero', 'dash', 'cardano', 'bitcoin cash']
    return currencies


def get_list_of_journals(chat_id):
    list_of_journals = ['get_bijournal_news()', 'get_forklog_news()',
                        'get_coindesk_news()']
    return list_of_journals


def get_main_meny(language='en'):
    commands = {}
    eng_commands = {'graph': '\U0001F4C8',
                    'news': '\U0001F4F0',
                    'rate': '\U0001F4B5',
                    'calculator': '\U0001F4F1',
                    #'languages': '\U0001F1FA\U0001F1F8',
                    #'random': '\U0001F39F\U0000FE0F',
                    }
    if language == 'en':
        for i in eng_commands:
            commands[i] = (f'{i}{eng_commands[i]}')
    else:
        translator = Translator(to_lang=language)
        for i in eng_commands:
            commands[i] = (f'{translator.translate(i)}{eng_commands[i]}')

    reply_markup_menu = types.InlineKeyboardMarkup()
    for command in commands:
        reply_markup_menu.add(types.InlineKeyboardButton(
            text=commands[command], callback_data=f'COMMAND={command}'))

    return reply_markup_menu


def get_language_settings():
    markup_language = types.InlineKeyboardMarkup(row_width=2)

    markup_language.add(types.InlineKeyboardButton(
        text='ru \U0001F1F7\U0001F1FA', callback_data='LANGUAGE=ru'))
    markup_language.add(types.InlineKeyboardButton(
        text='en \U0001F1FA\U0001F1F8', callback_data='LANGUAGE=en'))
    return markup_language


@bot.message_handler(commands=['start'])
def send_language_masrkup(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Choose your language:",
                     reply_markup=get_language_settings())


@bot.callback_query_handler(
    func=lambda call: True if call.data.split('=')[0] == 'LANGUAGE' else False)
def set_language(call):
    language = call.data.split('=')[1]
    if language == 'en':
        answer = 'What can i do for you ?'
    elif language == 'ru':
        answer = 'Смотри, что я могу!'
    bot.send_message(call.message.chat.id, answer,
                     reply_markup=get_main_meny(language))


@bot.message_handler(commands=["news"])
def send_news(message):
    chat_id = message.chat.id

    for i in get_list_of_journals(chat_id):
        for v in eval(i):
            if v != '':
                bot.send_message(chat_id, v)

    bot.send_photo(chat_id, get_newspaper_image())


@bot.message_handler(commands=['calculation'])
def send_answer(message):
    how_mach = 1.00
    cc = 'bitcoin'
    c = 'USD'

    currency_id_dict = get_json_dict()
    url = "https://api.coinmarketcap.com/v2/ticker"\
        f"/{currency_id_dict[cc]}/?convert={c}"

    request = get_request(url)

    answer = calculation(request, how_mach, cc, c)
    bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['get_currencies_rate'])
def send_currencies_rate(message):
    chat_id = message.chat.id
    c = 'USD'

    url = f"https://api.coinmarketcap.com/v2/ticker/?convert={c}"
    request = get_request(url)

    crypto_list = get_currencies_list(chat_id)
    currency_id_dict = get_json_dict()
    cc = {}

    for x in crypto_list:
        cc[str(currency_id_dict[x])] = x

    for i in get_currencies_rate(request, cc):
        bot.send_message(chat_id, i)


@bot.message_handler(commands=['get_currency_rate'])
def send_currency_rate(message):
    cc = 'ethereum'
    c = 'USD'

    currency_id_dict = get_json_dict()
    url = "https://api.coinmarketcap.com/v2/ticker"\
        f"/{currency_id_dict[cc]}/?convert={c}"
    currency_rate = get_currency_rate(get_request(url), cc, c)

    bot.send_message(message.chat.id, currency_rate)


@bot.message_handler(commands=['get_crypto_graph'])
def send_graph(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'BTC->USD (1year)')
    bot.send_photo(chat_id, get_cryptocurrency_graph())
# calculator


@bot.callback_query_handler(
    func=lambda call: True if call.data == 'COMMAND=calculator' else False)
def send_calculation(call):
    message = 'Enter your crypto currency:'

    # take dataabout language
    language = 'ru'

    if language != 'en':
        translator = Translator(to_lang=language)
        message = translator.translate(message)
    sent = bot.send_message(call.message.chat.id, message)
    bot.register_next_step_handler(sent, send_calculation2)


def send_calculation2(message):
    answer = 'Enter an amount:'
    chat_id = message.chat.id
    user_dict[chat_id] = message.text.upper()
    # take dataabout language
    language = 'ru'

    if language != 'en':
        translator = Translator(to_lang=language)
        answer = translator.translate(answer)
    sent = bot.send_message(chat_id, answer)
    bot.register_next_step_handler(sent, send_calculation3)


def send_calculation3(message):
    chat_id = message.chat.id
    cc = user_dict[chat_id]
    c = "USD"

    currency_dict = get_json_dict(id_='all')

    try:
        url = "https://api.coinmarketcap.com/v2/ticker"\
            f"/{currency_dict['name_id'][cc]}/?convert={c}"
        print(url)
        request = get_request(url)
        if not request['data']:
            raise Exception
    except Exception:
        try:
            cc = currency_dict['name_id'][currency_dict['symbol_name'][cc]]
            url = "https://api.coinmarketcap.com/v2/ticker"\
                f"/{cc}/?convert={c}"
            print(url)
            request = get_request(url)
            if not request['data']:
                raise Exception
        except Exception:
            bot.send_message(chat_id, 'ERROR\U0001F480')
    finally:
        del user_dict[chat_id]

    print(request)
    amount = float(message.text.replace(" ", ""))
    print(amount)
    answer = calculation(request, amount, cc, c)
    bot.send_message(chat_id, answer)

# graph


def get_histodata(time, time_co, cc, c, aggregate=1):
    answer = []
    url = f'https://min-api.cryptocompare.com/data/histo{time}'\
        f'?fsym={cc}&tsym={c}&limit={time_co}&aggregate={aggregate}&e=CCCAGG'
    data = get(url).json()
    for quotes in data['Data']:
        date = date2num(datetime.datetime.fromtimestamp(quotes['time']))
        answer.append(tuple([date, quotes['open'], quotes['high'],
                             quotes['low'], quotes['close']]))
    return answer


def get_cryptocurrency_graph(time='day', time_count='365',
                             cryptocurrency='BTC', currency='USD'):

    if time == 'day':
        datevstime = True
        aggregate = 1
    else:
        datevstime = False
        aggregate = 2
    histodata = get_histodata(time=time, time_co=time_count,
                              cc=cryptocurrency, c=currency,
                              aggregate=aggregate)
    return get_graph(histodata, c=cryptocurrency, cc=currency, dt=datevstime)


@bot.callback_query_handler(
    func=lambda call: True if call.data == 'COMMAND=graph' else False)
def send_graph(call):
    answer = 'Chose one of these'
    all_ = 'all'
    year = 'year'
    month = 'three months'
    week = 'two weeks'

    # take dataabout language
    language = 'ru'

    if language != 'en':
        translator = Translator(to_lang=language)
        answer = translator.translate(answer)
        all_ = translator.translate(all_)
        year = translator.translate(year)
        month = translator.translate(month)
        week = translator.translate(week)

    markup_photo_settings = types.InlineKeyboardMarkup(row_width=2)
    markup_photo_settings.add(types.InlineKeyboardButton(
        text=f'{all_}\U0001F30D', callback_data='GRAPH=all'))

    markup_photo_settings.add(types.InlineKeyboardButton(
        text=f'{year}\U0001F4C5', callback_data='GRAPH=1year'))

    markup_photo_settings.add(types.InlineKeyboardButton(
        text=f'{month}\U0001F570\U0000FE0F', callback_data='GRAPH=3month'))

    markup_photo_settings.add(types.InlineKeyboardButton(
        text=f'{week}\U000023F2\U0000FE0F', callback_data='GRAPH=2weeks'))

    bot.send_message(call.message.chat.id, answer,
                     reply_markup=markup_photo_settings)


@bot.callback_query_handler(
    func=lambda call: True if call.data.split('=')[0] == 'GRAPH' else False)
def graph_get_currency(call):
    chat_id = call.message.chat.id
    time_period = call.data.split("=")[1]

    if time_period == 'all':
        user_dict[chat_id] = ['day', '2000']
    elif time_period == '1year':
        user_dict[chat_id] = ['day', '365']
    elif time_period == '3month':
        user_dict[chat_id] = ['day', '100']
    elif time_period == '2weeks':
        user_dict[chat_id] = ['hour', '168']

    answer = 'Enter your crypto currency:'

    # take dataabout language
    language = 'ru'

    if language != 'en':
        translator = Translator(to_lang=language)
        answer = translator.translate(answer)

    sent = bot.send_message(chat_id, answer)
    bot.register_next_step_handler(sent, graph_get_currency)


def graph_get_currency2(message):
    chat_id = message.chat.id
    cc = message.text.upper()
    user_data = user_dict[chat_id]
    user_data.append(cc)

    # take dataabout language
    language = 'ru'

    try:
        bot.send_photo(chat_id,
                       get_cryptocurrency_graph(*user_data),
                       reply_markup=get_main_meny(language))
    except Exception as e:
        print(e)
        bot.send_message(chat_id, 'ERROR\U0001F480')
    finally:
        del user_data


try:
    bot.polling()
except KeyboardInterrupt:
    exit()
