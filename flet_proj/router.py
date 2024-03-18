from typing import Union

import flet as ft
from flet_proj.authentication_flet import authentication_view
from flet_proj.user_landing_page import user_landing_view
from flet_proj.initial_page import initial_page_view


class Router:

    def __init__(self, page):
        self.page = page
        self.sign_up_controller = authentication_view(self.page, self)
        # self.sign_up_controller.submit_button.on_click = self.sign_up_controller.sign_up_button_clicked
        # self.sign_up_controller.submit_button.text = "Sign Me Up!"
        self.sign_in_controller = authentication_view(self.page, self)
        # self.sign_in_controller.submit_button.on_click = self.sign_in_controller.sign_in_button_clicked
        # self.sign_in_controller.submit_button.text = "Sign Me In!"
        self.index = self.initial_page
        self.home = self.initial_page
        self.user_landing = user_landing_view(self.page)

        self.user_action = user_landing_view(self.page)
        self.user_action.title_text = "ACTION"

        self.initial_text: Union[ft.Text, None] = None

        self.routes = {}
        self.body: Union[ft.Container, None] = None

    def routes_definition(self):
        self.routes = {
            "/index": self.initial_content,
            "/home": self.initial_content,
            "/sign_up_flet": self.sign_up_controller.column,
            "/authentication_flet": self.sign_in_controller.column,
            "/user_landing_page": self.user_landing.content,
            "/user_action_page": self.user_action.content,
        }
        self.body = ft.Container(content=self.routes["/home"])

    def update_credentials(self) -> None:

        print(self.user_landing.details)
        if self.sign_in_controller.details["username"] == "":
            self.sign_up_controller.update_details()
            self.user_landing.details["username"] = self.sign_up_controller.details["username"]
            self.user_landing.details["email"] = self.sign_up_controller.details["email"]

        else:
            self.sign_in_controller.update_details()
            self.user_landing.details["username"] = self.sign_in_controller.details["username"]
            self.user_landing.details["email"] = self.sign_in_controller.details["email"]

        self.user_landing.update_text()
        print(self.user_landing.details)

    def initial_page(self, page: ft.Page):
        self.page = page
        self.initial_text = ft.Text("Initial Page", size=30)
        self.initial_content = ft.Column(
            [
                ft.Row(
                    [
                        self.initial_text
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ]
        )
        # page.scroll = ft.ScrollMode.HIDDEN
        # page.auto_scroll = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.add(self.initial_content)

        return self.page

    def route_change(self, route):
        self.body.content = self.routes[route.route]
        self.body.update()
