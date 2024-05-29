from flet_proj.authentication_flet import SignUp, SignIn, UpdateDetails
from flet_proj.navigation import *
from flet_proj.client_kmc import FilePicker
from flet_proj.data_table import DataTable
from flet_proj.client_former_data import FormerData
from flet_proj.former_table import FormerTable
from typing import Union
import pandas as pd





class UserDetails:
    def __init__(self, username: str, email: str, password: str, token: str):
        self.info = {"username": username, "email": email, "password": password, "token": token}

    # def update_info(self, username: str, email: str, password: str):
    #     self.info["username"] = username
    #     self.info["email"] = email
    #     self.info["password"] = password


class DataKeeper:
    def __init__(self, df: Union[pd.DataFrame, None] = None):
        self.df = df

    def update_df_content(self, updated_df):
        self.df = updated_df


def main(page: ft.Page, url: str):
    page.title = "Routes Example"
    page.scroll = ft.ScrollMode.ALWAYS

    user_information = UserDetails("", "", "", "")
    df_data_keeper = DataKeeper()
    guest_appbar = GuestAppBar(page).my_appbar
    guest_menu = GuestMenu(page).guest_menu
    user_appbar = UserAppBar(page).my_appbar
    user_menu = UserMenu(page).user_menu
    table_appbar = TableAppBar(page).my_appbar
    sign_up = SignUp(page, url)
    sign_in = SignIn(page, url)
    file_picker = FilePicker(page, url, "")
    former_data: Union[FormerData, None] = None



    def insert_user_information(username: str, email: str, password: str, token: str):
        if username != "":
            user_information.info["username"] = username
        if email != "":
            user_information.info["email"] = email
        if password != "":
            user_information.info["password"] = password
        if token != "":
            user_information.info["token"] = token

    def reset_information():
        user_information.info["username"] = ""
        user_information.info["email"] = ""
        user_information.info["password"] = ""


    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                route="/guest_home",
                controls=[
                    guest_appbar,
                    guest_menu,
                    ft.Row([ft.Image(src="../authentication/CompanyLogo.png"), ft.Text("Welcome Guest", size=50, color=ft.colors.DEEP_PURPLE_300)], Ro)
                ],
            )
        )
        if page.route == "/guest_home":
            reset_information()
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
        insert_user_information(sign_up.details["username"], sign_up.details["email"], sign_up.details["password"], sign_up.details["token"])
        insert_user_information(sign_in.details["username"], sign_in.details["email"], sign_in.details["password"], sign_in.details["token"])
        update_details = UpdateDetails(page, user_information.info["username"], user_information.info["email"], user_information.info["password"], user_information.info["token"], url)
        if file_picker.token == "":
            file_picker.token = user_information.info["token"]

        if page.route == "/user_home":
            page.views.append(
                ft.View(
                    "/user_home",
                    [
                        user_appbar,
                        user_menu,
                        ft.Row([ft.Image(src="../authentication/CompanyLogo.png"),
                                ft.Text("Welcome " + user_information.info["username"] + "", color=ft.colors.DEEP_PURPLE_300, size=50)])
                    ],
                )
            )
            user_appbar.leading = ft.TextButton(text=f"{user_information.info['username']}", disabled=True)
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
        if page.route == "/client_kmc":
            page.views.append(
                ft.View(
                    "client_kmc",
                    [
                        user_appbar,
                        user_menu,
                        file_picker.content,
                    ]
                )
            )

        if page.route == "/data_table":
            if file_picker.table_time_stamp == "":
                data_table = DataTable(page, url, user_information.info["token"], file_picker.file_df).column
            else:
                data_table = DataTable(page, url, user_information.info["token"], file_picker.file_df, file_picker.table_time_stamp).column
            page.views.append(
                ft.View(
                    "data_table",
                    [
                        table_appbar,
                        data_table,
                    ],
                    scroll=ft.ScrollMode.ALWAYS
                )
            )

        if page.route == "/former_data":
            global former_data
            former_data = FormerData(page, url, user_information.info["token"])
            page.views.append(
                ft.View(
                    "former_data",
                    [
                        user_appbar,
                        user_menu,
                        former_data.column,
                    ],
                    scroll=ft.ScrollMode.ALWAYS
                )
            )


        if page.route == "/former_table":
            df_data_keeper.update_df_content(former_data.selected_table_df)
            if df_data_keeper.df is not None:
                former_table = FormerTable(page, url, df_data_keeper.df, former_data.selected_table_groups)
                table_appbar.leading = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: page.go("/former_data"))
                page.views.append(
                    ft.View(
                        "former_table",
                        [
                            table_appbar,
                            former_table.column,
                        ],
                        scroll=ft.ScrollMode.ALWAYS
                    )
                )
            else:
                print("former table error: routing app line 155")

        page.update()

    # def view_pop(view):
    #    page.views.pop()
    #    top_view = page.views[-1]
    #    page.go(top_view.route)

    page.on_route_change = route_change
    # page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    IP = "127.0.0.1"
    PORT = 5555
    URL = f"http://{IP}:{PORT}/"
    ft.app(target=lambda page: main(page=page, url=URL))
