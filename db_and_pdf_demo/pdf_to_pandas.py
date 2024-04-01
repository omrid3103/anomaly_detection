import pdfplumber
import csv

# Open the PDF file
with pdfplumber.open(r"C:\Users\Sharon's PC\PycharmProjects\\anomaly_detection\db_and_pdf_demo\data_table.pdf") as pdf:
    # Initialize an empty list to store table data
    all_tables = []

    # Loop over the first two pages
    for page_number in range(2):
        # Extract text from the current page
        page = pdf.pages[page_number]
        text = page.extract_text()

        # Find the table coordinates (bounding box)
        table_settings = {
            "vertical_strategy": "text",
            "horizontal_strategy": "text",
        }
        table = page.extract_table(table_settings)

        # Append the extracted table data to the list
        all_tables.extend(table)

# Write the extracted table data to a CSV file
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write each row of the combined tables to the CSV file
    for row in all_tables:
        csv_writer.writerow(row)


# r"C:\Users\Sharon's PC\PycharmProjects\\anomaly_detection\db_and_pdf_demo\csv_table"