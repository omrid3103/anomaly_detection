import flet as ft
from flet_proj.home import home_view
from flet_proj.sign_up_flet import sign_up_view
from flet_proj.Index import index_view
from flet_proj.authentication_flet import authentication_view


class Router:

    def __init__(self, page):
        self.page = page
        self.routes = {
            "/index": index_view(page),
            "/home": home_view(page),
            "/sign_up_flet": sign_up_view(page),
            "/authentication_flet": authentication_view(page)
        }
        self.body = ft.Container(content=self.routes["/home"])

    def route_change(self, route):
        self.body.content = self.routes[route.route ]
        self.body.update()
