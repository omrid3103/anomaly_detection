import flet as ft
from db_and_pdf_demo import kmc_controller as kmc_cntrl
import pandas as pd
from typing import Union


class DataTable:

    def __init__(self, page: ft.Page, pdf_path: str = r"C:\Users\Sharon's PC\PycharmProjects\anomaly_detection\db_and_pdf_demo\client_data_table0.pdf"):
        self.page = page
        self.controller = kmc_cntrl.KMCController(pdf_path)
        self.controller.csv_to_dataframe()
        self.df: pd.DataFrame = self.controller.df

        self.columns_names_list = self.df.columns.tolist()
        self.num_rows: int = self.df.shape[0]
        self.num_cells_in_each_row: int = len(self.df.iloc[0].tolist())


        # =================================================================================
        # ******************   DropDown Selection & Button   ******************************
        # =================================================================================

        self.dropdown_button = ft.ElevatedButton(text="Submit", on_click=self.dropdown_button_clicked)
        self.dropdown_obj = ft.Dropdown(
            width=170,
            options=self.dropdown_options_generation()
            # [
            #     ft.dropdown.Option("Red"),
            #     ft.dropdown.Option("Green"),
            #     ft.dropdown.Option("Blue"),
            # ],
        )

        # =================================================================================
        # ************************   Search TextField   ***********************************
        # =================================================================================

        self.search_field = ft.TextField(label="search", width=350)


        # =================================================================================
        # ************************   DataTable Creation   *********************************
        # =================================================================================

        self.data_table = ft.DataTable(
            width=1000,
            bgcolor="yellow",
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
            columns=self.table_columns_generation(),
            rows=self.table_rows_generation()
        )


        self.search_row = ft.Row([self.dropdown_obj, self.search_field], spacing=80)
        self.button_row = ft.Row([self.dropdown_button])
        self.table_row = ft.Row([self.data_table])

        self.items = [self.search_row, self.button_row, self.table_row]
        self.column = ft.Column(spacing=20, controls=self.items)


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
                    ft.DataCell(ft.Text(f"{row_i_information[j]}", text_align=ft.TextAlign.CENTER))
                )
            rows_list.append(
                ft.DataRow(
                    cells=cells_list,
                    # color=ft.colors.BLUE_300,
                    selected=True,
                    on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                )
            )
            cells_list = []
        return rows_list

    def dropdown_options_generation(self) -> list[ft.dropdown.Option]:
        options_list = []
        for i in range(len(self.columns_names_list)):
            options_list.append(
                ft.dropdown.Option(f"{self.columns_names_list[i]}")
            )
        return options_list

    def dropdown_button_clicked(self, e):
        for k in range(len(self.columns_names_list)):
            if self.dropdown_obj.value == self.columns_names_list[k]:
                self.search_field.hint_text = f"Search in {self.dropdown_obj.value} column..."
        self.search_field.update()
        self.page.update()


    def main(self) -> None:
        # page.scroll = ft.ScrollMode.HIDDEN
        # page.auto_scroll = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.add(self.column)
        # self.page.floating_action_button = ft.FloatingActionButton(
        #     icon=ft.icons.ADD, on_click=self.fab_pressed, bgcolor=ft.colors.BLUE_200)



def dt_main():
    ft.app(target=lambda page: DataTable(page=page).main())


if __name__ == "__main__":
    dt_main()
