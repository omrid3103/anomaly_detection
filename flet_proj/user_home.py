import flet as ft


def home_view(page):

    def exit_app(e):
        page.window_destroy()

    content = ft.Column(
        [
            # ft.Stack(
            #     [
            #         ft.Image(
            #             src=f"https://www.google.com/url?sa=i&url=https%3A%2F%2Fgithub.com%2Fsaarques%2Fcredit-card-fraud-detection&psig=AOvVaw36lQIGiRMKl-u8F7BNT7nD&ust=1709835673312000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqFwoTCND1i7Gg4IQDFQAAAAAdAAAAABAE",
            #             width=300,
            #             height=300,
            #             fit=ft.ImageFit.CONTAIN,
            #         ),
            #         ft.Row(
            #             [
            #                 ft.Text(
            #                     "Image title",
            #                     color="white",
            #                     size=40,
            #                     opacity=0.5,
            #                 )
            #             ],
            #             alignment=ft.MainAxisAlignment.CENTER,
            #         ),
            #     ],
            #     width=300,
            #     height=300,
            # ),
            ft.Row(
                [
                    ft.Text("Home Page", size=30),
                    ft.IconButton(icon=ft.icons.HOME, icon_size=30)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                [
                    ft.TextButton("Exit", icon=ft.icons.CLOSE, icon_color="red", on_click=exit_app)
                ]
            )
        ]
    )
    return content

