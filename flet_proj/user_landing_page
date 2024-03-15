import flet as ft
import requests


class UserPage:

    def __init__(self, page: ft.Page):
        self.page: ft.Page = page
        self.details: dict[str, str] = {"username": "", "email": ""}
        self.title_text = ft.Text("Welcome to my site", size=30)
        self.username_text = ft.Text(f"{self.details['username']}", size=30, color=ft.colors.CYAN)
        self.content = ft.Column(
            [
                ft.Row(
                    [
                        self.title_text,
                        self.username_text
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        ft.TextButton("Exit", icon=ft.icons.CLOSE, icon_color="red")
                    ]
                )
            ]
        )

    def update_text(self):
        self.username_text.value = f"{self.details['username']}"
        self.page.update()


    def exit_app(self, e):
        self.page.window_destroy()


def user_landing_view(page):
    return UserPage(page)

# ft.Stack(
#     [
#         ft.Image(
#             src=f"https://www.google.com/url?sa=i&url=https%3A%2F%2Fgithub.com%2Fsaarques%2Fcredit-card-fraud-detection&psig=AOvVaw36lQIGiRMKl-u8F7BNT7nD&ust=1709835673312000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqFwoTCND1i7Gg4IQDFQAAAAAdAAAAABAE",
#             width=300,
#             height=300,
#             fit=ft.ImageFit.CONTAIN,
#         ),
#         ft.Row(
#             [
#                 ft.Text(
#                     "Image title",
#                     color="white",
#                     size=40,
#                     opacity=0.5,
#                 )
#             ],
#             alignment=ft.MainAxisAlignment.CENTER,
#         ),
#     ],
#     width=300,
#     height=300,
# )
