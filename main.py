import os
import upbit
import json
import requests
import pyupbit

#Currency class: contains information of specific currency
class Currency():

    def __init__(self, currency, balance, locked, avg_buy_price, avg_buy_price_modified, unit_currency):
        self.currency = currency
        self.balance = float(balance)
        self.locked = float(locked)
        self.avg_buy_price = float(avg_buy_price)
        self.avg_buy_price_modified = float(avg_buy_price_modified)
        self.unit_currency = unit_currency
        self.isKRW = self.currency == "KRW"
        if not self.isKRW:
            self.current_price = float(pyupbit.get_current_price(self.unit_currency + "-" + self.currency))
            self.total = self.balance * self.current_price


    #print currency name
    def printCurrency(self):
        print("Currency: ", self.currency)

    #print balance
    def printBalance(self):

        if self.isKRW:
            print("Balance is: ", format(round(self.balance), ',') + " " + self.currency)
        else:
            print("Balance is: ", format(round(self.balance, 1), ',') + " " + self.currency +
                  " (" + format(round(self.balance * self.current_price), ',') + " " + self.unit_currency + ")")

    #print locked amount
    def printLockedAmount(self):
        if self.locked == 0:
            print("No Locked Amount")
            return
        print("Locked Amount: ", format(round(self.locked), ','))

    #print average price I bought
    def printAvgBuyPrice(self):
        print("Average price you bought is: ", format(round(self.avg_buy_price), ',') + " " + self.unit_currency)

    #print if average price is modified
    def isAvgBuyPriceModified(self):
        if self.avg_buy_price_modified:
            print("It is modified!")
            return
        print("It is NOT modified.")

    #print unit currency
    def printUnitCurrency(self):
        print("Unit Currency is: ", self.unit_currency)

    #print all the values
    def printAll(self):
        self.printCurrency()
        self.printBalance()
        if not self.isKRW:
            self.printAvgBuyPrice()
            self.isAvgBuyPriceModified()
            self.printUnitCurrency()
            self.printLockedAmount()

#print total money I own in upbit account
def printTotalAsset(l):
    tmp = l[0].balance
    for item in l:
        if not item.isKRW:
            tmp += item.total
    print("\nTotal")
    print("~~~~~~")
    print(round(tmp), l[0].currency)

def main():
    print("******************************************")
    print("              Tom's Coin App              ")
    print("******************************************\n")

    print("LOG IN")
    access_key = input("Type Upbit OpenAPI Access Key: ")
    secret_key = input("Type Upbit OpenAPI Secret Key: ")
    print("==========================================\n")
    inp = input(
        "What would you like to do? \n1: Check balance\n2: Check market price(graph)\nq: quit\nType here ==> ")

    while inp != "q":

        # check balance
        if inp == "1":
            print("\n*************BALANCE*************")
            # contains all information of the currencies I have
            up_bal = upbit.balance(access_key, secret_key)

            # create class for each currency, then add each one to a list
            l = []
            for item in up_bal:
                tmp = Currency(item['currency'], item['balance'], item['locked'], item['avg_buy_price'],
                               item['avg_buy_price_modified'], item['unit_currency'])
                l.append(tmp)

            # print them all
            for item in l:
                item.printAll()
                print("----------------------------------")

            # print total money I own
            printTotalAsset(l)

        # see specific coins' market price graph
        elif inp == "2":
            graph_count = int(input("How many coin's price graph would you like to see?: "))
            min_ = input("Type time range(min): ")

            # make a list of all the coins name user want to check
            coin_list = []
            for i in range(graph_count):
                tmp = input("Type coin name: ")
                coin_list.append(tmp)

            df = upbit.coin_price(coin_list, min_)
            upbit.price_plt(df)

        # otherwise, quit
        else:
            return

        #check if user is going to continue
        cont = input("\nWould you like to continue? [Y/N]")
        if cont == "y" or cont == '':
            inp = input(
                "\nWhat would you like to do? \n1: Check balance\n2: Check market price(graph)\nother: quit\nType here ==> ")
        else:
            break

if __name__ == "__main__":
	main()