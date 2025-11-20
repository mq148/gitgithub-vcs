import pandas as pd
from app.data.db import connect_database

# -------------------------------
# INSERT NEW DATASET METADATA
# -------------------------------
def insert_dataset(conn, dataset_name, category=None, source=None, last_updated=None, record_count=None, file_size_mb=None):
    """
    Insert a new dataset record into datasets_metadata.
    
    Args:
        conn: sqlite3 connection
        dataset_name (str): Name of the dataset
        category (str, optional): Category, e.g., 'Threat Intelligence'
        source (str, optional): Source of dataset
        last_updated (str, optional): Last updated date 'YYYY-MM-DD'
        record_count (int, optional): Number of records
        file_size_mb (float, optional): File size in MB
    
    Returns:
        int: ID of the inserted dataset
    """
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO datasets_metadata (
            dataset_name, category, source, last_updated, record_count, file_size_mb
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated, record_count, file_size_mb))
    conn.commit()
    return cur.lastrowid

# -------------------------------
# GET ALL DATASETS
# -------------------------------
def get_all_datasets(conn):
    """
    Retrieve all dataset metadata as a pandas DataFrame.
    """
    try:
        df = pd.read_sql_query("SELECT * FROM datasets_metadata ORDER BY id DESC", conn)
        return df
    except Exception as e:
        print(f"Error retrieving datasets: {e}")
        return pd.DataFrame()

# -------------------------------
# UPDATE DATASET METADATA
# -------------------------------
def update_dataset(conn, dataset_id, **kwargs):
    """
    Update dataset metadata fields.
    
    Usage:
        update_dataset(conn, 1, category="New Category", record_count=500)
    """
    fields = ', '.join([f"{k} = ?" for k in kwargs.keys()])
    values = list(kwargs.values())
    values.append(dataset_id)

    cur = conn.cursor()
    sql = f"UPDATE datasets_metadata SET {fields} WHERE id = ?"
    cur.execute(sql, values)
    conn.commit()
    return cur.rowcount

# -------------------------------
# DELETE DATASET
# -------------------------------
def delete_dataset(conn, dataset_id):
    """
    Delete a dataset record.
    """
    cur = conn.cursor()
    cur.execute("DELETE FROM datasets_metadata WHERE id = ?", (dataset_id,))
    conn.commit()
    return cur.rowcount

# -------------------------------
# ANALYTICS EXAMPLES
# -------------------------------
def count_datasets_by_category(conn):
    """
    Count datasets grouped by category.
    """
    query = "SELECT category, COUNT(*) as count FROM datasets_metadata GROUP BY category ORDER BY count DESC"
    df = pd.read_sql_query(query, conn)
    return df