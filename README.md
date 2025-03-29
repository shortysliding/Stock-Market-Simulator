# Stock Market Simulator
#### Video Demo:  <https://youtu.be/ZJvViv5t6cI>
#### Description:
This is a simple command line which can simulate buying and selling stocks.
It saves all of your data in holdings.csv and report.csv

## __Requirements__
Required libraries can be downloaded by
```pip install -r requirements.txt```
Supported stock prices are taken by yfinance module
test_project.py uses pytest to 

## __Usage__
On the first time it will show the user some tasks to choose from. User can do as many tasks as possible before running out of money. However, if money is not deposited already user will not be able to use the program. There is no limit on depositing money.\
**Note: stock names have to be respective 
**Note: "Q" is to be inputted if user wants to quit(). Pressing Control-C will result the same.**

User can only sell the number of stocks they already bought(for a specific compnay).
It cannot be less or more.

Here is the first output which will guide the user.
```
What do you want to do?
    "Report": Check your report
    "Buy": Buy a stock
    "Sell": Sell a stock
    "Deposit": Deposit money to your account
    "Q": Quit the program
```

## __Functions__

The program has 4 functions in portfolio class and other exclusive 10 functions including main()

## __Portfolio Class__
**__init__()**\
Initializes a portfolio with an empty list of holdings and a valuation tracker

**__check()__**\
Reads the holdings.csv file to check for previous holdings and returns them. If the file is missing, it returns False.

__buy_stock(num, name, balance)__\
Buys a stock and adds it to the portfolio. Updates balance after the purchase. If the balance is insufficient, the program exits.

__sell_stock(num, name, stocks, balance)__\
Sells a stock and checks if there is a profit or loss. Updates balance accordingly and prints the selling price.

## _Main Functions__
__main()__\
Runs the main program loop, allowing users to check reports, buy/sell stocks, deposit money, or quit.

__deposit(n, balance)__\
Adds a specified amount to the balance and updates it.

__balance_check()__\
Checks and returns the last recorded balance from report.csv. If no record exists, it notifies the user.

__ call_api(name)__\
Fetches the latest stock price from Yahoo Finance. If there's an issue, it prints an error message.

__buy(balance)__\
Combines every funtion responsible for buying stocks.
Handles stock purchases by taking user input, buying the stock, and saving the details.

__sell()__\
Combines every funtion responsible for buying stocks.
Handles selling a stock by taking user input, updating records, and removing the stock from holdings.

__save_stock_csv(stocks)__\
Saves stock holdings to holdings.csv. If the file is empty, it writes a header first.

__sell_stock_csv(name)__\
Removes a sold stock from holdings.csv and updates its valuation.

__update(balance)__\
Calculates the current balance and total stock value, then updates report.csv.

__difference(difference, balance)__\
Adjusts the balance based on stock sale profits or losses.

# __Thanks__
I want to thank David Malan and every the entire CS50 team for such a wonderful course. I also want to thank you everyone who helped us in this journey.

   

