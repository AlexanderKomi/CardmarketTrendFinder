from string import printable
from pip import List
import requests
from bs4 import BeautifulSoup, SoupStrainer
import sys
import os
from currency_converter import CurrencyConverter

class Card:
    name: str
    price: float

def printTotalValue(cards):
    cc = CurrencyConverter()
    total_value = 0.0
    for card in cards:
        total_value += card.price
    print("Total: " + str(round(total_value, 2)) + " €")
    # print("or " + str(round(cc.convert(total_value, 'EUR', 'SEK'), 2)) + " SEK")

def printCards(cards: List[Card]): 
    delimiter = ";"
    with open("output.csv", "w") as output:
        output.write("name"+delimiter+"price\n")
        for card in cards:
            printableResult: str = card.name + delimiter + str(card.price) + "\n"
            print(printableResult)
            output.write(printableResult)


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_trend(r):
    soup = BeautifulSoup(r.text, "html.parser", parse_only=SoupStrainer(['h1', 'dt', 'dd']))
    nh1 = soup.find("h1")
    name = nh1.text.replace(nh1.find_next().text, "")
    trend = soup.find("dt", text="Price Trend").find_next("dd").findChildren()[0].text
    card = Card()
    card.name = name
    card.price = float(trend.replace(" €", "").replace(",", "."))
    return card

def search_card(session, search_string, only_exact = 1):
    search_string = search_string.replace(" ", "+")

    if (only_exact):
        url = 'https://www.cardmarket.com/en/Magic/Products/Search?searchString=%5B' + search_string.strip("\n") + '%5D'
    else:
        url = 'https://www.cardmarket.com/en/Magic/Products/Search?searchString=' + search_string.strip("\n")

    r = session.get(url)
    soup = BeautifulSoup(r.content, 'html.parser', parse_only=SoupStrainer(class_="col-12 col-md-8 px-2 flex-column"))

    body = soup.find("div", class_="table-body")
    if "/Search?" in r.url:
        try:
            return get_trend(session.get('https://www.cardmarket.com' + soup.find("a", class_=None)['href']))
        except:
            if (only_exact):
                return search_card(session, search_string, 0)
            else:
                print("Failed to find " + search_string)
                return 0

    else:
        return get_trend(r)

def main():
    try:
        file=open("input.txt", "r+")
        input_strings = file.readlines()
        file.close()
        #for testing with no input
        #input_strings = ["sdsadsdas"]

        session = requests.Session()
        
        cards = []

        for line in input_strings:
            if is_number(line[0]):
                card = search_card(session, line.replace(line[0], ""))
                card.price = card.price * int(line[0])
            else:
                card = search_card(session, line)
            cards.append(card)

        printCards(cards)
        printTotalValue(cards)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(str(exc_type) + " at line " + str(exc_tb.tb_lineno) + ": " + str(e))


main()
