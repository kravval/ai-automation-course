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


def sort_by_year(books: list, descending: bool = True) -> list:
    """
    Сортирует книги по году публикации.

    Args:
        books: Список словарей с книгами.
        descending: True — от новых к старым, False — от старых к новым.
    Returns:
        Новый отсортированный список.
    """
    # Книги без года — в конец списка
    books_with_year = [b for b in books if b.get("first_publish_year") is not None]
    books_without_year = [b for b in books if b.get("first_publish_year" is not None)]

    sorted_books = sorted(
        books_with_year,
        key=lambda book: book["first_publish_year"],
        reverse=descending
    )

    return sorted_books + books_without_year


def top_by_editions(books: list, n: int = 10) -> list:
    """Возвращает N книг с наибольшим количеством изданий."""
    return sorted(books, key=lambda b: b.get("edition_count", 0), reverse=True)[:n]


def get_decade(year: int | None) -> str:
    """
    Возвращает десятилетие для года: 1996 → "1990s", 2017 → "2010s".

    Args:
        year: Год публикации или None.
    Returns:
            Строка вида "2010s" или "Unknown" для None.
    """
    if year is None:
        return "Unknown"
    decade = (year // 10) * 10
    return f"{decade}s"

def count_by_decade(books: list) -> dict:
    """
    Подсчитывает количество книг в каждом десятилетии
    Args:
        books: Список словарей с книгами.
    Returns:
        Словарь {десятилетие: количество}, отсортированный по десятилетию.
    """
    counts = {}
    for book in books:
        decade = get_decade(book.get("first_publish_year"))
        counts[decade] = counts.get(decade, 0) + 1

    return dict(sorted(counts.items()))

def group_by_author(books: list) -> dict:
    """
    Группирует книги по автору.

    Args:
        books: Список словарей с книгами.
    Returns:
        Словарь {автор: [список_книг]}.
    """

    groups = {}

    for book in books:
        author = book.get("author", "Unknown Author")
        groups.setdefault(author, []).append(book)
    return groups

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

    newest_first = sort_by_year(books, descending=True)
    print(f"\nТоп-5 самых новых книг:")
    for book in newest_first[:5]:
        print(f"  {book['title']} ({book['first_publish_year']})")

    # Проверка: первая книга — с самым большим годом
    years = [b["first_publish_year"] for b in newest_first
             if b["first_publish_year"] is not None]
    assert years == sorted(years, reverse=True), "Сортировка нарушена"
    print("✓ sort_by_year")

    # Тест: топ по изданиям
    top_editions = top_by_editions(books, n=5)
    print(f"\nТоп-5 по количеству изданий:")
    for book in top_editions:
        print(f"  {book['title']}: {book['edition_count']} изданий")

    # Проверка: первая книга имеет больше всего изданий
    assert top_editions[0]["edition_count"] >= top_editions[-1]["edition_count"]
    print("✓ top_by_editions")

    # Тест: get_decade
    assert get_decade(1996) == "1990s"
    assert get_decade(2003) == "2000s"
    assert get_decade(2017) == "2010s"
    assert get_decade(2024) == "2020s"
    assert get_decade(None) == "Unknown"
    print("\n✓ get_decade")

    # Тест: подсчёт по десятилетиям
    decade_counts = count_by_decade(books)
    print(f"\nКниги по десятилетиям:")
    table = [[decade, count] for decade, count in decade_counts.items()]
    print(tabulate(table, headers=["Десятилетие", "Книг"], tablefmt="simple"))

    # Проверка: сумма всех значений = общему количеству книг
    assert sum(decade_counts.values()) == len(books), "Сумма не сходится"
    print("✓ count_by_decade")

    # Тест: группировка по автору
    author_groups = group_by_author(books)
    print(f"\nВсего уникальных авторов: {len(author_groups)}")
