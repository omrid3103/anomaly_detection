import flet as ft
import sign_authentication as sa
from typing import Union
import datetime


class App:
    def __init__(self):
        self.page: Union[ft.Page, None] = None

        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.PALETTE),
            leading_width=40,
            title=ft.Text("To-Do"),
            color=ft.colors.BLACK,
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=self.switch_theme, ),
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
        self.email_tb = ft.TextField(label="Email", max_lines=1, width=280, hint_text="Enter email here")
        self.username_tb = ft.TextField(label="Username", max_lines=1, width=280, hint_text="Enter username here")
        self.password_tb = ft.TextField(label="Password", password=True, can_reveal_password=True, max_lines=1, width=280, hint_text="Enter password here")
        self.submit_button = ft.ElevatedButton(text="Submit", on_click=self.button_clicked)
        self.items = [self.email_tb, self.username_tb, self.password_tb, self.submit_button]
        self.column = ft.Column(spacing=20, controls=self.items)


        # example_tb2 = ft.TextField(label="Disabled", disabled=True, read_only=True, hint_text="Please enter text here", icon=ft.icons.EMOJI_EMOTIONS, value="First name")
        self.date_picker = ft.DatePicker(
            on_change=self.change_date,
            on_dismiss=self.date_picker_dismissed,
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )
        self.date_button = ft.ElevatedButton(
            "Pick date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: self.date_picker.pick_date(),
        )


    def switch_theme(self, e):
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.appbar.color = ft.colors.WHITE
            self.page.floating_action_button.bgcolor = ft.colors.BLUE_900
        elif self.page.theme_mode == ft.ThemeMode.DARK:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.appbar.color = ft.colors.BLACK
            self.page.floating_action_button.bgcolor = ft.colors.BLUE_200
        self.page.update()

    # def check_item_clicked(self, e):
    #     e.control.checked = not e.control.checked
    #     self.page.update()

    def fab_pressed(self, e):
        # date = creating a date-picker that is going to set the date in a datetime object, convert it to string
        # name = creating an entry that is going to receive the task's name
        # description = creating an entry that is going to receive the task's description
        # self.add_task(date, name, description)
        pass

    def button_clicked(self, e):
        result = sa.sign_up(self.email_tb.value, self.username_tb.value, self.password_tb.value)
        result = ft.Text(result["response"])
        self.page.add(result)
        for i in self.items:
            i.value = ''
        self.page.update()

    def change_date(self, e):
        print(f"Date picker changed, value is {self.date_picker.value}")

    def date_picker_dismissed(self, e):
        print(f"Date picker dismissed, value is {self.date_picker.value}")

    def main(self, page: ft.Page) -> None:
        self.page = page
        # page.scroll = ft.ScrollMode.HIDDEN
        # page.auto_scroll = True

        self.page.appbar = self.appbar
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.overlay.append(self.date_picker)
        self.page.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.ADD, on_click=self.fab_pressed, bgcolor=ft.colors.BLUE_200)

        self.page.add(self.column)




def main() -> None:
    ft.app(target=App().main)


if __name__ == "__main__":
    main()