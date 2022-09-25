from typing import List

from card import Card


def csv_header(delimiter: str):
    return "found" + delimiter + \
        "name" + delimiter + \
        "edition" + delimiter + \
        "price_trend" + delimiter + \
        "price_from" + delimiter + \
        "thirty_days_average" + delimiter + \
        "seven_days_average" + delimiter + \
        "one_day_average" + delimiter + \
        "url"


def export_cards_to_csv(output_file: str, csvs: List[str], delimiter: str):
    with open(output_file, "w") as output:
        output.write(csv_header(delimiter=delimiter) + "\n")
        for card in csvs:
            output.write(card + "\n")


def cards_to_csv(cards: List[Card], delimiter: str) -> List[str]:
    csvs: List[str] = []
    for card in cards:
        csvs.append(__card_to_csv__(card, delimiter=delimiter))
    return csvs


def __card_to_csv__(card: Card, delimiter: str):
    return str(card.found) + \
        delimiter + \
        card.name + \
        delimiter + \
        card.edition + \
        delimiter + \
        str(card.price_trend) + \
        delimiter + \
        card.price_from + \
        delimiter + \
        card.thirty_days_average + \
        delimiter + \
        card.seven_days_average + \
        delimiter + \
        card.one_day_average + \
        delimiter + \
        card.url

