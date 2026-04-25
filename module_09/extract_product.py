import os
from dotenv import load_dotenv
import anthropic
from module_09.hello_llm import MAX_TOKENS

load_dotenv()

MODEL = "claude-haiku-4-5-20251001"
NAX_TOKENS = 500
TEMPERATURE = 0

SYSTEM_PROMPT = """
    Ты — ассистент для извлечения данных о товарах.
    Извлекай данные из описания товара и возвращай СТРОГО в JSON-формате.
    Никаких пояснений, комментариев или markdown-обёрток — только чистый JSON.
    
    Формат ответа:
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