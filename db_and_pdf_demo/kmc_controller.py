# from kmc_files import kmeans_clustering
from typing import Union
import pdfplumber
import csv
import pandas as pd
import os
import datetime
import numpy as np
import math
from datetime import datetime, timedelta
import random



# =================================================================================
# ***************************   KMeansController   ********************************
# =================================================================================


class KMCController:

    def __init__(self, pdf_path: str = r"C:\Users\Sharon's PC\PycharmProjects\anomaly_detection\db_and_pdf_demo\client_data_table0.pdf"):
        self.pdf_path = pdf_path
        self.csv_path: Union[None, str] = r"C:\Users\Sharon's PC\PycharmProjects\anomaly_detection\db_and_pdf_demo\output0.csv"
        self.df: Union[None, pd.DataFrame] = None


    def csv_file_name_generator(self, file_name: str):
        directory_path = r"C:\Users\Sharon's PC\PycharmProjects\anomaly_detection\db_and_pdf_demo"
        files = os.listdir(directory_path)
        flag = False
        while not flag:
            if file_name in files:
                file_extension = file_name.split('.')[1]
                file_index = str(int(file_name.split('.')[0][-1]) + 1)
                file_name = f"{file_name.split('.')[0][:-1]}{file_index}.{file_extension}"
            else:
                flag = True
        return file_name


    def pdf_to_csv(self) -> None:
        # Open the PDF file
        with pdfplumber.open(self.pdf_path) as pdf:
            # Initialize an empty list to store table data
            all_table_data = []

            # Loop over the first two pages
            for page_number in range(2):
                # Extract text from the current page
                page = pdf.pages[page_number]
                text = page.extract_text()

                # Split the text into lines
                lines = text.split('\n')

                # Identify the start and end indices of the table
                start_index = end_index = None
                for i, line in enumerate(lines):
                    if "header_row" in line.lower():  # Assuming some keyword identifying the header row
                        start_index = i + 1
                    elif start_index is not None and not line.strip():  # Empty line signifies end of table
                        end_index = i
                        break

                # Extract the table data for the current page
                table_data = []
                for line in lines[start_index:end_index]:
                    # Use a smarter way to split line into columns
                    columns = [col.strip() for col in line.split(' ') if col.strip()]
                    table_data.append(columns)

                # Append the table data to the list
                all_table_data.extend(table_data)

        # Write the combined table data to a CSV file

        csv_new_name = 'output0.csv'
        csv_new_name = self.csv_file_name_generator(csv_new_name)

        with open(csv_new_name, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(all_table_data)

        # Write the combined table data to a CSV file
        with open(csv_new_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(all_table_data)

        # Write the combined table data to a CSV file
        with open(csv_new_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(all_table_data)

        self.csv_path = rf"C:\Users\Sharon's PC\PycharmProjects\anomaly_detection\db_and_pdf_demo\{csv_new_name}"


    def csv_to_dataframe(self) -> None:
        df = pd.read_csv(self.csv_path)
        self.df = df



# =================================================================================
# ******************************   KMeansRow   ************************************
# =================================================================================


"""we will receive a list that contains the following criteria, and analyzes the inserted data accordingly:
    time of transaction - the time will be divided into 4 different groups:
          12:01AM-3AM (0), 3:01AM-6AM (1), 06:01AM-9AM (2), 9:01AM-12PM (3),
          12:01PM-3PM (4), 3:01PM-6PM (5), 6:01PM-9PM (7), 9:01PM-12AM (7)
    location of transaction - every time a new location is introduced, it will be given a number
    amount of money - will be represented by a float-typed number
    Was a card shown during the purchase"""


class KMeansRow:
    def __init__(self, date_str: str, transac_location: str, amount: float, was_card_shown: str, locations_dict: dict):
        self.date_str: str = date_str
        self.transac_location: str = transac_location
        self.locations: dict[str, float] = locations_dict
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


# =================================================================================
# ****************************   KMeansTable   ************************************
# =================================================================================


class KMeansTable:

    def __init__(self, data_table: pd.DataFrame):
        self.table: pd.DataFrame = data_table
        self.locations_dict = {}
        self.features: np.ndarray = self.define_features()

    def define_features(self) -> np.ndarray:
        external_list: list[list[float]] = []
        internal_list: list[float] = []
        rows_array = np.zeros([len(self.table), 4])
        for i, r in self.table.iterrows():
            row = KMeansRow(r["Date"], r["Location"], r["Transaction"], r["Was-Card-Shown"], self.locations_dict)
            self.locations_dict = row.locations
            internal_list = [row.time_of_transaction(), row.location(), row.amount, row.show_of_card()]
            row_arr = np.array(internal_list)
            rows_array[i, :] = row_arr
        return rows_array


# =================================================================================
# ****************************   mainRunning   ************************************
# =================================================================================


def kmc_controller_main(pdf_file_path: str = r"C:\Users\Sharon's PC\PycharmProjects\anomaly_detection\db_and_pdf_demo\client_data_table0.pdf"):

    controller = KMCController(pdf_file_path)
    # controller.pdf_to_csv()
    # print(controller.df)
    print(controller.csv_path)
    k_table = KMeansTable(controller.df)
    table_arr = k_table.define_features()
    # for i, r in enumerate(table_arr):
    #     print(i, r)
    return table_arr


if __name__ == "__main__":
    kmc_controller_main()
