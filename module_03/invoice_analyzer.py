from categorization import categorize_amount
from statistics import calculate_payment_stats, calculate_category_stats, find_max_debtor
from tabulate import tabulate

# Тестовые данные — список счетов от разных поставщиков
invoices = [
    {"number": "INV-001", "vendor": "Acme Corp", "amount": 1500.00, "status": "paid"},
    {"number": "INV-002", "vendor": "TechSupply", "amount": 3200.50, "status": "unpaid"},
    {"number": "INV-003", "vendor": "OfficeMax", "amount": 450.75, "status": "paid"},
    {"number": "INV-004", "vendor": "Acme Corp", "amount": 8900.00, "status": "unpaid"},
    {"number": "INV-005", "vendor": "TechSupply", "amount": 220.00, "status": "paid"},
    {"number": "INV-006", "vendor": "GlobalParts", "amount": 5670.30, "status": "unpaid"},
    {"number": "INV-007", "vendor": "OfficeMax", "amount": 175.00, "status": "paid"},
    {"number": "INV-008", "vendor": "Acme Corp", "amount": 2340.80, "status": "paid"},
]
table_data = []

for invoice in invoices:

    invoice["category"] = categorize_amount(invoice["amount"])

    if invoice["status"] == "paid":
        marker = "✓"
    else:
        marker = "✗"

    row = [
        marker,
        invoice["number"],
        invoice["vendor"],
        f"{invoice['amount']:.2f}",
        invoice["category"],
        invoice["status"]
    ]
    table_data.append(row)

payment_stats = calculate_payment_stats(invoices)
paid_count = payment_stats["paid_count"]
unpaid_count = payment_stats["unpaid_count"]
total_paid = payment_stats["total_paid"]
total_unpaid = payment_stats["total_unpaid"]
category_stats = calculate_category_stats(invoices)

headers = ["", "Number", "Vendor", "Amount", "Category", "Status"]

print("=== По размеру ===")
size_data = [
    ["small", category_stats["small"]["count"], f"{category_stats["small"]["amount"]:.2f}"],
    ["medium", category_stats["medium"]["count"], f"{category_stats["medium"]["amount"]:.2f}"],
    ["large", category_stats["large"]["count"], f"{category_stats["large"]["amount"]:.2f}"],
]
print(tabulate(size_data, headers=["Категория", "Количество", "Сумма"], tablefmt="fancy_grid"))

print()
print("=== По оплате ===")
payment_data = [
    ["Оплачено", paid_count, f"{total_paid:.2f}"],
    ["Не оплачено", unpaid_count, f"{total_unpaid:.2f}"],
    ["Всего", paid_count + unpaid_count, f"{total_paid + total_unpaid:.2f}"],
]
print(tabulate(payment_data, headers=["Статус", "Количество", "Сумма"], tablefmt="fancy_grid"))
print("=== Внимание: большие неоплаченные счета ===")

found_critical = False
for invoice in invoices:
    if invoice["amount"] >= 3000 and invoice["status"] == "unpaid":
        print(f"  ⚠ {invoice['number']} от {invoice['vendor']}: {invoice['amount']:.2f}")
        found_critical = True

if not found_critical:
    print("  Нет критических счетов")

print()
print("=== Поставщик с максимальной задолженностью ===")

max_debt_vendor, max_debt = find_max_debtor(invoices)

if max_debt_vendor:
    print(f"  {max_debt_vendor}: {max_debt:.2f}")
else:
    print("  Все счета оплачены")
