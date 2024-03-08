import flet as ft
import requests
import time
from typing import Union


class Authentication:
    def __init__(self, page, router):
        self.details: dict[str, str] = {"username": "", "email": ""}
        self.router = router
        self.page = page
        self.username_tb = ft.TextField(label="Username", max_lines=1, width=280, hint_text="Enter username here")
        self.email_tb = ft.TextField(label="Email", max_lines=1, width=280, hint_text="Enter email here")
        self.password_tb = ft.TextField(label="Password", password=True, can_reveal_password=True, max_lines=1, width=280, hint_text="Enter password here")
        self.submit_button = ft.ElevatedButton(text="Sign Me In!", on_click=self.submit_button_clicked)
        self.items = [self.username_tb, self.email_tb, self.password_tb, self.submit_button]
        self.column = ft.Column(spacing=20, controls=self.items)
        # example_tb2 = ft.TextField(label="Disabled", disabled=True, read_only=True, hint_text="Please enter text here", icon=ft.icons.EMOJI_EMOTIONS, value="First name")

    def submit_button_clicked(self, e):
        flag = True
        if self.username_tb.value == "":
            self.username_tb.border_color = ft.colors.RED_400
            self.username_tb.value = ''
            self.username_tb.label = "Username wasn't given"
            self.username_tb.hint_text = "Enter new username here"
            flag = False
        else:
            self.username_tb.border_color = ft.colors.SURFACE_VARIANT
            self.username_tb.label = "Username"
        if self.email_tb.value == "":
            self.email_tb.border_color = ft.colors.RED_400
            self.email_tb.value = ''
            self.email_tb.label = "Email wasn't given"
            self.email_tb.hint_text = "Enter new Email here"
            flag = False
        else:
            self.email_tb.border_color = ft.colors.SURFACE_VARIANT
            self.email_tb.label = "Email"
        if self.password_tb.value == "":
            self.password_tb.border_color = ft.colors.RED_400
            self.password_tb.value = ''
            self.password_tb.label = "password wasn't given"
            self.password_tb.hint_text = "Enter new password here"
            flag = False
        else:
            self.password_tb.border_color = ft.colors.SURFACE_VARIANT
            self.password_tb.label = "Password"
        if flag:
            result = requests.get("http://127.0.0.1:5555/authenticate",
                            params={"email": self.email_tb.value, "username": self.username_tb.value, "password": self.password_tb.value}).json()
            response = result["response"]
            print(response)
            if response == "Username doesnt exist!":
                self.username_tb.border_color = ft.colors.RED_400
                self.username_tb.value = ''
                self.username_tb.label = response
                self.username_tb.hint_text = "Enter new username here"
            else:
                self.username_tb.border_color = ft.colors.SURFACE_VARIANT
                self.username_tb.label = "Username"
            if response == "Invalid email!":
                self.email_tb.border_color = ft.colors.RED_400
                self.email_tb.value = ''
                self.email_tb.label = response
                self.email_tb.hint_text = "Enter new email here"
            else:
                self.email_tb.border_color = ft.colors.SURFACE_VARIANT
                self.email_tb.label = "Email"
            if response == "Not matching password!":
                self.password_tb.border_color = ft.colors.RED_400
                self.password_tb.value = ''
                self.password_tb.label = "Not matching password"
                self.password_tb.hint_text = "Enter new password here"
                flag = False
            else:
                self.password_tb.border_color = ft.colors.SURFACE_VARIANT
                self.password_tb.label = "Password"
            if response == "Signing in...":
                self.details["username"] = self.username_tb.value
                self.details["email"] = self.email_tb.value
                time.sleep(1)
                self.page.go('/user_landing_page')
        self.page.update()
        # redirect to another page

    def main(self) -> None:
        # page.scroll = ft.ScrollMode.HIDDEN
        # page.auto_scroll = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.add(self.column)
        # self.page.floating_action_button = ft.FloatingActionButton(
        #     icon=ft.icons.ADD, on_click=self.fab_pressed, bgcolor=ft.colors.BLUE_200)


def authentication_view(page: ft.Page, router):
    return Authentication(page, router)










