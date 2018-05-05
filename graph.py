import matplotlib.pyplot as plt
import json
import ast
#from matplotlib import rcParams
#from matplotlib.dates import DateFormatter, WeekdayLocator,DayLocator, MONDAY
#from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
import random


def crypto_graphik(currency, cryptocurrency, answer):
	'''
	x = []
	y = []

	main_dict = {}

	for i in answer:
		main_dict.update(i)
	K = 0
	for i in [*main_dict]:
		K += 1
		y.append(K)
		x.append(main_dict[i])
	print(x,y,'\n\n\n\n\n')

	plt.xlabel("Time")
	plt.ylabel(currency)

	plt.plot(y,x,'-',color='c')
	plt.grid()
	plt.title(cryptocurrency)
	

	numb = random.randint(999,10000)
	plt.savefig(f"photo/test{numb}.jpg")
	return os.path.abspath(f"photo/test{numb}.jpg")
	'''



	'''
	# (Year, month, day) tuples suffice as args for quotes_historical_yahoo
	date1 = (2004, 2, 1)
	date2 = (2004, 4, 12)


	mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
	alldays = DayLocator()              # minor ticks on the days
	weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
	dayFormatter = DateFormatter('%d')      # e.g., 12

	quotes = quotes_historical_yahoo_ohlc('INTC', date1, date2)
	if len(quotes) == 0:
	    raise SystemExit

	fig, ax = plt.subplots()
	fig.subplots_adjust(bottom=0.2)
	ax.xaxis.set_major_locator(mondays)
	ax.xaxis.set_minor_locator(alldays)
	ax.xaxis.set_major_formatter(weekFormatter)
	#ax.xaxis.set_minor_formatter(dayFormatter)

	#plot_day_summary(ax, quotes, ticksize=3)
	candlestick_ohlc(ax, quotes, width=0.6)
	ax.xaxis_date()
	ax.autoscale_view()
	plt.setp(plt.gca().get_xticklabels(), rotation=90, horizontalalignment='right')

	numb = random.randint(999,10000)
	plt.savefig(f"photo/test{numb}.jpg")'''
	return answer