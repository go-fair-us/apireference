import lancedb
import pandas as pd
import numpy as np
import argparse
from faker import Faker
import random

def generate_data(num_rows):
    fake = Faker()
    data = []

    # Define trial arms
    arms = ['Placebo', 'Low_Dose_5mg', 'High_Dose_10mg']
    statuses = ['Completed', 'Active', 'Withdrawn']

    for _ in range(num_rows):
        # Logic to make Efficacy Score slightly higher for "High_Dose"
        arm = random.choice(arms)
        if arm == 'High_Dose_10mg':
            efficacy = random.randint(6, 10)
        elif arm == 'Low_Dose_5mg':
            efficacy = random.randint(4, 8)
        else:
            efficacy = random.randint(1, 5)

        row = {
            "Subject_ID": f"SUBJ-{fake.unique.random_number(digits=5)}",
            "Site_ID": f"SITE-{random.randint(1, 10)}",
            "Age": random.randint(18, 85),
            "Gender": random.choice(['Male', 'Female']),
            "Ethnicity": random.choice(['Hispanic', 'Caucasian', 'African American', 'Asian', 'Other']),
            "City": fake.city(),
            "Arm": arm,
            "Enrollment_Date": fake.date_between(start_date='-2y', end_date='today').isoformat(),
            "Status": random.choice(statuses),
            "Weight_kg": round(random.uniform(50.0, 110.0), 1),
            "Systolic_BP": random.randint(110, 160),
            "Biomarker_Level": round(random.uniform(0.1, 5.5), 2),
            "Adverse_Event": random.random() < 0.15, # 15% chance of AE
            "Efficacy_Score": efficacy
        }
        data.append(row)

    return pd.DataFrame(data)

def save_to_lancedb(df, db_path="./clinical_trials_db", table_name="trials"):
    # Connect to local LanceDB
    db = lancedb.connect(db_path)

    # Create or overwrite the table
    tbl = db.create_table(table_name, data=df, mode="overwrite")
    print(f"Successfully saved {len(df)} rows to LanceDB table: '{table_name}'")
    print(f"Database location: {db_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate mock clinical trial data and save to LanceDB.")
    parser.add_argument(
        "--rows",
        type=int,
        default=100,
        help="Number of rows to generate (default: 100)"
    )

    args = parser.parse_args()

    print(f"Generating {args.rows} rows of mock data...")
    mock_df = generate_data(args.rows)

    save_to_lancedb(mock_df)
