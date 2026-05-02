"""Быстрая проверка чтения переменных из .env."""
import os
from dotenv import load_dotenv

# Сначала смотрим — переменная пустая (load_dotenv ещё не вызван)
print(f"До load_dotenv: {os.getenv('INVOICES_DATA_PATH')!r}")

load_dotenv()

# Теперь — есть
print(f"После load_dotenv: {os.getenv('INVOICES_DATA_PATH')!r}")