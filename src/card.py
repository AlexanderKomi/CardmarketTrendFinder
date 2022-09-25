class Card:
    found: bool = False
    name: str = ""
    edition: str = ""
    price_trend: float = 0
    price_from: str = ""
    thirty_days_average: str = ""
    seven_days_average: str = ""
    one_day_average: str = ""

    def __str__(self):
        return self.name
