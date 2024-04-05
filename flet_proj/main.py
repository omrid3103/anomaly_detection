import flet as ft
from flet_proj.appbar import AppBar

from flet_proj.router import Router
from flet_proj.appbar import AppBar


def main(page: ft.Page):

    page.theme_mode = "light"
    my_router = Router(page)
    temp_appbar = AppBar(page)
    if my_router.user_landing.details["username"] != "":
        temp_appbar.update_menu()
    page.appbar = temp_appbar.my_appbar

    page.on_route_change = my_router.route_change

    page.add(my_router.body)
    page.go("/home")


if __name__ == "__main__":
    ft.app(target=main)
