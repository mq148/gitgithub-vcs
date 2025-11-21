# app/data/db.py

import sqlite3
from pathlib import Path
import pandas as pd
import os
import sqlite3

# Path to the database (project root -> DATA/intelligence_platform.db)
DB_PATH = Path(__file__).parent.parent / "DATA" / "intelligence_platform.db"

# Ensure DATA folder exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def connect_database(db_path: Path = DB_PATH):
    """
    Connect to the SQLite database, create file if missing.
    - Use WAL journal mode and a busy timeout to reduce 'database is locked' errors.
    - Set check_same_thread=False to allow multiple connections from different threads (safe for simple apps).
    Returns sqlite3.Connection or raises exception.
    """
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # create connection
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    # improve concurrency and wait on locked DB
    try:
        conn.execute("PRAGMA journal_mode=WAL;")   # write-ahead logging
        conn.execute("PRAGMA busy_timeout = 5000;")  # wait up to 5000ms before failing
    except Exception:
        # If PRAGMA fails for whatever reason, don't crash here — connection still usable
        pass

    return conn


def load_csv_to_table(conn, csv_path, table_name):
    """
    Load a CSV file into a database table using pandas.
    - Skips rows that cause IntegrityError (e.g., unique constraint) and reports them.
    - Uses pandas to read CSV, then inserts using to_sql where possible, falling back to row-by-row inserts
      with error handling when necessary.
    Returns number of rows inserted (approx).
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        print(f"❌ CSV file not found: {csv_path}")
        return 0

    # Read CSV into DataFrame (let pandas do the heavy lifting)
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Error reading CSV '{csv_path}': {e}")
        return 0

    if df.empty:
        print(f"⚠ CSV '{csv_path.name}' is empty.")
        return 0

    # Try bulk insert via to_sql first; if it fails because of integrity constraints, fallback to row-by-row
    try:
        df.to_sql(name=table_name, con=conn, if_exists="append", index=False)
        row_count = len(df)
        print(f"✔ Loaded {row_count} rows into '{table_name}'")
        return row_count
    except Exception as e_bulk:
        # Bulk insert failed (often because of constraint). Fallback to row-by-row to skip bad rows.
        print(f"⚠ Bulk load failed for '{csv_path.name}': {e_bulk}. Falling back to row-by-row insertion.")

    # Row-by-row insertion with basic safety: build a simple INSERT that matches columns available in the DataFrame.
    inserted = 0
    cursor = conn.cursor()

    # Build insert query dynamically
    cols = list(df.columns)
    placeholders = ", ".join(["?"] * len(cols))
    col_names = ", ".join([f'"{c}"' for c in cols])  # quoted to be safe
    insert_sql = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})"

    for idx, row in df.iterrows():
        values = [None if pd.isna(x) else x for x in row.tolist()]
        try:
            cursor.execute(insert_sql, values)
            inserted += 1
        except sqlite3.IntegrityError as ie:
            # likely duplicate or constraint failure - skip and warn
            print(f"⚠ Skipped row {idx} in '{csv_path.name}' due to IntegrityError: {ie}")
            continue
        except sqlite3.OperationalError as oe:
            # table might not exist or other operational error
            print(f"❌ OperationalError inserting row {idx} into '{table_name}': {oe}")
            break
        except Exception as ex:
            print(f"❌ Unexpected error inserting row {idx} into '{table_name}': {ex}")
            continue

    conn.commit()
    print(f"✔ Inserted {inserted} rows into '{table_name}' (row-by-row fallback)")
    return inserted


def load_all_csv_data(conn):
    """
    Load all recognized CSV files in the project's DATA folder into their tables.
    Returns total rows loaded across files.
    """
    data_dir = Path(__file__).parent.parent / "DATA"
    total = 0
    csv_table_map = {
        "cyber_incidents.csv": "cyber_incidents",
        "it_tickets.csv": "it_tickets",
        "datasets_metadata.csv": "datasets_metadata",
    }

    for csv_file, table in csv_table_map.items():
        csv_path = data_dir / csv_file
        rows = load_csv_to_table(conn, csv_path, table)
        total += rows

    print(f"✔ Total rows loaded from CSVs: {total}")
    return total
