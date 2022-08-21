#uses rapidapi yh finance api, which allows 500 calls per month.
#23 x 7 hours equals 161 hours of trading per month, and if theres 500 calls, then you can do 3 calls per hour, max 20 minute refresh time
#https://www.advfn.com/p.php?pid=qkquote&symbol=



from dhooks import Webhook
import requests
import json
import threading
import time
import datetime
from tkinter import *
from tkinter import ttk
import requests
from bs4 import BeautifulSoup



config = {"stocks" : [], "webhook":"", "rate": 1200, "notifications":{}}
stocks=[]

try:
    fn=open("config.json","r")
except: 
    print("Error: File does not appear to exist. Creating config file.")
    fn = open("config.json","w")
    json.dump(config,fn)
else:
    config = json.load(fn)
    stocks = config['stocks']

flag = False

#sees if the market is open based on the date and time
def isopen():
    #0 = monday, 1 = tuesday, etc
    day = datetime.datetime.today().weekday()
    if day < 5:
        #day is a weekday
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        if (hour >= 9 and minute >= 30) or (hour > 9):
            if hour < 16:
                return True
    return False

#checks if the market is open, and if it is, wait the refresh rate and fetch new prices
def fetch(monitor=1200):
    global flag
    print(3)
    while flag:
        print(4)
        if isopen():
            T.configure(state="normal")
            T.insert(END, "market is open, fetching new prices")
            T.configure(state="disabled")
            print("market is open, fetching new prices")
            num = 0
            while num < monitor and flag:
                time.sleep(10)
                num += 10
                print("fetching new info in " + str(monitor-num) + " seconds")
            if flag == False:
                print("Monitor was stopped")
                return
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
        else:
            print("market is closed")
    
def menu(config):
    if start == "notify":
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
    
#triggered upon monitor button clicked
def go():
    global flag
    if flag == True:
        flag = False
    else:
        flag = True
    print(1)
    fetch(1200)

#adds the ticker to the stock list
def addticker():
    ticker = my_entry.get()
    if len(ticker) > 0 and ticker not in config['stocks']: 
        headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0"
        }
        r = requests.get('https://www.advfn.com/p.php?pid=qkquote&symbol=' + ticker, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        symbol = soup.find('h1',{'class':'symbol-h1'}).find('strong').text
        if symbol.upper() == ticker.upper():
            config['stocks'].append(ticker)
            my_entry.delete(0,END)
            fn = open("config.json","w")
            json.dump(config,fn)
            print(config['stocks'])

def testhook():
    hook = Webhook(url=webhook.get())
    hook.send("test")
    config['webhook'] = webhook.get()
    fn = open("config.json","w")
    json.dump(config,fn)

def gui():
    btn.pack()
    T.pack()
    my_entry.pack()
    submit.pack()
    webhook.pack()
    test.pack()
    Combo.pack()
    remove.pack()
    stopbtn.pack()
    if len(config['webhook']) > 0:
        webhook.insert(END,config["webhook"])

def unflag():
    global flag
    flag = False

def removeticker():
    ticker = Combo.get()
    config['stocks'].remove(ticker)
    Combo['values'] = config['stocks']
    #TODO dump config to file


window=Tk()
# add widgets here
btn=Button(window, text="Monitor", fg='blue', command=threading.Thread(target=go, daemon=True).start)
stopbtn = Button(window, text= "Stop Monitor", command= unflag)
T = Text(window, height = 5, width = 52, state="disabled")
my_entry = Entry(window)
submit = Button(window, text="submit", command=addticker)
webhook = Entry(window)
test = Button(window, command = testhook, text="test webhook")
Combo = ttk.Combobox(window, values = stocks)
Combo.set("Pick an Option")
remove = Button(window, text="remove ticker", command=removeticker)
window.title('Stock watcher')
window.geometry("350x350")

#runs gui
#hello
gui()
window.mainloop()

#t2 = threading.Thread(target= window.mainloop())
#t2.start()

#remove selector
#refresh rate section

