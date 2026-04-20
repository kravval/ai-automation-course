"""Функции для работы с файлами: чтение, запись, пути."""
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


if __name__ == "__main__":
    data_dir = get_data_dir()
    print(f"Папка данных: {data_dir}")
    print(f"Существует: {data_dir.exists()}")
    print(f"Это папка: {data_dir.is_dir()}")

    assert data_dir.exists(), "Папка данных должна существовать"
    assert data_dir.is_dir(), "Путь должен быть директорией"
    print("✓ get_data_dir tests passed!")
