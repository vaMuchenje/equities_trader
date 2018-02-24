import urllib.request
from bs4 import BeautifulSoup
from time import strftime
import json
import csv
import sys


stocks = ['AAPL', 'AMZN', 'INTC', 'MSFT', 'SNAP']

def get_position(stock):
	with open('positions.txt', 'r') as f:
	    a = json.load(f)
	    return a[stock]

def get_time():
	current_time = strftime("%a, %d %b %Y %H:%M:%S")
	return current_time

def get_data():
	global stocks
	data={}
	for stock in stocks:

		quote_page = 'https://www.bloomberg.com/quote/{}:US'.format(stock)
		page = urllib.request.urlopen(quote_page)
		soup = BeautifulSoup(page, 'html.parser')
		priceText = soup.find('span', attrs={'class':'priceText__1853e8a5'})
		priceT = priceText.text
		price = priceT.replace(',','')
		data.update({stock: price})
	return data

def get_wap(stock):
	filepath = 'wap/'+stock+'_wap.csv' 
	with open(filepath, 'r') as f:
	  reader = csv.reader(f)
	  trades = list(reader)
	  total_money = 0
	  number_stocks = 0
	  for trade in trades:
	  	total_money += float(trade[1])
	  	number_stocks += float(trade[0])
	  if number_stocks == 0:
	  	wap = float(0)
	  else:
	  	wap = float(total_money / number_stocks)
	  return wap

def upl(stock, prices):
	position = get_position(stock)
	if float(position) == 0:
		upl = 0 
	else:
		wap = get_wap(stock)
		current_price = float(prices[stock])
		upl = ((current_price - wap) * float(position)) - float(get_rpl(stock))
	return upl

def update_rpl(stock, lists):
	wap = float(get_wap(stock))
	sell_price = float(lists[0])
	quantity = float(lists[1])
	rpl_update = (sell_price - wap)*quantity
	with open('rpl.txt') as f:
	    a = json.load(f)

	with open('rpl.txt', 'w') as f:
		a[stock] += rpl_update
		json.dump(a, f)

def get_rpl(stock):
	with open('rpl.txt') as f:
		a = json.load(f)
		return a[stock]

def set_upl(stock, amount):
	orig = upl()
	final_rpl = float(amount) - orig
	with open('rpl.txt', 'w') as f:
		a[stock] += final_rpl
		json.dump(a, f)

def trade():
	trading()

def blotter():
	display_blotter()

def start():
	print('''
	Choose a number option:

	1 - Trade
	2 - Show Blotter
	3 - Show P/L
	4 - Quit 

	'''
	)

	choice = str(input("Enter number of action to perform: "))
	
	if choice == "1":
		print("Selected choice: 1")
		trade()
	if choice == "2":
		print("Selected choice: 2")
		blotter()
	if choice == "3":
		print("Selected choice: 3")
		display_pl()
	if choice == "4":
		print("Selected choice: 4")
		print("Exiting program")
		sys.exit(0)

def display_pl():
	global stocks
	print("Gathering stock data, please wait... ")
	prices = get_data()
	print("Done!")
	tab_data = []
	for stock in stocks:
		data=[stock,get_position(stock),prices[stock], get_wap(stock) , upl(stock, prices), get_rpl(stock)]
		tab_data.append(data)
	from tabulate import tabulate
	print(tabulate(tab_data, headers=['Ticker', 'Position', 'Market Price', 'WAP', 'UPL', 'RPL']))
	start()

def update_position(stock, quantity):
	with open('positions.txt') as f:
	    a = json.load(f)

	with open('positions.txt', 'w') as f:
		a[stock] += quantity
		json.dump(a, f)

def update_cash(amount):
	with open('cash.txt') as f:
	    a = json.load(f)

	with open('cash.txt', 'w') as f:
		a["AMOUNT"] += amount
		json.dump(a, f)

def append_transaction(list):
	with open('transactions.csv', 'a') as newFile:
	    newFileWriter = csv.writer(newFile)
	    newFileWriter.writerow(list)

def get_position(stock):
	with open('positions.txt', 'r') as f:
	    a = json.load(f)
	    return a[stock]

def get_cash():
	with open('cash.txt', 'r') as f:
	    a = json.load(f)
	    return a["AMOUNT"]

def display_blotter():
	with open('transactions.csv', 'r') as f:
		reader = csv.reader(f)
		transactions = list(reader)
		if transactions:
			from tabulate import tabulate
			print(tabulate(transactions, headers=['Side', 'Ticker', 'Qty', 'Exec. Price', 'Exec. Time', 'Money In/Out']))
		else:
			print("No transactions to show, buy or sell something first")
		start()
	  
def append_wap(stock,list):
	filepath = 'wap/'+stock+'_wap.csv'  
	with open(filepath, 'a') as newFile:
	    newFileWriter = csv.writer(newFile)
	    newFileWriter.writerow(list)

def get_stock_price(ticker_symbol):
	quote_page = 'https://www.bloomberg.com/quote/{}:US'.format(ticker_symbol)
	page = urllib.request.urlopen(quote_page)
	soup = BeautifulSoup(page, 'html.parser')
	priceText = soup.find('span', attrs={'class':'priceText__1853e8a5'})
	price = priceText.text
	price = price.replace(",", "")
	return float(price)

def buy():
	global stocks
	available_cash = get_cash()
	stock = (input("Enter stock symbol to buy (e.g. AMZN): ")).upper()
	if stock in stocks:
		print("Getting stock info...")
		stock_price = get_stock_price(stock)
		print("{} is trading at ${}".format(stock.upper(), stock_price))
		quantity=float(input("Enter quantity to buy: "))
		cost_of_buy = quantity * stock_price

		if cost_of_buy < available_cash : 
			print("Transaction cost for {} of {} is ${}.".format(quantity, stock, cost_of_buy)) 
			buy_choice = str(input("Execute?(Y/N): "))
			if buy_choice.upper() == "Y":
				buy_time = get_time()
				buy_quantity = quantity
				buy_price = stock_price
				buy_type = 'BUY'
				buy_total = cost_of_buy * (-1)
				buy_symbol = stock
				update_position(buy_symbol, buy_quantity)
				update_cash(buy_total)
				append_transaction([buy_type, buy_symbol, buy_quantity, buy_price, buy_time, cost_of_buy])
				append_wap(buy_symbol,[buy_quantity, cost_of_buy])
				start()

			if buy_choice.upper() == "N":
				print("Not Buying")
				start()

		else:
			print("Transaction not possible, you don't have enough money.")

		
	else:
		print("Entered stock symbol not available")

def sell():
	global stocks
	stock = (input("Enter stock symbol to sell (e.g. AMZN): ")).upper()
	if stock in stocks:
		print("Getting stock info...")
		stock_price = get_stock_price(stock)
		available_quantity = get_position(stock)
		print("{} is trading at ${} and you have {} of it".format(stock.upper(), stock_price, available_quantity))
		quantity=float(input("Enter quantity to sell: "))
		money_from_sell = quantity * stock_price

		if quantity < available_quantity : 
			print("Transaction will earn you ${} in cash".format(money_from_sell)) 
			sell_choice = str(input("Execute?(Y/N): "))
			if sell_choice.upper() == "Y":
				sell_time = get_time()
				sell_quantity = quantity * (-1)
				sell_price = stock_price
				sell_type = 'SELL'
				sell_total = money_from_sell
				sell_symbol = stock
				update_position(sell_symbol, sell_quantity)
				update_cash(sell_total)
				append_transaction([sell_type, sell_symbol, quantity, sell_price, sell_time, sell_total])
				update_rpl(stock, [sell_price, quantity])
				set_upl(stock, sell_total)
				start()
				
			if sell_choice.upper() == "N":
				print("Not Selling")
				start()

		else:
			print("Transaction not possible, you don't have enough stock.")

		
	else:
		print("Entered stock symbol not available")

def trading():

	print('''
		MAKE A TRADE:
		
		1 - Buy
		2 - Sell
		''')

	side = input("Buy or Sell?: ")

	if side == '1':
		buy()
	if side == '2':
	 	sell()

start()