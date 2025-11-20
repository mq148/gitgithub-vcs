# user_services.py

import sqlite3
import bcrypt
from app.data.db import connect_database

# ----------------------------
# USER MANAGEMENT FUNCTIONS
# ----------------------------

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


def register_user(username, password, role='user'):
    """
    Register a new user with hashed password.

    Args:
        username (str): Username
        password (str): Plain password
        role (str): Role of the user ('user' or 'admin')

    Returns:
        (bool, str): Success status and message
    """
    try:
        conn = connect_database()
        create_users_table(conn)
        cursor = conn.cursor()

        # Hash the password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("""
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
        """, (username, password_hash, role))

        conn.commit()
        conn.close()
        return True, f"User '{username}' registered successfully."
    except sqlite3.IntegrityError:
        return False, f"Username '{username}' already exists."
    except Exception as e:
        return False, f"Error registering user: {e}"


def login_user(username, password):
    """
    Verify a user's login credentials.

    Args:
        username (str): Username
        password (str): Plain password

    Returns:
        (bool, str): Success status and message
    """
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return False, "User not found."

        password_hash = row[0]
        if bcrypt.checkpw(password.encode('utf-8'), password_hash):
            return True, "Login successful."
        else:
            return False, "Incorrect password."
    except Exception as e:
        return False, f"Error logging in: {e}"


def migrate_users_from_file(conn, file_path="DATA/users.txt"):
    """
    Load users from a file into the database.

    File format: username,password,role
    """
    create_users_table(conn)
    count = 0
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                username, password, role = line.split(",")
                success, msg = register_user(username, password, role)
                if success:
                    count += 1
        print(f"✔ Migrated {count} users from file.")
    except FileNotFoundError:
        print(f"❌ Users file not found: {file_path}")
    except Exception as e:
        print(f"❌ Error migrating users: {e}")

    return count
