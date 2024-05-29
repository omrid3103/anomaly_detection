import flet as ft
import numpy as np
import json
# from db_and_pdf_demo import kmc_controller
# from db_and_pdf_demo import kmeans_clustering
import pandas as pd
from typing import Union
import requests
import time
from db_and_pdf_demo.kmc_controller import CommonChars


class FormerTable:

    def __init__(self, page: ft.Page, url: str, file_df: pd.DataFrame, grouping_list: list[list[int]]):
        self.page = page
        self.request_url = url
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


        self.df: pd.DataFrame = file_df
        # self.points_coordinates = np.array(json.loads(requests.get(f"{self.request_url}get_points_array", params={"json_df": self.df.to_json(orient='records')}).json()["points_array"]))
        self.grouping_list = grouping_list

        self.columns_names_list = self.df.columns.tolist()
        self.num_rows: int = self.df.shape[0]
        self.num_cells_in_each_row: int = len(self.df.iloc[0].tolist())
        self.row_colors: list[ft.colors] = []
        self.alert_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Timeout Error"),
            content=ft.Text("You are connected for too long. You will now be disconnected."),
            actions=[
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

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
        self.kmc_button = ft.ElevatedButton("kmc the table", on_click=self.kmc_table_definition, color=ft.colors.DEEP_PURPLE_300)

        self.anomalies_information_button = ft.ElevatedButton("Analyze Transactions", on_click=self.show_anomalies, color=ft.colors.DEEP_PURPLE_300)
        self.common_chars: Union[CommonChars, None] = None


        self.search_row = ft.Row([self.kmc_button, self.dropdown_obj, self.search_field, self.color_dropdown], spacing=80)
        # self.search_row = ft.Row([self.dropdown_obj, self.search_field, self.color_dropdown], spacing=80)
        self.message_row = ft.Row([self.data_not_found])
        self.table_row = ft.Row([self.data_table])
        self.anomaly_row = ft.Row([self.anomalies_information_button], visible=False)

        self.items = [self.search_row, self.table_row, self.anomaly_row]
        self.column = ft.Column(spacing=20, controls=self.items)
        self.column.scroll = ft.ScrollMode.ALWAYS
        # self.kmc_table_definition()


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
            row_i_information = self.df.iloc[i].tolist()
            for j in range(self.num_cells_in_each_row):
                cells_list.append(
                    ft.DataCell(ft.Text(f"{str(row_i_information[j])}", text_align=ft.TextAlign.CENTER, color=ft.colors.BLACK))
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
            if isinstance(self.df.iloc[0, i], str):
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
                    ft.DataCell(ft.Text(f"{str(x_c[self.columns_names_list[n]])}", color=ft.colors.BLACK))
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

        my_filtered_df = self.df[self.df[self.columns_names_list[self.columns_names_list.index(dropdown_value)]].str.contains(search_name)]
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
            self.common_chars = CommonChars(indexes_of_rows, self.df)
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
        # json_points = self.points_coordinates.tolist()
        # json_points = json.dumps(json_points)
        # returned_dict = requests.get(f"{self.request_url}most_efficient_n_of_clusters",
        #                              params={"points_json": json_points, "min_clusters_to_check": 4, "max_clusters_to_check": 15}).json()
        # if returned_dict["success"]:
        #     most_efficient_number_of_clusters = returned_dict["n_clusters"]
        # else:
        #     most_efficient_number_of_clusters = 4
        # print(most_efficient_number_of_clusters)
        #
        #
        # returned_dict = requests.get(f"{self.request_url}kmc_server",
        #                              params={"points_array": json.dumps(self.points_coordinates.tolist()), "n_clusters": most_efficient_number_of_clusters, "iterations": 35}).json()
        # # {"centers_array": centers_array, "grouping_list": grouping_list}
        # grouping_list: list[list[int]] = self.grouping_list
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
            self.dropdown_obj.visible = True
            self.data_table.update()
            self.column.update()
            self.page.update()


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


