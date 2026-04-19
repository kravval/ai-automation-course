"""
Анализ реальных книжных данных из Open Library.
Демонстрация фильтрации, сортировки и группировки.
"""
import json
from tabulate import tabulate


def load_books(filepath: str) -> list:
    """Загружает список книг из JSON-файла."""
    with open(filepath, "r", encoding="UTF-8") as f:
        books = json.load(f)
    print(f"Загружено {len(books)} книг из {filepath}")
    return books

def filter_by_year(books: list, min_year: int) -> list:
    """
    Возвращает книги, опубликованные не раньше указаннаго года.

    Args:
        books: Список словарей с книгами.
        min_year: Минимальный год публикации (включительно).

    Returns:
        Новый список книг, прошедших фильтр.
    """
    result = []

    for book in books:
        year = book.get("first_publish_year")
        if year is not None and year >= min_year:
            result.append(book)
    return result

def filter_with_pages(books: list) -> list:
    """Возвращает только те книги, у которых указано количество страниц."""
    return [book for book in books if book.get("pages") is not None]


if __name__ == "__main__":
    books = load_books("books.json")
    assert len(books) > 0
    print("✓ load_books")

    # Тест: фильтрация по году
    recent = filter_by_year(books, 2015)
    print(f"\nКниги с 2015 года: {len(recent)} из {len(books)}")
    for book in recent[:5]:
        print(f"  {book['title']} ({book['first_publish_year']})")

    # Проверка: все книги в результате — с годом >= 2015
    for book in recent:
        assert book["first_publish_year"] >= 2015, \
            f"Книга {book['title']} с годом {book['first_publish_year']} прошла фильтр"
    print("✓ filter_by_year")

    # Тест: фильтрация по наличию страниц
    with_pages = filter_with_pages(books)
    without_pages = len(books) - len(with_pages)
    print(f"\nС указанием страниц: {len(with_pages)}, без: {without_pages}")
    for book in with_pages[:3]:
        print(f"  {book['title']}: {book['pages']} стр.")
    print("✓ filter_with_pages")