# Activity 3:
import bcrypt
import os
USER_DATA_FILE = "users.txt"


# Activity 4:
def hash_password(plain_text_password):
    """Hash a password for storing."""
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)
    return hashed_password

# Activity 5:
def verify_password(plain_text_password, hashed_password):
    """Verify a stored password against one provided by user."""
    # Encode the plaintext password to bytes
    password_bytes = plain_text_password.encode('utf-8')
    # bcrypt.checkpw handles salt extraction and comparison
    return bcrypt.checkpw(password_bytes, hashed_password)

# TEMPORARY TEST CODE - Remove after testing
test_password = "SecurePassword123"

# Test hashing
hashed = hash_password(test_password)
print(f"Original password: {test_password}")
print(f"Hashed password: {hashed}")
print(f"Hash length: {len(hashed)} characters")

# Test verification with correct password
is_valid = verify_password(test_password, hashed)
print(f"\nVerification with correct password: {is_valid}")

# Test verification with incorrect password
is_invalid = verify_password("WrongPassword", hashed)
print(f"Verification with incorrect password: {is_invalid}")

# Activity 7:
def register_user(username, password):
    """
    Step 7. Implement the Registration Function:
    Registers a new user by hashing their password and storing credentials.

    Args:
        username (str): The username for the new account.
        password (str): The plaintext password to hash and store.

    Returns:
        bool: True if registration successful, False if username already exists.
    """
    if user_exists(username):
        return False

    hashed_password = hash_password(password)

    with open("users.txt", "a") as f:
        f.write(f"{username},{hashed_password.decode()}\n")

    return True



# Activity 8:
def user_exists(username):
    """
    Step 8. Implement the User Existence Check:
    Checks if a username already exists in the user file.

    Args:
        username (str): The username to check.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    try:
        with open("users.txt", "r") as f:
            for line in f:
                stored_user, _ = line.strip().split(',', 1)
                if stored_user == username:
                    return True
        return False
    except FileNotFoundError:
        return False

# Activity 9:
def login_user(username, password):
    """
    Step 9. Implement the Login Function:
    Authenticates a user by verifying their username and password.

    Args:
        username (str): The username to authenticate.
        password (str): The plaintext password to verify.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    try:
        with open("users.txt", "r") as f:
            for line in f:
                stored_user, stored_hash = line.strip().split(',', 1)
                if stored_user == username:
                    # Convert stored hash back to bytes
                    stored_hash = stored_hash.encode('utf-8')
                    return verify_password(password, stored_hash)
        return False
    except FileNotFoundError:
        # Handle the case where no users are registered yet
        return False


# Activity 10:
def validate_username(username):
    """
    Validates username format.

    Args:
        username (str): The username to validate.

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not username:
        return False, "Username cannot be empty."
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if not username.isalnum():
        return False, "Username can only contain letters and numbers."
    return True, ""



# Activity 11:
def validate_password(password):
    """
    Validates password strength.

    Args:
        password (str): The password to validate.

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number."
    if not any(c in "!@#$%^&*()-_+=" for c in password):
        return False, "Password must contain at least one special character (!@#$%^&*()-_+=)."
    return True, ""


# Activity 12:
def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)


# Activity 13:
def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Register the user
            if register_user(username, password):
                print(f"User '{username}' successfully registered.")
            else:
                print(f"Error: Username '{username}' already exists.")

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the dashboard.)")
                input("\nPress Enter to return to main menu...")
            else:
                print("Error: Invalid username or password.")

        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()


import bcrypt


def hash_password(plain_text_password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), salt)

def verify_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)

def user_exists(username):
    try:
        with open("users.txt", "r") as f:
            for line in f:
                stored_user, _ = line.strip().split(',', 1)
                if stored_user == username:
                    return True
        return False
    except FileNotFoundError:
        return False

def register_user(username, password):
    if user_exists(username):
        return False
    hashed_password = hash_password(password)
    with open("users.txt", "a") as f:
        f.write(f"{username},{hashed_password.decode()}\n")
    return True

def login_user(username, password):
    try:
        with open("users.txt", "r") as f:
            for line in f:
                stored_user, stored_hash = line.strip().split(',', 1)
                if stored_user == username:
                    stored_hash = stored_hash.encode('utf-8')
                    if verify_password(password, stored_hash):
                        return True
                    else:
                        return "invalid_password"
        return "user_not_found"
    except FileNotFoundError:
        return "user_not_found"

def validate_username(username):
    if not username:
        return False, "Username cannot be empty."
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if not username.isalnum():
        return False, "Username can only contain letters and numbers."
    return True, ""

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number."
    if not any(c in "!@#$%^&*()-_+=" for c in password):
        return False, "Password must contain at least one special character (!@#$%^&*()-_+=)."
    return True, ""

# Step 11: Main Menu

def display_menu():
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            if register_user(username, password):
                print(f"Success: User '{username}' registered successfully!")
            else:
                print(f"Error: Username '{username}' already exists.")

        elif choice == '2':
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            result = login_user(username, password)
            if result == True:
                print(f"Success: Welcome, {username}!")
            elif result == "invalid_password":
                print("Error: Invalid password.")
            else:
                print("Error: Username not found.")

            input("\nPress Enter to return to main menu...")

        elif choice == '3':
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()




# Optional part:
# Challenge 1:
import re

def check_password_strength(password):
    # Step 1: common weak passwords
    common_passwords = ["password", "123456", "qwerty", "letmein", "admin", "welcome"]
    if password.lower() in common_passwords:
        return "Weak"

    # Step 2: Initialize score
    score = 0

    # Step 3: Check length
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1  # bonus for long password

    # Step 4: Character variety
    if re.search(r"[a-z]", password):  # lowercase
        score += 1
    if re.search(r"[A-Z]", password):  # uppercase
        score += 1
    if re.search(r"\d", password):     # digit
        score += 1
    if re.search(r"[^A-Za-z0-9]", password):  # special char
        score += 1

    # Step 5: Evaluate score
    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"
    
# Challenge 2:
def register_user(username, password, role="user"):
    # Open the file in append mode
    with open("users.txt", "a") as file:
        # Write the username, password, and role separated by commas
        file.write(username + "," + password + "," + role + "\n")
    
    print("User '" + username + "' registered successfully with role '" + role + "'.")


# Challange 3:

import time

def login(username, password):
    # Read users
    users = {}
    with open("users.txt", "r") as f:
        for line in f:
            u, p, role = line.strip().split(",")
            users[u] = p  # store only password for simplicity

    # Read locked accounts
    locked_accounts = {}
    try:
        with open("locked.txt", "r") as f:
            for line in f:
                u, unlock_time = line.strip().split(",")
                locked_accounts[u] = float(unlock_time)
    except FileNotFoundError:
        pass

    # Check if account is locked
    if username in locked_accounts:
        if time.time() < locked_accounts[username]:
            print("Account is locked. Try again later.")
            return
        else:
            # Unlock account
            del locked_accounts[username]

    # Track failed attempts (in memory for simplicity)
    failed_attempts = {}

    # Initialize attempt count if first try
    if username not in failed_attempts:
        failed_attempts[username] = 0

    # Check login
    if username in users and users[username] == password:
        print("Login successful!")
        failed_attempts[username] = 0  # reset attempts after success
    else:
        print("Login failed!")
        failed_attempts[username] += 1

        # Lock account after 3 failed attempts
        if failed_attempts[username] >= 3:
            unlock_time = time.time() + 5*60  # 5 minutes lock
            locked_accounts[username] = unlock_time
            print("Account locked for 5 minutes!")

    # Save locked accounts
    with open("locked.txt", "w") as f:
        for u, t in locked_accounts.items():
            f.write(u + "," + str(t) + "\n")



import secrets
import time

def create_session(username):
    # Generate a random token
    token = secrets.token_hex(16)
    
    # Store the token with username and timestamp
    timestamp = time.time()  # current time in seconds
    
    with open("sessions.txt", "a") as f:
        f.write(username + "," + token + "," + str(timestamp) + "\n")
    
    print(f"Session created for {username}!")
    return token

