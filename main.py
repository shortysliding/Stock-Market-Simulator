"""https://youtu.be/byHcYRpMgI4?t=713
Need to make database
call_api() needs fix
"""

import yfinance as yf
import sqlite3
import datetime
import sys
import os 

def buy_stock(numof_shares, name):        
        """
        Buys a stock and adds it to the self._holdings.
        """
        lastprice = call_api(name)
        info = float(lastprice) * float(numof_shares)
        return info
        

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
def create_database(name, lastprice):

    connect = sqlite3.connect("database.db")

    # create cursor
    c = connect.cursor()
    #create table
    c.execute(""" CREATE TABLE stocks (
            name text,
            lastprice real )
            """)
    c.execute("INSERT INTO stocks (name, lastprice) VALUES (?, ?)",(name, lastprice))
    #commit
    connect.commit()
    #close
    connect.close()


     

def main():
     #create_database("NVDA",2) --- This works
    pass

main()
