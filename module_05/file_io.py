"""Функции для работы с файлами: чтение, запись, пути."""
import json
from pathlib import Path


def get_data_dir() -> Path:
    """
    Возвращает путь к папке с данными приложения.
    Создаёт папку, если её нет.

    Returns:
        Объект Path, указывающий на папку data внутри module_05.
    """

    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def save_invoices(invoices: list, path: Path) -> None:
    """
    Сохраняет список счетов в JSON-файл.

    Args:
        invoices: Список словарей со счетами.
        path: путь к файлу для записи.
    """

    with open(path, "w", encoding="utf-8") as f:
        json.dump(invoices, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    data_dir = get_data_dir()
    print(f"Папка данных: {data_dir}")

    # Тест save_invoices
    test_invoices = [
        {"number": "INV-001", "vendor": "Acme Corp", "amount": 1500.00, "status": "paid"},
        {"number": "INV-002", "vendor": "TechSupply", "amount": 3200.50, "status": "unpaid"},
        {"number": "INV-003", "vendor": "Поставщик №3", "amount": 450.75, "status": "paid"},
    ]

    test_path = data_dir / "test_invoices.json"
    save_invoices(test_invoices, test_path)

    assert test_path.exists(), "Файл должен быть создан"
    print(f"✓ Файл создан: {test_path}")

    # Проверим глазами — прочитаем файл как текст
    content = test_path.read_text(encoding="utf-8")
    print("Cодержимое файла:")
    print(content)

    # Должна быть кириллица, а не \u...
    assert "Поставщик" in content, "Кириллица должна быть читаемой"
    print("✓ save_invoices tests passed!")

