import requests
from tabulate import tabulate
import json
from pathlib import Path

url = "https://openlibrary.org/search.json"
params = {"q": "java", "limit": 10}


def search_books(query: str, limit: int = 10) -> list[dict]:
    """Выполняет запрос к Open Library API и возвращает список кник"""


def extract_book_info(doc: dict) -> dict:
    """Извлекает title, author, year из одного элемента docs."""


def save_to_json(books: list[dict], path: Path) -> None:
    """Сохраняет список книг в JSON-файл."""


def print_books_table(books: list[dict]) -> None:
    """"Выводит книги в виде форматированной таблицы."""


def main() -> None:
    """Главная фунция: ищет книги и выводит результаты."""


if __name__ == "__main__":
    main()

try:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    print("Ошибка: истекло время ожидания запроса (сервер не ответил в течение 10 секунд)")
    exit(1)
except requests.exceptions.ConnectionError:
    print("Ошибка: не удалось установить соединение (проверьте подключение к интернету)")
    exit(1)
except requests.exceptions.HTTPError as e:
    print(f"Ошибка: API вернул код ошибки: {e}")
    exit(1)
except requests.exceptions.RequestException as e:
    print(f"Ошибка: непредвиденная ошибка при запросе: {e}")
    exit(1)

if not data.get("docs"):
    print(f"По запросу не найдено книг: '{params['q']}'")
    exit(0)

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
