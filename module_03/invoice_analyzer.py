from tabulate import tabulate
from categorization import categorize_amount
from statistics import calculate_payment_stats, calculate_category_stats, find_max_debtor
from reporting import print_invoices_table, print_payment_summary, print_category_summary

# Тестовые данные — список счетов от разных поставщиков
invoices = [
    {"number": "INV-001", "vendor": "Acme Corp",   "amount": 1500.00, "status": "paid"},
    {"number": "INV-002", "vendor": "TechSupply",  "amount": 3200.50, "status": "unpaid"},
    {"number": "INV-003", "vendor": "OfficeMax",   "amount": 450.75,  "status": "paid"},
    {"number": "INV-004", "vendor": "Acme Corp",   "amount": 8900.00, "status": "unpaid"},
    {"number": "INV-005", "vendor": "TechSupply",  "amount": 220.00,  "status": "paid"},
    {"number": "INV-006", "vendor": "GlobalParts", "amount": 5670.30, "status": "unpaid"},
    {"number": "INV-007", "vendor": "OfficeMax",   "amount": 175.00,  "status": "paid"},
    {"number": "INV-008", "vendor": "Acme Corp",   "amount": 2340.80, "status": "paid"},
]

# Подготовка счетов: добавляем category и marker
enriched_invoices = []
for invoice in invoices:
    category = categorize_amount(invoice["amount"])
    marker = "✓" if invoice["status"] == "paid" else "✗"
    enriched = {**invoice, "category": category, "marker": marker}
    enriched_invoices.append(enriched)

# Расчёт статистики
payment_stats = calculate_payment_stats(enriched_invoices)
category_stats = calculate_category_stats(enriched_invoices)
max_debt_vendor, max_debt = find_max_debtor(enriched_invoices)

# Вывод таблицы счетов (теперь через функцию)
print("=== Список счетов ===")
print_invoices_table(enriched_invoices)

# Вывод статистики по размеру (пока напрямую, вынесем в итерации 7)
print()
print("=== По размеру ===")
print_category_summary(category_stats)

# Вывод статистики по оплате (пока напрямую, вынесем в итерации 6)
print()
print("=== По оплате ===")
print_payment_summary(payment_stats)

# Критические счета
print()
print("=== Внимание: большие неоплаченные счета ===")
found_critical = False
for invoice in enriched_invoices:
    if invoice["amount"] >= 3000 and invoice["status"] == "unpaid":
        print(f"  ⚠ {invoice['number']} от {invoice['vendor']}: {invoice['amount']:.2f}")
        found_critical = True

if not found_critical:
    print("  Нет критических счетов")

# Максимальный должник
print()
print("=== Поставщик с максимальной задолженностью ===")
if max_debt_vendor:
    print(f"  {max_debt_vendor}: {max_debt:.2f}")
else:
    print("  Все счета оплачены")