import requests
from pprint import pprint
from tabulate import tabulate

url = "https://openlibrary.org/search.json"
params = {"q": "java", "limit": 10}

response = requests.get(url, params=params)

data = response.json()

books = []

for doc in data["docs"]:
    title = doc.get("title", "Unknown title")
    authors = doc.get("author_name", ["Unknown author"])
    year = doc.get("first_publish_year")

    book = {
        "title": title,
        "author": ", ".join(authors),
        "year": year
    }

    books.append(book)

print(tabulate(books, headers="keys", tablefmt="fancy_outline",
               numalign="center", stralign="center"))
