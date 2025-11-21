# app/data/schema.py

from app.data.db import connect_database
import sqlite3

# -------------------------------
# USERS TABLE
# -------------------------------
def create_users_table(conn):
    """
    Create the users table if it doesn't exist.
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("✅ Users table created successfully.")


# -------------------------------
# CYBER INCIDENTS TABLE
# -------------------------------
def create_cyber_incidents_table(conn):
    """
    Create the cyber_incidents table if it doesn't exist.
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            incident_type TEXT,
            severity TEXT,
            status TEXT,
            description TEXT,
            reported_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("✅ Cyber incidents table created successfully.")


# -------------------------------
# DATASETS METADATA TABLE
# -------------------------------
def create_datasets_metadata_table(conn):
    """
    Create the datasets_metadata table if it doesn't exist.
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT NOT NULL,
            category TEXT,
            source TEXT,
            last_updated TEXT,
            record_count INTEGER,
            file_size_mb REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("✅ Datasets metadata table created successfully.")


# -------------------------------
# IT TICKETS TABLE
# -------------------------------
def create_it_tickets_table(conn):
    """
    Create the it_tickets table if it doesn't exist.
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE NOT NULL,
            priority TEXT,
            status TEXT,
            category TEXT,
            subject TEXT NOT NULL,
            description TEXT,
            created_date TEXT,
            resolved_date TEXT,
            assigned_to TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("✅ IT tickets table created successfully.")


# -------------------------------
# CREATE ALL TABLES
# -------------------------------
def create_all_tables(conn):
    """
    Create all tables in the database.
    """
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)
    print("✅ All tables created successfully.")
