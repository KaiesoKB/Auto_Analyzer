import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Generate retail dataset
start_date = datetime(2025, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(100)]

products = ["Widget A", "Widget B", "Widget C", "Widget D"]
regions = ["North", "South", "East", "West"]

data = {
    "Date": dates,
    "Product": [random.choice(products) for _ in range(100)],
    "Sales": [random.randint(800, 1500) for _ in range(100)],
    "Units_Sold": [random.randint(5, 25) for _ in range(100)],
    "Region": [random.choice(regions) for _ in range(100)]
}

retail_df = pd.DataFrame(data)
retail_df.to_csv("sample_data/retail_demo.csv", index=False)
print("Retail demo dataset generated with 100 records.")

# Generate 100 finance dataset
customer_ids = [f"C{str(i).zfill(3)}" for i in range(1, 101)]

data = {
    "Date": [start_date + timedelta(days=i) for i in range(100)],
    "Customer_ID": customer_ids,
    "Loan_Amount": [random.choice([3000, 5000, 7500, 10000, 12000]) for _ in range(100)],
    "Paid_Back": [random.choice([0,1]) for _ in range(100)],
    "Risk_Score": [round(random.uniform(0.05, 0.7), 2) for _ in range(100)]
}

finance_df = pd.DataFrame(data)
finance_df.to_csv("sample_data/finance_demo.csv", index=False)
print("Finance demo dataset generated with 100 records.")

# Generating healthcare dataset
departments = ["ER", "Radiology", "Cardiology", "Oncology", "Pediatrics"]

data = {
    "Date": [start_date + timedelta(days=i) for i in range(100)],
    "Department": [random.choice(departments) for _ in range(100)],
    "Patients_Served": [random.randint(15, 60) for _ in range(100)],
    "Avg_Wait_Time": [random.randint(10, 50) for _ in range(100)],  # in minutes
    "Staff_Count": [random.randint(5, 15) for _ in range(100)]
}

healthcare_df = pd.DataFrame(data)
healthcare_df.to_csv("sample_data/healthcare_demo.csv", index=False)
print("Healthcare demo dataset generated with 100 records.")
