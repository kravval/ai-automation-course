"""
Проверка, что API-ключ корректно загружается из .env
Не отправляет запросов к API - только загружает ключ и проверяет его форму.
"""
import os
from dotenv import load_dotenv
from pip._internal.resolution.resolvelib import provider


def load_api_key(provider: str) -> str:
    """
    Загружает API ключ из .env по имени провайдера.

    Args:
        provider: "openai" или "anthropic".

    Returns:
        Ключ как строка.

    Raises:
        ValueError: если провайдер неизвестен, ключ не найден или подозрительно короткий.
    """
    load_dotenv()

    env_vars = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY"
    }

    if provider not in env_vars:
        raise ValueError(f"Неизвестный провайдер: {provider}")

    env_var = env_vars[provider]
    key = os.getenv(env_var)

    if not key:
        raise ValueError(f"{env_var} не найден в .env")

    if "replace-with" in key or len(key) < 20:
        raise ValueError(f"{env_var} выглядит как плейсхолдер - подставь реальный ключ")

    return key

def mask_key(key: str) -> str:
    """
    Возвращает замаскированный ключ для безопасного вывода в логи.
    """
    if len(key) < 12:
        return "***"
    return f"{key[:7]}...{key[-4:]}"

if __name__ == "__main__":
    provider = "openai"

    try:
        key = load_api_key(provider)
        print(f"✓ Ключ {provider} успешно загружен: {mask_key(key)}")
        print(f" Длина: {len(key)} символов")
    except ValueError as e:
        print(f"✗ Ошибка: {e}")

