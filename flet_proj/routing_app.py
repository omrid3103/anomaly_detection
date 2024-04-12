from flet_proj.authentication_flet import SignUp, SignIn, UpdateDetails
from flet_proj.navigation import *
from flet_proj.client_kmc import FilePicker




class UserDetails:
    def __init__(self, username: str, email: str, password: str):
        self.info = {"username": username, "email": email, "password": password}

    def update_info(self, username: str, email: str, password: str):
        self.info["username"] = username
        self.info["email"] = email
        self.info["password"] = password


def main(page: ft.Page, url: str):
    page.title = "Routes Example"

    user_information = UserDetails("", "", "")
    guest_appbar = GuestAppBar(page).my_appbar
    guest_menu = GuestMenu(page).guest_menu
    user_appbar = UserAppBar(page).my_appbar
    user_menu = UserMenu(page).user_menu
    sign_up = SignUp(page, url)
    sign_in = SignIn(page, url)
    file_picker = FilePicker(page).content


    def insert_user_information(username: str, email: str, password: str):
        if username != "":
            user_information.info["username"] = username
        if email != "":
            user_information.info["email"] = email
        if password != "":
            user_information.info["password"] = password


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
                    "/sign_in",
                    [
                        guest_appbar,
                        guest_menu,
                        sign_in.column,
                    ],
                )
            )
        insert_user_information(sign_up.details["username"], sign_up.details["email"], sign_up.details["password"])
        insert_user_information(sign_in.details["username"], sign_in.details["email"], sign_in.details["password"])
        update_details = UpdateDetails(page, user_information.info["username"], user_information.info["email"], user_information.info["password"], url)
        if page.route == "/user_home":
            page.views.append(
                ft.View(
                    "/user_home",
                    [
                        user_appbar,
                        user_menu,
                        ft.Text("User Home\nHello " + user_information.info["username"] + ""),
                    ],
                )
            )
        if page.route == "/update_details":
            page.views.append(
                ft.View(
                    "/update_details",
                    [
                        user_appbar,
                        user_menu,
                        update_details.column,
                    ],
                )
            )
        if user_information.info["username"] != update_details.details["username"]:
            user_information.update_info(update_details.details["username"], update_details.details["email"], update_details.details["password"])

        if page.route == "/client_kmc":
            page.views.append(
                ft.View(
                    "client_kmc",
                    [
                        user_appbar,
                        user_menu,
                        file_picker,
                    ]
                )
            )
        page.update()

    # def view_pop(view):
    #    page.views.pop()
    #    top_view = page.views[-1]
    #    page.go(top_view.route)

    page.on_route_change = route_change
    # page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    IP = "192.168.29.125"
    PORT = 5555
    URL = f"http://{IP}:{PORT}/"
    ft.app(target=lambda page: main(page=page, url=URL))
