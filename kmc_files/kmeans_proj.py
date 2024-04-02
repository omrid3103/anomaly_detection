import datetime
import numpy as np
import math
from datetime import datetime, timedelta
import random
import pandas as pd
from db_and_pdf_demo.pdf_to_pandas import csv_to_dataframe, CSV_FILE_PATH


#

def random_date_generator() -> str:
    start_date = datetime.now().replace(month=3, day=1)
    end_date = start_date + timedelta(days=30)
    random_date = start_date + (end_date - start_date) * random.random()
    formatted_random_date = random_date.strftime('%d/%m %H:%M')
    return formatted_random_date


random_locations = ["Yellow", "School", "Home", "Cinema-City", "Nike", "Adidas", "Pull and Bear", "Web", "Train", "Beach", "Airport", "Bit"]
yes_or_no = ["Yes", "No"]

# we will receive a list that contains the following criteria, and analyzes the inserted data accordingly:
#     time of transaction - the time will be divided into 4 different groups:
#           12:01AM-3AM (0), 3:01AM-6AM (1), 06:01AM-9AM (2), 9:01AM-12PM (3),
#           12:01PM-3PM (4), 3:01PM-6PM (5), 6:01PM-9PM (7), 9:01PM-12AM (7)
#     location of transaction - every time a new location is introduced, it will be given a number
#     amount of money - will be represented by a float-typed number
#     Was a card shown during the purchase


date = [random_date_generator() for _ in range(149)]
location = [random.choice(random_locations) for _ in range(149)]
amount = [round(random.uniform(0.5, 201), 1) for _ in range(149)]
was_card_shown = [random.choice(yes_or_no) for _ in range(149)]
df_dict = {'date': date, 'location': location, 'amount': amount, 'was_card_shown': was_card_shown}

DATA_TABLE: pd.DataFrame = csv_to_dataframe(CSV_FILE_PATH)
LOCATIONS = {}



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
        datetime_object = datetime.strptime(self.date_str, '%d/%m-%H:%M')
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
        self.features: np.ndarray = self.define_features()

    def define_features(self) -> np.ndarray:
        external_list: list[list[float]] = []
        internal_list: list[float] = []
        rows_array = np.zeros([len(self.table), 4])
        for i, r in self.table.iterrows():
            # print(r)
            row = KMeansRow(r["Date"], r["Location"], r["Transaction"], r["Was-Card-Shown"])
            internal_list = [row.time_of_transaction(), row.location(), row.amount, row.show_of_card()]
            row_arr = np.array(internal_list)
            rows_array[i, :] = row_arr
        return rows_array




def kmeans_proj_main():
    # print(DATA_TABLE)
    k_table = KMeansTable()
    table_arr = k_table.define_features()
    # for i, r in enumerate(table_arr):
    #     print(i, r)
    # print(type(table_arr))
    return table_arr


if __name__ == "__main__":
    kmeans_proj_main()
