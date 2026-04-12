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


if __name__ == "__main__":
   test_invoices = [
       {"number": "T-001", "amount": 1000.00, "status": "paid"},
       {"number": "T-002", "amount": 2000.00, "status": "unpaid"},
       {"number": "T-003", "amount": 500.00, "status": "paid"},
   ]

   stats =calculate_payment_stats(test_invoices)
   print("Result:", stats)

   assert stats["paid_count"] == 2
   assert stats["unpaid_count"] == 1
   assert stats["total_paid"] == 1500.00
   assert stats["total_unpaid"] == 2000.00

   print("✓ calculate_payment_stats tests passed!")