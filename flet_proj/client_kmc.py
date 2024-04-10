import flet as ft


class FilePicker:

    def __init__(self, page: ft.Page):
        self.page: ft.Page = page
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.selected_files = ft.Text()
        self.page.overlay.append(self.pick_files_dialog)
        self.row = ft.Row(
            [
                ft.ElevatedButton(
                    "Pick files",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: self.pick_files_dialog.pick_files(
                        allow_multiple=True
                    ),
                ),
                self.selected_files,
            ]
        )
        self.items = [self.row, self.selected_files]
        self.content = ft.Column(spacing=20, controls=self.items)

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        self.selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        self.selected_files.update()



