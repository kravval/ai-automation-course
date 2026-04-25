import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 200

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model=MODEL,
    max_tokens=MAX_TOKENS,
    messages=[
        {"role": "user", "content": "Привет! Ответь одним предложением: что такое LLM?"}
    ]
)

print(message.content[0].text)
