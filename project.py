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
    lastprice REAL
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
    while num != "Q":
        try:
            num = input("Enter a task: ").upper()

        except ValueError:
            print("Please enter a valid task")
        match num:
            case "REPORT":
                cur.execute("SELECT * FROM stocks")
                items = cur.fetchall()
                for item in items:
                    print(item)
                print(f"Your Balance is: {balance}$")
            case "RESET":
                reset(cur)
                connect.commit()

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
                buy_in_database(cur, name, lastprice)
                print("=========================")
                balance = balance_check(cur)
                connect.commit()

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
                sell_in_database(cur, name, lastprice)
                print("=========================")
                balance = balance_check(cur)
                connect.commit()

    print("Goodbye!")


def balance_check(cur):
    # checks for the last balance

    cur.execute("SELECT lastprice FROM stocks")
    items = cur.fetchall()
    # item has only 1 thing >> lastprice
    spend = sum(item[0] for item in items)
    return 100000 - spend


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


def buy_in_database(cur, name, lastprice):

    a = cur.execute("SELECT EXISTS(SELECT 1 FROM stocks WHERE name = ?)", (name,))

    result = int(a.fetchone()[0])

    if result == 0:
        cur.execute(
            "INSERT INTO stocks (name, lastprice) VALUES (?, ?)", (name, lastprice)
        )
    else:
        cur.execute(
            "UPDATE stocks SET lastprice = lastprice + ? WHERE name = ?",
            (lastprice, name),
        )


def sell_in_database(cur, name, lastprice):

    cur.execute("SELECT lastprice FROM stocks WHERE name = ?", (name,))

    item = cur.fetchone()
    if item is None:
        print("You don't own this stock")
        return

    current = item[0]

    if current < lastprice:
        return "You can't sell more than you have"

    new_value = current - lastprice

    if new_value == 0:
        cur.execute("DELETE FROM stocks WHERE name = ?", (name,))
    else:
        cur.execute(
            "UPDATE stocks SET lastprice = ? WHERE name = ?",
            (new_value, name),
        )


def reset(cur):
    cur.execute("DROP TABLE stocks")

    sys.exit(
        """You are bankrupt
                   Resetting
              Restart the program"""
    )


if __name__ == "__main__":
    main()
