import requests
import datetime

try:
	def function_(option = []):

		cryptocurrency = option[0].upper()
		currency = option[1].upper()
		time_period = option[2].upper()

		method = f'BITSTAMP_SPOT_{cryptocurrency}_{currency}'
		time_period = time_period.split('=')

		days = 0
		seconds = 0 
		minutes = 0 
		hours = 0

		time_dict = {
			'SEC':  'seconds = int(time_period[0])',
			'MIN':  'minutes = int(time_period[0])',
			'HRS':  'hours = int(time_period[0])',
			'DAY':  'days = int(time_period[0])',
			'MTH':  'days = int(time_period[0])*30',
			'YRS':  'days = int(time_period[0])*365',
		}

		answer_ = time_dict.get(time_period[1], False)
		if answer_:
			exec(answer_, locals(), globals())
			print(answer_)
		else:	
			raise Exception

		print(time_period)
		print(days,minutes,seconds,hours)
		datetime_ = datetime.datetime.today() - datetime.timedelta(days=days, seconds=seconds, minutes=minutes, hours=hours,)
		time_start = 'T'.join(str(datetime_).split(' ')).split('.')[0]

		time_period[1] = {'YRS':'MTH', 'MTH':'DAY', 'DAY':'HRS', 'HRS':'MIN', 'MIN':'SEC'}.get(time_period[1],time_period[1])
		print(time_period)
		period = ''.join(time_period)

		url = f'https://rest.coinapi.io/v1/ohlcv/{method}/history?period_id={period}&time_start={time_start}'
		print(url)
		data = requests.get(url, headers = {'X-CoinAPI-Key' : 'E133C99D-E45D-4236-99BD-3C6C5D49228F'} )
		print(data.json())

	function_(option = ['BTC','USD','1=MTH'])

	input()	
except Exception as a:
	print(a)
	input()