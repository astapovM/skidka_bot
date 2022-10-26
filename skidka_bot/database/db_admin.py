import sqlite3

def sql_start():
    global base, cur
    base = sqlite3.connect(r'database\users.db')
    cur = base.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id AUTOINCREMENT, user_id INTEGER PRIMARY KEY, user_name TEXT")