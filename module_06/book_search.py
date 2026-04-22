import requests
from pprint import pprint

url = "https://openlibrary.org/search.json"
params = {"q": "python", "limit": 10}

response = requests.get(url, params=params)

data = response.json()

print("Top-level keys:", list(data.keys()))
print("Общее количество найденных книг (numFound):", data["numFound"])
print("Количество возвращенных документов:", len(data["docs"]))
print()
print("=== Структура первой книги ===")
pprint(data["docs"][0])
