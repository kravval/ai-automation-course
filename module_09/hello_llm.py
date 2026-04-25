import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 200
TEMPERATURE = 0

SYSTEM_PROMPT = """Ты — краткий технический ассистент.
    Отвечай строго одним предложением. Без вступлений и пояснений."""

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model=MODEL,
    max_tokens=MAX_TOKENS,
    temperature=TEMPERATURE,
    system=SYSTEM_PROMPT,
    messages=[
        {"role": "user", "content": "Что такое LLM?"}
    ]
)

print(message.content[0].text)



