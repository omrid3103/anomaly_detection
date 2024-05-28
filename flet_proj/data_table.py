from datetime import datetime

import flet as ft
import numpy as np
import json
# from db_and_pdf_demo import kmc_controller
# from db_and_pdf_demo import kmeans_clustering
import pandas as pd
from typing import Union
import requests
import time
from io import StringIO

class DataTable:

    def __init__(self, page: ft.Page, url: str, token, file_df: pd.DataFrame, time_stamp: str = ""):
        self.page = page
        self.request_url = url
        self.token = token
        self.table_time_stamp = time_stamp
        self.file_df = file_df
        print(self.table_time_stamp)
        self.page.scroll = True
        self.alert_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Timeout Error"),
            content=ft.Text("You are connected for too long. You will now be disconnected."),
            actions=[
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.data = requests.get(f"{self.request_url}controller_actions", params={"json_df": self.file_df.to_json(orient='records')}).json()

        self.COLORS: dict[ft.colors, str] = {
                "Yellow": ft.colors.YELLOW_200,
                "Teal": ft.colors.TEAL_50,
                "Blue": ft.colors.BLUE_100,
                "Red": ft.colors.RED_200,
                "Purple": ft.colors.PURPLE_200,
                "Green": ft.colors.GREEN_200,
                "Orange": ft.colors.ORANGE_200,
                "Pink": ft.colors.PINK_200,
                "Cyan": ft.colors.CYAN_50
        }


        # self.points_coordinates = self.data["points_array"].decode()
        self.points_coordinates = json.loads(self.data["points_array"])
        self.points_coordinates = np.array(self.points_coordinates)
        self.grouping_list: list[list[int]] = []

        self.columns_names_list = self.file_df.columns.tolist()
        self.num_rows: int = self.file_df.shape[0]
        self.num_cells_in_each_row: int = len(self.file_df.iloc[0].tolist())
        self.row_colors: list[ft.colors] = []


        # =================================================================================
        # ******************   DropDown Selection & Button   ******************************
        # =================================================================================

        self.dropdown_obj = ft.Dropdown(
            width=170,
            options=self.search_dropdown_options_generation(),
            hint_text="Filter Table",
            on_change=self.dropdown_button_clicked,
            visible=False
        )
        self.data_not_found = ft.Text("Data was not found...", weight="bold", size=20)

        # =================================================================================
        # ************************   Search TextField   ***********************************
        # =================================================================================

        self.search_field = ft.TextField(label="search", width=350, on_change=self.search_field_input_changed, visible=False)
        self.color_dropdown = ft.Dropdown(
            width=150,
            # options=self.colors_dropdown_options_generation(),
            options=[],
            hint_text="Color Cluster",
            on_change=self.color_dropdown_changed,
            visible=False
        )


        # =================================================================================
        # ************************   DataTable Creation   *********************************
        # =================================================================================

        self.data_table = ft.DataTable(
            width=1000,
            bgcolor="grey",
            border=ft.border.all(2, "red"),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, "brown"),
            horizontal_lines=ft.border.BorderSide(1, "red"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.colors.BLACK12,
            heading_row_height=50,
            data_row_color={"hovered": "0x30FF0000"},
            divider_thickness=0,
            column_spacing=150,
            data_row_max_height=45,
            columns=self.table_columns_generation(),
            rows=self.table_rows_generation()
        )
        self.kmc_button = ft.ElevatedButton("kmc the table", on_click=self.kmc_table_definition)

        self.save_table = ft.ElevatedButton("Save table", on_click=self.save_table_in_db, disabled=True)
        self.anomalies_information_button = ft.ElevatedButton("Analyze Transactions", on_click=self.show_anomalies)
        self.common_chars: Union[CommonChars, None] = None


        self.search_row = ft.Row([self.kmc_button, self.dropdown_obj, self.search_field, self.color_dropdown], spacing=80)
        self.save_row = ft.Row([self.save_table])
        self.message_row = ft.Row([self.data_not_found])
        self.table_row = ft.Row([self.data_table])
        self.anomaly_row = ft.Row([self.anomalies_information_button], visible=False)

        self.items = [self.search_row, self.save_row, self.table_row, self.anomaly_row]
        self.column = ft.Column(spacing=20, controls=self.items)
        self.column.scroll = ft.ScrollMode.ALWAYS


    # =================================================================================
    # *******   DataFrame Information Extraction Into Columns & Rows   ****************
    # =================================================================================

    def table_columns_generation(self) -> list[ft.DataColumn]:
        columns_list = []
        for i in range(len(self.columns_names_list)):
            columns_list.append(
                ft.DataColumn(
                    ft.Text(self.columns_names_list[i], text_align=ft.TextAlign.CENTER),
                )
            )
        return columns_list

    def table_rows_generation(self) -> list[ft.DataRow]:
        rows_list: list[ft.DataRow] = []
        cells_list: list[ft.DataCell] = []

        for i in range(self.num_rows):
            row_i_information = self.file_df.iloc[i].tolist()
            for j in range(self.num_cells_in_each_row):
                cells_list.append(
                    ft.DataCell(ft.Text(f"{str(row_i_information[j])}", text_align=ft.TextAlign.CENTER))
                )
            if len(self.row_colors) == 0:
                rows_list.append(
                    ft.DataRow(
                        cells=cells_list,
                        # color=ft.colors.BLUE_300,
                        selected=True,
                        on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    )
                )
            else:
                rows_list.append(
                    ft.DataRow(
                        cells=cells_list,
                        color=self.row_colors[i],
                        selected=True,
                        on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                    )
                )
            cells_list = []
        return rows_list


    # =================================================================================
    # *******************   Dropdown Options & Button  ********************************
    # =================================================================================


    def colors_dropdown_options_generation(self) -> list[ft.dropdown.Option]:
        ft_options_list = []
        for c in self.row_colors:
            if c not in ft_options_list:
                ft_options_list.append(c)
        options_list = []
        for c in self.COLORS.keys():
            if self.COLORS[c] in ft_options_list:
                options_list.append(ft.dropdown.Option(c))
        # for c in self.COLORS.keys():
        #     options_list.append(
        #         ft.dropdown.Option(c)
        #     )
        options_list.append(ft.dropdown.Option("None"))
        return options_list

    def search_dropdown_options_generation(self) -> list[ft.dropdown.Option]:
        options_list = []
        for i in range(len(self.columns_names_list)):
            if isinstance(self.file_df.iloc[0, i], str):
                options_list.append(
                    ft.dropdown.Option(f"{self.columns_names_list[i]}")
                )
        options_list.append(ft.dropdown.Option("Cluster Color"))
        return options_list

    def dropdown_button_clicked(self, e):
        if self.dropdown_obj.value != "Cluster Color":
            for k in range(len(self.columns_names_list)):
                if self.dropdown_obj.value == self.columns_names_list[k]:
                    self.search_field.hint_text = f"Search in the {self.dropdown_obj.value} column..."
            self.search_field.visible = True
            if self.color_dropdown in self.search_row.controls:
                self.color_dropdown.visible = False
                self.color_dropdown.update()
            self.search_field.update()
        else:
            if self.search_field in self.search_row.controls:
                self.search_field.visible = False
                self.search_field.update()
            self.color_dropdown.visible = True
            self.color_dropdown.update()
        self.search_row.update()
        self.page.update()

    def search_field_input_changed(self, e):

        def cells_generation(x_c: dict[str, str]) -> list[ft.DataCell]:
            cells_g = []
            for n in range(self.num_cells_in_each_row):
                cells_g.append(
                    ft.DataCell(ft.Text(f"{str(x_c[self.columns_names_list[n]])}"))
                )
            return cells_g

        def get_filtered_row_index(x_c: dict[str, str]) -> int:
            table_rows_full_data = self.table_rows_generation()
            row_color: Union[None, ft.colors] = None
            for i, r in enumerate(table_rows_full_data):
                if r.cells[0].content.value == x_c[self.columns_names_list[0]] and r.cells[1].content.value == x_c[self.columns_names_list[1]] \
                        and r.cells[2].content.value == x_c[self.columns_names_list[2]]:
                    return i

        search_name = self.search_field.value
        dropdown_value = self.dropdown_obj.value

        my_filtered_df = self.file_df[self.file_df[self.columns_names_list[self.columns_names_list.index(dropdown_value)]].str.contains(search_name)]
        my_filter = my_filtered_df.astype(str).to_dict(orient='records')
        self.data_table.rows = []

        if not self.search_field.value == "":
            if self.message_row in self.items:
                self.items.remove(self.message_row)
            if len(my_filter) > 0:
                for x in my_filter:
                    if len(self.row_colors) == 0:
                        self.data_table.rows.append(
                            ft.DataRow(
                                cells=cells_generation(x)
                            )
                        )
                    else:
                        self.data_table.rows.append(
                            ft.DataRow(
                                cells=cells_generation(x),
                                color=self.row_colors[get_filtered_row_index(x)]
                            )
                        )
            else:
                self.items.remove(self.table_row)
                self.items.append(self.message_row)
                self.items.append(self.table_row)
        else:
            if self.message_row in self.items:
                self.items.remove(self.message_row)
            self.data_table.rows = self.table_rows_generation()

        self.data_table.update()
        self.page.update()


    def color_dropdown_changed(self, e):
        if self.color_dropdown.value != "None":
            flet_row_color: ft.colors = self.COLORS[self.color_dropdown.value]
            rows_to_present: list[ft.DataRow] = []
            indexes_of_rows: list[int] = []
            for i, r in enumerate(self.data_table.rows):
                if r.color == flet_row_color:
                    rows_to_present.append(r)
                    indexes_of_rows.append(i)
            self.common_chars = CommonChars(indexes_of_rows, self.file_df)
            self.data_table.rows = rows_to_present
            if len(rows_to_present) == 0:
                self.items.remove(self.table_row)
                self.anomaly_row.visible = False
                self.anomaly_row.update()
                self.items.append(self.message_row)
                self.items.append(self.table_row)
            else:
                self.anomaly_row.visible = True
                self.anomaly_row.update()
                self.column.update()
        else:
            if self.message_row in self.items:
                self.items.remove(self.message_row)
            self.data_table.rows = self.table_rows_generation()
            self.anomaly_row.visible = False
            self.anomaly_row.update()

        self.data_table.update()
        self.page.update()

    def show_anomalies(self, e):
        if self.common_chars is not None:
            self.alert_dlg.title = ft.Text("Analysis")
            self.alert_dlg.content = self.common_chars.alert_dialog_update()
            self.alert_dlg.actions = [ft.TextButton("Close", on_click=self.close_dlg)]
            self.open_dlg()
        else:
            self.alert_dlg.title = ft.Text("Error")
            self.alert_dlg.content = ft.Text("An error has occurred")
            self.alert_dlg.actions = [ft.TextButton("Close", on_click=self.close_dlg)]

    def kmc_table_definition(self, e) -> None:
        payload = {"points_json": json.dumps(self.points_coordinates.tolist()), "min_clusters_to_check": 4, "max_clusters_to_check": 9}
        returned_dict = requests.get(f"{self.request_url}most_efficient_n_of_clusters", params=payload).json()
        print(returned_dict)
        if returned_dict["success"]:
            most_efficient_number_of_clusters = returned_dict["n_clusters"]
        else:
            most_efficient_number_of_clusters = 4

        returned_dict = requests.get(f"{self.request_url}kmc_server",
                                     params={"points_array": json.dumps(self.points_coordinates.tolist()), "n_clusters": most_efficient_number_of_clusters, "iterations": 35}).json()
        # {"centers_array": centers_array, "grouping_list": grouping_list}
        self.grouping_list: list[list[int]] = json.loads(returned_dict["grouping_list"])
        grouping_list_length = sum(len(sublist) for sublist in self.grouping_list)

        def group_index(g_list: list[list[int]], index_to_check: int) -> int:
            for g_index, g in enumerate(g_list):
                if index_to_check in g:
                    return g_index


        if grouping_list_length == len(self.data_table.rows):
            for i, r in enumerate(self.data_table.rows):
                r.color = list(self.COLORS.values())[group_index(self.grouping_list, i)]
                self.row_colors.append(r.color)
            self.color_dropdown.options = self.colors_dropdown_options_generation()
            self.search_row.controls.remove(self.kmc_button)
            self.save_table.disabled = False
            self.save_table.update()
            self.dropdown_obj.visible = True
            self.data_table.update()
            self.column.update()
            self.page.update()

    def save_table_in_db(self, e):
        payload = {
            "token": self.token,
            "time_stamp": self.table_time_stamp,
            "json_df": self.file_df.to_json(orient='records'),
            "grouping_list": json.dumps(self.grouping_list)
        }
        result = requests.post(f"{self.request_url}save_table", params=payload).json()
        print(result)
        if result["success"]:
            self.alert_dlg.title = ft.Text("Success")
            self.alert_dlg.content = ft.Text("Table has been saved.")
            self.alert_dlg.actions = [ft.TextButton("Close", on_click=self.close_dlg)]
            self.open_dlg()
            self.items.remove(self.save_row)
        else:
            if result["response"] != "Token expired":
                self.alert_dlg.title = ft.Text("Error")
                self.alert_dlg.content = ft.Text("Something went wrong. Try again.")
                self.alert_dlg.actions = [ft.TextButton("Close", on_click=self.close_dlg)]
                self.open_dlg()
            else:
                self.open_dlg()
                time.sleep(4)
                self.page.go("/guest_home")
        self.save_row.update()
        self.column.update()
        self.page.update()
        # def save_table(username: str, password: str, json_df: dict, time_stamp: str):
        # return {"success": False, "response": "Not Matching Password"}


    def open_dlg(self,):
        self.page.dialog = self.alert_dlg
        self.alert_dlg.open = True
        self.page.update()

    def close_dlg(self, e):
        self.alert_dlg.open = False
        self.page.update()


    #🦾🫡🪖

    def main(self) -> None:

        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.add(self.column)



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

        avg: float = 0.0
        for t in self.times:
            avg += time_of_transaction(t)
        avg = avg / len(self.times)
        indexes_of_anomalies: list[int] = []
        for s in self.times:
            if time_of_transaction(s) < avg * 0.67 or time_of_transaction(s) > avg * 1.33:
                for i in self.rows_indexes_list:
                    if self.file_df.iloc[i]["Date"] == s:
                        indexes_of_anomalies.append(i)
        if int(avg) == 0:
            return ft.Text("\tMost Transactions occurred between 12AM and 3AM.", size=15), ft.Text("\tA check of the transactions is recommended due to the unusual time!", size=15, color=ft.colors.RED_300), indexes_of_anomalies
        if int(avg) == 1:
            return ft.Text("\tMost Transactions occurred between 3AM and 6AM.", size=15), ft.Text("\tA check of the transactions is recommended due to the very unusual time!", size=15, color=ft.colors.RED_500), indexes_of_anomalies
        if int(avg) == 2:
            return ft.Text("\tMost Transactions occurred between 6AM and 9AM.", size=15), ft.Text("\tA check of some of the transactions is recommended due to the unusual times.", size=15, color=ft.colors.RED_300), indexes_of_anomalies
        if int(avg) == 3:
            return ft.Text("\tMost Transactions occurred between 9AM and 12PM.", size=15), ft.Text("\tMost transactions times look normal.", size=15, color=ft.colors.GREEN_400), indexes_of_anomalies
        if int(avg) == 4:
            return ft.Text("\tMost Transactions occurred between 12PM and 3PM.", size=15), ft.Text("\tMost transactions times look normal.", size=15, color=ft.colors.GREEN_400), indexes_of_anomalies
        if int(avg) == 5:
            return ft.Text("\tMost Transactions occurred between 3PM and 6PM.", size=15), ft.Text("\tMost transactions times look normal.", size=15, color=ft.colors.GREEN_400), indexes_of_anomalies
        if int(avg) == 6:
            return ft.Text("\tMost Transactions occurred between 6PM and 9PM.", size=15), ft.Text("\tMost transactions times look normal.", size=15, color=ft.colors.GREEN_400), indexes_of_anomalies
        if int(avg) == 7:
            return ft.Text("\tMost Transactions occurred between 9PM and 12AM.", size=15), ft.Text("\tA check of the transactions is recommended due to the very unusual time!", size=15, color=ft.colors.RED_500), indexes_of_anomalies

    def transactions_avg_size(self):
        avg: float = 0.0
        for s in self.transactions:
            avg += s
        avg /= len(self.transactions)
        indexes_of_anomalies: list[int] = []
        for s in self.transactions:
            if s < avg * 0.7 or s > avg * 1.3:
                for i in self.rows_indexes_list:
                    if self.file_df.iloc[i]["Transaction"] == s:
                        indexes_of_anomalies.append(i)
        if avg > 1000.0:
            return ft.Text(f"\tThe average transaction size is {avg}.", size=15), ft.Text("\tA check of the transactions is recommended due to the amount of money that was spent!", size=15, color=ft.colors.RED_500), indexes_of_anomalies
        elif avg > 750.0:
            return ft.Text(f"\tThe average transaction size is {avg}.", size=15), ft.Text("\tA check of the transactions is recommended due to the amount of money that was spent!", size=15, color=ft.colors.RED_300), indexes_of_anomalies
        return ft.Text(f"\tThe average transaction size is {avg}.", size=15), ft.Text("\tMost of the transactions' sizes do not stand out", size=15, color=ft.colors.GREEN_400), indexes_of_anomalies

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
                potential_anomalies[pointer] = index_in_group(i, self.rows_indexes_list) + 1
            print(f"anomalies_for_sure: {anomalies_for_sure}\npotential_anomalies: {potential_anomalies}")
            return anomalies_for_sure, potential_anomalies




        time_row_title = ft.Row(controls=[ft.Text("Date Affiliations:", color=ft.colors.BLACK, size=20, weight=ft.FontWeight.BOLD)])
        time_row_info = ft.Row([information_messages[0]])
        time_row_alert = ft.Row([alert_messages[0]])
        transaction_row_title = ft.Row(controls=[ft.Text("Transactions Affiliations:", color=ft.colors.BLACK, size=20, weight=ft.FontWeight.BOLD)])
        transaction_row_info = ft.Row([information_messages[1]])
        transaction_row_alert = ft.Row([alert_messages[1]])
        card_showing_row_title = ft.Row(controls=[ft.Text("Card Appearance Affiliations:", color=ft.colors.BLACK, size=20, weight=ft.FontWeight.BOLD)])
        card_showing_row_info = ft.Row([information_messages[2]])
        is_anomaly_info = is_anomaly(anomalies_indexes)
        print(f"is_anomaly_info: {is_anomaly_info}")
        anomalies_row_title = ft.Row([ft.Text("Potential anomalies:", color=ft.colors.BLACK, size=20,weight=ft.FontWeight.BOLD)])
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







