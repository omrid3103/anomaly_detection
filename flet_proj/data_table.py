import flet as ft
import numpy as np

from db_and_pdf_demo import kmc_controller
from db_and_pdf_demo import kmeans_clustering
import pandas as pd
from typing import Union


class DataTable:

    def __init__(self, page: ft.Page, url: str, pdf_path: str = r"C:\Users\Sharon's PC\PycharmProjects\anomaly_detection\db_and_pdf_demo\client_data_table0.pdf"):
        self.page = page
        self.request_url = url
        self.page.scroll = True
        if pdf_path != "":
            self.controller = kmc_controller.KMCController(pdf_path)
        else:
            self.controller = kmc_controller.KMCController(r"C:\Users\Sharon's PC\PycharmProjects\anomaly_detection\db_and_pdf_demo\client_data_table0.pdf")
        self.controller.pdf_to_csv()
        self.controller.csv_to_dataframe()
        self.df: pd.DataFrame = self.controller.df

        self.columns_names_list = self.df.columns.tolist()
        self.num_rows: int = self.df.shape[0]
        self.num_cells_in_each_row: int = len(self.df.iloc[0].tolist())
        self.row_colors: list[ft.colors] = []


        # =================================================================================
        # ******************   DropDown Selection & Button   ******************************
        # =================================================================================

        self.dropdown_obj = ft.Dropdown(
            width=170,
            options=self.dropdown_options_generation(),
            on_change=self.dropdown_button_clicked
        )
        self.data_not_found = ft.Text("Data was not found...", weight="bold", size=20)

        # =================================================================================
        # ************************   Search TextField   ***********************************
        # =================================================================================

        self.search_field = ft.TextField(label="search", width=350, on_change=self.input_changed)


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


        self.search_row = ft.Row([self.dropdown_obj, self.search_field], spacing=80)
        self.message_row = ft.Row([self.data_not_found])
        self.table_row = ft.Row([self.data_table, self.kmc_button])

        self.items = [self.search_row, self.table_row]
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
            row_i_information = self.df.iloc[i].tolist()
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


    def dropdown_options_generation(self) -> list[ft.dropdown.Option]:
        options_list = []
        for i in range(len(self.columns_names_list)):
            if isinstance(self.df.iloc[0, i], str):
                options_list.append(
                    ft.dropdown.Option(f"{self.columns_names_list[i]}")
                )
        return options_list

    def dropdown_button_clicked(self, e):
        for k in range(len(self.columns_names_list)):
            if self.dropdown_obj.value == self.columns_names_list[k]:
                self.search_field.hint_text = f"Search in the {self.dropdown_obj.value} column..."
        self.search_field.update()
        self.page.update()

    def input_changed(self, e):

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

        my_filtered_df = self.df[self.df[self.columns_names_list[self.columns_names_list.index(self.dropdown_obj.value)]].str.contains(search_name)]
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


    def kmc_table_definition(self, e) -> None:
        points_coordinates_array: np.ndarray = kmc_controller.KMeansTable(self.df).define_features()
        most_efficient_number_of_clusters = kmeans_clustering.most_efficient_n_of_clusters(points_coordinates_array, 3, 9)
        grouping_list: list[list[int]] = kmeans_clustering.kmc(points_coordinates_array, most_efficient_number_of_clusters, iterations=35)[1]
        grouping_list_length = sum(len(sublist) for sublist in grouping_list)

        COLORS: list[ft.colors] = [ft.colors.YELLOW_200, ft.colors.TEAL_50, ft.colors.BLUE_100, ft.colors.RED_200, ft.colors.BLUE_200,
                  ft.colors.GREEN_200, ft.colors.ORANGE_200, ft.colors.PINK_200, ft.colors.CYAN_50]

        def group_index(g_list: list[list[int]], index_to_check: int) -> int:
            for g_index, g in enumerate(g_list):
                if index_to_check in g:
                    return g_index


        if grouping_list_length == len(self.data_table.rows):
            for i, r in enumerate(self.data_table.rows):
                r.color = COLORS[group_index(grouping_list, i)]
                self.row_colors.append(r.color)
            self.table_row.controls.remove(self.kmc_button)
            self.data_table.update()
            self.column.update()
            self.page.update()




    def main(self) -> None:
        # page.scroll = ft.ScrollMode.HIDDEN
        # page.auto_scroll = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        # self.page.theme = ft.Theme(
        #     scrollbar_theme=ft.ScrollbarTheme(
        #         track_color={
        #             ft.MaterialState.HOVERED: ft.colors.AMBER,
        #             ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT,
        #         },
        #         track_visibility=True,
        #         track_border_color=ft.colors.BLUE,
        #         thumb_visibility=True,
        #         thumb_color={
        #             ft.MaterialState.HOVERED: ft.colors.RED,
        #             ft.MaterialState.DEFAULT: ft.colors.GREY_300,
        #         },
        #         thickness=30,
        #         radius=15,
        #         main_axis_margin=5,
        #         cross_axis_margin=10,
        #     )
        # )
        self.page.add(self.column)
        # self.page.floating_action_button = ft.FloatingActionButton(
        #     icon=ft.icons.ADD, on_click=self.fab_pressed, bgcolor=ft.colors.BLUE_200)


