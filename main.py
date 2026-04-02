"""https://youtu.be/byHcYRpMgI4?t=713
Need to make database"""

import yfinance as yf
import sqlite3
import datetime
import sys
import os 

def buy_stock(numof_shares, name, balance):        
        """
        Buys a stock and adds it to the self._holdings.
        """
        lastprice = call_api(name)
        info = float(lastprice) * float(numof_shares)
        stocks = {"name": name, "valuation": info}
        
        
        

def call_api(name):
    try:
        stock = yf.Ticker(name)

        lastprice = float(stock.fast_info["lastPrice"])
        return lastprice

    except KeyError:
        print("Enter a valid stock name")
    except:
        print("Unable to fetch data from the API")

#OOO
