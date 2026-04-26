import os
from dotenv import load_dotenv
import anthropic
import json
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

load_dotenv()

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 500
TEMPERATURE = 0

SYSTEM_PROMPT = """
    Ты — ассистент для извлечения данных о товарах.
    Извлекай данные из описания товара и возвращай СТРОГО в JSON-формате.
    Никаких пояснений, комментариев или markdown-обёрток — только чистый JSON.
    
    Формат ответа СТРОГО такой:
    {
      "name": "название товара (string)",
      "price": цена числом (number, без валюты),
      "currency": "валюта трёхбуквенным кодом (string): USD, EUR, RUB",
      "category": "категория товара (string)"
    }
    
    Если какое-то поле невозможно извлечь — используй null.
    Не используй тройные обратные кавычки.
"""

PRODUCT_DESCRIPTION = """
    Apple iPhone 15 Pro Max 256GB Natural Titanium — 1 299 €
    Флагманский смартфон с процессором A17 Pro, дисплеем ProMotion 6.7",
    системой камер Pro с 5x оптическим зумом. Категория: смартфоны премиум-сегмента.
    """


def strip_code_fences(text: str) -> str:
    """
        Убирает markdown-обёртку ```...``` вокруг ответа модели, если она есть.
        """
    text = text.strip()

    if text.startswith("```"):
        if "\n" in text:
            text = text.split("\n", 1)[1]
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]

    return text.strip()


def validate_product(data: dict) -> None:
    """
    Проверяет структуру распарсенного словаря.
    Бросает ValueError при ошибке.
    """
    required_fields = {
        "name": str,
        "price": (int, float),
        "currency": str,
        "category": str
    }

    for field, expected_type in required_fields.items():
        if field not in data:
            raise ValueError(f"Отсутствует обязательное поле: '{field}'")

        value = data[field]

        if value is None:
            continue

        if not isinstance(value, expected_type):
            raise ValueError(
                f"Поле '{field}' имеет неверный тип: "
                f"ожидался {expected_type}, получен {type(value).__name__}"
            )


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type((
            anthropic.RateLimitError,
            anthropic.APIConnectionError,
            anthropic.APIStatusError
    )),
    reraise=True
)
def call_llm(client: anthropic.Anthropic, system_prompt: str, user_message: str) -> str:
    """
    Вызывает Claude и возвращает текст ответа.
    Автоматически повторяется при временных ошибках API.
    """
    message = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    return message.content[0].text


def extract_product(client: anthropic.Anthropic, description: str) -> dict:
    """
    Извлекает структурированные данные о товаре из текстового описания.

    Args:
        client: клиент Anthropic API
        description: текст описания товара
    Returns:
        dict с полями: name, price, currency, category
    Raises:
        anthropic.APIError: при проблемах с API после исчерпания retry
        json.JSONDecoderError: если модель вернула невалидный API
        ValueError: если структура данных не прошла валидацию
    """
    user_message = f"Извлеки данные из следующего описания товара:\n\n{description}"
    raw_response = call_llm(client, SYSTEM_PROMPT, user_message)
    # print(f"Ответ модели:\n {raw_response}")
    cleaned_response = strip_code_fences(raw_response)
    # print(f"Очищенный результат:\n {cleaned_response}")
    product = json.loads(cleaned_response)
    # print(f"Конвертация JSON в dict:\n {product}")
    validate_product(product)

    return product


def main():
    """
    Точка входа: обрабатывает список товаров и печатает сводный отчёт.
    """
    product_descriptions = [
        """
        Apple iPhone 15 Pro Max 256GB Natural Titanium — 1 299 €
        Флагманский смартфон с процессором A17 Pro, дисплеем ProMotion 6.7",
        системой камер Pro с 5x оптическим зумом.
        """,

        """
        Sony WH-1000XM5 Black — наушники беспроводные с активным шумоподавлением,
        до 30 часов работы. Цена: 379.99 USD. Категория: аудиотехника.
        """,

        """
        Книга "Чистый код" Роберт Мартин, издательство Питер, 464 страницы.
        Стоимость: 1890 руб. Категория: техническая литература по программированию.
        """,

        """
        Кофемашина DeLonghi Magnifica S — автоматическая, эспрессо и капучино,
        встроенная кофемолка. Розничная цена 549 евро.
        """,

        """
        Lenovo ThinkPad X1 Carbon Gen 11, Intel Core i7, 16GB RAM, 1TB SSD,
        14" 2.8K OLED дисплей. 1 899 USD. Бизнес-ноутбуки.
        """,
    ]

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    results = []
    errors = []

    for i, description in enumerate(product_descriptions, start=1):
        print(f"Обрабатываю товар {i} из {len(product_descriptions)}...")

        try:
            product = extract_product(client, description)
            results.append(product)
        except(anthropic.APIError, json.JSONDecodeError, ValueError) as e:
            error_info = {"index": i, "error": str(e), "type": type(e).__name__}
            errors.append(error_info)
            print(f"    ⚠️  Ошибка: {type(e).__name__}: {e}")

    print("\n" + "=" * 50)
    print(f"Обработано успешно: {len(results)} из {len(product_descriptions)}")
    print(f"Ошибок: {len(errors)}")
    print("=" * 50)

    if results:
        print("\n=== Извлечённые данные ===")
        for i, product in enumerate(results, start=1):
            print(f"\n[{i}] {product['name']}")
            print(f"    Цена:   {product['price']} {product['currency']}")
            print(f"    Категория:  {product['category']}")

    if errors:
        print("\n=== Ошибки ===")
        for err in errors:
            print(f"    Товар:  #{err['index']}: {err['type']}: {err['error']}")


if __name__ == "__main__":
    main()
