from categorization import  categorize_amount
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
paid_count = 0
unpaid_count = 0
total_paid = 0.0
total_unpaid = 0.0
small_count = 0
small_amount = 0.0
medium_count = 0
medium_amount = 0.0
large_count = 0
large_amount = 0.0

for invoice in invoices:

    category = categorize_amount(invoice["amount"])

    if invoice["status"] == "paid":
        marker = "✓"
        paid_count += 1
        total_paid += invoice["amount"]
    else:
        marker = "✗"
        unpaid_count += 1
        total_unpaid += invoice["amount"]

    row = [
        marker,
        invoice["number"],
        invoice["vendor"],
        f"{invoice['amount']:.2f}",
        category,
        invoice["status"]
    ]
    table_data.append(row)

headers = ["", "Number", "Vendor", "Amount", "Category", "Status"]

print("=== По размеру ===")
size_data = [
    ["small", small_count, f"{small_amount:.2f}"],
    ["medium", medium_count, f"{medium_amount:.2f}"],
    ["large", large_count, f"{large_amount:.2f}"],
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
max_debt = 0.0
max_debt_vendor = ""
for invoice in invoices:
    if invoice["status"] == "unpaid" and invoice["amount"] > max_debt:
        max_debt = invoice["amount"]
        max_debt_vendor = invoice["vendor"]

if max_debt_vendor:
    print(f"  {max_debt_vendor}: {max_debt:.2f}")
else:
    print("  Все счета оплачены")
