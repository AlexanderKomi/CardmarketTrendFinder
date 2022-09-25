import argparse
from typing import List

from card import Card

from card_csv_export import export_cards_to_csv, cards_to_csv, csv_header
from scrape import search_cards


def read_input_file(input_file: str) -> List[str]:
    with open(input_file, "r+") as file:
        return file.readlines()


def handle_found_cards(cards: List[Card], output_file: str, delimiter: str):
    def print_total_value(cards: List[Card]) -> None:
        total_value = 0.0
        for card in cards:
            total_value += card.price_trend
        print("Total: " + str(round(total_value, 2)) + " €")
        # cc = CurrencyConverter()
        # print("or " + str(round(cc.convert(total_value, 'EUR', 'SEK'), 2)) + " SEK")

    csvs = cards_to_csv(cards, delimiter)
    print(csv_header(delimiter))
    for csv in csvs:
        print(csv)
    export_cards_to_csv(output_file, csvs, delimiter)
    print_total_value(cards)


def main():
    parser = argparse.ArgumentParser(
        description='A simple script, which find the trending cards on '
                    'cardmarket.com and lets you export them to a file.')
    parser.add_argument('-d', '--debug_mode', default=False, type=bool, nargs='?',
                        help='print debug information')
    parser.add_argument('-i', '--input_file', default='input.txt', type=str, nargs='?',
                        help='file with the card names')
    parser.add_argument('-o', '--output_file', default='output.csv', type=str, nargs='?',
                        help='file with the results')
    parser.add_argument('-c', '--csv_delimiter', default=';', type=str, nargs='?',
                        help='delimiter for the csv file')
    args: argparse.Namespace = parser.parse_args()

    debug_mode = args.debug_mode
    input_file = args.input_file
    output_file = args.output_file
    delimiter = args.csv_delimiter

    input_strings = []
    try:
        input_strings = read_input_file(input_file)
    except:
        print("Input file cannot be openend: " + input_file)
    cards: List[Card] = search_cards(input_strings, debug_mode=debug_mode)
    handle_found_cards(cards, output_file, delimiter)


if __name__ == "__main__":
    main()

