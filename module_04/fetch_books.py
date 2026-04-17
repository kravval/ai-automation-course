"""
Скрипт для скачивания данных о книгах с Open Library API.
Сохраняет результат в JSON-файл для дальнейшего анализа.
"""
import requests
from urllib3.util import timeout


def fetch_books(query: str, limit: int = 50) -> list:
    """
    Скачивает книги с Open Library Search API.

    Args:
        query: Поисковый запрос (например, "python programming").
        limit: Максимальное количество книг.

    Returns:
        Список словарей с «сырыми» данными о книгах.
    """
    url = "https://openlibrary.org/search.json"
    params = {"q": query, "limit": limit}

    print(f"Запрашиваю книги по запросу '{query}' (limit={limit})...")
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    raw_books = data["docs"]
    print(f"Получено {len(raw_books)} результатов от API")

    return raw_books

if __name__ == "__main__":
    # Тест 1: скачать 3 книги для быстрой проверки
    test_books = fetch_books("python programming", limit=3)

    print(f"\nПолучено {len(test_books)} книг")
    assert len(test_books) == 3, f"Ожидалось 3, получено {len(test_books)}"

    # Посмотрим, как выглядят сырые данные
    print("\nПоля первой книги:")
    first = test_books[0]
    for key in sorted(first.keys()):
        value = first[key]
        # Обрезаем длинные значения для читаемости
        if isinstance(value, list) and len(value) > 3:
            value = value[:3]
        print(f"  {key}: {value}")

    print("\n✓ fetch_books работает!")