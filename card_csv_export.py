from typing import List

from card import Card

delimiter: str = ";"

CSV_HEADER: str = "name" + delimiter + \
             "edition" + delimiter + \
             "price_trend" + delimiter + \
             "price_from" + delimiter + \
             "thirty_days_average" + delimiter + \
             "seven_days_average" + delimiter + \
             "one_day_average"


def export_cards_to_csv(output_file: str, csvs: List[str]):
    with open(output_file, "w") as output:
        output.write(CSV_HEADER + "\n")
        for card in csvs:
            output.write(card + "\n")


def cards_to_csv(cards: List[Card]) -> List[str]:
    csvs: List[str] = []
    for card in cards:
        csvs.append(__card_to_csv__(card))
    return csvs


def __card_to_csv__(card: Card):
    return card.name + \
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
           card.one_day_average
