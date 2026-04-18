"""
Скрипт для скачивания данных о книгах с Open Library API.
Сохраняет результат в JSON-файл для дальнейшего анализа.
"""
import requests
import json

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


def clean_book(raw: dict) -> dict:
    """
    Извлекает нужные поля из «сырых» данных Open Library.
    Open Library возвращает десятки полей для каждой книги.
    Эта функция выбирает только полезные и приводит к единому формату.

    Args:
        raw: Словарь с «сырыми» данными одной книги от API.

    Returns:
        Словарь с очищенными данными.
    """
    return {
        "title": raw.get("title", "Unknown Title"),
        "author": ", ".join(raw.get("author_name", ["Unknown Author"])),
        "first_publish_year": raw.get("first_publish_year"),
        "publisher": raw.get("publisher", ["Unknown Publisher"])[0]
        if raw.get("publisher")
        else "Unknown Publisher",
        "pages": raw.get("number_of_pages_median"),
        "edition_count": raw.get("edition_count", 0),
        "language": raw.get("language", ["unknown"][0])
        if raw.get("language")
        else "unknown",
        "subject": raw.get("subject", [])[:5]
    }

def save_to_json(books: list, filepath: str) -> None:
    """Сохраняет список книг в JSON-файл."""
    with open(filepath, "w", encoding="UTF-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)
    print(f"Сохранено {len(books)} книг в {filepath}")

if __name__ == "__main__":
    # Тест 1: fetch_books
    test_books = fetch_books("python programming", limit=3)
    assert len(test_books) == 3
    print("✓ fetch_books работает")

    # Тест 2: clean_book на реальных данных
    first_clean = clean_book(test_books[0])
    assert isinstance(first_clean["title"], str)
    assert isinstance(first_clean["author"], str)
    assert isinstance(first_clean["subject"], list)
    print("✓ clean_book работает")

    # Тест 3: clean_book на пустом словаре
    empty_clean = clean_book({})
    assert empty_clean["title"] == "Unknown Title"
    assert empty_clean["publisher"] == "Unknown Publisher"
    print("✓ clean_book обрабатывает отсутствующие поля")

    # Тест 4: save_to_json
    test_clean_books = [clean_book(raw) for raw in test_books]
    save_to_json(test_clean_books, "test_books.json")
    print("✓ save_to_json работает (проверь файл module_04/test_books.json)")

    print("\nВсе тесты пройдены! Запускаю полное скачивание...\n")

    # --- Полное скачивание ---
    queries = [
        ("python programming", 25),
        ("java spring framework", 25),
    ]

    all_books = []
    for query, limit in queries:
        raw_books = fetch_books(query, limit)
        for raw in raw_books:
            clean = clean_book(raw)
            all_books.append(clean)

    print(f"\nВсего собрано {len(all_books)} книг")
    save_to_json(all_books, "books.json")

    # Показываем первые 5 для финальной проверки
    print("\nПервые 5 книг:")
    for i, book in enumerate(all_books[:5], start=1):
        print(f"  {i}. {book['title']} — {book['author']} ({book['first_publish_year']})")