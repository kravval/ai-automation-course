from tabulate import tabulate

from module_02.invoice_analyzer import headers


def print_invoices_table(invoices: list) -> None:
    """
    Выводит таблицу счетов в консоль.

    Args:
        invoices:Список словарей со счетами.
        Каждый счёт должен содержать поля
            number, vendor, amount, status, category, marker.
    """

    table_data = []

    for invoice in invoices:
        row = [
            invoice["marker"],
            invoice["number"],
            invoice["vendor"],
            f"{invoice['amount']:.2f}",
            invoice["category"],
            invoice["status"]
        ]

        table_data.append(row)

    headers = ["", "Number", "Vendor", "Amount", "Category", "Status"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid",
                   numalign="center", stralign="center"))


def print_payment_summary(stats: dict) -> None:
    """выводит таблицу статистики по статусу оплаты"""
    data = [
        ["Оплачено", stats["paid_count"], f"{stats['total_paid']:.2f}"],
        ["Не оплачено", stats["unpaid_count"], f"{stats['total_unpaid']:.2f}"],
        ["Всего", stats["paid_count"] + stats["unpaid_count"],
         f"{stats['total_paid'] + stats['total_unpaid']:.2f}"]
    ]
    print(tabulate(data, headers=["Статус", "Количество", "Сумма"], tablefmt="fancy_grid",
        numalign="center", stralign="center"))
if __name__ == "__main__":
    test_invoices = [
        {"number": "T-001", "vendor": "TestCorp", "amount": 1500.00, "status": "paid",
         "category": "medium", "marker": "✓"},
        {"number": "T-002", "vendor": "OtherCo", "amount": 4000.00, "status": "unpaid",
         "category": "large", "marker": "✗"}
    ]

    print("=== Test: print_invoices_table ===")
    print_invoices_table(test_invoices)
    print()
    print("===Test: print_payment_summary===")
    test_invoices

    test_payment_stats = {
        "paid_count": 2,
        "unpaid_count": 1,
        "total_paid": 1500.00,
        "total_unpaid": 4000.00
    }

    print_payment_summary(test_payment_stats)