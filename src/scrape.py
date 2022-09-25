from concurrent.futures import ThreadPoolExecutor
from typing import List

from bs4 import BeautifulSoup, SoupStrainer
import requests

from card import Card


card_market_base_url = "https://www.cardmarket.com"


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


def __get_trend__(text) -> Card:
    soup = BeautifulSoup(text, "html.parser", parse_only=SoupStrainer(['h1', 'dt', 'dd']))
    # print(str(soup.text))
    card = __scrape_fields__(soup)
    card.found = True
    card.name = __get_name__(soup)
    card.price_trend = __get_price_trend__(soup)
    card.edition = __get_printed_in__(soup)
    return card


def __search_card__(session, search_string, only_exact=1, debug_mode=False) -> Card:
    def get_url(search: str):
        search = search.replace(" ", "+")

        if only_exact:
            url = card_market_base_url + '/en/Magic/Products/Search?searchString=%5B' + search.strip("\n") + '%5D'
        else:
            url = card_market_base_url + '/en/Magic/Products/Search?searchString=' + search.strip("\n")
        if debug_mode:
            print("Requesting url: " + url)
        return session.get(url)

    r = get_url(search_string)
    soup = BeautifulSoup(r.content, 'html.parser', parse_only=SoupStrainer(class_="col-12 col-md-8 px-2 flex-column"))

    # body = soup.find("div", class_="table-body")
    if "/Search?" in r.url:
        try:
            return __get_trend__(session.get(card_market_base_url + soup.find("a", class_=None)['href']).text)
        except:
            if only_exact:
                return __search_card__(session, search_string, 0, debug_mode=debug_mode)
            else:
                print("Failed to find " + search_string)
                card: Card = Card()
                card.name = search_string
                return card
    else:
        return __get_trend__(r.text)


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
    session = requests.Session()
    cards = []

    with ThreadPoolExecutor() as executor:
        futures = []
        for line in input_strings:
            futures.append(executor.submit(__search_card_by_line__, session, line, debug_mode=debug_mode))

        for future in futures:
            card = future.result() # this will block
            cards.append(card)
    return cards
