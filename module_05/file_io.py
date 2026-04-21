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

def load_invoices(path: Path) -> list:
    """
    Читает список счетов из JSON-файла.

    Args:
        path: Путь к JSON-файлу.

    Returns:
        Список словарей со счетами.
        Если файл не существует - возвращает пустой список.
    """
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

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

    content = test_path.read_text(encoding="utf-8")
    assert "Поставщик" in content
    print("✓ save_invoices: OK")

    # Тест load_invoices — прочитаем, что записали
    loaded = load_invoices(test_path)
    print(f"Прочитано {len(loaded)} счетов")

    assert len(loaded) == 3, "Должно быть 3 счёта"
    assert loaded[0]["number"] == "INV-001"
    assert loaded[2]["vendor"] == "Поставщик №3"
    assert loaded[1]["amount"] == 3200.50
    print("✓ load_invoices: данные соответствуют тем, что записали")

    # Тест: чтение несуществующего файла → пустой список
    missing_path = data_dir / "does_not_exist.json"
    empty = load_invoices(missing_path)
    assert empty == [], "Для несуществующего файла должен быть пустой список"
    print("✓ load_invoices: пустой список для несуществующего файла")

    print("\n✓ All file_io tests passed!")

