import os
from http import client

from dotenv import load_dotenv
import anthropic


load_dotenv()

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 500
TEMPERATURE = 0

SYSTEM_PROMPT = """
Ты - ассистент для извлечения данных о товарах.
Твоя задача - прочитать описание товара и выделить из него ключевые поля:
    название, цена, валюта, категория.
Отвечай кратко и по существу, без лишних пояснений. 
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

print(message.content[0].text)
