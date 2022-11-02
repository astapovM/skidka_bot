import sqlite3


def sql_start():
    global base, cur
    base = sqlite3.connect('database/skidka.db')
    cur = base.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id , user_name TEXT, connect_date, discount, FOREIGN KEY (id) REFERENCES packages (user_id) )"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS packages(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id, package_url UNIQUE, package_name, brand_name, old_price FLOAT, "
        "new_price FLOAT)"
    )
    base.commit()


def add_new_user(params):
    cur.execute("INSERT INTO users (user_id, user_name, connect_date) VALUES(?,?,?)", params)
    base.commit()


def add_item_info(params):
    cur.execute("INSERT INTO packages (user_id, package_url, package_name, brand_name, old_price) VALUES(?,?,?,?,?)",
                params)
    base.commit()


def check_user_in_db(user_id):
    cur.execute(f"SELECT * FROM users WHERE user_id={user_id}")
    return cur.fetchone()


def check_packages(user_id):
    cur.execute(f"SELECT id, package_url, package_name, brand_name, old_price FROM packages WHERE user_id ={user_id}")
    return cur.fetchall()

def delete_item_from_db(id):
    cur.execute(f"DELETE from packages WHERE id ={id}")
    base.commit()

def add_discount(user_id, discount):
    cur.execute(f"UPDATE users SET discount ={discount} WHERE user_id = {user_id}")
    base.commit()