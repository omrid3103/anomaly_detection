import flet as ft
import requests
from typing import Union
import pandas as pd
import json
from io import StringIO


class FormerData:
    def __init__(self, page: ft.Page, url: str, info: dict):
        self.page: ft.Page = page
        self.request_url: str = url
        self.username: str = info["username"]
        self.password: str = info["password"]

        self.no_data_mag = ft.Text("You don't have any data saved...", visible=True,
                                   weight=ft.FontWeight("bold"), color=ft.colors.RED_400, size=30)

        self.data: Union[list[dict], None] = self.get_user_data()
        self.num_of_tables: Union[int, None] = None
        self.dataframes_list: list[pd.DataFrame] = []
        self.items: list = [self.no_data_mag]
        if self.data is not None:
            self.num_of_tables = len(self.data)
            self.items = self.generate_buttons()
            self.table_dropdown = ft.Dropdown(
                width=150,
                options=self.table_options_generation(),
                hint_text="Pick Table",
                on_change=self.tables_dropdown_changed
            )
            self.show_table = ft.ElevatedButton(
                        "Show Table",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=2)
                        ),
                        color=ft.colors.BLUE_400,
                        disabled=True,
                        on_click=self.button_clicked
                    )
            self.dropdown_row = ft.Row([self.table_dropdown])
            self.table_button_row = ft.Row([self.show_table])

            self.items.append(self.dropdown_row)
            self.items.append(self.table_button_row)

        self.selected_table_df: Union[pd.DataFrame, None] = None

        self.column = ft.Column(controls=self.items)



    def get_user_data(self) -> Union[list[dict], None]:
        result = requests.get(f"{self.request_url}extract_user_data", params={"username": self.username, "password": self.password}).json()
        if result["success"]:
            if result["response"] == "Sending data":
                return result["data"]
        return None

    def generate_buttons(self) -> list[ft.Row]:
        buttons_list: list = [ft.Row([ft.Text("Click To See Your Tables:", color=ft.colors.BLACK, size=60)])]

        for i, t in enumerate(self.data):
            json_buffer = StringIO(t["json_df"])
            table_df = pd.read_json(json_buffer)
            self.dataframes_list.append(table_df)
            buttons_list.append(ft.Row(
                [
                    ft.Text(f"Table #{i + 1}: {t['table_time_stamp']}", weight=ft.FontWeight("bold"), color=ft.colors.BLACK, size=30),
                    # ft.ElevatedButton(
                    #     f"Table #{i + 1}",
                    #     style=ft.ButtonStyle(
                    #         shape=ft.RoundedRectangleBorder(radius=2)
                    #     ),
                    #     color=ft.colors.BLUE_400,
                    #     on_click=lambda event: self.button_clicked(event, i)
                    # )
                ]
            )
            )
        return buttons_list


    def button_clicked(self, e):
        dropdown_value = self.table_dropdown.value
        table_to_show_index = int(dropdown_value.split('#')[1]) - 1
        json_buffer = StringIO(self.data[table_to_show_index]["json_df"])
        self.selected_table_df = pd.read_json(json_buffer)
        self.page.update()
        if self.selected_table_df is not None:
            self.page.go('/former_table')

    def table_options_generation(self):
        options_list = []
        for i in range(self.num_of_tables):
            options_list.append(
                ft.dropdown.Option(f"Table #{i + 1}")
            )
        return options_list

    def tables_dropdown_changed(self, e):
        if self.show_table.disabled:
            self.show_table.disabled = False
        self.show_table.update()
        self.table_dropdown.update()
        self.table_button_row.update()
        self.dropdown_row.update()
        self.column.update()
        self.page.update()



    def main(self) -> None:
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.add(self.column)
