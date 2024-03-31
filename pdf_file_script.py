import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from datetime import datetime, timedelta
import random


transactions_fields_list = ["Food", "Clothing", "Leisure", "Lodging", "Rent", "Taxes", "Insurance", "Utilities", "Transportation", "Pension", "Accessories"]
weights = [0.13, 0.19, 0.2, 0.05, 0.01, 0.02, 0.02, 0.10, 0.18, 0.02, 0.08]


# Function to generate random dates
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


# Function to generate data for the table
def generate_data(rows):
    data = []
    amount = 0.0
    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)
    for i in range(rows):
        row_data = [
            i + 1,  # Counting index
            random_date(start_date, end_date).strftime('%d/%m %H:%M'),  # Random date
            random.choices(transactions_fields_list, weights, k=1),  # Random location
        ]
        if row_data[2] == "Food" or row_data[2] == "Clothing" or row_data[2] == "Utilities" or row_data[2] == "Accessories" or row_data[2] == "Pension" or row_data[2] == "Insurance":
            amount = round(random.uniform(20, 400), 2)  # Random transaction value
        if row_data[2] == "Leisure" or row_data[2] == "Lodging":
            amount = round(random.uniform(500, 1200), 2)
        if row_data[2] == "Rent":
            amount = 3500.0
        if row_data[2] == "Taxes":
            amount = round(random.uniform(1500, 2000), 2)
        if row_data[2] == "Transportation":
            amount = round(random.uniform(5, 40), 2)
        row_data.append(amount)
        row_data.append(random.choice(["Yes", "No"]))  # Was card shown
        data.append(row_data)
    return data


# Create data for the table
data = generate_data(100)

# Add column headers
data.insert(0, ["Counting Index", "Date", "Location", "Transaction", "Was Card Shown"])

# Create pandas DataFrame
df = pd.DataFrame(data)

# Create PDF
pdf_filename = "data_table.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

# Convert DataFrame to list of lists
table_data = [df.columns.values.tolist()] + df.values.tolist()

# Create table
table = Table(table_data)

# Add style to table
style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ])
table.setStyle(style)

# Build PDF
doc.build([table])
