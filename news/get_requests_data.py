import requests
from lxml.html import fromstring


def get_bijournal_news(date=False):

    answer = []

    if not date:

        url = 'https://bitjournal.media/news/'
        page_data = requests.get(url)
        html = fromstring(page_data.text)
        for i in html.find_class("title"):
            answer.append(i.values()[0])
    else:
        pass

    return answer


def get_forklog_news():

    answer = []
    url = 'https://forklog.com/news/'
    page_data = requests.get(url)
    html = fromstring(page_data.text)

    for i in html.find_class("item"):
        answer.append(i.findall('a')[0].values()[0])

    return answer


def get_coinmarket_news():

    answer = []
    url = 'https://coinmarket.news/novosti/'
    page_data = requests.get(url)
    html = fromstring(page_data.content.decode())

    for i in html.find_class("post-title"):
        answer.append(i.findall('a').append(''))

    return answer


def get_coindesk_news():

    answer = []
    url = 'https://www.coindesk.com/'
    page_data = requests.get(url)
    html = fromstring(page_data.text)

    for i in html.find_class("fade"):
        if i.values()[0] == 'fade':
            answer.append(i.values()[1])
        else:
            answer.append(i.values()[0])

    return answer
