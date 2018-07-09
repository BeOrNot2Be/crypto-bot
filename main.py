import telebot
import config
from news.daily_news import get_news
from calculations.get_rate import (calculation, get_currencies_rarte,
                                 get_currency_rarte)
from graph.get_graph import get_cryptocurrency_graph

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=["news"])
def send_news(message):
    news = get_news()
    for i in news[0]:
        if i != '':
            bot.send_message(message.chat.id, i)
    bot.send_photo(message.chat.id, news[1])


@bot.message_handler(commands=['calculation'])
def send_answer(message):
    answer = calculation()
    bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['get_currencies_rarte'])
def send_currencies_rarte(message):
    currencies_rarte = get_currencies_rarte()
    for i in currencies_rarte:
        bot.send_message(message.chat.id, i)


@bot.message_handler(commands=['get_currency_rarte'])
def send_currency_rarte(message):
    currency_rarte = get_currency_rarte()
    bot.send_message(message.chat.id, currency_rarte)


@bot.message_handler(commands=['get_crypto_graph'])
def send_graph(message):
    bot.send_photo(message.chat.id, get_cryptocurrency_graph())



bot.polling()
