# app/services/user_service.py

import os
import sqlite3
import bcrypt
from app.data.db import connect_database

# NOTE: these functions accept an optional `conn` parameter.
# If you pass a connection (recommended for bulk ops / tests), they will reuse it
# and will NOT open a new connection, avoiding concurrent locks.

def create_users_table(conn):
    """Ensure users table exists (uses the provided conn)."""
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash BLOB NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


def register_user(username, password, role='user', conn=None):
    """
    Register a new user. If conn is None, will open its own connection.
    Returns: (success: bool, message: str)
    """
    own_conn = False
    try:
        if conn is None:
            conn = connect_database()
            own_conn = True

        create_users_table(conn)
        cur = conn.cursor()

        # hash password (bcrypt returns bytes)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            conn.commit()
            return True, f"User '{username}' registered successfully."
        except sqlite3.IntegrityError:
            return False, f"Username '{username}' already exists."
    except Exception as e:
        return False, f"Error registering user: {e}"
    finally:
        if own_conn and conn:
            conn.close()


def login_user(username, password, conn=None):
    """
    Verify login. Returns (success: bool, message: str)
    """
    own_conn = False
    try:
        if conn is None:
            conn = connect_database()
            own_conn = True

        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = cur.fetchone()

        if row is None:
            return False, "User not found."

        password_hash = row[0]
        # password_hash is stored as bytes; ensure it's bytes
        if isinstance(password_hash, str):
            password_hash = password_hash.encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), password_hash):
            return True, "Login successful."
        else:
            return False, "Incorrect password."
    except Exception as e:
        return False, f"Error logging in: {e}"
    finally:
        if own_conn and conn:
            conn.close()


def migrate_users_from_file(conn=None, file_path="DATA/users.txt"):
    """
    Migrate users from a file into the users table.
    File format: username,password,role (role optional)
    Returns number of users migrated.
    """
    own_conn = False
    migrated = 0
    try:
        if conn is None:
            conn = connect_database()
            own_conn = True

        create_users_table(conn)

        # open file with UTF-8 and ignore undecodable bytes
        if not os.path.exists(file_path):
            print(f"❌ Users file not found: {file_path}")
            return 0

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) < 2:
                    # skip invalid lines
                    continue
                username = parts[0]
                password = parts[1]
                role = parts[2] if len(parts) > 2 else "user"

                success, msg = register_user(username, password, role, conn=conn)
                if success:
                    migrated += 1
        if migrated:
            print(f"✔ Migrated {migrated} users from file '{file_path}'")
        else:
            print("No new users migrated (all users may already exist or file empty).")
        return migrated
    except Exception as e:
        print(f"❌ Error migrating users: {e}")
        return migrated
    finally:
        if own_conn and conn:
            conn.close()
