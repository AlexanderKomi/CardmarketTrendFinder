from typing import List

from src.card import Card

from src.card_csv_export import export_cards_to_csv, cards_to_csv, CSV_HEADER
from src.scrape import search_cards

# debug_mode = False
debug_mode = True

inputFile = "input.txt"
outputFile = "output.csv"
delimiter = ";"


def read_input_file(input_file: str) -> List[str]:
    with open(input_file, "r+") as file:
        return file.readlines()


def handle_found_cards(cards: List[Card]):
    def print_total_value(cards: List[Card]) -> None:
        total_value = 0.0
        for card in cards:
            total_value += card.price_trend
        print("Total: " + str(round(total_value, 2)) + " €")
        # cc = CurrencyConverter()
        # print("or " + str(round(cc.convert(total_value, 'EUR', 'SEK'), 2)) + " SEK")

    csvs = cards_to_csv(cards)
    print(CSV_HEADER)
    for csv in csvs:
        print(csv)
    export_cards_to_csv(outputFile, csvs)
    print_total_value(cards)


def main():
    input_strings = read_input_file(inputFile)
    cards: List[Card] = search_cards(input_strings, debug_mode=debug_mode)
    handle_found_cards(cards)


if __name__ == "__main__":
    main()

