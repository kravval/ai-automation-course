from tabulate import tabulate


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


if __name__ == "__main__":
    test_invoices = [
        {"number": "T-001", "vendor": "TestCorp", "amount": 1500.00, "status": "paid",
         "category": "medium", "marker": "✓"},
        {"number": "T-002", "vendor": "OtherCo", "amount": 4000.00, "status": "unpaid",
         "category": "large", "marker": "✗"}
    ]

    print("=== Test: print_invoices_table ===")
    print_invoices_table(test_invoices)