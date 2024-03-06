import flet as ft



def appbar(page):

    menu = ft.NavigationDrawer(
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                icon_content=ft.TextButton("Home", icon=ft.icons.HOME, icon_color=ft.colors.BLACK, on_click=lambda _: page.go('/home')),
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.TextButton("Sign Up", icon=ft.icons.DOOR_BACK_DOOR, icon_color=ft.colors.BLACK, on_click=lambda _: page.go('/sign_up_flet')),
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.TextButton("Sign In", icon=ft.icons.LOCK_OPEN, icon_color=ft.colors.BLACK, on_click=lambda _: page.go('/authentication_flet')),
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.TextButton("About Us", icon=ft.icons.INFO, icon_color=ft.colors.BLACK, on_click=lambda _: page.go('/index')),
            )
        ],

    )
    page.drawer = menu

    def switch_theme(e):
        if page.theme_mode == "dark":
            page.theme_mode = "light"
        else:
            page.theme_mode = "dark"
        page.update()

    def show_menu(e):
        menu.open = True
        page.drawer = menu
        page.update()

    my_appbar = ft.AppBar(
        leading=ft.TextButton("Menu", icon=ft.icons.MENU, icon_color=ft.colors.BLACK, on_click=show_menu),
        leading_width=40,
        title=ft.Text("Welcome"),
        color=ft.colors.BLACK,
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=switch_theme),
        ],
    )
    return my_appbar






