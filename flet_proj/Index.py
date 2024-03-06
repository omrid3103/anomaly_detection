import flet as ft


def index_view(page):

    content = ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Initial Page", size=30)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ]
    )
    return content

