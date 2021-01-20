import sqlite3

db_file = "lite.db"


def create_table():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS store (title TEXT, author TEXT, year INTEGER, isbn INTEGER)")
    conn.commit()
    conn.close()


def view():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM store")
    rows = cur.fetchall()  # returns a List of Tuples
    conn.close()
    return rows


def search(title, author, year, isbn):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM store WHERE title=? OR author=? OR year=? OR isbn=?", (title, author, year, isbn))
    rows = cur.fetchall()  # returns a List of Tuples
    conn.close()
    return rows


def insert(title, author, year, isbn):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("INSERT INTO store VALUES (?, ?, ?, ?)", (title, author, year, isbn))
    conn.commit()
    conn.close()


def update(title, author, year, isbn):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("UPDATE store SET author=?, year=?, isbn=? WHERE title=?", (author, year, isbn, title))
    conn.commit()
    conn.close()


def delete(title):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("DELETE FROM store WHERE title=?", (title,))
    conn.commit()
    conn.close()


create_table()
insert("Book1", "Author1", "2001", "2343098450985")
insert("Book2", "Author2", "2020", "2123112253983")
# delete("Book1")
# update("Book1", "Author2", "2001", "2343098450985")
# print(view())
# print(search("Book1", "", "", ""))
print(search("", "", "", "2123112253983"))
