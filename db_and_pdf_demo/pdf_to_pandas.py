import pdfplumber
import csv
import pandas as pd

PDF_FILE_PATH = r"C:\Users\Sharon's PC\PycharmProjects\\anomaly_detection\db_and_pdf_demo\data_table.pdf"
CSV_FILE_PATH = r"C:\Users\Sharon's PC\PycharmProjects\anomaly_detection\db_and_pdf_demo\output.csv"


def pdf_to_csv(pdf_file_path: str) -> None:
    # Open the PDF file
    with pdfplumber.open(pdf_file_path) as pdf:
        # Initialize an empty list to store table data
        all_table_data = []

        # Loop over the first two pages
        for page_number in range(2):
            # Extract text from the current page
            page = pdf.pages[page_number]
            text = page.extract_text()

            # Split the text into lines
            lines = text.split('\n')

            # Identify the start and end indices of the table
            start_index = end_index = None
            for i, line in enumerate(lines):
                if "header_row" in line.lower():  # Assuming some keyword identifying the header row
                    start_index = i + 1
                elif start_index is not None and not line.strip():  # Empty line signifies end of table
                    end_index = i
                    break

            # Extract the table data for the current page
            table_data = []
            for line in lines[start_index:end_index]:
                # Use a smarter way to split line into columns
                columns = [col.strip() for col in line.split(' ') if col.strip()]
                table_data.append(columns)

            # Append the table data to the list
            all_table_data.extend(table_data)

    # Write the combined table data to a CSV file
    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(all_table_data)

    # Write the combined table data to a CSV file
    with open('output.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(all_table_data)

    # Write the combined table data to a CSV file
    with open('output.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(all_table_data)


def csv_to_dataframe(csv_file_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_file_path)
    return df


def main():
    # pdf_to_csv()
    df: pd.DataFrame = csv_to_dataframe(CSV_FILE_PATH)
    print(df)


if __name__ == "__main__":
    main()




