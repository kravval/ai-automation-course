"""Чтение и запись list[dict] в форматах JSON и CSV."""
import csv
import json
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def load_json(path: Path) -> list[dict]:
    """Читает JSON-файл и возвращает list[dict].

    Если файла нет — возвращает пустой список.
    """
    if not path.exists():
        logging.info("Файл данных не найден: %s. Возвращаю пустой список.", path)
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    logging.info("Загружено %d записей из %s", len(data), path)
    return data


def save_json(path: Path, data: list[dict]) -> None:
    """Записывает list[dict] в JSON-файл с отступами и кириллицей как есть."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logging.info("Сохранено %d записей в %s", len(data), path)


def export_csv(path: Path, data: list[dict], fieldnames: list[str]) -> None:
    """Экспортирует list[dict] в CSV.

    fieldnames — список колонок и их порядок.
    """
    if not data:
        logging.warning("Пустой список — CSV не будет создан")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)
    logging.info("Экспортировано %d записей в %s", len(data), path)

if __name__ == "__main__":
    json_path = Path("data/invoices.json")
    csv_path = Path("data/invoices_export.csv")

    invoices = load_json(json_path)
    print(f"\nЗагружено: {len(invoices)} счетов")

    export_csv(
        csv_path,
        invoices,
        fieldnames=["number", "amount"],
    )

    print(f"Экспортировано в {csv_path}")
