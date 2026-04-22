import requests
from tabulate import tabulate
import json
from pathlib import Path

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

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

output_file = output_dir / "books_python.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print(f"Сохранено {len(books)} книг в {output_file}")
print()
print(tabulate(books, headers="keys", tablefmt="fancy_outline",
               numalign="center", stralign="center"))
