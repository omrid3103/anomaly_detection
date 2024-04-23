import flet as ft


def main(page: ft.Page):
    # MY FAKE DATA
    datax = [
        {"name": "joe", "last": "sumidin", "age": 12},
        {"name": "danr", "last": "sumidin", "age": 12},
        {"name": "soedwo", "last": "sumidin", "age": 12},
        {"name": "michele", "last": "sumidin", "age": 12},
        {"name": "anto", "last": "sumidin", "age": 12},
        {"name": "budi", "last": "sumidin", "age": 12},
        {"name": "gogong", "last": "sumidin", "age": 12},
        {"name": "urip", "last": "sumidin", "age": 12},
        {"name": "uwur", "last": "sumidin", "age": 12},
        {"name": "jaka sumidan", "last": "sumidin", "age": 12},
        {"name": "pedro", "last": "sumidin", "age": 12},

    ]
    print(type(datax))

    dt = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("First name")),
            ft.DataColumn(ft.Text("Last name")),
            ft.DataColumn(ft.Text("Age")),
        ],
        rows=[]

    )

    # PUSH DATA TO DATATABLE
    for x in datax:
        dt.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(x['name'])),
                    ft.DataCell(ft.Text(x['last'])),
                    ft.DataCell(ft.Text(x['age']))
                ]

            )

        )

    def inputsearch(e):
        search_name = nameinput.value.lower()
        # myfiler = list(filter(lambda x: search_name in x['name'].lower(), datax))

        print("you find ", myfiler)
        dt.rows = []

        # IF NO INPUT IN YOU TEXTFIELD SEARCH
        # THEN PUSH THE RESULT TO YOU TABLE
        if not nameinput.value == "":
            # AND IF LENGHT OF RESULT > 0
            if len(myfiler) > 0:
                datanotfound.visible = False
                for x in myfiler:
                    dt.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(x['name'])),
                                ft.DataCell(ft.Text(x['last'])),
                                ft.DataCell(ft.Text(x['age'])),

                            ]

                        )

                    )
                    page.update()
            else:
                print("data not found")
                datanotfound.visible = True
                page.update()

        # IF NO INPUT IN YOU TEXTFIELD
        # THEN PUSH AGAIN DATAX IN YOU DATATABLE
        else:
            datanotfound.visible = False
            page.update()
            for x in datax:
                dt.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(x['name'])),
                            ft.DataCell(ft.Text(x['last'])),
                            ft.DataCell(ft.Text(x['age'])),

                        ]

                    )

                )
            page.update()

    nameinput = ft.TextField(label="Search name",
                          # IF YOU SEARCH NAME THEN RUN FUNCTION
                          on_change=inputsearch

                          )

    # IF DATA NOT FOUND THE SHOW TEXT NOT FOUND
    datanotfound = ft.Text("YOu search Not found...",
                        weight="bold",
                        size=20

                        )

    # SET DEFAULT IS FALSE
    datanotfound.visible = False

    page.add(
        ft.Column([
            nameinput,
            dt,
            datanotfound

        ])

    )


ft.app(target=main)

