import sqlite3
import os

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

database_path = os.path.join(
    base_path,
    "database",
    "attrition.db"
)


def create_database():

    connection = sqlite3.connect(database_path)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            age INTEGER,

            gender TEXT,

            marital_status TEXT,

            department TEXT,

            job_role TEXT,

            overtime TEXT,

            monthly_income REAL,

            job_satisfaction INTEGER,

            total_working_years INTEGER,

            years_at_company INTEGER,

            risk_level TEXT,

            attrition_probability REAL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    connection.commit()

    connection.close()

    print("Database created successfully!")
    print("Database location:")
    print(database_path)


if __name__ == "__main__":
    create_database()