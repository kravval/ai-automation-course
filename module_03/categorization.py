def categorize_amount(amount: float) -> str:
    """
    Возвращает категорию счёта по его сумме.

    Args:
        amount: Сумма счёта.

    Returns:
        Строка: "small" (<500), "medium" (< 3000), "large" (>= 3000).
    """

    if amount < 500:
        return "small"
    elif amount < 3000:
        return "medium"
    else:
        return "large"

if __name__=="__main__":
    assert categorize_amount(100) == "small"
    assert categorize_amount(499.99) == "small"
    assert categorize_amount(500) == "medium"
    assert categorize_amount(1500) == "medium"
    assert categorize_amount(2999.99) == "medium"
    assert categorize_amount(3000) == "large"
    assert categorize_amount(10000) == "large"
    print("✓ All categorization tests passed!")
