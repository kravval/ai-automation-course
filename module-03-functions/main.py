from pricing import calculate_total
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def read_positive_int(prompt: str) -> int:
    """Спрашивает у пользователя положительное целое.
    Повторяет запрос до корректного ввода."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            logging.warning("Некорректный ввод (не int): %r", raw)
            print(f"  ❌ '{raw}' — не целое число. Попробуйте ещё раз.")
            continue
        if value <= 0:
            logging.warning("Некорректный ввод (не положительное): %d", value)
            print(f"  ❌ Значение должно быть больше 0. Попробуйте ещё раз.")
            continue

        return value


def read_positive_float(prompt: str) -> float:
    """Спрашивает у пользователя положительное число с плавающей точкой."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            logging.warning("Некорректный ввод (не float): %r", raw)
            print(f"  ❌ '{raw}' — не число. Попробуйте ещё раз.")
            continue
        if value <= 0:
            logging.warning("Некорректный ввод (не положительное): %d", value)
            print(f"  ❌ Значение должно быть больше 0. Попробуйте ещё раз.")
            continue
        return value


def print_order_result(subtotal: float, discount: float, total: float) -> None:
    """Печатает результат одного заказа в форматированном виде."""
    print(f"  Подытог:  ${subtotal:>10,.2f}")
    print(f"  Скидка:   {discount:>10.0%}")
    print(f"  К оплате: ${total:>10,.2f}")


def print_summary(orders_count: int, total_pages: int, total_revenue: int) -> None:
    """Печатает финальную сводку по всем заказам."""
    print("\n" + "=" * 40)
    print(f"Заказов обработано: {orders_count}")
    print(f"Всего страниц:      {total_pages:,}")
    print(f"Общая выручка:      ${total_revenue:,.2f}")


def main():
    logging.info("Калькулятор запущен")

    print("=" * 40)
    print("  Калькулятор стоимости парсинга")
    print("=" * 40)

    total_pages = 0
    total_revenue = 0.0
    orders_count = 0

    while True:
        pages = read_positive_int("\nКоличество страниц: ")
        price_per_page = read_positive_float("Цена за страницу ($): ")

        subtotal, discount, total = calculate_total(pages, price_per_page)
        logging.info(
            "Заказ #%d: %d страниц × $%.2f → подытог $%.2f, скидка %.0f%%, итого $%.2f",
            orders_count + 1, pages, price_per_page, subtotal, discount * 100, total,
        )

        print_order_result(subtotal, discount, total)

        total_pages += pages
        total_revenue += total
        orders_count += 1

        answer = input("\nПродолжить? (y/n): ").strip().lower()

        if answer not in ("y", "yes"):
            break

    logging.info(
        "Завершение: %d заказов, %d страниц, выручка $%.2f",
        orders_count, total_pages, total_revenue,
    )

    print_summary(orders_count, total_pages, total_revenue)


if __name__ == "__main__":
    main()
