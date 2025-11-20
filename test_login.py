# test_login.py

from app.services.users import login_user

# List of users for testing::
test_users = [
    ("jave", "Password123"),
    ("peter", "Stopby123"),
    ("john", "Hlloo8798My"),
    ("dave", "Passby2025"),
    ("eshal", "Secureisit789"),
    ("farhad", "MySecret321")
]

for username, password in test_users:
    success, msg = login_user(username, password)
    if success:
        print(f"✅ {username}: Login successful!")
    else:
        print(f"❌ {username}: Login failed - {msg}")
