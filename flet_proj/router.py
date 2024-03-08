import flet as ft
from flet_proj.home import home_view
from flet_proj.sign_up_flet import sign_up_view
from flet_proj.Index import index_view
from flet_proj.authentication_flet import authentication_view
from flet_proj.user_landing_page import user_landing_view


class Router:

    def __init__(self, page):

        self.signup_controller = sign_up_view(page, self)
        self.signin_controller = authentication_view(page, self)
        self.page = page
        self.routes = {
            "/index": index_view(page, self),
            "/home": home_view(page, self),
            "/sign_up_flet": self.signup_controller.column,
            "/authentication_flet": self.signin_controller.column,
            "/user_landing_page": user_landing_view(page, self)
        }
        self.body = ft.Container(content=self.routes["/home"])

    def route_change(self, route):
        self.body.content = self.routes[route.route]
        self.body.update()
