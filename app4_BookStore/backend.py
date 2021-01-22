import sqlite3

db_file = "lite.db"


def create_table():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS store (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, "
                "isbn TEXT)")
    conn.commit()
    conn.close()


def view():
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM store")
    rows = cur.fetchall()  # returns a List of Tuples
    conn.close()
    return rows


def search(title="", author="", year="", isbn=""):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * FROM store WHERE title=? OR author=? OR year=? OR isbn=?", (title, author, year, isbn))
    rows = cur.fetchall()  # returns a List of Tuples
    conn.close()
    return rows


def insert(title, author, year, isbn):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("INSERT INTO store VALUES (NULL, ?, ?, ?, ?)", (title, author, year, isbn))
    # id is an auto-incremented value
    conn.commit()
    conn.close()


def update(id, title, author, year, isbn):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("UPDATE store SET title=?, author=?, year=?, isbn=? WHERE id=?", (title, author, year, isbn, id))
    conn.commit()
    conn.close()


def delete(id):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("DELETE FROM store WHERE id=?", (id,))
    conn.commit()
    conn.close()


create_table()
# insert("Book1", "Author1", "2001", "2343098450985")
# insert("Book2", "Author2", "2001", "2123112253983")
# Create Dummy DB:
# for i in range(50):
#     insert("Book%s" % i, "Author%s" % i, "19%02d" % i, "%02d34567891123" % i)
# delete(1)
# update(2, "Book_2", "Author_2", "2001", "2343098450985")
# print(view())
# print(search(year="2001"))
