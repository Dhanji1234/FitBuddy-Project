import sqlite3

conn = sqlite3.connect("fitbuddy.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
age INTEGER,
weight INTEGER,
goal TEXT,
intensity TEXT
)
""")

conn.commit()