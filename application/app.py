from configparser import ConfigParser
import mysql.connector

#Read config.ini file
config_object = ConfigParser()
config_object.read("../config.ini")
db = config_object["LOCALDB"]

# connect with DB
con = mysql.connector.connect(user = db["user"],password = db["password"],host = db["host"],database = db["database"])
cursor = con.cursor()

def translate(input_data):
    cursor.execute("SELECT explanation FROM dictionary WHERE word = '%s'" % input_data)
    results = cursor.fetchall()
    return results

def explanations(query_results):
    for query_result in query_results:
        print('* '+query_result[0])

word=input("Enter the word: ")
results = translate(word)

if results:
    explanations(results)
else:
    cursor.execute("SELECT word FROM dictionary WHERE word LIKE %(word)s LIMIT 1",{'word':word+'%'})
    searched_result = cursor.fetchall()
    if searched_result:
        suggested_word = searched_result[0][0]
        if suggested_word:
            yn = input("Did you mean %s instead? Press 'Y' if yes, or 'N' if no: " % suggested_word)
            if yn.casefold() == "y":
                suggested_results = translate(suggested_word)
                explanations(suggested_results)
            elif yn.casefold() == "n":
                print("%s is not exists. Please recheck." % word)
            else:
                print("You didn't enter the right key. Try again")
    else:
        print("No word found!")

