import flet as ft


class InitialPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.text = ft.Text("Initial Page", size=30)
        self.content = ft.Column(
                [
                    ft.Row(
                        [
                            self.text
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            )

    def main(self) -> None:
        # page.scroll = ft.ScrollMode.HIDDEN
        # page.auto_scroll = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.add(self.content)
        # self.page.floating_action_button = ft.FloatingActionButton(
        #     icon=ft.icons.ADD, on_click=self.fab_pressed, bgcolor=ft.colors.BLUE_200)


def initial_page_view(page: ft.Page):
    return InitialPage(page)
