# app/services/users.py

import sqlite3
import bcrypt
import os
from app.data.db import connect_database, DATA_DIR

# -----------------------------
# Register a new user
def register_user(username, password, role="user"):
    conn = connect_database()
    c = conn.cursor()

    # Check if user exists
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    if c.fetchone():
        conn.close()
        return False, f"Username '{username}' already exists."

    # Hash the password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    password_hash = hashed.decode('utf-8')

    # Insert user
    c.execute(
        "INSERT INTO users(username, password_hash, role) VALUES(?,?,?)",
        (username, password_hash, role)
    )
    conn.commit()
    conn.close()
    return True, f"User '{username}' registered successfully!"

# -----------------------------
# Login user
def login_user(username, password):
    conn = connect_database()
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()

    if not row:
        return False, "Username not found."

    stored_hash = row[0].encode('utf-8')
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return True, f"Welcome, {username}!"
    else:
        return False, "Incorrect password."

# -----------------------------
# Get all users
def get_all_users():
    conn = connect_database()
    c = conn.cursor()
    c.execute("SELECT id, username, role FROM users")
    users = c.fetchall()
    conn.close()
    return users

# -----------------------------
# Migrate users from users.txt
def migrate_users_from_file(conn=None):
    if conn is None:
        conn = connect_database()
    filepath = DATA_DIR / "users.txt"
    if not os.path.exists(filepath):
        print(f"⚠️ File not found: {filepath}")
        return 0

    cursor = conn.cursor()
    migrated = 0

    with open(filepath, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) < 2 or parts[0].lower() == "username":
                continue  # skip empty or header line
            username, password = parts[0], parts[1]
            # hash the password
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            try:
                cursor.execute(
                    "INSERT OR IGNORE INTO users(username,password_hash,role) VALUES(?,?,?)",
                    (username, hashed, "user")
                )
                if cursor.rowcount > 0:
                    migrated += 1
            except sqlite3.Error as e:
                print(f"Error migrating {username}: {e}")
                continue

    conn.commit()
    print(f"✅ Migrated {migrated} users from {filepath.name}")
    return migrated
