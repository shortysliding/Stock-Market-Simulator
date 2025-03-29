import yfinance as yf
import csv
import datetime
import sys
import os 


class Portfolio:
    def __init__(self):
        self._holdings = []
        self._valuation_before = 0  


    def check(self):
        # checks the holdings.csv file and returns the previous holdings
        try:
            with open("holdings.csv", "r") as file:
                reader = list(csv.DictReader(file))
                self._holdings = reader
                
                return self._holdings
        except FileNotFoundError:
            return False
        

    def buy_stock(self, num, name, balance):        
        """
        Buys a stock and adds it to the self._holdings.
        """
        info = call_api(name)
        info = float(info) * float(num)
        self._stocks = {"name": name, "valuation": info}
        self._holdings.append(self._stocks)
        balance -= float(info)
        if balance < 0:
            sys.exit("\nYou have run out of money")

        return self._holdings, balance

    def sell_stock(self, num, name, stocks, balance):
        """
        Sells a stock and checks if we made profits or loss.
        """
        #checks prevous valuation and current valuation
        info = call_api(name)
        for i in stocks:
            if i["name"] == name:
                self._valuation_before = i["valuation"]
                i["valuation"] = float(info) * float(num)

        #calculates the difference between the previous valuation and current valuation
        # and updates the balance accordingly
        self._difference = float(self._valuation_before) - float(info) * float(num)
        self._diff = 0
        balance = difference(difference=self._difference, balance=balance)    
        update(balance)       
        print(f"{name} was sold at {info}")


def main():
    
    balance = 0
    balance = balance_check()
    portfolio = Portfolio()
    portfolio.check()
    update(balance)

    print(
        f"""
        What do you want to do?
        "Report": Check your report
        "Buy": Buy a stock
        "Sell": Sell a stock
        "Deposit": Deposit money to your account
        "Q": Quit the program
        """
    )

    num = 0
    while num != "Q":
        try:
            num = input("Enter a task: ").capitalize()
            
        except ValueError:
            print("Please enter a valid task")
        match num:
            case "Report":
                balance = balance_check()
                update(balance)
                
            case "Buy":
                balance = balance_check()
                balance = buy(balance)
                update(balance)
                
            case "Sell":
                sell()
            case "Deposit":
                amount = float(input("How much to deposit? "))
                deposit(n = amount, balance=balance)
                print(f"Deposited {amount} to your account")


    update(balance_check())
    print("Goodbye!")

def deposit(n, balance):
    print("===== Deposit money =====")
    balance += float(n)
    update(balance)
    print("=========================")
    return balance
    

def balance_check():
    # checks for the last balance
    balance = 0
    try:
        with open("report.csv", "r") as file:
            reader = list(csv.reader(file))
            try:
                balance = float(reader[-1][2])
            except IndexError:
                print("\nReminder: ")
                print("You have not deposited any money yet")
            return balance
    
    except FileNotFoundError:
        print("You have not deposited any money yet")
        return balance
        


    

def call_api(name):
    try:
        stock = yf.Ticker(name)

        info = float(stock.fast_info["lastPrice"])
        return info

    except KeyError:
        print("Enter a valid stock name")
    except:
        print("Unable to fetch data from the API")


def buy(balance):
    #combines everything 
    # buys a stock and saves into a csv >>save_stock_csv(stock)
    print("===== Buy a stock =====")
    name = input("Which stock to buy? ")
    n = float(input("How many shares you want to buy? "))

    portfolio = Portfolio()

    stock, balance = portfolio.buy_stock(name=name, num=n, balance=balance)
    save_stock_csv(stock)
    print("=========================")
    return balance

    


def sell():
    #combines everything
    # sells a stock and removes it from the csv >>sell_stock_csv(stock)
    print("===== Sell a stock =====")
    name = input("Which stock to sell? ")
    portfolio = Portfolio()
    stocks = portfolio.check()
    n = float(input("how many shares to sell? "))
    portfolio.sell_stock(num=n, name=name, stocks=stocks, balance=balance_check())
    sell_stock_csv(name=name)
    print("=========================")
    return True
    
    
def save_stock_csv(stocks):
    # saves the stocks into a csv file
    with open("holdings.csv", "r") as file:
        reader = list(csv.reader(file))

        # checks if the file is empty or not
    with open("holdings.csv", "a+", newline="") as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=["name", "valuation"])
        if reader == []:
            writer.writeheader()
        # for lines in writer:
        for i in stocks:
            #if i["valuation"] != "valuation":
            writer.writerow(i)
                
            


def sell_stock_csv(name):
    p = Portfolio()
    stocks = p.check()
    for i in stocks:
        if i["name"] == name:
            previous_valuation = i["valuation"]
            break
    # writes every line except the line that contains the stock to be sold
    with (
        open("holdings.csv", "r", newline="") as file):
        # reads the file and stores it in a list
        reader = list(csv.reader(file))
    
    with open("holdings.csv", "w", newline="") as outfile:
        # opens the file in write mode and writes every line except the line that contains the stock to be sold
        writer = csv.writer(outfile)
        for row in reader:
            if name ==row[0]:  
                row[1] = float(row[1]) - float(previous_valuation)
                try:
                    if row[1] >= 0:
                        writer.writerow(row[0], row[1])
                except TypeError:
                    print("You can only sell the number of stocks you bought")
            else:
                # writes the row to the file
                writer.writerow(row)


def update(balance):   
    # calculates the current balance from the holdings.csv file
    print("===== Report =====")
    own = 0
    try:
        with open("holdings.csv", "r") as file:
            reader = list(csv.reader(file))
            for row in reader:
                try:
                    if row[1] != "valuation":
                        #calculates how much you own in total
                        own += float(row[1])
                except IndexError:
                    print("You have not bought any stocks yet")
    except FileNotFoundError:
        _= open("holdings.csv", "w")
        _.close()

    print(f"\nYou own: {own}$")
    print(f"Your Balance is: {balance}$")
    now = datetime.datetime.now()     
    row = []
    row.extend([now, own, balance])
   
    # and checks if the report.csv file exists or not "
    
    if not os.path.exists("report.csv"):
        open("report.csv", 'w').close()  
        
    ## writes the current balance and date, time to the report.csv file
    with open("report.csv", "r+", newline="") as report:
        reader = list(csv.reader(report))
        report = csv.writer(report)
        #checks if the report.csv file is empty or not
        if reader == []:
            report.writerow(["Date", "Total Owned", "Balance"])
            print("You have not bought any stocks yet\n")
        report.writerow(row)
    print("\nreport.csv saved\n")
    print("============================================")
    return True


def difference(difference, balance):  
    if difference> 0:
        balance += difference
    elif difference < 0:
        balance -= abs(difference)
    else:
        balance += 0
    return balance

    
if __name__ == "__main__":
    main()
