"""
Подсчёт токенов и оценка стоимости обработки документов через LLM.
Использует tiktoken для точного подсчёта под модели OpenAI.
Для Claude - приблизительная оценка по символам.
"""
import tiktoken

# Цены в USD за 1 млн токенов (input / output).
# Источник: platform.openai.com/docs/pricing и anthropic.com/pricing.
# ВАЖНО: цены меняются — перепроверь на официальных сайтах перед использованием.

PRICING = {
    "gpt-4o-mini": {"input": 0.15, "output": 1.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "claude-haiku-3.5": {"input": 0.80, "output": 4.00},
    "claude-sonnet-4": {"input": 3.00, "output": 15.00},
    "gpt-5-mini": {"input": 0.25, "output": 2.00},
    "gpt-5.2": {"input": 1.75, "output": 14.00}
}


def count_tokens_openai(text: str, model: str = "gpt-4o-mini") -> int:
    """
    Точный подсчёт токенов для моделей OpenAI через tiktoken.

    Args:
        text: Текст для подсчёта.
        model: Название модели OpenAI (определяет токенизатор).

    Returns:
        Количество токенов
    """

    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Для совсем свежих моделей, которых ещё нет в tiktoken,
        # используем универсальный энкодер
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def estimate_tokens_claude(text: str) -> int:
    """
    Приблизительная оценка токенов для Claude.
    Эмпирическая формула: ~4 символа = 1 токен (для английского).

    Args:
        text: Текст для оценки.

    Returns:
        Приблизительное количество токенов (округлённое вверх).
    """
    return max(1, (len(text) + 3) // 4)


def estimate_cost(
        input_tokens: int,
        output_tokens: int,
        model: str,
) -> float:
    """
    Считает стоимость одного запроса в долларах.

    Args:
        input_tokens: Количество входящих токенов.
        output_tokens: Количество исходящих токенов.
        model: Ключ модели из PRICING.

    Returns:
        Стоимость в USD.

    Raises:
        ValueError: если модель не найдена в PRICING.
    """
    if model not in PRICING:
        raise ValueError(f"Неизвестная модель: {model}")

    rates = PRICING[model]
    cost = (input_tokens / 1_000_000) * rates["input"]
    cost += (output_tokens / 1_000_000) * rates["output"]
    return cost


if __name__ == "__main__":
    # Сценарий: 100 документов по 2 страницы.
    # Одна страница A4 делового текста ≈ 500 слов ≈ 2500 символов ≈ ~600 токенов.
    # Исходящий JSON с извлечёнными полями ≈ 300 токенов.
    TOKENS_PER_DOC_INPUT = 1200
    TOKENS_PER_DOC_OUTPUT = 300
    DOCUMENTS = 100

    total_input = TOKENS_PER_DOC_INPUT * DOCUMENTS
    total_output = TOKENS_PER_DOC_OUTPUT * DOCUMENTS

    print(f"Сценарий: обработка {DOCUMENTS} документов по 2 страницы")
    print(f"  Входящих токенов:  {total_input:>8,}")
    print(f"  Исходящих токенов: {total_output:>8,}")
    print(f"  Всего:             {total_input + total_output:>8,}")
    print()
    print(f"{'Модель':<20} {'Стоимость':>12}")
    print("-" * 34)

    for model in PRICING:
        cost = estimate_cost(total_input, total_output, model)
        print(f"{model:<20} ${cost:>11.4f}")

    print()
    print("--- Проверка токенизатора на реальном промпте ---")
    sample = (
        "Extract the following fields from this invoice: invoice number, "
        "date, vendor name, total amount, currency. Return the result as JSON."
    )
    tokens_oa = count_tokens_openai(sample, "gpt-4o-mini")
    tokens_cl = estimate_tokens_claude(sample)
    print(f"Текст ({len(sample)} символов):")
    print(f"  «{sample}»")
    print(f"  tiktoken (точно для OpenAI):  {tokens_oa} токенов")
    print(f"  приближение для Claude:       {tokens_cl} токенов")
