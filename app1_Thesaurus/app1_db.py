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


def get_expressions():
    query = cursor.execute("SELECT Expression FROM Dictionary")
    return cursor.fetchall()
    
    
def get_definition(word):
    word = word.lower()
    query = cursor.execute("SELECT * FROM Dictionary WHERE Expression = '%s' " % word)
    results = cursor.fetchall()
    # returns a list of tuples [('Expression', 'Definition1'), ('Expression', 'Definition2'), ...]
    if results:
        return results
    else:
        # find closer matches among dictionary expressions (words)
        expressions = [i[0] for i in get_expressions()]
        if len(get_close_matches(word, expressions)) > 0:
            closest_match = get_close_matches(word, expressions)[0]
            yn = input("Did you mean '%s' instead? [Y/N]: " % closest_match)
            if yn == "Y":
                query = cursor.execute("SELECT * FROM Dictionary WHERE Expression = '%s' " % closest_match)
                results =  cursor.fetchall()
                return results
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

