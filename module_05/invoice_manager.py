"""Менеджер счетов с хранением данных в JSON."""
from file_io import get_data_dir, load_invoices, save_invoices

def main():
    data_dir = get_data_dir()
    invoices_path = data_dir / "invoices.json"

    # Читаем счета. Если файла нет — стартуем с пустого списка.
    invoices = load_invoices(invoices_path)

    if not invoices:
        print("Файл данных не найден. Создаю начальные данные...")
        invoices = [
            {"number": "INV-001", "vendor": "Acme Corp", "amount": 1500.00, "status": "paid"},
            {"number": "INV-002", "vendor": "TechSupply", "amount": 3200.50, "status": "unpaid"},
            {"number": "INV-003", "vendor": "OfficeMax", "amount": 450.75, "status": "paid"},
            {"number": "INV-004", "vendor": "Acme Corp", "amount": 8900.00, "status": "unpaid"},
            {"number": "INV-005", "vendor": "TechSupply", "amount": 220.00, "status": "paid"},
        ]
        save_invoices(invoices, invoices_path)
        print(f"Создан файл: {invoices_path}")

    # Вывод всех счетов
    print(f"\n=== Счета ({len(invoices)}) ===")
    for invoice in invoices:
        marker = "✓" if invoice["status"] == "paid" else "✗"
        print(f"{marker} {invoice['number']} | {invoice['vendor']:10} | {invoice['amount']:>10.2f} | {invoice['status']}")

if __name__ == "__main__":
    main()
