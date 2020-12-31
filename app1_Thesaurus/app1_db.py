import mysql.connector
from difflib import get_close_matches

con = mysql.connector.connect(
user = "ardit700_student",
password = "ardit700_student",
host = "108.167.140.122",
database = "ardit700_pm1database"
)
# DB have two columns: "Expression" and "Definition"

cursor = con.cursor()


def db_get_expressions():
    query = cursor.execute("SELECT Expression FROM Dictionary")
    return [i[0] for i in cursor.fetchall()]


def db_get_definition(word):
    query = cursor.execute("SELECT * FROM Dictionary WHERE Expression = '%s' " % word)
    return cursor.fetchall()


def get_definition(word):
    word = word.lower()
    results = db_get_definition(word)
    # returns a list of tuples [('Expression', 'Definition1'), ('Expression', 'Definition2'), ...]
    if results:
        return results
    elif db_get_definition(word.title()):  # for proper names (like "Paris")
        return db_get_definition(word.title())
    elif db_get_definition(word.upper()):  # for acronyms (like "NATO")
        return db_get_definition(word.upper())
    else:
        # find closer matches among dictionary expressions (words)
        expressions = db_get_expressions() 
        if len(get_close_matches(word, expressions)) > 0:
            closest_match = get_close_matches(word, expressions)[0]
            yn = input("Did you mean '%s' instead? [Y/N]: " % closest_match)
            if yn == "Y":
                return db_get_definition(closest_match)
            else:
                return None
        else:
            return None


word = input("Enter a word: ")

results = get_definition(word)

if results:
    for result in results:
        print(result[1])  # print only Definition
else:
    print("Word not found")

