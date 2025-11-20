# app/data/db.py

import sqlite3
from pathlib import Path
import pandas as pd
import os

# -------------------------------
# DATABASE PATH
# -------------------------------
DB_PATH = Path(__file__).parent.parent / "DATA" / "intelligence_platform.db"


# -------------------------------
# CONNECT TO DATABASE
# -------------------------------
def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database.
    Creates the database file if it doesn't exist.
    
    Args:
        db_path (str or Path): Path to the database file.
        
    Returns:
        sqlite3.Connection: Database connection object
    """
    db_path = Path(db_path)
    if not db_path.parent.exists():
        db_path.parent.mkdir(parents=True)
    return sqlite3.connect(str(db_path))


# -------------------------------
# LOAD CSV TO TABLE
# -------------------------------
def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.
    
    Args:
        conn (sqlite3.Connection): Active database connection
        csv_path (str or Path): Path to the CSV file
        table_name (str): Name of the database table
        
    Returns:
        int: Number of rows loaded (0 if failed)
    """
    csv_path = Path(csv_path)
    
    if not csv_path.exists():
        print(f"❌ CSV file not found: {csv_path}")
        return 0
    
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return 0
    
    try:
        df.to_sql(
            name=table_name,
            con=conn,
            if_exists='append',
            index=False
        )
    except Exception as e:
        print(f"❌ Error loading data into table '{table_name}': {e}")
        return 0
    
    row_count = len(df)
    print(f"✔ Loaded {row_count} rows into '{table_name}'")
    return row_count


# -------------------------------
# LOAD ALL CSV FILES (OPTIONAL HELPER)
# -------------------------------
def load_all_csv_data(conn):
    """
    Load all CSV files in the DATA folder into their respective tables.
    """
    data_dir = Path(__file__).parent.parent / "DATA"
    total_rows = 0

    csv_table_map = {
        "cyber_incidents.csv": "cyber_incidents",
        "it_tickets.csv": "it_tickets",
        "datasets_metadata.csv": "datasets_metadata"
    }

    for csv_file, table in csv_table_map.items():
        csv_path = data_dir / csv_file
        rows = load_csv_to_table(conn, csv_path, table)
        total_rows += rows

    print(f"✔ Total rows loaded from all CSVs: {total_rows}")
    return total_rows
