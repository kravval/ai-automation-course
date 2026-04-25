import os

from dotenv import load_dotenv
import anthropic
import json

load_dotenv()

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 500
TEMPERATURE = 0

SYSTEM_PROMPT = """
Ты — ассистент для извлечения данных о товарах.
    Извлекай данные из описания товара и возвращай СТРОГО в JSON-формате.
    Никаких пояснений, комментариев или markdown-обёрток — только чистый JSON.
    СТРОГО БЕЗ ```json```
    
    Формат ответа СТРОГО такой:
    {
      "name": "название товара (string)",
      "price": цена числом (number, без валюты),
      "currency": "валюта трёхбуквенным кодом (string): USD, EUR, RUB",
      "category": "категория товара (string)"
    }
    
    Если какое-то поле невозможно извлечь — используй null.
"""

PRODUCT_DESCRIPTION = """
    Apple iPhone 15 Pro Max 256GB Natural Titanium — 1 299 €
    Флагманский смартфон с процессором A17 Pro, дисплеем ProMotion 6.7",
    системой камер Pro с 5x оптическим зумом. Категория: смартфоны премиум-сегмента.
    """


def strip_code_fences(text: str) -> str:
    """
        Убирает ```json ... ``` или ``` ... ``` вокруг ответа модели.
        Если обёртки нет — возвращает строку как есть.
        """
    text = text.strip()

    if text.startswith("```"):
        if "\n" in text:
            text = text.split("\n", 1)[1]
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]

    return text.strip()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
message = client.messages.create(
    model=MODEL,
    max_tokens=MAX_TOKENS,
    temperature=TEMPERATURE,
    system=SYSTEM_PROMPT,
    messages=[
        {
            "role": "user",
            "content": f"Извлеки данные из следующего описания товара:\n\n{PRODUCT_DESCRIPTION}"
        }
    ]
)

raw_response = message.content[0].text

print("=== Сырой ответ модели ===")
print(raw_response)

cleaned_response = strip_code_fences(raw_response)

print("=== Очищенный JSON ===")
print(cleaned_response)

try:
    product = json.loads(cleaned_response)
except json.JSONDecodeError as e:
    print(f"\n❌ Ошибка парсинга JSON: {e}")
    print(f"Модель вернула не валидный JSON. Проверь промпт или попробуй снова.")
    raise SystemExit(1)

print("\n=== Распарсенные данные ===")
print(f"    Название:   {product['name']}")
print(f"    Цена:       {product['price']} {product['currency']}")
print(f"    Категория:  {product['category']}")
print(f"\nТип объекта product: {type(product).__name__}")
