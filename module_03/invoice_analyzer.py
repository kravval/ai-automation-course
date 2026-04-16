from tabulate import tabulate
import logging
from categorization import categorize_amount
from statistics import calculate_payment_stats, calculate_category_stats, find_max_debtor
from reporting import (
    print_invoices_table,
    print_payment_summary,
    print_category_summary,
    print_critical_invoices,
    print_max_debtor
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


def process_invoice(invoice: dict) -> dict | None:
    """
    Подготавливает один счёт к выводу: добавляет категорию и маркер.

    Args:
        invoice: Словарь с полями number, vendor, amount, status.

    Returns:
        Расширенный словарь с полями category и marker, или None, если счёт невалидный.
    """
    try:
        amount = invoice["amount"]
        status = invoice["status"]

        category = categorize_amount(amount)
        marker = "✓" if status == "paid" else "✗"

        return {**invoice, "category": category, "marker": marker}

    except KeyError as e:
        logger.error("Невалидный счёт %s: отсутствует поле %s",
                     invoice.get("number", "UNKNOWN"), e)
        return None
    except TypeError as e:
        logger.error("Невалидный счёт %s: ошибка типа данных — %s",
                     invoice.get("number", "UNKNOWN"), e)
        return None


def main():
    """Главная функция: обрабатывает счета и выводит отчёт."""
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
    logger.info("Начинаю обработку %d счетов", len(invoices))

    # Подготовка счетов: добавляем category и marker
    enriched_invoices = []
    for invoice in invoices:
        result = process_invoice(invoice)
        if result is not None:
            enriched_invoices.append(result)

    logger.info("Подготовлено %d счетов к выводу", len(enriched_invoices))

    # Расчёт статистики
    payment_stats = calculate_payment_stats(enriched_invoices)
    category_stats = calculate_category_stats(enriched_invoices)
    max_debt_vendor, max_debt = find_max_debtor(enriched_invoices)

    # Вывод таблицы счетов
    print("=== Список счетов ===")
    print_invoices_table(enriched_invoices)

    # Вывод статистики по размеру
    print()
    print("=== По размеру ===")
    print_category_summary(category_stats)

    # Вывод статистики по оплате
    print()
    print("=== По оплате ===")
    print_payment_summary(payment_stats)

    # Критические счета
    print()
    print("=== Внимание: большие неоплаченные счета ===")
    print_critical_invoices(enriched_invoices)

    # Максимальный должник
    print()
    print("=== Поставщик с максимальной задолженностью ===")
    print_max_debtor(max_debt_vendor, max_debt)


if __name__ == "__main__":
    main()
