#uses rapidapi yh finance api, which allows 500 calls per month.
#23 x 7 hours equals 161 hours of trading per month, and if theres 500 calls, then you can do 3 calls per hour, max 20 minute refresh time

from dhooks import Webhook
import requests
import json
import threading
import time

config = {"stocks" : [], "notifications":"", "rate": 1200}
stocks=[]

def fetch(monitor):
    num = 0
    while num < monitor:
        time.sleep(10)
        num += 10
        print("fetching new info in " + str(monitor-num) + " seconds")
    print('fetching!')
    '''headers = {
	"X-RapidAPI-Key": "2b1ab8509cmsh1d250472e255ecbp1b3a8djsnac24acb5b68b",
	"X-RapidAPI-Host": "yh-finance.p.rapidapi.com" }
    url = "https://yh-finance.p.rapidapi.com/market/v2/get-quotes"


    stocks = ','.join(config['stocks'])
    querystring = {"region":"US","symbols":"AMD,IBM,AAPL"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)
    askprice = response["quoteResponse"]['result'][0]['ask']
    print(askprice)'''

def notify(url):
    hook = Webhook(url=url)
    hook.send("test")
    
def menu(config):
    try:
        fn=open("config.json","r")
    except: 
        print("Error: File does not appear to exist. Creating config file.")
        fn = open("config.json","w")
        json.dump(config,fn)
    else:
        config = json.load(fn)
        stocks = config['stocks']

    start = input("What would you like to do?")
    if start == "add":
        go = input("Enter your stock ticker")
        try:
            config['stocks'].append(go)
        #if there is no stocks key, start one with this input as the first key in a list
        except:
            config['stocks'] = [go]
        fn = open('config.json','w')
        json.dump(config, fn)
    elif start == "notify":
        sys = input("Enter the stock ticker you would like to watch")
        price = input("Enter the price target")
        ou = input("Over or under this price target?")
        try:
            config['notifications'].append([sys,price,ou])
        except:
            config['notifications'] = [sys,price,ou]
    elif start == "remove":
        start = input("enter the stock ticker you would like to remove")
        try:
            config['stocks'].pop(start)
        except:
            print("This stock is not in the list")
    elif start == "config":
        inp = input("What would you like to change?")
        if inp == "refresh rate":
            pass
        elif inp == "notify":
            url = input("enter your webhook URL")
            notify(url=url)
    elif start == "monitor":
        try:
            rate = config["rate"]
        except:
            rate = 1200
            config["rate"] = 1200
        t = threading.Thread(target=fetch(rate))

menu(config)
    






