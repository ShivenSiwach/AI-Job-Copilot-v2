import os
import sqlite3

os.makedirs("data", exist_ok=True)

conn   = sqlite3.connect("data/users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS profiles (
    username  TEXT PRIMARY KEY,
    education TEXT,
    skills    TEXT,
    experience TEXT,
    role      TEXT,
    location  TEXT,
    FOREIGN KEY (username) REFERENCES users(username)
)""")

conn.commit()
conn.close()
print("✅ Database initialised at data/users.db")