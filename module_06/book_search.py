import sys
import json
import logging
from pathlib import Path
import requests
from tabulate import tabulate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)
API_URL = "https://openlibrary.org/search.json"
TIMEOUT_SECONDS = 10
OUTPUT_DIR = Path("output")


def search_books(query: str, limit: int = 10) -> list[dict] | None:
    """
    Выполняет запрос к Open Library API и возвращает список книг

    Args:
        query: Поисковый запрос (тема, название, автор).
        limit: Максимальное количество книг в ответе.
    Returns:
        Список словарей с данными книг или None в случае ошибки.
    """
    params = {"q": query, "limit": limit}
    logger.info("Searching for '%s' (limit=%d)", query, limit)

    try:
        response = requests.get(API_URL, params=params, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        logger.error("Request timed out after %d seconds", TIMEOUT_SECONDS)
        return None
    except requests.exceptions.ConnectionError:
        logger.error("Connection failed (check internet connection)")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error("API returned error status: %s", e)
        return None
    except requests.exceptions.RequestException as e:
        logger.error("Unexpected request error: %s", e)
        return None

    docs = data.get("docs", [])
    logger.info("API returned %d books (total in catalog): %d", len(docs), data.get("numFound", 0))

    return [extract_book_info(doc) for doc in docs]


def extract_book_info(doc: dict) -> dict:
    """
    Извлекает title, author, year из одного элемента docs.

    Args:
        doc: Словарь книги из ответа Open Library API.
    Returns:
       Словарь с ключами title, author, year.
    """
    authors = doc.get("author_name", ["Unknown author"])

    return {
        "title": doc.get("title", "Unknown title"),
        "author": ", ".join(authors),
        "year": doc.get("first_publish_year")
    }


def save_to_json(books: list[dict], path: Path) -> None:
    """
    Сохраняет список книг в JSON-файл.

    Args:
        books: Список словарей с данными книг.
        path: Путь к выходному файлу.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)
    logger.info("Saved %d books to %s", len(books), path)


def print_books_table(books: list[dict]) -> None:
    """"
    Выводит книги в виде форматированной таблицы.
    Args:
        books:
    """
    print(tabulate(books, headers="keys", tablefmt="fancy_outline",
               numalign="center", stralign="center"))

def main() -> None:
    """
    Главная функция: ищет книги и выводит результаты.
    """

    if len(sys.argv) < 2:
        print("Usage: python3 book_search.py <query> [limit]")
        print("Example: python3 book_search.py 'machine_learning' 20")
        exit(1)

    query = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) >= 3 else 10

    books = search_books(query, limit=limit)

    if books is None:
        logger.error("Failed to fetch books")
        exit(1)

    if not books:
        logger.warning("No books found for query: '%s'", query)
        exit(0)

    safe_query = query.replace(" ", "_")
    output_file = OUTPUT_DIR / f"books_{safe_query}.json"
    save_to_json(books, output_file)

    print_books_table(books)


if __name__ == "__main__":
    main()
