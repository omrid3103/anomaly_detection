from flet_proj.authentication_flet import SignUp, SignIn
from flet_proj.navigation import *


def main(page: ft.Page):
    page.title = "Routes Example"

    guest_appbar = GuestAppBar(page).my_appbar
    guest_menu = GuestMenu(page).guest_menu
    user_appbar = UserAppBar(page)
    sign_up = SignUp(page)
    sign_in = SignIn(page)

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                route="/guest_home",
                controls=[
                    guest_appbar,
                    guest_menu,
                    ft.Text("Home")
                ],
            )
        )
        if page.route == "/sign_up":
            page.views.append(
                ft.View(
                    "/sign_up",
                    [
                        guest_appbar,
                        guest_menu,
                        sign_up.column,
                    ],
                )
            )
        if page.route == "/sign_in":
            page.views.append(
                ft.View(
                    "/sign_up",
                    [
                        guest_appbar,
                        guest_menu,
                        sign_in.column,
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)
