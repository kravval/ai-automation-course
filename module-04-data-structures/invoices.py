"""Мини-каталог счетов.

Демонстрация работы с list[dict]: фильтрация, сортировка, агрегация.
"""
import logging
from tabulate import tabulate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def get_initial_invoices() -> list[dict]:
    """Возвращает стартовый набор счетов для демонстрации."""
    return [
        {"number": "INV-2024-001", "vendor": "Acme Corp", "amount": 1500.00, "paid": True, "date": "2024-10-15"},
        {"number": "INV-2024-002", "vendor": "TechSupply", "amount": 3200.00, "paid": False, "date": "2024-10-22"},
        {"number": "INV-2024-003", "vendor": "Acme Corp", "amount": 750.00, "paid": False, "date": "2024-11-01"},
        {"number": "INV-2024-004", "vendor": "GlobalShipping", "amount": 4250.00, "paid": True, "date": "2024-11-08"},
        {"number": "INV-2024-005", "vendor": "Acme Corp", "amount": 2100.00, "paid": False, "date": "2024-11-12"},
        {"number": "INV-2024-006", "vendor": "TechSupply", "amount": 890.00, "paid": True, "date": "2024-11-20"},
        {"number": "INV-2024-007", "vendor": "MegaCorp", "amount": 5600.00, "paid": False, "date": "2024-12-01"},
    ]


def filter_unpaid(invoices: list[dict]) -> list[dict]:
    """Возвращает только неоплаченные счета."""
    return [inv for inv in invoices if not inv["paid"]]


def filter_by_min_amount(invoices: list[dict], min_amount: float) -> list[dict]:
    """Возвращает счета на сумму больше или равную min_amount."""
    return [inv for inv in invoices if inv["amount"] >= min_amount]


def filter_by_vendor(invoices: list[dict], vendor: str) -> list[dict]:
    """Возвращает счета от указанного поставщика."""
    return [inv for inv in invoices if inv["vendor"] == vendor]


def sort_by_amount(invoices: list[dict], descending: bool = False) -> list[dict]:
    """Сортирует счета по сумме."""
    return sorted(invoices, key=lambda inv: inv["amount"], reverse=descending)


def sort_by_date(invoices: list[dict], descending: bool = False) -> list[dict]:
    """Сортирует счета по дате."""
    return sorted(invoices, key=lambda inv: inv["date"], reverse=descending)


def total_amount(invoices: list[dict]) -> float:
    """Считает сумму всех счетов в списке."""
    return sum(inv["amount"] for inv in invoices)


def average_amount(invoices: list[dict]) -> float:
    """Среднюю сумму. Если список пуст — возвращает 0."""
    if not invoices:
        return 0
    return total_amount(invoices) / len(invoices)


def count_unpaid(invoices: list[dict]) -> int:
    return sum(1 for inv in invoices if not inv["paid"])


def unique_vendors(invoices: list[dict]) -> set[str]:
    """Возвращает множество уникальных поставщиков."""
    return {inv["vendor"] for inv in invoices}


def group_by_vendor(invoices: list[dict]) -> dict[str, list[dict]]:
    """Группирует счета по поставщику.

    Возвращает словарь {имя поставщика: [список его счетов]}.
    """
    result: dict[str, list[dict]] = {}

    for inv in invoices:
        vendor = inv["vendor"]
        result.setdefault(vendor, []).append(inv)
    return result


def print_invoices_table(invoices: list[dict], title: str = "Счета") -> None:
    """Печатает таблицу счетов с заголовком."""
    if not invoices:
        print(f"\n{title}: (пусто)")
        return

    rows = [
        {
            "Number": inv["number"],
            "Vendor": inv["vendor"],
            "Amount": f" ${inv['amount']:,.2f}",
            "Paid": "✓" if inv["paid"] else "✗",
            "Date": inv["date"]
        }
        for inv in invoices
    ]

    print(f"\n=== {title} ({len(invoices)}) ===")
    print(tabulate(rows, headers="keys", tablefmt="grid"))


def main():
    invoices = get_initial_invoices()
    logging.info("Загружено %d счетов", len(invoices))

    print_invoices_table(invoices, "Все счета")

    unpaid = filter_unpaid(invoices)
    print_invoices_table(unpaid, "Неоплаченные")

    big = filter_by_min_amount(invoices, 2000)
    print_invoices_table(big, "Дороже $2,000")

    acme = filter_by_vendor(invoices, "Acme Corp")
    print_invoices_table(acme, "Только Acme Corp")

    by_amount = sort_by_amount(invoices, descending=True)
    print_invoices_table(by_amount, "По сумме (убывание)")

    by_date = sort_by_date(invoices)
    print_invoices_table(by_date, "По дате (возрастание)")

    print(f"\nВсего на руках:        ${total_amount(invoices):,.2f}")
    print(f"Средний размер счёта:  ${average_amount(invoices):,.2f}")
    print(f"Неоплаченных:          {count_unpaid(invoices)}")
    print(f"К получению:           ${total_amount(filter_unpaid(invoices)):,.2f}")

    vendors = unique_vendors(invoices)
    print(f"\nПоставщиков:           {len(vendors)}")
    print(f"Список:                {', '.join(sorted(vendors))}")

    by_vendor = group_by_vendor(invoices)
    print(f"\n=== По поставщикам ===")
    for vendor, vendor_invoices in by_vendor.items():
        total = total_amount(vendor_invoices)
        print(f"    {vendor}: {len(vendor_invoices)} счёт(а) на ${total:,.2f}")


if __name__ == "__main__":
    main()
