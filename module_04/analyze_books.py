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

if __name__ == "__main__":
    books = load_books("books.json")

    # Быстрая проверка: данные загрузились, структура правильная
    assert len(books) > 0, "Файл пустой"
    assert "title" in books[0], "Нет поля title"
    assert "author" in books[0], "Нет поля author"
    print(f"Первая книга: {books[0]['title']}")
    print("✓ load_books работает")