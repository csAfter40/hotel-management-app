import json

file = open('countries.json', 'r')
data = json.load(file)

language_data = []
language_set = set()
currency_data = []
currency_set = set()
for i, country in enumerate(data, 1): # start from 1
    language_name = country["language"]["name"]
    language_code = country["language"]["code"]
    language = {
        "model": "main.language",
        "pk": i,
        "fields": {
            "code": language_code,
            "name": language_name
        }
    }
    if language_code not in language_set:
        language_set.add(language_code)
        language_data.append(language)

    currency_code = country["currency"]["code"]
    currency_name = country["currency"]["name"]
    currency_symbol = country["currency"]["symbol"]
    currency = {
        "model": "main.currency",
        "pk": i,
        "fields": {
            "code": currency_code,
            "name": currency_name,
            "symbol": currency_symbol
        }
    }
    if currency_code not in currency_set:
        currency_set.add(currency_code)
        currency_data.append(currency)

with open("languages.json", "w") as file:
    data = json.dump(language_data, file)

with open("currencies.json", "w") as file:
    data = json.dump(currency_data, file)

file.close()