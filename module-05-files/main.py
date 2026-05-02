"""Менеджер каталога счетов: чтение JSON, меню действий, экспорт в CSV."""
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from invoice_catalog import (
    filter_unpaid,
    print_invoices_table,
    sort_by_amount,
    total_amount,
    unique_vendors
)
from storage import export_csv, load_json, save_json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def read_data_path() -> Path:
    """Считывает путь к файлу данных из .env."""
    load_dotenv()
    raw = os.getenv("INVOICES_DATA_PATH")
    if not raw:
        raise RuntimeError(
            "Переменная INVOICES_DATA_PATH не задана. "
            "Создайте .env в корне проекта по образцу .env.example."
        )
    print(Path(raw))
    return Path(raw)


def add_invoice(invoice: list[dict]) -> dict:
    """Спрашивает у пользователя поля нового счёта и добавляет его в список."""
    print("\n--- Новый счёт ---")
    number = input("Номер: ").strip()
    vendor = input("Поставщик: ").strip()
    amount = float(input("Сумма ($): ").strip())
    paid_raw = input("Оплачен? (y/n): ").strip().lower()
    date = input("Дата (YYYY-MM-DD): ").strip()

    new_inv = {
        "number": number,
        "vendor": vendor,
        "amount": amount,
        "paid": paid_raw in ("y", "yes"),
        "date": date
    }
    invoice.append(new_inv)
    logging.info("Добавлен счёт %s от %s на $%.2f", number, vendor, amount)
    return new_inv


def show_menu() -> str:
    print("\n=== Меню ===")
    print("  1. Показать все счета")
    print("  2. Показать неоплаченные")
    print("  3. Показать ТОП-3 по сумме")
    print("  4. Добавить счёт")
    print("  5. Экспортировать всё в CSV")
    print("  6. Сводка")
    print("  0. Выйти")
    return input("\nВыбор: ").strip()


def main():
    data_path = read_data_path()
    invoices = load_json(data_path)
    print(f"Загружено счетов: {len(invoices)}")

    while True:
        choice = show_menu()

        if choice == "1":
            print_invoices_table(invoices, "Все счета")
        elif choice == "2":
            print_invoices_table(filter_unpaid(invoices), "Неоплаченные счета")
        elif choice == "3":
            top = sort_by_amount(invoices, descending=True)[:3]
            print_invoices_table(top, "ТОП-3 по сумме")
        elif choice == "4":
            add_invoice(invoices)
        elif choice == "5":
            csv_path = data_path.parent / "invoices_export.csv"
            export_csv(
                csv_path,
                invoices,
                fieldnames=["number", "vendor", "amount", "paid", "date"]
            )
            print(f"Экспортировано в: {csv_path}")
        elif choice == "6":
            vendors = unique_vendors(invoices)
            print(f"\nВсего счетов: {len(invoices)}")
            print(f"Поставщиков:  {len(vendors)}")
            print(f"На сумму:     ${total_amount(invoices):,.2f}")
            print(f"К получению:  ${total_amount(filter_unpaid(invoices)):,.2f}")
        elif choice == "0":
            save_json(data_path, invoices)
            print("Сохранено. До встречи.")
            break
        else:
            print(f"  ❌ Неизвестный выбор: {choice!r}")


if __name__ == "__main__":
    main()
