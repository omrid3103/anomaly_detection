import datetime
import numpy as np
import math
from datetime import datetime


# we will receive a list that contains the following criteria, and analyzes the inserted data accordingly:
#     time of transaction - the time will be divided into 4 different groups: 12:01AM-6AM (0), 6:01AM-12PM (1), 12:01PM-6PM (2), 6:01PM-12AM (3)
#     location of transaction - every time a new location is introduced, it will be given a number
#     amount of money - will be represented by a float-typed number
#     frequency of transaction - (in the given time "jump" between every insertion of the list)
#     Was a card shown during the purchase


class kMeansPiece:
    def __init__(self, date_str: str, transac_location: str, amount: float, was_card_shown: bool):
        self.date_str: str = date_str
        self.transac_location: str = transac_location
        self.locations: dict[str, float] = {}
        # maybe take the dict as a parameter in the init func?
        self.amount: float = amount
        self.was_card_shown: bool = was_card_shown

    def time_of_transaction(self) -> float:
        datetime_object = datetime.strptime(self.date_str, '%H:%M')
        datetime_object = datetime_object.strftime('%H:%M')
        datetime_object = datetime.strptime(datetime_object, '%H:%M')
        group_0 = datetime.strptime('00:00', '%H:%M')
        group_1 = datetime.strptime('06:00', '%H:%M')
        group_2 = datetime.strptime('12:00', '%H:%M')
        group_3 = datetime.strptime('18:00', '%H:%M')
        if datetime_object < group_1:
            return 0.0
        if datetime_object < group_2:
            return 1.0
        if datetime_object < group_3:
            return 2.0
        return 3.0

    def location(self) -> float:
        if self.locations == {}:
            self.locations[self.transac_location] = 0.0
            self.locations["last_num"] = self.locations[self.transac_location]
            return self.locations[self.transac_location]
        if self.transac_location not in self.locations.keys():
            self.locations[self.transac_location] = float(int(self.locations["last_num"]) + 1)
            self.locations["last_num"] = self.locations[self.transac_location]
            return self.locations[self.transac_location]
        return self.locations[self.transac_location]

    def show_of_card(self) -> float:
        """if 0.0 was returned, a card has been shown during the purchase. If 1.0 is returned, a card hasn't been shown."""
        if self.was_card_shown:
            return 0.0
        return 1.0







