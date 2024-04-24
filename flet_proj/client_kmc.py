import flet as ft
import requests
from typing import Union
import time


class FilePicker:

    def __init__(self, page: ft.Page, url: str):
        self.page: ft.Page = page
        self.request_url = url
        self.confirmation = ft.Text("Your file has been uploaded", color=ft.colors.GREEN_200)
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
        self.upload_button = ft.ElevatedButton(
            "Upload File",
            icon=ft.icons.FILE_COPY_OUTLINED,
            color=ft.colors.BLUE_400,
            on_click=self.upload_file
        )
        self.row = ft.Row(
            [
                self.pick_button
            ]
        )
        self.items = [self.row]
        self.content = ft.Column(spacing=20, controls=self.items)

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.files:
            with open(e.files[0].path, "rb") as file:
                saved_file = file.read()
                self.saved_file = saved_file
                print("OK", e.files[0].name)
                if self.saved_file is not None:
                    self.row.controls.append(self.upload_button)
                    self.row.update()
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
            self.row.controls.append(self.confirmation)
            self.row.update()
            self.content.update()
            self.page.update()
            time.sleep(2)
            self.page.go('/data_table')








