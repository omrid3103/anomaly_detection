import datetime
import numpy as np
import math
from datetime import datetime
import pandas as pd


# we will receive a list that contains the following criteria, and analyzes the inserted data accordingly:
#     time of transaction - the time will be divided into 4 different groups:
#           12:01AM-3AM (0), 3:01AM-6AM (1), 06:01AM-9AM (2), 9:01AM-12PM (3),
#           12:01PM-3PM (4), 3:01PM-6PM (5), 6:01PM-9PM (7), 9:01PM-12AM (7)
#     location of transaction - every time a new location is introduced, it will be given a number
#     amount of money - will be represented by a float-typed number
#     Was a card shown during the purchase


date = ["18/05 00:38", "25/01 06:30", "07/04 08:15", "18/04 17:02", "28/07 17:18", "15/08 19:53", "04/10 22:22"]
location = ["yellow", "school", "yellow", "cinema-city", "nike", "rami-levi", "bit"]
amount = [13.9, 10, 11.9, 65, 289.9, 24.2, 20]
was_card_shown = ['Yes', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'No']
df_dict = {'date': date, 'location': location, 'amount': amount, 'was_card_shown': was_card_shown}


LOCATIONS: dict[str, float] = {}
DATA_TABLE: pd.DataFrame = pd.DataFrame(df_dict)



class KMeansRow:
    def __init__(self, date_str: str, transac_location: str, amount: float, was_card_shown: str):
        self.date_str: str = date_str
        self.transac_location: str = transac_location
        self.locations: dict[str, float] = LOCATIONS
        self.amount: float = amount
        self.was_card_shown: bool = True
        if was_card_shown == 'Yes':
            self.was_card_shown: bool = True
        else:
            self.was_card_shown: bool = False

    def time_of_transaction(self) -> float:
        datetime_object = datetime.strptime(self.date_str, '%d/%m %H:%M')
        datetime_object = datetime_object.strftime('%H:%M')
        datetime_object = datetime.strptime(datetime_object, '%H:%M')
        group_0 = datetime.strptime('00:00', '%H:%M')
        group_1 = datetime.strptime('03:00', '%H:%M')
        group_2 = datetime.strptime('06:00', '%H:%M')
        group_3 = datetime.strptime('09:00', '%H:%M')
        group_4 = datetime.strptime('12:00', '%H:%M')
        group_5 = datetime.strptime('15:00', '%H:%M')
        group_6 = datetime.strptime('18:00', '%H:%M')
        group_7 = datetime.strptime('21:00', '%H:%M')
        if datetime_object < group_1:
            return 0.0
        if datetime_object < group_2:
            return 1.0
        if datetime_object < group_3:
            return 2.0
        if datetime_object < group_4:
            return 3.0
        if datetime_object < group_5:
            return 4.0
        if datetime_object < group_6:
            return 5.0
        if datetime_object < group_7:
            return 6.0
        return 7.0

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


class KMeansTable:
    def __init__(self):
        self.table: pd.DataFrame = DATA_TABLE
        self.features: list[list[float]] = self.define_features()

    def define_features(self) -> list[list[float]]:
        external_list: list[list[float]] = []
        internal_list: list[float] = []
        for i, r in self.table.iterrows():
            print(r)
            row = KMeansRow(r["date"], r["location"], r["amount"], r["was_card_shown"])
            internal_list = [row.time_of_transaction(), row.location(), row.amount, row.show_of_card()]
            external_list.append(internal_list)
        return external_list


class kMeansClustering:
    pass


k_table = KMeansTable()
print(k_table.define_features())