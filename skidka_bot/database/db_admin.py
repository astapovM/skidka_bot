import sqlite3


def sql_start():
    global base, cur
    base = sqlite3.connect('database/skidka.db')
    cur = base.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id , user_name TEXT, connect_date, FOREIGN KEY (id) REFERENCES packages (user_id) )"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS packages(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id, package_url UNIQUE, package_name, brand_name, old_price FLOAT, "
        "new_price FLOAT)"
    )
    base.commit()


def check_user_in_db(user_id):
    cur.execute(f"SELECT * FROM users WHERE user_id={user_id}")
    return cur.fetchone()


def check_packages(user_id):
    cur.execute(f"SELECT package_url, package_name, brand_name, old_price FROM packages WHERE user_id ={user_id}")
    return cur.fetchall()

