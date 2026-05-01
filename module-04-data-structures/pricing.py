"""Расчёт стоимости парсинга со скидками за объём."""


def calculate_discount(pages: int) -> float:
    """Возвращает долю скидки (0, 0.10 или 0.20) в зависимости от объёма."""
    if pages > 500:
        return 0.2
    elif pages > 100:
        return 0.1
    else:
        return 0


def calculate_total(pages: int, price_per_page: float) -> tuple[float, float, float]:
    """Считает подытог, скидку и итоговую сумму. Возвращает все три значения."""
    subtotal = pages * price_per_page
    discount = calculate_discount(pages)
    total = subtotal * (1 - discount)

    return subtotal, discount, total


if __name__ == "__main__":
    # Быстрая проверка модуля при прямом запуске:
    #   python pricing.py
    print(calculate_total(250, 5.0))
    print(calculate_total(600, 6.0))
    print(calculate_total(50, 4.0))
