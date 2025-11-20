import pandas as pd
from app.data.db import connect_database

# -------------------------------
# INSERT NEW INCIDENT
# -------------------------------
def insert_incident(conn, date, incident_type, severity, status, description, reported_by=None):
    """
    Insert a new cyber incident into the database.

    Args:
        conn: sqlite3.Connection
        date (str): Incident date YYYY-MM-DD
        incident_type (str)
        severity (str)
        status (str)
        description (str)
        reported_by (str, optional)

    Returns:
        int: ID of the inserted incident
    """
    cur = conn.cursor()
    sql = """
    INSERT INTO cyber_incidents (
        date, incident_type, severity, status, description, reported_by
    ) VALUES (?, ?, ?, ?, ?, ?)
    """
    cur.execute(sql, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    return cur.lastrowid

# -------------------------------
# GET ALL INCIDENTS
# -------------------------------
def get_all_incidents(conn):
    """
    Retrieve all incidents from the database.
    Returns:
        pd.DataFrame: All incidents ordered by ID descending
    """
    try:
        df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY id DESC", conn)
        return df
    except Exception as e:
        print(f"Error retrieving incidents: {e}")
        return pd.DataFrame()

# -------------------------------
# UPDATE INCIDENT STATUS
# -------------------------------
def update_incident_status(conn, incident_id, new_status):
    """
    Update the status of an incident.
    
    Args:
        conn: sqlite3.Connection
        incident_id: int
        new_status: str

    Returns:
        int: number of rows updated
    """
    cur = conn.cursor()
    cur.execute("UPDATE cyber_incidents SET status = ? WHERE id = ?", (new_status, incident_id))
    conn.commit()
    return cur.rowcount

# -------------------------------
# DELETE INCIDENT
# -------------------------------
def delete_incident(conn, incident_id):
    """
    Delete an incident from the database.
    
    Args:
        conn: sqlite3.Connection
        incident_id: int

    Returns:
        int: number of rows deleted
    """
    cur = conn.cursor()
    cur.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()
    return cur.rowcount

# -------------------------------
# ANALYTICS FUNCTIONS
# -------------------------------
def get_incidents_by_type_count(conn):
    """
    Count incidents by type.
    Returns a DataFrame with columns: incident_type, count
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)

def get_high_severity_by_status(conn):
    """
    Count high severity incidents by status.
    Returns a DataFrame with columns: status, count
    """
    query = """
    SELECT status, COUNT(*) as count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)

def get_incident_types_with_many_cases(conn, min_count=5):
    """
    Find incident types with more than min_count cases.
    
    Args:
        conn: sqlite3.Connection
        min_count: int, threshold for cases

    Returns:
        pd.DataFrame
    """
    query = """
    SELECT incident_type, COUNT(*) as count
    FROM cyber_incidents
    GROUP BY incident_type
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn, params=(min_count,))