import flet as ft



class AppBar:
    def __init__(self, page: ft.Page):
        self.page = page
        self.menu = ft.NavigationDrawer(
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    icon_content=ft.TextButton("Home", icon=ft.icons.HOME, icon_color=ft.colors.BLUE_300, on_click=lambda _: page.go('/home')),
                ),
                ft.NavigationDrawerDestination(
                    icon_content=ft.TextButton("Sign Up", icon=ft.icons.DOOR_BACK_DOOR, icon_color=ft.colors.BLUE_300, on_click=lambda _: page.go('/sign_up_flet')),
                ),
                ft.NavigationDrawerDestination(
                    icon_content=ft.TextButton("Sign In", icon=ft.icons.LOCK_OPEN, icon_color=ft.colors.BLUE_300, on_click=lambda _: page.go('/authentication_flet')),
                ),
                ft.NavigationDrawerDestination(
                    icon_content=ft.TextButton("About Us", icon=ft.icons.INFO, icon_color=ft.colors.BLUE_300, on_click=lambda _: page.go('/index')),
                ),
            ],

        )
        self.page.drawer = self.menu
        self.menu_text = ft.TextButton("Menu", icon=ft.icons.MENU, icon_color=ft.colors.BLACK, on_click=self.show_menu)
        self.theme_icon = ft.IconButton(icon=ft.icons.WB_SUNNY_OUTLINED, on_click=self.switch_theme)
        self.title_text = ft.Text("2-G2OD")
        self.my_appbar = ft.AppBar(
            leading=self.menu_text,
            leading_width=40,
            title=self.title_text,
            color=ft.colors.BLACK,
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                self.theme_icon,
            ],
        )

    def switch_theme(self, e):
        if self.page.theme_mode == "dark":
            self.page.theme_mode = "light"
            self.theme_icon.icon = ft.icons.WB_SUNNY_OUTLINED
            self.theme_icon.icon_color = ft.colors.BLACK
            self.title_text.color = ft.colors.BLACK
            self.menu_text.icon_color = ft.colors.BLACK
        else:
            self.page.theme_mode = "dark"
            self.theme_icon.icon = ft.icons.MODE_NIGHT_OUTLINED
            self.theme_icon.icon_color = ft.colors.WHITE
            self.title_text.color = ft.colors.WHITE
            self.menu_text.icon_color = ft.colors.WHITE
        self.page.update()

    def show_menu(self, e):
        self.menu.open = True
        self.page.drawer = self.menu
        self.page.update()






