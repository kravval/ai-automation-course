def main():
    print("=" * 40)
    print("  Калькулятор стоимости парсинга")
    print("=" * 40)

    total_pages = 0
    total_revenue = 0.0
    orders_count = 0

    while True:
        pages = int(input("\nКоличество страниц: "))
        price_per_page = float(input("Цена за страницу ($): "))

        if pages > 500:
            discount = 0.20
        elif pages > 100:
            discount = 0.10
        else:
            discount = 0

        subtotal = pages * price_per_page
        total = subtotal * (1 - discount)
        
        print(f"Pages: {pages}")
        print(f"  Подытог:  ${subtotal:>10,.2f}")
        print(f"  Скидка:   {discount:>10.0%}")
        print(f"  К оплате: ${total:>10,.2f}")

        total_pages += pages
        total_revenue += total
        orders_count += 1



        answer = input("\nПродолжить? (y/n): ").strip().lower()
        if answer not in ("y", "yes"):
            break

    print("\n" + "=" * 40)
    print(f"Заказов обработано: {orders_count}")
    print(f"Всего страниц:      {total_pages:,}")
    print(f"Общая выручка:      ${total_revenue:,.2f}")


if __name__ == "__main__":
    main()
