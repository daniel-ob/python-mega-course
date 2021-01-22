import sqlite3

db_file = "books.db"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS store (id INTEGER PRIMARY KEY, title TEXT, author TEXT, "
                         "year INTEGER, isbn TEXT)")
        self.conn.commit()

    def view(self):
        self.cur.execute("SELECT * FROM store")
        rows = self.cur.fetchall()  # returns a List of Tuples
        return rows

    def search(self, title="", author="", year="", isbn=""):
        self.cur.execute("SELECT * FROM store WHERE title=? OR author=? OR year=? OR isbn=?",
                         (title, author, year, isbn))
        rows = self.cur.fetchall()  # returns a List of Tuples
        return rows

    def insert(self, title, author, year, isbn):
        self.cur.execute("INSERT INTO store VALUES (NULL, ?, ?, ?, ?)", (title, author, year, isbn))
        # id is an auto-incremented value
        self.conn.commit()

    def update(self, id, title, author, year, isbn):
        self.cur.execute("UPDATE store SET title=?, author=?, year=?, isbn=? WHERE id=?",
                         (title, author, year, isbn, id))
        self.conn.commit()

    def delete(self, id):
        self.cur.execute("DELETE FROM store WHERE id=?", (id,))
        self.conn.commit()

    def __end__(self):
        self.conn.close()
