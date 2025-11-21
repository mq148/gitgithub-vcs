# main.py

import os
import pandas as pd
from pathlib import Path

# ----------------------------------------
# DATABASE AND SCHEMA IMPORTS
# ----------------------------------------
from app.data.db import connect_database, load_csv_to_table, load_all_csv_data
from app.data.schema import create_all_tables

# ----------------------------------------
# INCIDENTS IMPORTS
# ----------------------------------------
from app.data.incidents import (
    insert_incident,
    get_all_incidents,
    update_incident_status,
    delete_incident,
    get_incidents_by_type_count,
    get_high_severity_by_status
)

# ----------------------------------------
# USER SERVICES
# (FIXED — correct module name)
# ----------------------------------------
from app.services.user_service import (
    register_user,
    login_user,
    migrate_users_from_file
)

# ----------------------------------------
# INITIAL SETUP
# ----------------------------------------
def initialize_database():
    conn = connect_database()
    print("Connected to database.")

    # Create tables if they don't exist
    create_all_tables(conn)
    print("Tables created.")

    # Load CSV files into tables
    data_dir = Path("DATA")
    load_csv_to_table(conn, data_dir / "cyber_incidents.csv", "cyber_incidents")
    load_csv_to_table(conn, data_dir / "it_tickets.csv", "it_tickets")
    load_csv_to_table(conn, data_dir / "datasets_metadata.csv", "datasets_metadata")
    print("CSV data loaded.")

    # Migrate users from file
    user_count = migrate_users_from_file(conn)
    print(f"Migrated {user_count} users from file.")

    return conn


# ----------------------------------------
# MAIN FUNCTION
# ----------------------------------------
def main():
    conn = initialize_database()

    # Add test incident
    test_id = insert_incident(
        conn,
        "2025-01-01",
        "Test",
        "Low",
        "Open",
        "This is a test",
        "admin"
    )
    print(f"Inserted test incident with ID {test_id}")

    # Show all incidents
    df = get_all_incidents(conn)
    print(df)

    conn.close()


# ----------------------------------------
# DATABASE SETUP SUMMARY
# ----------------------------------------
def setup_database_complete():
    print("\n" + "=" * 60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("=" * 60)

    conn = initialize_database()

    # Show table row counts
    print("\nDatabase Summary:")
    cursor = conn.cursor()
    tables = ['users', 'cyber_incidents', 'datasets_metadata', 'it_tickets']
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table:<25} {count:<10}")

    conn.close()
    print("\nDATABASE SETUP COMPLETE!")


# ----------------------------------------
# RUN TESTS
# ----------------------------------------
def run_comprehensive_tests():
    print("\n" + "=" * 60)
    print("RUNNING COMPREHENSIVE TESTS")
    print("=" * 60)

    conn = connect_database()

    # Test 1 – Authentication
    print("\n[TEST 1] Authentication")
    success, msg = register_user("test_user", "TestPass123!", "user")
    print("Register:", msg)
    success, msg = login_user("test_user", "TestPass123!")
    print("Login:", msg)

    # Test 2 – CRUD
    print("\n[TEST 2] CRUD Operations")
    test_id = insert_incident(
        conn,
        "2024-11-05",
        "Test Incident",
        "Low",
        "Open",
        "This is a test incident",
        "test_user"
    )
    print(f"Created Incident #{test_id}")

    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?",
        conn,
        params=(test_id,)
    )
    print("Read OK")

    update_incident_status(conn, test_id, "Resolved")
    print("Update OK")

    delete_incident(conn, test_id)
    print("Delete OK")

    # Test 3 – Analytics
    print("\n[TEST 3] Analytics")
    df1 = get_incidents_by_type_count(conn)
    print("Incident Types:", len(df1))
    df2 = get_high_severity_by_status(conn)
    print("High Severity:", len(df2))

    conn.close()
    print("\nALL TESTS PASSED!")


# ----------------------------------------
# ENTRY POINT
# ----------------------------------------
if __name__ == "__main__":
    main()
    setup_database_complete()
    run_comprehensive_tests()
