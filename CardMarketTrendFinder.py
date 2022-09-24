from string import printable
from pip import List
import requests
from bs4 import BeautifulSoup, SoupStrainer
import sys
import os
from currency_converter import CurrencyConverter

debugMode = True
inputFile = "input.txt"
outputFile = "output.csv"
delimiter = ";"


class Card:
    CSV_HEADER = "name" + delimiter +\
                 "price_trend" + delimiter + \
                 "edition" + delimiter + \
                 "price_from" + delimiter + \
                 "thirty_days_average" + delimiter + \
                 "seven_days_average" + delimiter + \
                 "one_day_average"
    name: str = ""
    price_trend: str = ""
    edition: str = ""
    price_from: str = ""
    thirty_days_average: str = ""
    seven_days_average: str = ""
    one_day_average: str = ""

    def __str__(self):
        return self.name + \
               delimiter + \
               str(self.price_trend) + \
               delimiter + \
               self.edition + \
               delimiter + \
               str(self.price_from) + \
               delimiter + \
               str(self.thirty_days_average) + \
               delimiter + \
               str(self.seven_days_average) + \
               delimiter + \
               str(self.one_day_average)


def print_total_value(cards):
    total_value = 0.0
    for card in cards:
        total_value += card.price_trend
    print("Total: " + str(round(total_value, 2)) + " €")
    # cc = CurrencyConverter()
    # print("or " + str(round(cc.convert(total_value, 'EUR', 'SEK'), 2)) + " SEK")


def print_cards(cards: List[Card]):
    with open(outputFile, "w") as output:
        print(Card.CSV_HEADER)
        output.write(Card.CSV_HEADER + "\n")
        for card in cards:
            printable_result: str = str(card)
            print(printable_result)
            output.write(printable_result + "\n")


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def get_name(soup: BeautifulSoup):
    nh1 = soup.find("h1")
    name = nh1.text.replace(nh1.find_next().text, "")
    return name


def get_price_trend(soup: BeautifulSoup):
    price_trends = soup.find("dt", text="Price Trend")
    dd = price_trends.find_next("dd")
    children = dd.findChildren()
    trend = children[0].text
    return float(trend.replace(" €", "").replace(",", "."))


def scrape_fields(soup):
    card: Card = Card()
    try:
        strings = []
        for field in soup.strings:
            strings.append(field)
            if debugMode:
                print(field)
        for i, field in enumerate(strings):
            if field == 'From':
                card.price_from = strings[i+1]
            if field == '30-days average price':
                card.thirty_days_average = strings[i+1]
            if field == '7-days average price':
                card.seven_days_average = strings[i+1]
            if field == '1-day average price':
                card.one_day_average = strings[i+1]
    except Exception as e:
        print(e)
    return card


def get_trend(r):
    soup = BeautifulSoup(r.text, "html.parser", parse_only=SoupStrainer(['h1', 'dt', 'dd']))
    # print(str(soup.text))
    card = scrape_fields(soup)
    card.name = get_name(soup)
    card.price_trend = get_price_trend(soup)
    return card


def search_card(session, search_string, only_exact=1):
    search_string = search_string.replace(" ", "+")

    if only_exact:
        url = 'https://www.cardmarket.com/en/Magic/Products/Search?searchString=%5B' + search_string.strip("\n") + '%5D'
    else:
        url = 'https://www.cardmarket.com/en/Magic/Products/Search?searchString=' + search_string.strip("\n")
    if debugMode:
        print("Requesting url: " + url)
    r = session.get(url)
    soup = BeautifulSoup(r.content, 'html.parser', parse_only=SoupStrainer(class_="col-12 col-md-8 px-2 flex-column"))

    body = soup.find("div", class_="table-body")
    if "/Search?" in r.url:
        try:
            return get_trend(session.get('https://www.cardmarket.com' + soup.find("a", class_=None)['href']))
        except:
            if only_exact:
                return search_card(session, search_string, 0)
            else:
                print("Failed to find " + search_string)
                return 0

    else:
        return get_trend(r)


def search_cards(input_strings: []):
    session = requests.Session()
    cards = []
    for line in input_strings:
        if is_number(line[0]):
            card = search_card(session, line.replace(line[0], ""))
            card.price_trend = card.price_trend * int(line[0])
        else:
            card = search_card(session, line)
        cards.append(card)
    return cards


def main():
    try:
        with open(inputFile, "r+") as file:
            input_strings = file.readlines()
    except:
        print("File cannot be opened: " + inputFile)
    try:
        # for testing with no input
        # input_strings = ["sdsadsdas"]

        cards = search_cards(input_strings)
        print_cards(cards)
        print_total_value(cards)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(str(exc_type) + " at line " + str(exc_tb.tb_lineno) + ": " + str(e))


main()
