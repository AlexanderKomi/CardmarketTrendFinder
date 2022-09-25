from typing import List

from bs4 import BeautifulSoup, SoupStrainer
import requests

import sys
import os

from card import Card


def __get_name__(soup: BeautifulSoup) -> str:
    nh1 = soup.find("h1")
    name = nh1.text.replace(nh1.find_next().text, "")
    return name


def __trim_euro_symbol__(price) -> float:
    return float(price.replace(" €", "").replace(",", "."))


def __get_price_trend__(soup: BeautifulSoup) -> float:
    price_trends = soup.find("dt", text="Price Trend")
    dd = price_trends.find_next("dd")
    children = dd.findChildren()
    trend = children[0].text
    return __trim_euro_symbol__(trend)


def __get_printed_in__(soup: BeautifulSoup) -> str:
    price_trends = soup.find("dt", text="Printed in")
    dd = price_trends.find_next("dd")
    children = dd.findChildren()
    trend = children[0].text
    return trend


def __scrape_fields__(soup, debug_mode=False) -> Card:
    card: Card = Card()
    try:
        strings = []
        for field in soup.strings:
            strings.append(field)
            if debug_mode:
                print(field)
        for i, field in enumerate(strings):
            if field == 'From':
                card.price_from = strings[i + 1]
            elif field == '30-days average price':
                card.thirty_days_average = strings[i + 1]
            elif field == '7-days average price':
                card.seven_days_average = strings[i + 1]
            elif field == '1-day average price':
                card.one_day_average = strings[i + 1]
            elif field == 'Printed in':
                card.edition = strings[i + 1]

    except Exception as e:
        print(e)
    return card


def __get_trend__(r, debug_mode=False) -> Card:
    soup = BeautifulSoup(r.text, "html.parser", parse_only=SoupStrainer(['h1', 'dt', 'dd']))
    # print(str(soup.text))
    card = __scrape_fields__(soup)
    card.name = __get_name__(soup)
    card.price_trend = __get_price_trend__(soup)
    card.edition = __get_printed_in__(soup)
    return card


def __search_card__(session, search_string, only_exact=1, debug_mode=False) -> Card:
    search_string = search_string.replace(" ", "+")

    if only_exact:
        url = 'https://www.cardmarket.com/en/Magic/Products/Search?searchString=%5B' + search_string.strip("\n") + '%5D'
    else:
        url = 'https://www.cardmarket.com/en/Magic/Products/Search?searchString=' + search_string.strip("\n")
    if debug_mode:
        print("Requesting url: " + url)
    r = session.get(url)
    soup = BeautifulSoup(r.content, 'html.parser', parse_only=SoupStrainer(class_="col-12 col-md-8 px-2 flex-column"))

    # body = soup.find("div", class_="table-body")
    if "/Search?" in r.url:
        try:
            return __get_trend__(session.get('https://www.cardmarket.com' + soup.find("a", class_=None)['href']),
                                 debug_mode=debug_mode)
        except:
            if only_exact:
                return __search_card__(session, search_string, 0, debug_mode=debug_mode)
            else:
                print("Failed to find " + search_string)
                return 0

    else:
        return __get_trend__(r)


def __search_card_by_line__(session, line: str, debug_mode=False) -> Card:
    def __is_number__(s) -> bool:
        try:
            int(s)
            return True
        except ValueError:
            return False

    # Hack to ignore leading numbers
    if __is_number__(line[0]):
        card = __search_card__(session, line.replace(line[0], ""), debug_mode=debug_mode)
        card.price_trend = card.price_trend * int(line[0])
    else:
        card = __search_card__(session, line, debug_mode=debug_mode)
    return card


def search_cards(input_strings: [], debug_mode=False) -> List[Card]:
    try:
        session = requests.Session()
        cards = []
        for line in input_strings:
            card = __search_card_by_line__(session, line, debug_mode=debug_mode)
            cards.append(card)

        return cards
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(str(exc_type) + " at line " + str(exc_tb.tb_lineno) + ": " + str(e))
