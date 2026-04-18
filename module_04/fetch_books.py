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


if __name__ == "__main__":
    # Тест 1: fetch_books
    test_books = fetch_books("python programming", limit=3)
    assert len(test_books) == 3
    print("✓ fetch_books работает")

    # Тест 2: clean_book на реальных данных
    print("\nТест clean_book на первой книге:")
    first_raw = test_books[0]
    first_clean = clean_book(first_raw)

    print(f"  title:    {first_clean['title']}")
    print(f"  author:   {first_clean['author']}")
    print(f"  year:     {first_clean['first_publish_year']}")
    print(f"  publisher:{first_clean['publisher']}")
    print(f"  pages:    {first_clean['pages']}")
    print(f"  editions: {first_clean['edition_count']}")
    print(f"  language: {first_clean['language']}")
    print(f"  subjects: {first_clean['subject']}")

    # Проверяем типы полей
    assert isinstance(first_clean["title"], str), "title должен быть строкой"
    assert isinstance(first_clean["author"], str), "author должен быть строкой"
    assert isinstance(first_clean["edition_count"], int), "edition_count должен быть числом"
    assert isinstance(first_clean["subject"], list), "subject должен быть списком"

    print("✓ clean_book работает, типы полей правильные")

    # Тест 3: clean_book на «битых» данных (пустой словарь)
    print("\nТест clean_book на пустом словаре:")
    empty_clean = clean_book({})
    print(f"  Результат: {empty_clean}")
    assert empty_clean["title"] == "Unknown Title"
    assert empty_clean["author"] == "Unknown Author"
    assert empty_clean["publisher"] == "Unknown Publisher"
    assert empty_clean["pages"] is None
    assert empty_clean["subject"] == []

    print("✓ clean_book корректно обрабатывает отсутствующие поля")