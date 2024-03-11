import flet as ft
from flet_proj.authentication_flet import authentication_view
from flet_proj.user_landing_page import user_landing_view
from flet_proj.initial_page import initial_page_view


class Router:

    def __init__(self, page):
        self.page = page
        self.sign_up_controller = authentication_view(self.page, self)
        self.sign_up_controller.submit_button.on_click = self.sign_up_controller.sign_up_button_clicked
        self.sign_up_controller.submit_button.text = "Sign Me Up!"

        self.sign_in_controller = authentication_view(self.page, self)
        self.sign_in_controller.submit_button.on_click = self.sign_in_controller.sign_in_button_clicked
        self.sign_in_controller.submit_button.text = "Sign Me In!"

        self.index = initial_page_view(self.page)
        self.home = initial_page_view(self.page)

        self.user_landing = user_landing_view(self.page)
        if self.sign_up_controller.details["username"] == "":
            self.user_landing.details = self.sign_in_controller.details

        else:
            self.user_landing.details = self.sign_up_controller.details

        self.user_landing.update_text()

        self.routes = {
            "/index": self.index.content,
            "/home": self.home.content,
            "/sign_up_flet": self.sign_up_controller.column,
            "/authentication_flet": self.sign_in_controller.column,
            "/user_landing_page": self.user_landing.content
        }
        self.body = ft.Container(content=self.routes["/home"])

    def route_change(self, route):
        self.body.content = self.routes[route.route]
        self.body.update()
