import requests
from bs4 import BeautifulSoup, SoupStrainer
import sys
import os
from currency_converter import CurrencyConverter

try:
    cc = CurrencyConverter()

    session = requests.Session()

    def search_card(search_string):

        search_string = search_string.replace(" ", "+")

        url = 'https://www.cardmarket.com/en/Magic/Products/Search?searchString=%5B' + search_string + '%5D'
        r = session.get(url)
        soup = BeautifulSoup(r.content, 'html.parser', parse_only=SoupStrainer(class_="col-12 col-md-8 px-2 flex-column"))

        body = soup.find("div", class_="table-body")
        if "/Search?" in r.url:
            return get_trend(session.get('https://www.cardmarket.com' + soup.find("a", class_=None)['href']))
        else:
            return get_trend(r)

    def get_trend(r):
        soup = BeautifulSoup(r.text, "html.parser", parse_only=SoupStrainer(['h1', 'dt', 'dd']))
        nh1 = soup.find("h1")

        name = nh1.text.replace(nh1.find_next().text, "")
        trend = soup.find("dt", text="Price Trend").find_next("dd").findChildren()[0].text

        print(name + ": " + trend)
        return float(trend.replace(" €", "").replace(",", "."))

    def is_number(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    input_strings = open("input.txt", "r+").readlines()

    total_value = 0.0
    for line in input_strings:
        if is_number(line[0]):
            price = search_card(line.replace(line[0], ""))
            total_value += price * int(line[0])
            print("x"+line[0])
        else:
            price = search_card(line)
            total_value += price

    print("Total: " + str(round(total_value, 2)) + " €")
    print("or " + str(round(cc.convert(total_value, 'EUR', 'SEK'), 2)) + " SEK")
    input("Press any key to exit")

except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(str(exc_type) + " at line " + str(exc_tb.tb_lineno) + ": " + str(e))
