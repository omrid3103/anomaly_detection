import flet as ft


def home_view(page):

    def exit_app(e):
        page.window_destroy()

    content = ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Home Page", size=30),
                    ft.IconButton(icon=ft.icons.HOME, icon_size=30)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                [
                    ft.TextButton("Exit", icon=ft.icons.CLOSE, icon_color="red", on_click=exit_app)
                ]
            )
        ]
    )
    return content

