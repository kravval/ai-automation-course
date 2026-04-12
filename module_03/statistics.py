def calculate_payment_stats(invoices: list) -> dict:
    """
    Подсчитывает количество и сумму оплаченных и неоплаченных счетов.

    Args:
        invoices: Список словарей со счетами.
            Каждый счёт должен содержать поля
            "status" и "amount".

    Returns:
        Словарь с ключами: paid_count, unpaid_count, total_paid, total_unpaid.
    """

    paid_count = 0
    unpaid_count = 0
    total_paid = 0.0
    total_unpaid = 0.0

    for invoice in invoices:
        if invoice["status"] == "paid":
            paid_count += 1
            total_paid += invoice["amount"]
        else:
            unpaid_count += 1
            total_unpaid += invoice["amount"]
    return {
        "paid_count": paid_count,
        "unpaid_count": unpaid_count,
        "total_paid": total_paid,
        "total_unpaid": total_unpaid,
    }


def calculate_category_stats(invoices: list) -> dict:
    """
    Подсчитывает количество и сумму счетов по категориям размеров
        ("small", "medium", "large").

    Args:
        invoices: Список словарей со счетами.
            У каждого должно быть поле "category".
            "category" - результат categorize_amount().

    Returns:
        Словарь вида {"small": {"count": ..., "amount": ...},
                      "medium": ...,
                      "large":  ...}
    """

    stats = {
        "small": {"count": 0, "amount": 0.0},
        "medium": {"count": 0, "amount": 0.0},
        "large": {"count": 0, "amount": 0.0},
    }

    for invoice in invoices:
        category = invoice['category']
        stats[category]["count"] += 1
        stats[category]["amount"] += invoice["amount"]

    return stats


if __name__ == "__main__":
    test_invoices = [
        {"number": "T-001", "amount": 1000.00, "status": "paid", "category": "medium"},
        {"number": "T-002", "amount": 2000.00, "status": "unpaid", "category": "medium"},
        {"number": "T-003", "amount": 300.00, "status": "paid", "category": "small"},
        {"number": "T-004", "amount": 5000.00, "status": "unpaid", "category": "large"}
    ]

    # Тест 1: payment_stats
    stats = calculate_payment_stats(test_invoices)
    print("Payment:", stats)
    assert stats["paid_count"] == 2
    assert stats["unpaid_count"] == 2
    assert stats["total_paid"] == 1300.00
    assert stats["total_unpaid"] == 7000.00
    print("✓ calculate_payment_stats")

    # Тест 2: category_stats
    cat_stats = calculate_category_stats(test_invoices)
    print("Categories:", cat_stats)
    assert cat_stats["small"]["count"] == 1
    assert cat_stats["medium"]["count"] == 2
    assert cat_stats["large"]["count"] == 1
    assert cat_stats["small"]["amount"] == 300.00
    assert cat_stats["medium"]["amount"] == 3000.00
    assert cat_stats["large"]["amount"] == 5000.00
    print("✓ calculate_category_stats")

    print("\n✓ All statistics tests passed!")