import flet as ft

from flet_proj.router import Router
from flet_proj.appbar import appbar


def main(page: ft.Page):

    page.theme_mode = "light"

    page.appbar = appbar(page)
    my_router = Router(page)

    page.on_route_change = my_router.route_change

    page.add(my_router.body)
    page.go("/home")


if __name__ == "__main__":
    ft.app(target=main)
