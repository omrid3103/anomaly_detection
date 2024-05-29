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
import flet as ft



# =================================================================================
# ***************************   KMeansController   ********************************
# =================================================================================

"""
class KMCController:

    def __init__(self, pdf_path: str = r"..\file_saver\client_data_table0.pdf"):
        self.pdf_path = pdf_path
        self.csv_path: Union[None, str] = r"..\file_saver\output0.csv"
        self.df: Union[None, pd.DataFrame] = None


    def csv_file_name_generator(self, file_name: str):
        directory_path = r"..\file_saver"
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
        print(self.pdf_path)
        # Open the PDF file
        with pdfplumber.open(self.pdf_path) as pdf:
            # Initialize an empty list to store table data
            all_table_data = []

            # Loop over the first two pages
            for page_number in range(len(pdf.pages)):
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
        csv_new_name = rf"..\file_saver\{csv_new_name}"

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

        self.csv_path = csv_new_name


    def csv_to_dataframe(self) -> None:
        df = pd.read_csv(self.csv_path)
        self.df = df
"""


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
# ****************************   CommonChars   ************************************
# =================================================================================


class CommonChars:

    def __init__(self, rows_indexes_list: list[int], file_df: pd.DataFrame):
        self.rows_indexes_list = rows_indexes_list
        print(f"rows_indexes_list: {self.rows_indexes_list}")
        self.file_df = file_df
        data = self.data_extraction()
        self.times: list[str] = data[0]
        self.locations: list[str] = data[1]
        self.transactions: list[float] = data[2]
        self.yes_or_no: list[str] = data[3]


    def data_extraction(self) -> tuple[list[str], list[str], list[float], list[str]]:
        times_list = []
        locations_list = []
        transac_list = []
        bool_list = []
        for i in self.rows_indexes_list:
            row_data = self.file_df.iloc[i]
            times_list.append(row_data["Date"])
            locations_list.append(row_data["Location"])
            transac_list.append(row_data["Transaction"])
            bool_list.append(row_data["Was-Card-Shown"])

        return times_list, locations_list, transac_list, bool_list

    def is_time_common(self):

        def time_of_transaction(time_object: str) -> float:
            datetime_object = datetime.strptime(time_object, '%d/%m-%H:%M')
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

        counter_dict: dict[float, int] = {0.0: 0, 1.0: 0, 2.0: 0, 3.0: 0, 4.0: 0, 5.0: 0, 6.0: 0, 7.0: 0}
        for t in self.times:
            counter_dict[time_of_transaction(t)] += 1
        max_key = max(counter_dict, key=counter_dict.get)
        indexes_of_anomalies: list[int] = []
        if counter_dict[max_key] > int(len(self.times)*0.5):
            for s in self.times:
                if time_of_transaction(s) < counter_dict[max_key] * 0.67 or time_of_transaction(s) > counter_dict[max_key] * 1.33:
                    for i in self.rows_indexes_list:
                        if self.file_df.iloc[i]["Date"] == s:
                            indexes_of_anomalies.append(i)
                if int(time_of_transaction(s)) < 3:
                    for i in self.rows_indexes_list:
                        if self.file_df.iloc[i]["Date"] == s and i not in indexes_of_anomalies:
                            indexes_of_anomalies.append(i)
            if int(max_key) == 0:
                return ft.Text("\tMost Transactions occurred between 12AM and 3AM.", size=15), ft.Text("\tA check of the transactions is recommended due to the unusual time!", size=15, color=ft.colors.RED_300), indexes_of_anomalies
            if int(max_key) == 1:
                return ft.Text("\tMost Transactions occurred between 3AM and 6AM.", size=15), ft.Text("\tA check of the transactions is recommended due to the very unusual time!", size=15, color=ft.colors.RED_500), indexes_of_anomalies
            if int(max_key) == 2:
                return ft.Text("\tMost Transactions occurred between 6AM and 9AM.", size=15), ft.Text("\tA check of some of the transactions is recommended due to the unusual times.", size=15, color=ft.colors.RED_300), indexes_of_anomalies
            if int(max_key) == 3:
                return ft.Text("\tMost Transactions occurred between 9AM and 12PM.", size=15), ft.Text("\tMost transactions times look normal.", size=15, color=ft.colors.GREEN_400), indexes_of_anomalies
            if int(max_key) == 4:
                return ft.Text("\tMost Transactions occurred between 12PM and 3PM.", size=15), ft.Text("\tMost transactions times look normal.", size=15, color=ft.colors.GREEN_400), indexes_of_anomalies
            if int(max_key) == 5:
                return ft.Text("\tMost Transactions occurred between 3PM and 6PM.", size=15), ft.Text("\tMost transactions times look normal.", size=15, color=ft.colors.GREEN_400), indexes_of_anomalies
            if int(max_key) == 6:
                return ft.Text("\tMost Transactions occurred between 6PM and 9PM.", size=15), ft.Text("\tMost transactions times look normal.", size=15, color=ft.colors.GREEN_400), indexes_of_anomalies
            if int(max_key) == 7:
                return ft.Text("\tMost Transactions occurred between 9PM and 12AM.", size=15), ft.Text("\tA check of the transactions is recommended due to the very unusual time!", size=15, color=ft.colors.RED_500), indexes_of_anomalies
        else:
            for s in self.times:
                if int(time_of_transaction(s)) < 3:
                    for i in self.rows_indexes_list:
                        if self.file_df.iloc[i]["Date"] == s:
                            indexes_of_anomalies.append(i)
            return ft.Text("\tThe transactions in this group appear to have been made in different hours."), ft.Text("\tA check of transactions that were made in abnormal hours is recommended.", size=15, color=ft.colors.BLUE_400), indexes_of_anomalies

    def transactions_avg_size(self):
        avg: float = 0.0
        for s in self.transactions:
            avg += s
        avg /= len(self.transactions)
        indexes_of_anomalies: list[int] = []
        if avg < 250.0:
            for s in self.transactions:
                if (s > avg and s - avg > 50.0) or (s < avg and avg - s > 50.0):
                    for i in self.rows_indexes_list:
                        if self.file_df.iloc[i]["Transaction"] == s:
                            indexes_of_anomalies.append(i)
            return ft.Text(f"\tThe average transaction size is {avg}.", size=15), ft.Text("\tMost of the transactions' sizes do not stand out", size=15, color=ft.colors.GREEN_400), indexes_of_anomalies
        elif 250.0 < avg < 400.0:
            for s in self.transactions:
                if (s > avg and s - avg > 75.0) or (s < avg and avg - s > 75.0):
                    for i in self.rows_indexes_list:
                        if self.file_df.iloc[i]["Transaction"] == s:
                            indexes_of_anomalies.append(i)
            return ft.Text(f"\tThe average transaction size is {avg}.", size=15), ft.Text("\tMost of the transactions' sizes do not stand out", size=15, color=ft.colors.GREEN_400), indexes_of_anomalies
        elif avg > 550.0:
            for s in self.transactions:
                if (s > avg and s - avg > 150.0) or (s < avg and avg - s > 150.0):
                    for i in self.rows_indexes_list:
                        if self.file_df.iloc[i]["Transaction"] == s:
                            indexes_of_anomalies.append(i)
            return ft.Text(f"\tThe average transaction size is {avg}.", size=15), ft.Text("\tA check of the transactions is recommended due to the amount of money that was spent!", size=15, color=ft.colors.RED_300), indexes_of_anomalies

    def binary_common(self):
        yes_counter = 0
        no_counter = 0
        for b in self.yes_or_no:
            if b == "Yes":
                yes_counter += 1
            else:
                no_counter += 1
        indexes_of_anomalies: list[int] = []
        if yes_counter > no_counter:
            for s in self.yes_or_no:
                if s != "Yes":
                    for i in self.rows_indexes_list:
                        if self.file_df.iloc[i]["Was-Card-Shown"] == s:
                            indexes_of_anomalies.append(i)
            return ft.Text("\tA card was shown in most of the transactions.", size=15), indexes_of_anomalies
        if yes_counter < no_counter:
            for s in self.yes_or_no:
                if s != "No":
                    for i in self.rows_indexes_list:
                        if self.file_df.iloc[i]["Was-Card-Shown"] == s:
                            indexes_of_anomalies.append(i)
            return ft.Text("\tA card was not shown in most of the transactions.", size=15), indexes_of_anomalies
        if yes_counter == no_counter:
            return ft.Text("\tA card was shown in half of the transactions, and was not shown in the other half.", size=15), indexes_of_anomalies

    def alert_dialog_update(self):
        common_actions_results = [self.is_time_common(), self.transactions_avg_size(), self.binary_common()]
        print(f"common_actions_results: {common_actions_results}")
        information_messages: list[ft.Text] = [common_actions_results[0][0], common_actions_results[1][0], common_actions_results[2][0]]
        alert_messages: list[ft.Text] = [common_actions_results[0][1], common_actions_results[1][1]]
        anomalies_indexes: list[list[int]] = [common_actions_results[0][2], common_actions_results[1][2], common_actions_results[2][1]]

        def index_in_group(index_to_check: int, all_indexes_list):
            for index, i in enumerate(all_indexes_list):
                if index_to_check == i:
                    return index

        def is_anomaly(anomalies_indexes_list: list[list[int]]):
            anomalies_for_sure: list[int] = []
            potential_anomalies: list[int] = []
            for i in anomalies_indexes_list[0]:
                if i in anomalies_indexes_list[1] and i in anomalies_indexes_list[2]:
                    anomalies_for_sure.append(i)
                elif i in anomalies_indexes_list[1] or i in anomalies_indexes_list[2]:
                    potential_anomalies.append(i)
            for i in anomalies_indexes_list[1]:
                if i is not anomalies_indexes_list[0] and i in anomalies_indexes_list[2]:
                    potential_anomalies.append(i)
            for pointer, i in enumerate(anomalies_for_sure):
                anomalies_for_sure[pointer] = index_in_group(i, self.rows_indexes_list) + 1
            for pointer, i in enumerate(potential_anomalies):
                if index_in_group(i, self.rows_indexes_list) + 1 not in anomalies_for_sure:
                    potential_anomalies[pointer] = index_in_group(i, self.rows_indexes_list) + 1
            print(f"anomalies_for_sure: {anomalies_for_sure}\npotential_anomalies: {potential_anomalies}")
            return anomalies_for_sure, potential_anomalies




        time_row_title = ft.Row(controls=[ft.Text("Date Affiliations:", size=20, weight=ft.FontWeight.BOLD)])
        time_row_info = ft.Row([information_messages[0]])
        time_row_alert = ft.Row([alert_messages[0]])
        transaction_row_title = ft.Row(controls=[ft.Text("Transactions Affiliations:", size=20, weight=ft.FontWeight.BOLD)])
        transaction_row_info = ft.Row([information_messages[1]])
        transaction_row_alert = ft.Row([alert_messages[1]])
        card_showing_row_title = ft.Row(controls=[ft.Text("Card Appearance Affiliations:", size=20, weight=ft.FontWeight.BOLD)])
        card_showing_row_info = ft.Row([information_messages[2]])
        is_anomaly_info = is_anomaly(anomalies_indexes)
        print(f"is_anomaly_info: {is_anomaly_info}")
        anomalies_row_title = ft.Row([ft.Text("Potential anomalies:", size=20,weight=ft.FontWeight.BOLD)])
        controls_list_for_sure = []
        controls_list_maybe = []
        if is_anomaly_info[0] != [] and is_anomaly_info[1] != []:
            controls_list_for_sure = [ft.Text(f"Most likely anomalies transactions in this group are transactions in the place of: {is_anomaly_info[0]}\n", color=ft.colors.RED_600, size=17)]
            controls_list_maybe = [ft.Text(f"Less likely but potentially anomalies transactions in this group are transactions in the place of: {is_anomaly_info[1]}", color=ft.colors.RED_300, size=17)]
        elif is_anomaly_info[0] == [] and is_anomaly_info[1] != []:
            controls_list_for_sure = [ft.Text("There are no transactions that are definitely anomalies.", color=ft.colors.BLUE_400, size=17)]
            controls_list_maybe = [ft.Text(f"Less likely but potentially anomalies transactions in this group are transactions in the place of: {is_anomaly_info[1]}", color=ft.colors.RED_300, size=17)]
        elif is_anomaly_info[0] != [] and is_anomaly_info[1] == []:
            controls_list_for_sure = [ft.Text(f"Most likely anomalies transactions in this group are transactions in the place of: {is_anomaly_info[0]}", color=ft.colors.RED_600, size=17)]
            controls_list_maybe = [ft.Text("There are not any more transactions that seem suspicious.", color=ft.colors.BLUE_300, size=17)]
        elif is_anomaly_info[0] == [] and is_anomaly_info[1] == []:
            controls_list_for_sure = [ft.Text(f"No potential anomalies detected!", color=ft.colors.GREEN_400, size=17)]
        if len(self.rows_indexes_list) < 5:
            controls_list_for_sure = [ft.Text(f"Most likely anomalies transactions in this group are transactions in the place of: {self.rows_indexes_list}", color=ft.colors.RED_600, size=17)]
            controls_list_maybe = [ft.Text("There are not any more transactions that seem suspicious.", color=ft.colors.BLUE_300, size=17)]
        anomalies_row_for_sure = ft.Row(controls=controls_list_for_sure)
        anomalies_row_maybe = ft.Row(controls=controls_list_maybe)
        alert_column = ft.Column(controls=[
            time_row_title,
            time_row_info,
            time_row_alert,
            transaction_row_title,
            transaction_row_info,
            transaction_row_alert,
            card_showing_row_title,
            card_showing_row_info,
            anomalies_row_title,
            anomalies_row_for_sure,
            anomalies_row_maybe
        ]
        )
        return alert_column


# =================================================================================
# ****************************   mainRunning   ************************************
# =================================================================================


def kmc_controller_main(file_df: pd.DataFrame) -> np.ndarray:

    # controller = KMCController(pdf_file_path)
    # controller.pdf_to_csv()
    # controller.csv_to_dataframe()
    # print(controller.df)
    # print(controller.csv_path)
    k_table = KMeansTable(file_df)
    table_arr = k_table.define_features()
    # for i, r in enumerate(table_arr):
    #     print(i, r)
    return table_arr


if __name__ == "__main__":
    print(kmc_controller_main())
