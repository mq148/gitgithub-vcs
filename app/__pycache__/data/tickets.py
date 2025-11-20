import pandas as pd
from app.data.db import connect_database

# -------------------------------
# INSERT A TICKET
# -------------------------------
def insert_ticket(conn, issue, status="Open"):
    """
    Insert a new IT ticket into the database.
    
    Args:
        conn: sqlite3 connection
        issue (str): Description of the issue
        status (str): Status of the ticket (default "Open")
    
    Returns:
        int: ID of the inserted ticket
    """
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO it_tickets (issue, status)
        VALUES (?, ?)
    """, (issue, status))
    conn.commit()
    return cur.lastrowid

# -------------------------------
# GET ALL TICKETS
# -------------------------------
def get_all_tickets(conn):
    """
    Retrieve all IT tickets as a pandas DataFrame.
    
    Returns:
        pd.DataFrame
    """
    try:
        df = pd.read_sql_query("SELECT * FROM it_tickets ORDER BY id DESC", conn)
        return df
    except Exception as e:
        print(f"Error retrieving tickets: {e}")
        return pd.DataFrame()

# -------------------------------
# UPDATE TICKET STATUS
# -------------------------------
def update_ticket_status(conn, ticket_id, new_status):
    """
    Update the status of a ticket.
    """
    cur = conn.cursor()
    cur.execute("UPDATE it_tickets SET status = ? WHERE id = ?", (new_status, ticket_id))
    conn.commit()
    return cur.rowcount

# -------------------------------
# DELETE TICKET
# -------------------------------
def delete_ticket(conn, ticket_id):
    """
    Delete a ticket from the database.
    """
    cur = conn.cursor()
    cur.execute("DELETE FROM it_tickets WHERE id = ?", (ticket_id,))
    conn.commit()
    return cur.rowcount

# -------------------------------
# ANALYTICS EXAMPLE
# -------------------------------
def count_tickets_by_status(conn):
    """
    Count tickets grouped by status.
    """
    query = "SELECT status, COUNT(*) as count FROM it_tickets GROUP BY status ORDER BY count DESC"
    df = pd.read_sql_query(query, conn)
    return df