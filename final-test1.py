import requests
import pandas_datareader
from pandas_datareader import data
import pandas as pd
import numpy as np
from pandas_datareader import data
import datetime
import matplotlib.pyplot as plt

Alpha_key = "9CZWI7NQ3IAGIFOO"
Polygon_key = "f2N9IZ6EdkGPmFw_AjGB9Y05p4SppIwp"

def search_by_character(keywords):
    '''
    Input: Any character the users are thinking about. For example: APP
    Output: A list of stock's symbol which is in the US market, and the stock symbol is based on input. 
    '''
    Alpha_search_url="https://www.alphavantage.co/query?function=SYMBOL_SEARCH&"
    r = requests.get(f"{Alpha_search_url}keywords={keywords}&apikey={Alpha_key}")
    data = r.json()['bestMatches']
    len_data = len(data)
    if len_data==0: ##to be tested!!检验是否会重新开始循环！
        print("There are no stocks that match your search. Please input other character  ")
        keywords=input("What letters you like?Please input more than one letter.(For example: AP)  ")
        search_by_character(keywords)
    else:
        print(f"\nThere are {len_data} stocks that match your search. The stock symbols are ")
        # print(data)
        symbol_list=[]
        us_symbol_list=[]
        for i in range(len_data):
            symbol_list.append(data[i]['1. symbol'])
            print(i, data[i]['1. symbol'])
            if data[i]['4. region']=='United States':
                us_symbol_list.append(data[i]['1. symbol'])
        print(data)
        print(symbol_list)
        print("Currently we can only support for the stocks which is in United States market. The stocks currently in US are")
        print(us_symbol_list) #如果us是空的也要重新输入

    return us_symbol_list

def stocks_detail(symbol_list):
    '''
    Input: us_symbol_list; the date which users want to have a look.
    Output: the price detail of the stocks on that date 
    '''
    date = input("Which date's price do you want to see? Please ensure it was a trading date! (For example:2022-11-29)  ")
    stocks_detail_url = "https://api.polygon.io/v2/aggs/ticker/"
    stock_detail=[]
    for stock in symbol_list:
        try:
            r = requests.get(f"{stocks_detail_url}{stock}/range/1/day/{date}/{date}?adjusted=true&sort=asc&limit=120&apiKey={Polygon_key}")
            data = r.json()
            print(data)
            stock_detail.append(data)
            ### 如果输入的日子不是 ...
        except:
            print(f"{stock} is not active anymore. Will be skipped")
    return stock_detail
        # try:
            # price = data.DataReader(stock,'yahoo',date)
            # print(stock)
            # print(price)
        # except:
            # print(f"{stock} is not active anymore. Will be skipped")
        # print(price)

def price_tree(stock_detail):
    '''
    input: us_symbol_list;
    output:  a tree in the format of a dictionary, which is classified by price.
    '''
    priceTree = {'$0-$100': [], '$100-$200': [], '>$200': []}
    
    for stock in stock_detail:
        if 'results' not in stock.keys():
            continue
        if stock['results'][0]['o']<100:
            priceTree['$0-$100'].append(stock['ticker'])
        if 100<=stock['results'][0]['o']<=200:
            priceTree['$100-$200'].append(stock['ticker'])
        if stock['results'][0]['o']>200:
            priceTree['>$200'].append(stock['ticker'])
    return priceTree
    


def choose_stock(priceTree):
    '''
    choose the stock based on the price-tree
    '''
    price_choice = input("Which stock price range you want to choose?(Please choose from: $0-$100, $100-$200, >$200) . ")
    # if priceTree[price_choice] is None:
        # price_choice = ("The price you choose is not availbale for these stocks. Please reentry a price range: ")
        # choose_stock(priceTree)
    price_stock = priceTree[price_choice]
    print(price_stock)
    stock_choice = input(f"These are the stock which price is {price_choice}: {price_stock}. Which stock you would like to choose?  ")
    # print("Here is the detail information for this stock")
    return stock_choice


def get_company(stock_choice):
    '''
    Will provide the detailed information about the company
    '''
    get_company_url= "https://api.polygon.io/v3/reference/tickers/"
    ans = input("Do you want to know more about this company? (Yes/No) ")
    if ans.strip().lower() == "yes":
        try:
            r = requests.get(f"{get_company_url}{stock_choice}?apiKey={Polygon_key}")
            data = r.json()     
            key_list = [data["results"].keys()]
            key = input(f"What kind of information you want to know? Please choose from {key_list}")
            print(data["results"][key])
        except: #测试如果那种没有results的key，最后会怎么样
            print("Not available information")

def SMA(stock_choice):
    '''
    Return SMA to provide some trading recommendation.
    '''
    ans = input("Do you want to have some technicial choice? (Yes/No) ")
    if ans.strip().lower() == "yes":
        print("The following plot is Simple Moving Average (SMA)-5 and SMA-10 days for that stock")
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days = 100)
        price = data.DataReader(stock_choice,'yahoo',
                        start_date,
                        end_date)
        price.head()
        price['ma5'] = price['Adj Close'].rolling(5).mean()
        price['ma20'] = price['Adj Close'].rolling(20).mean()
        price.tail()
        fig = plt.figure(figsize=(16,9))
        ax1 = fig.add_subplot(111, ylabel='Price')
        price['Adj Close'].plot(ax=ax1, color='g', lw=2., legend=True)
        price.ma5.plot(ax=ax1, color='r', lw=2., legend=True)
        price.ma20.plot(ax=ax1, color='b', lw=2., legend=True)
        plt.grid()
        plt.show()
        print("When the short term moving average crosses above the long term moving average, this indicates a buy signal. Contrary, when the short term moving average crosses below the long term moving average, it may be a good moment to sell.")
    else:
        print("Good Bye!")


if __name__=='__main__':
    keywords=input("what character you like?(please input more than one character) ")
    us_symbol_list = search_by_character(keywords)
    print("==========================================================================")
    stock_detail = stocks_detail(us_symbol_list)
    print("==========================================================================")
    tree_of_price = price_tree(stock_detail)
    print(tree_of_price)
    # choose_stock(tree_of_price)
    print("==========================================================================")
    stock_choice = choose_stock(tree_of_price)
    get_company(stock_choice)
    # choose_stock(tree_of_price)
    print("==========================================================================")
    SMA(stock_choice)

