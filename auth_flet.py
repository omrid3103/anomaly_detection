import flet as ft
import sign_authentication as sa
from typing import Union


class App:
    def __init__(self):
        self.page: Union[ft.Page, None] = None
        self.appbar = ft.AppBar(
            leading=ft.IconButton(ft.icons.MENU, on_click=self.show_nav_drawer),
            leading_width=40,
            title=ft.Text("Sign-Up"),
            color=ft.colors.BLACK,
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=self.switch_theme),
                # ft.IconButton(ft.icons.FILTER_3)
                # ft.IconButton(ft.icons.MENU, tooltip="Menu", icon_color=ft.colors.BLACK87)
                # ft.PopupMenuButton(
                #     items=[
                #         ft.PopupMenuItem(text="Item 1"),
                #         ft.PopupMenuItem(),
                #         ft.PopupMenuItem(
                #             text="Checked item", checked=False, on_click=self.check_item_clicked
                #         ),
                #     ]
                # ),
            ],
        )
        self.nav_drawer = ft.NavigationDrawer(
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.HOME),
                    label="Home",
                    selected_icon=ft.icons.HOME
                ),
                ft.NavigationDrawerDestination(
                    label="Sign-Up",
                    icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
                ),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.LOCK_OPEN),
                    label="Sign-In",
                    selected_icon=ft.icons.LOCK_OPEN,
                ),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.INFO),
                    label="About Us",
                    selected_icon=ft.icons.INFO,
                )
            ],
        )
        self.email_tb = ft.TextField(label="Email", max_lines=1, width=280, hint_text="Enter email here")
        self.username_tb = ft.TextField(label="Username", max_lines=1, width=280, hint_text="Enter username here")
        self.password_tb = ft.TextField(label="Password", password=True, can_reveal_password=True, max_lines=1, width=280, hint_text="Enter password here")
        self.submit_button = ft.ElevatedButton(text="Submit", on_click=self.submit_button_clicked)
        self.items = [self.email_tb, self.username_tb, self.password_tb, self.submit_button]
        self.column = ft.Column(spacing=20, controls=self.items)
        # example_tb2 = ft.TextField(label="Disabled", disabled=True, read_only=True, hint_text="Please enter text here", icon=ft.icons.EMOJI_EMOTIONS, value="First name")

    def switch_theme(self, e):
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.appbar.color = ft.colors.WHITE
            # self.page.floating_action_button.bgcolor = ft.colors.BLUE_900
        elif self.page.theme_mode == ft.ThemeMode.DARK:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.appbar.color = ft.colors.BLACK
            # self.page.floating_action_button.bgcolor = ft.colors.BLUE_200
        self.page.update()

    def submit_button_clicked(self, e):
        result = sa.sign_up(self.email_tb.value, self.username_tb.value, self.password_tb.value)
        response = result["response"]
        print(response)
        if response == "Username invalid!":
            self.username_tb.border_color = ft.colors.RED_400
            self.username_tb.value = ''
            self.username_tb.label = response
            self.username_tb.hint_text = "Enter new username here"
            self.email_tb.border_color = ft.colors.SURFACE_VARIANT
            self.email_tb.label = "Email"
        if response == "Invalid email address!" or response == "Account with the same email exists!":
            self.email_tb.border_color = ft.colors.RED_400
            self.email_tb.value = ''
            self.email_tb.label = response
            self.email_tb.hint_text = "Enter new email here"
            self.username_tb.border_color = ft.colors.SURFACE_VARIANT
            self.username_tb.label = "Username"
        self.page.update()
        if response == "Signed up successfully!":
            pass
            # redirect to another page

    def show_nav_drawer(self, e):
        self.nav_drawer.open = True
        self.nav_drawer.update()
        self.page.update()

    def main(self, page: ft.Page) -> None:
        self.page = page
        # page.scroll = ft.ScrollMode.HIDDEN
        # page.auto_scroll = True
        self.page.appbar = self.appbar
        self.page.drawer = self.nav_drawer
        self.page.theme_mode = ft.ThemeMode.LIGHT
        # self.page.floating_action_button = ft.FloatingActionButton(
        #     icon=ft.icons.ADD, on_click=self.fab_pressed, bgcolor=ft.colors.BLUE_200)

        self.page.add(self.column)




def main() -> None:
    ft.app(target=App().main)


if __name__ == "__main__":
    main()










