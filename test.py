import requests
import json
import datetime

X_CoinAPI_Key = 'E133C99D-E45D-4236-99BD-3C6C5D49228F'
method = 'BITSTAMP_SPOT_BTC_USD'

input_period = '1 MTH'.upper()
input_period = input_period.split(' ')
print(input_period)
days = 0
seconds = 0 
minutes = 0 
hours = 0
time_dict = {
	'SEC':  'seconds = int(input_period[0])',
	'MIN':  'minutes = int(input_period[0])',
	'HRS':  'hours = int(input_period[0])',
	'DAY':  'days = int(input_period[0])',
	'MTH':  'days = int(input_period[0])*30',
	'YRS':  'days = int(input_period[0])*365',
}
answer_ = time_dict.get(input_period[1], False)
if answer_:
	exec(answer_)
else:	
	raise Exception
print(days,minutes,seconds,hours)
print(input_period[0])
input_period[1] = {'YRS':'MTH', 'MTH':'DAY', 'DAY':'HRS', 'HRS':'MIN', 'MIN':'SEC'}.get(input_period[1],input_period[1])
period = ''.join(input_period)


try:
	datetime_ = datetime.datetime.today() - datetime.timedelta(days=days, seconds=seconds, minutes=minutes, hours=hours,)
	time_start = 'T'.join(str(datetime_).split(' ')).split('.')[0]
	print(time_start)
	url = f'https://rest.coinapi.io/v1/ohlcv/{method}/history?period_id={period}&time_start={time_start}'

	with open('request.txt', 'w') as f:
			f.write('')

	headers = {'X-CoinAPI-Key' : X_CoinAPI_Key}
	data = requests.get(url, headers=headers)
	with open('request.txt', 'a') as f:
		for post in data:
			f.write(post.decode())
	with open('request.txt', 'r+') as f:
		request = json.loads(f.read())
		answer = [str({example['time_close']:example['price_close']})+'\n'  for example in request ]
	with open('request.txt', 'w') as f:
		f.write(str(answer))
except Exception as e:
	print(e)
finally:
	input()