import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from datetime import datetime, timedelta
import random


transactions_fields_list = ["Food", "Clothing", "Leisure", "Lodging", "Rent", "Taxes", "Insurance", "Utilities", "Transportation", "Pension", "Accessories"]
weights = [0.16, 0.15, 0.15, 0.04, 0.04, 0.04, 0.04, 0.09, 0.17, 0.04, 0.08]


# Function to generate random dates
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_hours = random.randint(0, 24)
    random_minutes = random.randint(0, 60)
    return start_date + timedelta(days=random_days, hours=random_hours, minutes=random_minutes)


def generate_price(field: str) -> float:
    amount = 0.0
    if field == "Food" or field == "Clothing" or field == "Utilities" or field == "Accessories" or field == "Pension" or field == "Insurance":
        amount = round(random.uniform(20, 400), 2)  # Random transaction value
    if field == "Leisure" or field == "Lodging":
        amount = round(random.uniform(500, 1200), 2)
    if field == "Rent":
        amount = 3500.0
    if field == "Taxes":
        amount = round(random.uniform(1500, 2000), 2)
    if field == "Transportation":
        amount = round(random.uniform(5, 40), 2)
    return amount


# Function to generate data for the table
def generate_data(rows):
    data = []
    start_date = datetime.now()
    end_date = start_date + timedelta(days=30)
    for i in range(rows):
        date = random_date(start_date, end_date).strftime('%d/%m-%H:%M')  # Random date
        field: str = random.choices(transactions_fields_list, weights, k=1)[0]  # Random location
        price: float = generate_price(field)  # Random transaction value
        was_card_shown: str = random.choice(["Yes", "No"])  # Was card shown
        row_data = [date, field, price, was_card_shown]
        data.append(row_data)
    return data


# Create data for the table
data = generate_data(200)
print(data)

# Add column headers
data.insert(0, ["Date", "Location", "Transaction", "Was-Card-Shown"])

# Create pandas DataFrame
df = pd.DataFrame(data)

# Create PDF
pdf_filename = "data_table4.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

# Convert DataFrame to list of lists
# table_data = [df.columns.values.tolist()] + df.values.tolist()
table_data = df.values.tolist()

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
