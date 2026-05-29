import sqlite3
import bcrypt
import os

if not os.path.exists("data"):
    os.makedirs("data")

conn = sqlite3.connect("data/users.db", check_same_thread=False)
cursor = conn.cursor()

# 1. Create the login table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')

# 2. Create the profile table with the CORRECT 6 columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_profiles (
        username TEXT PRIMARY KEY,
        education TEXT,
        skills TEXT,
        experience TEXT,
        role TEXT,
        location TEXT
    )
''')
conn.commit()

def create_user(username: str, password: str) -> bool:
    try:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        cursor.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username: str, password: str) -> bool:
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if not row:
        return False
    return bcrypt.checkpw(password.encode("utf-8"), row[0])
