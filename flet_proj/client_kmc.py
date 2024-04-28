import flet as ft
import requests
from typing import Union
import time
import datetime


class FilePicker:

    def __init__(self, page: ft.Page, url: str):
        self.page: ft.Page = page
        self.request_url = url
        self.confirmation = ft.Text("Your file has been uploaded", color=ft.colors.GREEN_200, weight=ft.FontWeight("bold"))
        self.table_welcoming_text_button = ft.TextButton(
            content=ft.Text("Your credit table is ready for showing! Show it", color=ft.colors.BLUE_400),
            on_hover=False,
            on_click=self.text_button_clicked
        )
        self.saved_file: Union[None, bytes] = None
        self.file_name: str = ""
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)

        self.page.overlay.append(self.pick_files_dialog)

        # self.pick_files =
        self.pick_button = ft.ElevatedButton(
            "Pick File",
            icon=ft.icons.UPLOAD_FILE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=2)
            ),
            color=ft.colors.BLUE_400,
            on_click=lambda _: self.pick_files_dialog.pick_files()
        )


        self.start_date_picker = ft.DatePicker(
            on_change=self.start_change_date,
            first_date=datetime.datetime(2006, 1, 1),
            last_date=datetime.datetime(2026, 1, 1),
        )
        page.overlay.append(self.start_date_picker)

        self.start_date_button = ft.ElevatedButton(
            "Pick start date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: self.start_date_picker.pick_date(),
        )
        self.start_date_value: str = ""



        self.end_date_picker = ft.DatePicker(
            on_change=self.end_change_date,
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )
        page.overlay.append(self.end_date_picker)

        self.end_date_button = ft.ElevatedButton(
            "Pick end date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: self.end_date_picker.pick_date(),
        )
        self.end_date_value: str = ""
        self.table_time_stamp: str = ""



        self.upload_button = ft.ElevatedButton(
            "Upload File",
            icon=ft.icons.FILE_COPY_OUTLINED,
            color=ft.colors.BLUE_400,
            on_click=self.upload_file,
            visible=False
        )

        self.buttons_row = ft.Row([self.pick_button])
        self.start_date_row = ft.Row([self.start_date_button])
        self.end_date_row = ft.Row([self.end_date_button])
        self.upload_row = ft.Row([self.upload_button])
        self.confirmation_row = ft.Row([self.confirmation], visible=False)
        self.table_redirection_row = ft.Row([self.table_welcoming_text_button], visible=False)
        self.items = [self.buttons_row, self.start_date_row, self.end_date_row, self.upload_row, self.confirmation_row, self.table_redirection_row]
        self.content = ft.Column(spacing=20, controls=self.items)

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            with open(e.files[0].path, "rb") as file:
                saved_file = file.read()
                self.saved_file = saved_file
                print("OK", e.files[0].name)
                if self.saved_file is not None:
                    self.buttons_row.update()
                    self.content.update()
                    self.page.update()
        else:
            print("No files selected or cancelled.")

    def upload_file(self, e):
        result = requests.post(f"{self.request_url}upload_files", params={"file_bytes": self.saved_file}).json()
        response = result["success"]
        print(result["file_path"])
        if response:
            self.file_name = result["file_path"]
            self.confirmation_row.visible = True
            self.confirmation_row.update()
            self.table_redirection_row.visible = True
            self.table_redirection_row.update()
            self.content.update()
            self.page.update()

    def text_button_clicked(self, e):
        self.table_redirection_row.visible = False
        self.table_redirection_row.update()
        self.confirmation_row.visible = False
        self.confirmation_row.update()
        self.upload_row.visible = False
        self.upload_row.update()
        self.start_date_row.controls.remove(self.start_date_row.controls[1])
        self.end_date_row.controls.remove(self.end_date_row.controls[1])
        self.content.update()
        self.page.update()
        self.page.go("/data_table")

    def start_change_date(self, e):
        if self.start_date_value != "":
            if len(self.start_date_row.controls) > 1:
                self.start_date_row.controls.remove(self.start_date_row.controls[1])
            self.content.update()
            self.page.update()
        self.start_date_value = self.start_date_picker.value.strftime("%d/%m/%y")
        start_date_msg = ft.Text(f"Start Date for your table is: {self.start_date_value}", visible=True,
                               weight=ft.FontWeight("bold"), color=ft.colors.BLUE_400, size=20)
        self.start_date_row.controls.append(start_date_msg)
        self.start_date_row.update()
        if self.end_date_value != "":
            self.upload_button.visible = True
            self.upload_row.visible = True
            self.upload_row.update()
        self.content.update()
        self.page.update()

    def end_change_date(self, e):
        if self.end_date_value != "":
            if len(self.end_date_row.controls) > 1:
                self.end_date_row.controls.remove(self.end_date_row.controls[1])
            self.content.update()
            self.page.update()
        self.end_date_value = self.end_date_picker.value.strftime("%d/%m/%y")
        self.table_time_stamp = f"{self.start_date_value} - {self.end_date_value}"
        end_date_msg = ft.Text(f"End Date for your table is: {self.end_date_value}", visible=True,
                               weight=ft.FontWeight("bold"), color=ft.colors.BLUE_400, size=20)
        self.end_date_row.controls.append(end_date_msg)
        self.end_date_row.update()
        if self.start_date_value != "":
            self.upload_button.visible = True
            self.upload_row.visible = True
            self.upload_row.update()
        self.content.update()
        self.page.update()










