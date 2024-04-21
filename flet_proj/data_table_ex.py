import flet as ft
from db_and_pdf_demo import kmc_controller as kmc_cntrl
import pandas as pd


def main(page: ft.Page):

    controller = kmc_cntrl.KMCController()
    controller.csv_to_dataframe()
    df = controller.df

    columns_names_list = df.columns.tolist()
    columns_list = []
    for i in range(len(columns_names_list)):
        columns_list.append(
            ft.DataColumn(
                ft.Text(columns_names_list[i]),
                on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
            )
        )


    rows_list = []
    for i in range(10):
        rows_list.append(
            ft.DataRow(
                cells=[ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
                selected=True,
                on_select_changed=lambda e: print(f"row select changed: {e.data}"),
            )
        )

    page.add(
        ft.DataTable(
            width=1000,
            bgcolor="yellow",
            border=ft.border.all(2, "red"),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(3, "blue"),
            horizontal_lines=ft.border.BorderSide(1, "green"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.colors.BLACK12,
            heading_row_height=100,
            data_row_color={"hovered": "0x30FF0000"},
            show_checkbox_column=True,
            divider_thickness=0,
            column_spacing=200,
            columns=columns_list,
            # [
            #     ft.DataColumn(
            #         ft.Text("Column 1"),
            #         on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
            #     ),
            #     ft.DataColumn(
            #         ft.Text("Column 2"),
            #         tooltip="This is a second column",
            #         numeric=True,
            #         on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
            #     ),
            # ],
            rows=[
                ft.DataRow(
                    [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1")), ft.DataCell(ft.Text("1")), ft.DataCell(ft.Text("1"))],
                    selected=True,
                    on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                ),
                # ft.DataRow([ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))]),
            ],
        ),
    )

ft.app(target=main)
