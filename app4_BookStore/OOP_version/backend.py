import sqlite3

db_file = "books.db"


class Database:
    def __init__(self):
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS store (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, "
                    "isbn TEXT)")
        conn.commit()
        conn.close()

    def view(self):
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT * FROM store")
        rows = cur.fetchall()  # returns a List of Tuples
        conn.close()
        return rows

    def search(self, title="", author="", year="", isbn=""):
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT * FROM store WHERE title=? OR author=? OR year=? OR isbn=?", (title, author, year, isbn))
        rows = cur.fetchall()  # returns a List of Tuples
        conn.close()
        return rows

    def insert(self, title, author, year, isbn):
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("INSERT INTO store VALUES (NULL, ?, ?, ?, ?)", (title, author, year, isbn))
        # id is an auto-incremented value
        conn.commit()
        conn.close()

    def update(self, id, title, author, year, isbn):
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("UPDATE store SET title=?, author=?, year=?, isbn=? WHERE id=?", (title, author, year, isbn, id))
        conn.commit()
        conn.close()

    def delete(self, id):
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("DELETE FROM store WHERE id=?", (id,))
        conn.commit()
        conn.close()
