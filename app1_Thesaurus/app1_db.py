import mysql.connector

con = mysql.connector.connect(
user = "ardit700_student",
password = "ardit700_student",
host = "108.167.140.122",
database = "ardit700_pm1database"
)
# DB have two columns: "Expression" and "Definition"

cursor = con.cursor()

word = input("Enter a word: ")

query = cursor.execute("SELECT * FROM Dictionary WHERE Expression = '%s' " % word)
results = cursor.fetchall()
# results is a list of tuples [('Expression', 'Definition1'), ('Expression', 'Definition2'), ...]

if results:
    for result in results:
        print(result[1])  # print only Definition
else:
    print("Word not found")

