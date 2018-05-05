import requests
import json
import re
import datetime
from graph import crypto_graphik

def _get_url(where='bittrex', method='', params=''):
	if where == 'bittrex':
		url = f'https://bittrex.com/api/v1.1/public/{method}?{params}'
	else:
		url = f'{where}{method}?{params}'	
	return url

def calculator(option=[]):
	if not option:
		pass
	else:
		value = option[0]
		from_ = option[1]
		into = option[2].lower()
		params = None
		resp = requests.get(url=_get_url(where=f'https://api.coinmarketcap.com/v1/ticker/{from_}/', params=f'convert={into}'), params=params)
		data = resp.json()
		price_usd = data[0][f'price_{into}']
		return [f'{from_.upper()}-->{round(float(price_usd), 5)}', f'{into.upper()}-->{round(float(value) * float(price_usd), 5)}']


def main_graph(option=[ ]):
	if not option:
		pass
	else:
		
		return


def crypto_graph(option=[]):
	if not option:
		pass
	else:
		cryptocurrency = option[0].upper()
		currency = option[1].upper()
		time_period = option[2].upper()

		method = f'BITSTAMP_SPOT_{cryptocurrency}_{currency}'
		time_period = time_period.split('=')

		days = 0
		seconds = 0 
		minutes = 0 
		hours = 0

		if time_period[1] == 'SEC':
			seconds = int(time_period[0])
		elif time_period[1] == 'MIN':
			minutes = int(time_period[0])
		elif time_period[1] == 'HRS':
			hours = int(time_period[0])
		elif time_period[1] == 'DAY':
			days = int(time_period[0])
		elif time_period[1] == 'MTH':
			days = int(time_period[0])*30
		elif time_period[1] == 'YRS':
			days = int(time_period[0])*365
		else:	
			raise Exception

		datetime_ = datetime.datetime.today() - datetime.timedelta(days=days, seconds=seconds, minutes=minutes, hours=hours,)
		time_start = 'T'.join(str(datetime_).split(' ')).split('.')[0]

		time_period[1] = {'YRS':'MTH', 'MTH':'DAY', 'DAY':'HRS', 'HRS':'MIN', 'MIN':'SEC'}.get(time_period[1],time_period[1])
		period = ''.join(['1',time_period[1]])

		url = f'https://rest.coinapi.io/v1/ohlcv/{method}/history?period_id={period}&time_start={time_start}'
		data = requests.get(url, headers = {'X-CoinAPI-Key' : 'E133C99D-E45D-4236-99BD-3C6C5D49228F'} )
		
		
		request = data.json()
		answer = [{example['time_close']:example['price_close']} for example in request ]
		print(answer)
		return crypto_graphik(currency , cryptocurrency, answer)

def my_wallet(option=[]):
	if not option:
		pass
	else:
		
		return	