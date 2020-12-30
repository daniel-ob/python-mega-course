import json  # json standard library
from difflib import get_close_matches

data_file = "data.json"

with open(data_file) as file:
    data = json.load(file)
    # print(type(data))  # <class 'dict'>


def get_definition(word):
    word = word.lower()
    if word in data:
        return "\n".join(data[word])  # return one definition per line
    elif word.title() in data:  # if user enter "paris", this will look for "Paris"
        return "\n".join(data[word.title()])
    elif word.upper() in data:  # for acronyms (like USA or NATO)
        return "\n".join(data[word.upper()])
    elif len(get_close_matches(word, data.keys())) > 0:
        closest_match = get_close_matches(word, data.keys())[0]
        yn = input("Did you mean %s instead? [Y/N]: " % closest_match)
        if yn == "Y":
            return "\n".join(data[closest_match])
        else:
            return "Word not found"
    else:
        return "Word not found"


word = input("Enter a word: ")

print(get_definition(word))

