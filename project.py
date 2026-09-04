import yfinance as yf
import sqlite3
import sys
import os



def main():
    connect = sqlite3.connect("database.db")

    cur = connect.cursor()
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS stocks (
    name TEXT,
    lastprice REAL,
    number REAL
    )
    """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS account (
            balance REAL
            )
        """
        
    )
    connect.commit()

    balance = balance_check(cur)

    print(
        f"""Default balance is 100000$. Will Reset Automatically after you run out of money
        What do you want to do?
        "Report": Check your report
        "Buy": Buy a stock
        "Sell": Sell a stock
        "Q": Quit the program
        "Reset": Reset everything
        """
    )
    # so that num is defined
    num = ""
    while(True):
        try:
            num = input("Enter a task: ").upper()

        except ValueError:
            print("Please enter a valid task")
        match num:
            case "REPORT":
                try:
                    cur.execute("SELECT * FROM stocks")
                    items = cur.fetchall()
                    for item in items:
                        print(item)
                    print(f"Your Balance is: {balance}$")
                except sqlite3.OperationalError:
                    print("You didn't buy or sell anything yet")
            case "RESET":
                reset(cur)
                connect.commit()
                balance = 100000

            case "BUY":

                if balance > 0:
                    pass
                else:

                    reset(cur)
                # combines everything
                print("===== Buy a stock =====")
                name = input("Which stock to buy? ")
                n = float(input("How many shares you want to buy? "))
                lastprice = calc_price(n, name)
                if lastprice is None:
                    print(
                        f"""Failed to fetch stock price. Try with proper ticker such as 'NVDA'.
                    If it still fails create and issue at https://github.com/shortysliding/Stock-Market-Simulator/issues
                    """
                    )  
                    continue
                elif (balance-lastprice)>0:
                    buy_in_database(cur, name, lastprice, n)
                    print("=========================")
                    balance = balance_check(cur)
                    connect.commit()
                    print("Complete!")
                else:
                    print(f"You don't have enough balance. Shortage {(balance - lastprice)*-1}$")
                    print("=========================")

            case "SELL":
                print("===== Sell a stock =====")
                name = input("Which stock to sell? ")
                n = float(input("How many shares you want to sell? "))
                lastprice = calc_price(n, name)
                
                if lastprice is None:
                    print(
                        f"""Failed to fetch stock price. Try with proper ticker such as 'NVDA'.
                    If it still fails create and issue at https://github.com/shortysliding/Stock-Market-Simulator/issues
                    """
                    )  
                    continue
                lastprice_main = float(lastprice/n)
                print(profit(cur, lastprice_main, name))
                sell_in_database(cur, name, lastprice, n)
                print("=========================")
                balance = balance_check(cur)
                connect.commit()


            case "Q":
                balance_check(cur)
                connect.commit()
                break
                

    print("Goodbye!")

def profit(cur, lastprice, name):
    cur.execute("SELECT lastprice FROM stocks WHERE name = ?", (name,))
    lastprice1 = cur.fetchone()
    cur.execute("SELECT number FROM stocks WHERE name = ?", (name,))
    number1 = cur.fetchone()
    real_lastprice = int(lastprice1[0])/int(number1[0])
    
    
    if((real_lastprice)<lastprice):
        return f"You may lose {lastprice-real_lastprice}$ per stock"
    elif(real_lastprice>=lastprice):
        return f"You may gain {real_lastprice-lastprice}$ per stock"



def balance_check(cur):
    # checks for the last balance
    
    cur.execute("SELECT balance FROM account")
    balance = cur.fetchone()
    
    if balance is None:
        cur.execute("SELECT lastprice FROM stocks")
        items = cur.fetchall()
        # item has only 1 thing >> lastprice
        spend = sum(item[0] for item in items)
        balance = 100000 - spend
        cur.execute(
            "UPDATE account SET balance = ?",
            (balance,)
        )
        return 100000 - spend
    else:

        return float(balance[0])
    




def calc_price(numof_shares, name):

    lastprice = call_api(name)
    if lastprice is None:
        return None
    
    return float(lastprice) * float(numof_shares)


def call_api(name):
    try:

        stock = yf.Ticker(name)

        # Get latest market data
        data = stock.history(period="1d")

        # Get last price
        last_price = data["Close"].iloc[-1]
        if last_price is None:
            return None
        
        return last_price

    except Exception:
        print("Unable to fetch data from API")
        return None


def buy_in_database(cur, name, lastprice, n):

    a = cur.execute("SELECT EXISTS(SELECT 1 FROM stocks WHERE name = ?)", (name,))

    result = int(a.fetchone()[0])

    if result == 0:
        cur.execute(
            "INSERT INTO stocks (name, lastprice, number) VALUES (?, ?, ?)", (name, lastprice, n)
        )
    else:
        cur.execute(
            "UPDATE stocks SET lastprice = lastprice + ? WHERE name = ?",
            (lastprice, name),

        )
        cur.execute(
            "UPDATE stocks SET number = number + ? WHERE name = ?",
            (n, name),
        )
    


def sell_in_database(cur, name, lastprice, n):

    cur.execute("SELECT lastprice FROM stocks WHERE name = ?", (name,))

    item = cur.fetchone()
    if name is None:
        print("You don't own this stock")
        return

    current = item[0]
    cur.execute("SELECT number FROM stocks WHERE name = ?", (name,))
    n2 = cur.fetchone()
    if int(n2[0]) < n:
        print("You can't sell more than you have")
        return
    
  

    new_value = current - lastprice
    new_n = n2[0] - n;
    if new_n == 0:
        cur.execute("DELETE FROM stocks WHERE name = ?", (name,))
    else:
        cur.execute(
            "UPDATE stocks SET lastprice = ? WHERE name = ?",
            (new_value, name),
        )

        cur.execute(
            "UPDATE stocks SET number = ? WHERE name = ?",
            (new_n, name),
        )
    print("Complete!")


def reset(cur):
    cur.execute("DROP TABLE stocks")
    connect = sqlite3.connect("database.db")
    cur = connect.cursor()
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS stocks (
    name TEXT,
    lastprice REAL,
    number REAL
    )
    """
    )
    connect.commit()

    print(
        """You are bankrupt
                   Resetting
              Reset Complete!"""
    )


if __name__ == "__main__":
    main()
