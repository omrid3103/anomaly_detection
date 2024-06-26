import time

import flet as ft


class GuestMenu:
    def __init__(self, page: ft.Page):
        self.page = page
        # self.menu_text = ft.TextButton(icon=ft.icons.MENU, icon_color=ft.colors.BLACK)
        self.guest_menu = ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(
                    icon_content=ft.TextButton("Home", icon=ft.icons.HOME, icon_color=ft.colors.DEEP_PURPLE_300, width=200,
                                               on_click=lambda _: page.go("/guest_home"))
                ),
                ft.NavigationDestination(
                    icon_content=ft.TextButton("Sign Up", icon=ft.icons.DOOR_BACK_DOOR, icon_color=ft.colors.DEEP_PURPLE_300,
                                               on_click=lambda _: page.go("/sign_up"))
                ),
                ft.NavigationDestination(
                    icon_content=ft.TextButton("Log In", icon=ft.icons.LOCK_OPEN, icon_color=ft.colors.DEEP_PURPLE_300,
                                               on_click=lambda _: page.go("/sign_in"))
                )
            ]
        )
        self.page.navigation_bar = self.guest_menu
        # self.guest_menu = ft.NavigationDrawer(
        #     controls=[
        #         ft.Container(height=12),
        #         ft.NavigationDrawerDestination(
        #             icon_content=ft.TextButton(text="Home", icon=ft.icons.HOME, icon_color=ft.colors.BLUE_300, on_click=lambda _:self.page.go("/guest_home")),
        #         ),
        #         ft.NavigationDrawerDestination(
        #             icon_content=ft.TextButton(text="Sign Up", icon=ft.icons.DOOR_BACK_DOOR, icon_color=ft.colors.BLUE_300, on_click=lambda _:self.page.go("/sign_up")),
        #         ),
        #         ft.NavigationDrawerDestination(
        #             icon_content=ft.TextButton(text="Sign In", icon=ft.icons.LOCK_OPEN, icon_color=ft.colors.BLUE_300),
        #         ),
        #         ft.NavigationDrawerDestination(
        #             icon_content=ft.TextButton(text="About Us", icon=ft.icons.INFO, icon_color=ft.colors.BLUE_300),
        #         ),
        #     ],
        # )
        # self.page.drawer = self.guest_menu



class UserMenu:
    def __init__(self, page: ft.Page):
        self.page = page
        # self.menu_text = ft.TextButton(icon=ft.icons.MENU, icon_color=ft.colors.BLACK)
        self.user_menu = ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(
                    icon_content=ft.TextButton("Home", icon=ft.icons.HOME, icon_color=ft.colors.DEEP_PURPLE_300,
                                               on_click=lambda _: page.go("/user_home"))
                ),
                ft.NavigationDestination(
                    icon_content=ft.TextButton("Insert File", icon=ft.icons.ATTACH_FILE, icon_color=ft.colors.DEEP_PURPLE_300,
                                               on_click=lambda _: page.go("/client_kmc"))
                ),
                ft.NavigationDestination(
                    icon_content=ft.TextButton("Former Data", icon=ft.icons.TABLE_CHART_ROUNDED,
                                               icon_color=ft.colors.DEEP_PURPLE_300,
                                               on_click=lambda _: page.go("/former_data"))
                ),
                ft.NavigationDestination(
                    icon_content=ft.TextButton("Personal Info", icon=ft.icons.SUPERVISED_USER_CIRCLE_ROUNDED,
                                               icon_color=ft.colors.DEEP_PURPLE_300,
                                               on_click=lambda _: page.go("/update_details"))
                ),
            ]
        )
        self.page.navigation_bar = self.user_menu
        # self.guest_menu = ft.NavigationDrawer(
        #     controls=[
        #         ft.Container(height=12),
        #         ft.NavigationDrawerDestination(
        #             icon_content=ft.TextButton(text="Home", icon=ft.icons.HOME, icon_color=ft.colors.BLUE_300, on_click=lambda _:self.page.go("/guest_home")),
        #         ),
        #     ],
        # )
        # self.page.drawer = self.guest_menu

    # def show_menu(self, e):
    #     self.user_menu.open = True
    #     self.page.drawer = self.user_menu
    #     self.page.update()


class GuestAppBar:
    def __init__(self, page: ft.Page):
        self.page = page
        # self.menu = GuestMenu(page)
        # self.menu.menu_text.on_click = self.show_menu
        self.theme_icon = ft.IconButton(icon=ft.icons.WB_SUNNY_OUTLINED, on_click=self.switch_theme, icon_color=ft.colors.WHITE)
        self.hello_guest = ft.TextButton(text="Guest", icon_color=ft.colors.WHITE, disabled=True)
        self.title_text = "2-G2OD"
        self.my_appbar = ft.AppBar(
            leading=self.hello_guest,
            leading_width=100,
            title=ft.Text(
                        spans=
                        [
                            ft.TextSpan(
                                self.title_text,
                                ft.TextStyle(
                                    size=27,
                                    weight=ft.FontWeight.BOLD,
                                    foreground=ft.Paint(
                                        gradient=ft.PaintLinearGradient(
                                            (0, 20),
                                            (750, 20),
                                            [
                                                ft.colors.BLACK,
                                                ft.colors.WHITE
                                            ]
                                        )
                                    )
                                )
                            )
                        ]
                    ),
            color=ft.colors.WHITE,
            center_title=True,
            bgcolor=ft.colors.DEEP_PURPLE_300,
            actions=[
                self.theme_icon,
            ],
        )
        self.page.appbar = self.my_appbar

    def switch_theme(self, e):
        if self.page.theme_mode == "dark":
            self.page.theme_mode = "light"
            self.theme_icon.icon = ft.icons.WB_SUNNY_OUTLINED
            # self.menu.menu_text.icon_color = ft.colors.BLACK
        else:
            self.page.theme_mode = "dark"
            self.theme_icon.icon = ft.icons.MODE_NIGHT_OUTLINED
            # self.menu.menu_text.icon_color = ft.colors.WHITE
        self.page.update()

    # def show_menu(self, e):
    #     self.menu.guest_menu.open = True
    #     self.page.drawer = self.menu.guest_menu
    #     self.page.update()


class UserAppBar:
    def __init__(self, page: ft.Page):
        self.page = page
        # self.menu = UserMenu(page)
        self.theme_icon = ft.IconButton(icon=ft.icons.WB_SUNNY_OUTLINED, on_click=self.switch_theme, icon_color=ft.colors.WHITE)
        self.title_text = "2-G2OD"
        self.popup_button = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.VPN_KEY_OFF, color=ft.colors.DEEP_PURPLE_300),
                            ft.Text("Sign Out", color=ft.colors.DEEP_PURPLE_300),
                        ]
                    ),
                    on_click=self.sign_out,
                ),
            ]
        )

        self.my_appbar = ft.AppBar(
            leading_width=100,
            title=ft.Text(
                        spans=
                        [
                            ft.TextSpan(
                                self.title_text,
                                ft.TextStyle(
                                    size=27,
                                    weight=ft.FontWeight.BOLD,
                                    foreground=ft.Paint(
                                        gradient=ft.PaintLinearGradient(
                                            (0, 20),
                                            (750, 20),
                                            [
                                                ft.colors.BLACK,
                                                ft.colors.WHITE
                                            ]
                                        )
                                    )
                                )
                            )
                        ]
                    ),
            color=ft.colors.WHITE,
            center_title=True,
            bgcolor=ft.colors.DEEP_PURPLE_300,
            actions=[
                self.theme_icon,
                self.popup_button,
            ],
        )

    def switch_theme(self, e):
        if self.page.theme_mode == "dark":
            self.page.theme_mode = "light"
            self.theme_icon.icon = ft.icons.WB_SUNNY_OUTLINED
            # self.menu.menu_text.icon_color = ft.colors.BLACK
        else:
            self.page.theme_mode = "dark"
            self.theme_icon.icon = ft.icons.MODE_NIGHT_OUTLINED
            # self.menu.menu_text.icon_color = ft.colors.WHITE
        self.page.update()

    def sign_out(self, e):
        time.sleep(1)
        self.page.go('/guest_home')


class TableAppBar:
    def __init__(self, page: ft.Page):
        self.page = page
        # self.menu = UserMenu(page)
        self.theme_icon = ft.IconButton(icon=ft.icons.WB_SUNNY_OUTLINED, on_click=self.switch_theme, icon_color=ft.colors.WHITE)
        self.title_text = "2-G2OD"
        self.my_appbar = ft.AppBar(
            leading=ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: self.page.go("/client_kmc"), icon_color=ft.colors.WHITE),
            leading_width=40,
            title=ft.Text(
                        spans=
                        [
                            ft.TextSpan(
                                self.title_text,
                                ft.TextStyle(
                                    size=27,
                                    weight=ft.FontWeight.BOLD,
                                    foreground=ft.Paint(
                                        gradient=ft.PaintLinearGradient(
                                            (0, 20),
                                            (750, 20),
                                            [
                                                ft.colors.BLACK,
                                                ft.colors.WHITE
                                            ]
                                        )
                                    )
                                )
                            )
                        ]
                    ),
            color=ft.colors.WHITE,
            center_title=True,
            bgcolor=ft.colors.DEEP_PURPLE_300,
            actions=[
                self.theme_icon,
            ],
        )

    def switch_theme(self, e):
        if self.page.theme_mode == "dark":
            self.page.theme_mode = "light"
            self.theme_icon.icon = ft.icons.WB_SUNNY_OUTLINED
            # self.menu.menu_text.icon_color = ft.colors.BLACK
        else:
            self.page.theme_mode = "dark"
            self.theme_icon.icon = ft.icons.MODE_NIGHT_OUTLINED
            # self.menu.menu_text.icon_color = ft.colors.WHITE
        self.page.update()


