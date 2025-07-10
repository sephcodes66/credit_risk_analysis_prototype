"""
This script handles the ETL process for the credit risk data.
It reads the raw data, transforms it, and loads it into a PostgreSQL database.
"""
import os
from dotenv import load_dotenv
import psycopg2
from src.data_processing import read_data, transform_data, feature_engineering

# Load environment variables from .env
load_dotenv()

# Database credentials
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Path to the data file
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'german.data')

def load_to_postgres(df):
    """Connects to PostgreSQL and loads the DataFrame."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()

        # For simplicity, we'll clear the table before each run.
        cur.execute("TRUNCATE TABLE german_credit_data")

        # Insert data row by row
        for _, row in df.iterrows():
            cur.execute(
                """
                INSERT INTO german_credit_data (
                    status_of_existing_checking_account, duration_in_month, credit_history,
                    purpose, credit_amount, savings_account_bonds, present_employment_since,
                    installment_rate_in_percentage_of_disposable_income, personal_status_and_sex,
                    other_debtors_guarantors, present_residence_since, property, age_in_years,
                    other_installment_plans, housing, number_of_existing_credits_at_this_bank,
                    job, number_of_people_being_liable_to_provide_maintenance_for, telephone,
                    foreign_worker, risk
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                tuple(row)
            )

        conn.commit()
        cur.close()
        print("Data loaded successfully into PostgreSQL.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    raw_data = read_data(DATA_PATH)
    transformed_data = transform_data(raw_data)
    featured_data = feature_engineering(transformed_data)
    load_to_postgres(featured_data)
