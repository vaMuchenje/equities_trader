import urllib.request
from bs4 import BeautifulSoup
from time import strftime
import json
import csv
import sys


stocks = ['AAPL', 'AMZN', 'INTC', 'MSFT', 'SNAP']

def get_position(stock):
	with open('./db/positions.txt', 'r') as f:
	    a = json.load(f)
	    return a[stock]

def get_time():
	current_time = strftime("%a, %d %b %Y %H:%M:%S")
	return current_time

def get_data():
	global stocks
	data={}
	for stock in stocks:

		quote_page = 'https://finance.yahoo.com/quote/{}/'.format(stock)
		page = urllib.request.urlopen(quote_page)
		soup = BeautifulSoup(page, 'html.parser')
		prices = soup.findAll('span', attrs={"class":"Trsdu(0.3s) "})
		bid_priceText= prices[3].text
		priceSplit = bid_priceText.split(' ')
		price_final = priceSplit[0].replace(',','')	
		data.update({stock: float(price_final)})
	return(data)

def get_wap(stock):
	filepath = './wap/'+stock+'_wap.csv' 
	with open(filepath, 'r') as f:
		reader = csv.reader(f)
		trades = list(reader)
		if trades:
			total_money=0.0
			num_stocks= 0.0
			wap = 0.0
			for trade in trades:
				if float(trade[1]) != 0.0:
					total_money += float(trade[1])
					num_stocks += float(trade[0])
				else:
					continue
				wap = (total_money/num_stocks)
			return wap
		else:
			wap = float(0)
			return wap

def upl(stock, prices):
	position = get_position(stock)
	if float(position) == 0:
		upl = 0 
	else:
		wap = get_wap(stock)
		current_price = float(prices[stock])
		upl = ((current_price - wap) * float(position))
	return upl

def update_rpl(stock, profit_from_sell):
	with open('./db/rpl.txt') as f:
	    a = json.load(f)

	with open('./db/rpl.txt', 'w') as f:
		a[stock] += profit_from_sell
		json.dump(a, f)

def get_rpl(stock):
	with open('./db/rpl.txt') as f:
		a = json.load(f)
		return a[stock]


def set_upl(stock, amount):
	orig = get_rpl(stock)
	final_rpl = float(amount) - orig
	with open('./db/rpl.txt') as f:
	    a = json.load(f)

	with open('./db/rpl.txt', 'w') as f:
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
	5 - Reset Program 

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
	if choice == "5":
		print("Selected choice: 5")
		reset()

def display_pl():
	global stocks
	print("Gathering stock data, please wait... ")
	prices = get_data()
	print("Done!")
	tab_data = []
	for stock in stocks:
		data=[stock,get_position(stock),prices[stock], get_wap(stock) , upl(stock, prices),get_rpl(stock)]
		tab_data.append(data)
	from tabulate import tabulate
	print(tabulate(tab_data, headers=['Ticker', 'Position', 'Market Price', 'WAP', 'UPL', 'RPL']))
	start()

def update_position(stock, quantity):
	with open('./db/positions.txt') as f:
	    a = json.load(f)

	with open('./db/positions.txt', 'w') as f:
		a[stock] += quantity
		json.dump(a, f)

def update_cash(amount):
	with open('./db/cash.txt') as f:
	    a = json.load(f)

	with open('./db/cash.txt', 'w') as f:
		a["AMOUNT"] += amount
		json.dump(a, f)

def append_transaction(list):
	with open('./db/transactions.csv', 'a') as newFile:
	    newFileWriter = csv.writer(newFile)
	    newFileWriter.writerow(list)

def get_position(stock):
	with open('./db/positions.txt', 'r') as f:
	    a = json.load(f)
	    return a[stock]

def get_cash():
	with open('./db/cash.txt', 'r') as f:
	    a = json.load(f)
	    return a["AMOUNT"]

def display_blotter():
	with open('./db/transactions.csv', 'r') as f:
		reader = csv.reader(f)
		transactions = list(reader)
		if transactions:
			from tabulate import tabulate
			print(tabulate(transactions, headers=['Side', 'Ticker', 'Qty', 'Exec. Price', 'Exec. Time', 'Money In/Out']))
		else:
			print("No transactions to show, buy or sell something first")
		start()
	  
def append_wap(stock,list):
	filepath = './wap/'+stock+'_wap.csv'  
	with open(filepath, 'a') as newFile:
	    newFileWriter = csv.writer(newFile)
	    newFileWriter.writerow(list)

def get_stock_sell_price(stock):
	quote_page = 'https://finance.yahoo.com/quote/{}/'.format(stock)
	page = urllib.request.urlopen(quote_page)
	soup = BeautifulSoup(page, 'html.parser')
	prices = soup.findAll('span', attrs={"class":"Trsdu(0.3s) "})
	bid_priceText= prices[2].text
	priceSplit = bid_priceText.split(' ')
	price_final = float(priceSplit[0].replace(',',''))
	return price_final


def get_stock_buy_price(stock):
	quote_page = 'https://finance.yahoo.com/quote/{}/'.format(stock)
	page = urllib.request.urlopen(quote_page)
	soup = BeautifulSoup(page, 'html.parser')
	prices = soup.findAll('span', attrs={"class":"Trsdu(0.3s) "})
	bid_priceText= prices[3].text
	priceSplit = bid_priceText.split(' ')
	price_final = float(priceSplit[0].replace(',',''))
	return price_final



def buy():
	global stocks
	available_cash = get_cash()
	stock = (input("Enter stock symbol to buy (e.g. AMZN): ")).upper()
	if stock in stocks:
		print("Getting stock info...")
		stock_price = get_stock_buy_price(stock)
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
				print("Transaction executed successfully")
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
		stock_price = get_stock_sell_price(stock)
		available_quantity = get_position(stock)
		print("{} is trading at ${} and you have {} of it".format(stock.upper(), stock_price, available_quantity))
		quantity=float(input("Enter quantity to sell: "))
		money_from_sell = quantity * stock_price
		rpl =  money_from_sell - (get_wap(stock) * quantity)

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
				update_rpl(stock, rpl)
				set_upl(stock, sell_total)
				print("Transaction executed successfully")
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

def reset():
	global stocks
	action = str(input("Are you sure you want to reset the program?(Y/N): "))
	if action.upper() == "Y":
		print("Resetting program...")
		for stock in stocks:
			with open("./wap/" + stock + "_wap.csv", 'w'):
				pass
		with open("./db/transactions.csv", 'w'):
			pass	
		with open("./db/cash.txt", "w") as f:
			amount = {"AMOUNT": 10000000.0}
			json.dump(amount, f)
		with open("./db/positions.txt", "w") as f:
			positions = {"AMZN": 0, "SNAP": 0, "MSFT": 0, "AAPL": 0, "INTC": 0}
			json.dump(positions, f)
		with open("./db/rpl.txt", "w") as f:
			rpl = {"AMZN": 0, "SNAP": 0, "MSFT": 0, "AAPL": 0, "INTC": 0}
			json.dump(rpl, f)
		print("Done!")
		start()
	else:
		print("Reset abandoned")
		start()
		
start()