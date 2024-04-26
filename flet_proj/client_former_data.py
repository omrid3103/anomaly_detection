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
        self.items: list = [self.no_data_mag]
        if self.data is not None:
            self.num_of_tables = len(self.data)
            self.items = self.generate_buttons()

        self.selected_table_df: Union[dict, None] = None

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
            buttons_list.append(ft.Row(
                [
                    ft.Text(f"Table #{i + 1}: {t['table_time_stamp']}", weight=ft.FontWeight("bold"), color=ft.colors.BLACK, size=30),
                    ft.ElevatedButton(
                        f"Table #{i + 1}",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=2)
                        ),
                        color=ft.colors.BLUE_400,
                        on_click=lambda event: self.button_clicked(event, table_df)
                    )
                ]
            )
            )
        return buttons_list


    def button_clicked(self, e, table_df: pd.DataFrame):
        def move_to_table_page():
            self.page.go('/former_table')

        self.selected_table_df = table_df
        self.page.update()
        move_to_table_page()

    def main(self) -> None:
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.add(self.column)
