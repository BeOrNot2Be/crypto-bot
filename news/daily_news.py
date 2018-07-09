from news.get_requests_data import get_bijournal_news, get_forklog_news, get_coindesk_news
from  news.get_newspaper_image import get_newspaper_image


list_of_journals = ['get_bijournal_news()', 'get_forklog_news()',
'get_coindesk_news()']


def get_news(list_of_journals=list_of_journals):
    answer = []
    for i in list_of_journals:
        for v in eval(i):
            answer.append(v)
    return [answer, get_newspaper_image()]
