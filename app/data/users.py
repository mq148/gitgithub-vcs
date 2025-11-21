# app/services/users.py

import sqlite3
import bcrypt
from app.data.db import connect_database

# -------------------------------
# REGISTER USER
# -------------------------------
def register_user(conn, username, password, role="user"):
    """
    Register a new user.

    Args:
        conn: sqlite3.Connection
        username: str
        password: str
        role: str, default 'user'

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        cursor = conn.cursor()
        # Hash password
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        cursor.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
            """,
            (username, password_hash, role)
        )
        conn.commit()
        return True, f"User '{username}' registered successfully."
    except sqlite3.IntegrityError:
        return False, f"Username '{username}' already exists."
    except Exception as e:
        return False, f"Error: {e}"

# -------------------------------
# LOGIN USER
# -------------------------------
def login_user(conn, username, password):
    """
    Authenticate user.

    Args:
        conn: sqlite3.Connection
        username: str
        password: str

    Returns:
        tuple: (success: bool, message: str)
    """
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row is None:
        return False, "Username not found."
    
    password_hash = row[0]
    if bcrypt.checkpw(password.encode("utf-8"), password_hash):
        return True, "Login successful."
    else:
        return False, "Incorrect password."

# -------------------------------
# MIGRATE USERS FROM FILE
# -------------------------------
def migrate_users_from_file(conn, filepath="DATA/users.txt"):
    """
    Load users from a text file into the database.
    File format: username,password,role

    Args:
        conn: sqlite3.Connection
        filepath: str

    Returns:
        int: number of users successfully migrated
    """
    if not os.path.exists(filepath):
        print(f"Users file not found: {filepath}")
        return 0

    count = 0
    with open(filepath, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) < 2:
                continue
            username, password = parts[0], parts[1]
            role = parts[2] if len(parts) > 2 else "user"
            success, _ = register_user(conn, username, password, role)
            if success:
                count += 1
    return count

# -------------------------------
# GET ALL USERS
# -------------------------------
def get_all_users(conn):
    """
    Return a list of all users.

    Args:
        conn: sqlite3.Connection

    Returns:
        list of dict
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    rows = cursor.fetchall()
    return [{"id": r[0], "username": r[1], "role": r[2]} for r in rows]
