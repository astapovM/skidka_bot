import sqlite3


def sql_start():
    global base, cur
    base = sqlite3.connect('database/skidka.db')
    cur = base.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users(user_id PRIMARY KEY, user_name TEXT, connect_date )"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS packages(id , package_url TEXT, old_price FLOAT, "
        "new_price FLOAT, amount INT)"
    )
    base.commit()


def check_user_in_db(user_id):
    cur.execute(f"SELECT * FROM users WHERE user_id={user_id}")
    return cur.fetchone()

def add_package_url(user_id, data):
    cur.execute("""INSERT INTO packages(id, package_url) VALUES(?,?)""",f"({user_id},{data['url']})")
