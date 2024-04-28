import flet as ft
import requests
import time
from typing import Union


class SignUp:
    def __init__(self, page: ft.Page, url: str):
        self.details: dict[str, str] = {"username": "", "email": "", "password": ""}
        self.page = page
        self.request_url = url
        self.username_tb = ft.TextField(label="Username", max_lines=1, width=280, hint_text="Enter username here")
        self.email_tb = ft.TextField(label="Email", max_lines=1, width=280, hint_text="Enter email here", keyboard_type=ft.KeyboardType.EMAIL)
        self.password_tb = ft.TextField(label="Password", password=True, can_reveal_password=True, max_lines=1, width=280, hint_text="Enter password here")
        self.submit_button = ft.ElevatedButton(text="Sign Me Up!", color=ft.colors.BLUE_300, on_click=self.sign_up_button_clicked)
        self.items = [self.username_tb, self.email_tb, self.password_tb, self.submit_button]
        self.column = ft.Column(spacing=20, controls=self.items)
        # example_tb2 = ft.TextField(label="Disabled", disabled=True, read_only=True, hint_text="Please enter text here", icon=ft.icons.EMOJI_EMOTIONS, value="First name")

    def sign_up_button_clicked(self, e):
        result = requests.get(f"{self.request_url}sign_up",
                              params={"email": self.email_tb.value, "username": self.username_tb.value, "password": self.password_tb.value}).json()
        user_information = {"email": self.email_tb.value, "username": self.username_tb.value, "password": self.password_tb.value}
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
            self.details["password"] = self.password_tb.value
            time.sleep(1)
            self.page.go('/user_home')

    def main(self) -> None:
        # page.scroll = ft.ScrollMode.HIDDEN
        # page.auto_scroll = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.add(self.column)
        # self.page.floating_action_button = ft.FloatingActionButton(
        #     icon=ft.icons.ADD, on_click=self.fab_pressed, bgcolor=ft.colors.BLUE_200)


class SignIn:
    def __init__(self, page, url):
        self.details: dict[str, str] = {"username": "", "email": "", "password": ""}
        self.page = page
        self.request_url = url
        self.username_tb = ft.TextField(label="Username", max_lines=1, width=280, hint_text="Enter username here", value="Sxd3306")
        self.email_tb = ft.TextField(label="Email", max_lines=1, width=280, hint_text="Enter email here", keyboard_type=ft.KeyboardType.EMAIL, value="shadag71@gmail.com")
        self.password_tb = ft.TextField(label="Password", password=True, can_reveal_password=True, max_lines=1, width=280, hint_text="Enter password here", value="79741BSN")
        self.submit_button = ft.ElevatedButton(text="Sign Me In!", color=ft.colors.BLUE_300, on_click=self.sign_in_button_clicked)
        self.items = [self.username_tb, self.email_tb, self.password_tb, self.submit_button]
        self.column = ft.Column(spacing=20, controls=self.items)
        # example_tb2 = ft.TextField(label="Disabled", disabled=True, read_only=True, hint_text="Please enter text here", icon=ft.icons.EMOJI_EMOTIONS, value="First name")


    def sign_in_button_clicked(self, e):
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
            result = requests.get(f"{self.request_url}authenticate",
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
                self.details["password"] = self.password_tb.value
                time.sleep(1)
                self.page.go('/user_home')
        self.page.update()


    def main(self) -> None:
        # page.scroll = ft.ScrollMode.HIDDEN
        # page.auto_scroll = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.add(self.column)
        # self.page.floating_action_button = ft.FloatingActionButton(
        #     icon=ft.icons.ADD, on_click=self.fab_pressed, bgcolor=ft.colors.BLUE_200)


class UpdateDetails:
    def __init__(self, page: ft.Page, username: str, email: str, password: str, url):
        self.details: dict[str, str] = {"username": username, "email": email, "password": password}
        self.page = page
        self.request_url = url
        self.title_text = ft.Text("Update Your Information, " + self.details["username"] + "")
        self.alert_message = ft.Text("No Detail Has Been Changed", color=ft.colors.RED_400)
        self.username_tb = ft.TextField(label="Username", max_lines=1, width=280, hint_text="Enter username here", value=self.details["username"], disabled=True)
        self.email_tb = ft.TextField(label="Email", max_lines=1, width=280, hint_text="Enter email here", keyboard_type=ft.KeyboardType.EMAIL, value=self.details["email"])
        self.password_tb = ft.TextField(label="Password", password=True, can_reveal_password=True, max_lines=1, width=280, value=self.details["password"])
        self.submit_button = ft.ElevatedButton(text="Update Details!", color=ft.colors.BLUE_300, on_click=self.update_details)
        self.items = [self.title_text, self.username_tb, self.email_tb, self.password_tb, self.submit_button]
        self.column = ft.Column(spacing=20, controls=self.items)
        # example_tb2 = ft.TextField(label="Disabled", disabled=True, read_only=True, hint_text="Please enter text here", icon=ft.icons.EMOJI_EMOTIONS, value="First name")

    def update_details(self, e):
        if self.username_tb.value == self.details["username"] and self.email_tb.value == self.details["email"] and self.password_tb.value == self.details["password"]:
            self.items.append(self.alert_message)
            self.column.controls = self.items
            self.page.update()
        else:
            result = requests.get(f"{self.request_url}update_information",
                                  params={"old_username": self.details["username"], "new_username": self.username_tb.value, "new_email": self.email_tb.value,
                                          "new_password": self.password_tb.value}).json()
            response = result["response"]
            print(response)
            if response == "Invalid email address!" or response == "Account with the same email exists!":
                self.email_tb.border_color = ft.colors.RED_400
                self.email_tb.value = self.details["email"]
                self.email_tb.label = response
                # self.email_tb.hint_text = self.details["email"]
                self.username_tb.border_color = ft.colors.SURFACE_VARIANT
                self.password_tb.border_color = ft.colors.SURFACE_VARIANT
                self.username_tb.label = "Username"
                self.password_tb.label = "Password"
            if response == "Invalid password!":
                self.password_tb.border_color = ft.colors.RED_400
                self.password_tb.value = self.details["password"]
                self.password_tb.label = response
                # self.password_tb.hint_text = self.details["password"]
                self.username_tb.border_color = ft.colors.SURFACE_VARIANT
                self.email_tb.border_color = ft.colors.SURFACE_VARIANT
                self.username_tb.label = "Username"
                self.email_tb.label = "Email"
            self.page.update()
            if response == "Details Updated Successfully!":
                self.details = {"email": self.email_tb.value, "username": self.username_tb.value,
                                "password": self.password_tb.value}

                self.alert_message = ft.Text("Your Details Have Been Updated!", color=ft.colors.GREEN_300)
                self.items.append(self.alert_message)
                self.column.controls = self.items
                # self.page.update()
                # self.username_tb.value = self.details["username"]
                # self.email_tb.value = self.details["email"]
                # self.password_tb.value = self.details["password"]
                self.details.update()
                self.title_text.update()
                self.email_tb.value = self.details["email"]
                self.email_tb.update()
                self.password_tb.value = self.details["password"]
                self.password_tb.update()
                self.column.update()
                self.page.update()
                time.sleep(1)
                self.page.go("/guest_home")
            # need to check if the new details aren't similar to any other clients



    def main(self) -> None:
        # page.scroll = ft.ScrollMode.HIDDEN
        # page.auto_scroll = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.add(self.column)
        # self.page.floating_action_button = ft.FloatingActionButton(
        #     icon=ft.icons.ADD, on_click=self.fab_pressed, bgcolor=ft.colors.BLUE_200)










