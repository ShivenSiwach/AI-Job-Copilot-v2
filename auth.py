import sqlite3
import bcrypt
import os

# 1. Create the folder if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# 2. Connect to the database
conn = sqlite3.connect("data/users.db", check_same_thread=False)
cursor = conn.cursor()

# 3. ADD THIS: Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')
conn.commit()

def create_user(username: str, password: str) -> bool:
    """Register a new user. Returns False if username exists."""
    try:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO users VALUES (?, ?)",
            (username, hashed)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username: str, password: str) -> bool:
    """Verify credentials. Returns True if valid."""
    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    if not row:
        return False
    return bcrypt.checkpw(password.encode("utf-8"), row[0])
