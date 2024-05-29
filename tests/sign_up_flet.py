import flet as ft
import requests
import time


class SignUP:
    def __init__(self, page: ft.Page, router):
        self.router = router
        self.page = page
        self.details: dict[str, str] = {"username": "", "email": ""}
        self.username_tb = ft.TextField(label="Username", max_lines=1, width=280, hint_text="Enter username here")
        self.email_tb = ft.TextField(label="Email", max_lines=1, width=280, hint_text="Enter email here")
        self.password_tb = ft.TextField(label="Password", password=True, can_reveal_password=True, max_lines=1, width=280, hint_text="Enter password here")
        self.submit_button = ft.ElevatedButton(text="Sign Me Up!", on_click=self.submit_button_clicked, color=ft.colors.DEEP_PURPLE_300)
        self.items = [ self.username_tb, self.email_tb, self.password_tb, self.submit_button]
        self.column = ft.Column(spacing=20, controls=self.items)
        # example_tb2 = ft.TextField(label="Disabled", disabled=True, read_only=True, hint_text="Please enter text here", icon=ft.icons.EMOJI_EMOTIONS, value="First name")

    def submit_button_clicked(self, e):
        result = requests.get("http://127.0.0.1:5555/sign_up",
                              params={"email": self.email_tb.value, "username": self.username_tb.value,
                                      "password": self.password_tb.value}).json()
        user_information = {"email": self.email_tb.value, "username": self.username_tb.value, "password": self.password_tb.value}
        # result = sa.sign_up(self.email_tb.value, self.username_tb.value, self.password_tb.value)
        response = result["response"]
        print(response)
        if response == "Username invalid!":
            self.username_tb.border_color = ft.colors.RED_400
            self.username_tb.value = ''
            self.username_tb.label = response
            self.username_tb.hint_text = "Enter new username here"
            self.email_tb.border_color = ft.colors.SURFACE_VARIANT
            self.password_tb.border_color = ft.colors.SURFACE_VARIANT
            self.email_tb.label = "Email"
            self.password_tb.label = "Password"
        if response == "Invalid email address!" or response == "Account with the same email exists!":
            self.email_tb.border_color = ft.colors.RED_400
            self.email_tb.value = ''
            self.email_tb.label = response
            self.email_tb.hint_text = "Enter new email here"
            self.username_tb.border_color = ft.colors.SURFACE_VARIANT
            self.password_tb.border_color = ft.colors.SURFACE_VARIANT
            self.username_tb.label = "Username"
            self.password_tb.label = "Password"
        if response == "Invalid password!":
            self.password_tb.border_color = ft.colors.RED_400
            self.password_tb.value = ''
            self.password_tb.label = response
            self.password_tb.hint_text = "Enter new password here"
            self.username_tb.border_color = ft.colors.SURFACE_VARIANT
            self.email_tb.border_color = ft.colors.SURFACE_VARIANT
            self.username_tb.label = "Username"
            self.email_tb.label = "Email"
        self.page.update()
        if response == "Signed up successfully!":
            self.details["username"] = self.username_tb.value
            self.details["email"] = self.email_tb.value
            time.sleep(1)
            self.page.go('/user_landing_page')
    # def show_nav_drawer(self, e, page):
    #     nav_drawer.open = True
    #     nav_drawer.update()
    #     page.update()

    def main(self) -> None:
        # page.scroll = ft.ScrollMode.HIDDEN
        # page.auto_scroll = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.add(self.column)
        # self.page.floating_action_button = ft.FloatingActionButton(
        #     icon=ft.icons.ADD, on_click=self.fab_pressed, bgcolor=ft.colors.BLUE_200)


def sign_up_view(page: ft.Page, router) -> SignUP:
    return SignUP(page, router)











