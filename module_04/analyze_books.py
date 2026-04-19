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


def find_prolific_authors(groups: dict, min_books: int = 2) -> list:
    """
    Находит авторов с количеством книг >= min_books.

    Args:
        groups: Словарь {автор: [список_книг]} из group_by_author.
        min_books: Минимальное количество книг.
    Returns:
            Список словарей {"author": ..., "book_count": ..., "titles": [...]},
            отсортированный по количеству книг по убыванию.
    """

    prolific = []

    for author, author_books in groups.items():
        if len(author_books) >= min_books:
            prolific.append({
                "author": author,
                "book_count": len(author_books),
                "titles": [b["title"] for b in author_books]
            })
        prolific.sort(key=lambda a: ["book_count"], reverse=True)
        return prolific

def decade_stats(books: list) -> list:
        """
        Рассчитывает статистику по каждому десятилетию.

        Args:
            books: Список словарей с книгами.

        Returns:
            Список словарей с полями: decade, book_count, avg_editions, top_book,
            отсортированный хронологически.
        """
        # Группировка книг по десятилетиям
        groups = {}
        for book in books:
            decade = get_decade(book.get("first_publish_year"))
            groups.setdefault(decade, []).append(book)

        stats = []
        for decade, decade_books in sorted(groups.items()):
            editions = [b.get("edition_count", 0) for b in decade_books]
            avg_editions = round(sum(editions) / len(editions), 1)

            # Самая издаваемая книга десятилетия
            top_book = max(decade_books, key=lambda b: b.get("edition_count", 0))

            stats.append({
                "decade": decade,
                "book_count": len(decade_books),
                "avg_editions": avg_editions,
                "top_book": top_book["title"],
                "top_editions": top_book.get("edition_count", 0),
            })

        return stats

def analyze_languages(books: list) -> dict:
    """
    Анализирует языковое распределение книг.

    Обрабатывает два формата поля language:
    - список: ["eng", "ger"] — книга на нескольких языках
    - строка: "unknown" — язык неизвестен

    Returns:
        Словарь с ключами:
        - "language_counts": {язык: количество_книг}
        - "multilingual": список книг на 2+ языках
    """
    lang_counts = {}
    multilingual = []

    for book in books:
        lang = book.get("language", "unknown")

        # Нормализация: строку превращаем в список
        if isinstance(lang, str):
            languages = [lang]
        else:
            languages = lang

        # Подсчёт каждого языка
        for language in languages:
            lang_counts[language] = lang_counts.get(language, 0) + 1

        # Мультиязычные книги
        if len(languages) > 1:
            multilingual.append({
                "title": book["title"],
                "languages": languages,
            })

    # Сортировка по количеству
    lang_counts = dict(sorted(lang_counts.items(), key=lambda p: p[1], reverse=True))

    return {
        "language_counts": lang_counts,
        "multilingual": multilingual,
    }

def print_full_report(books: list) -> None:
    """Выводит полный аналитический отчёт по каталогу книг."""
    print(f"\n{'='*60}")
    print(f"  АНАЛИТИЧЕСКИЙ ОТЧЁТ ПО КАТАЛОГУ ({len(books)} книг)")
    print(f"{'='*60}")

    # Общая статистика
    recent = filter_by_year(books, 2020)
    total_editions = sum(b.get("edition_count", 0) for b in books)
    print(f"\n📊 Общая статистика:")
    print(f"  Всего книг: {len(books)}")
    print(f"  Опубликовано с 2020 года: {len(recent)}")
    print(f"  Суммарно изданий: {total_editions}")

    # Топ по изданиям
    top_ed = top_by_editions(books, n=5)
    print(f"\n🏆 Топ-5 по количеству изданий:")
    for i, book in enumerate(top_ed, start=1):
        print(f"  {i}. {book['title']} — {book['edition_count']} изд. "
              f"({book['first_publish_year']})")

    # По десятилетиям
    d_stats = decade_stats(books)
    print(f"\n📅 Книги по десятилетиям:")
    table = [
        [s["decade"], s["book_count"], s["avg_editions"],
         s["top_book"][:40], s["top_editions"]]
        for s in d_stats
    ]
    print(tabulate(
        table,
        headers=["Декада", "Книг", "Ср. изд.", "Топ книга", "Изд."],
        tablefmt="fancy_grid"
    ))

    # Авторы с несколькими книгами
    author_groups = group_by_author(books)
    prolific = find_prolific_authors(author_groups, min_books=2)
    if prolific:
        print(f"\n✍️ Авторы с 2+ книгами:")
        for a in prolific:
            titles = ", ".join(a["titles"][:3])
            if len(a["titles"]) > 3:
                titles += f" (+{len(a['titles']) - 3})"
            print(f"  {a['author']}: {a['book_count']} книг — {titles}")
    else:
        print(f"\n✍️ Авторов с 2+ книгами не найдено")

    # Языки
    lang_analysis = analyze_languages(books)
    multilingual = lang_analysis["multilingual"]
    if multilingual:
        print(f"\n🌍 Мультиязычные книги ({len(multilingual)}):")
        for book in multilingual:
            print(f"  {book['title']}: {', '.join(book['languages'])}")

    # Самые новые
    newest = sort_by_year(books, descending=True)[:5]
    print(f"\n📅 5 самых новых книг:")
    for book in newest:
        print(f"  {book['title']} ({book['first_publish_year']})")

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

    # Проверка: сумма книг по всем авторам = общему количеству
    total = sum(len(group) for group in author_groups.values())
    assert total == len(books), "Группировка потеряла книги"
    print("✓ group_by_author")

    # Тест: авторы с несколькими книгами
    prolific = find_prolific_authors(author_groups, min_books=2)
    print(f"\nАвторы с 2+ книгами:")
    for author_info in prolific:
        print(f"  {author_info['author']} ({author_info['book_count']} книг):")
        for title in author_info["titles"]:
            print(f"    — {title}")
    print("✓ find_prolific_authors")

    # Тест: статистика по десятилетиям
    d_stats = decade_stats(books)
    print(f"\nСтатистика по десятилетиям:")
    table = [
        [s["decade"], s["book_count"], s["avg_editions"],
         s["top_book"], s["top_editions"]]
        for s in d_stats
    ]
    print(tabulate(
        table,
        headers=["Декада", "Книг", "Ср. изданий", "Топ книга", "Изданий"],
        tablefmt="fancy_grid"
    ))

    # Проверка
    total = sum(s["book_count"] for s in d_stats)
    assert total == len(books), "Статистика потеряла книги"
    print("✓ decade_stats")

    # Тест: анализ языков
    lang_analysis = analyze_languages(books)

    print(f"\nРаспределение по языкам:")
    for lang, count in lang_analysis["language_counts"].items():
        print(f"  {lang}: {count}")

    print(f"\nМультиязычные книги ({len(lang_analysis['multilingual'])}):")
    for book in lang_analysis["multilingual"]:
        print(f"  {book['title']}: {book['languages']}")

    # Проверка: английский должен быть самым частым
    assert "eng" in lang_analysis["language_counts"], "Нет английских книг?"
    print("✓ analyze_languages")
