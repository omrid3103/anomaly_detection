from typing import Dict
import flet as ft


class UploadFile:
    def __init__(self, page: ft.Page):
        self.page = page
        self.prog_bars: Dict[str, ft.ProgressRing] = {}
        self.files = ft.Ref[ft.Column]()
        self.upload_button = ft.Ref[ft.ElevatedButton]()
        self.file_picker = ft.FilePicker(on_result=self.file_picker_result, on_upload=self.on_upload_progress)
        self.page.overlay.append(self.file_picker)
        self.row = ft.Row([
            ft.ElevatedButton(
                text="Select files...",
                icon=ft.icons.FOLDER_OPEN,
                on_click=lambda _: self.file_picker.pick_files(allow_multiple=True)
                ),
            ft.Column(ref=self.files),
            ft.ElevatedButton(
                "Upload",
                ref=self.upload_button,
                icon=ft.icons.UPLOAD,
                on_click=self.upload_files,
                disabled=True
                )
            ]
        )
        self.column = ft.Column(controls=[self.row])

    def file_picker_result(self, e: ft.FilePickerResultEvent):
        self.upload_button.current.disabled = True if e.files is None else False
        self.prog_bars.clear()
        self.files.current.controls.clear()
        if e.files is not None:
            for f in e.files:
                prog = ft.ProgressRing(value=0, bgcolor=ft.colors.BLUE_400, width=20, height=20)
                self.prog_bars[f.name] = prog
                self.files.current.controls.append(ft.Row([prog, ft.Text(f.name)]))
        self.page.update()

    def on_upload_progress(self, e: ft.FilePickerUploadEvent):
        self.prog_bars[e.file_name].value = e.progress
        self.prog_bars[e.file_name].update()

    def upload_files(self, e):
        uf = []
        if self.file_picker.result is not None and self.file_picker.result.files is not None:
            for f in self.file_picker.result.files:
                print(f.name)
                uf.append(
                    ft.FilePickerUploadFile(
                        f.name,
                        upload_url=self.page.get_upload_url(f.name, 600),
                    )
                )
            self.file_picker.upload(uf)

    # hide dialog in a overlay


def main(page: ft.Page):
    upload = UploadFile(page).column
    page.add(upload)



ft.app(target=main, upload_dir="my_uploads")


