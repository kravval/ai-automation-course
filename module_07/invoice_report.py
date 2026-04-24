"""Генерация Excel-отчёта по счетам."""

import logging
import pandas as pd
from reports import build_excel_report

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


def load_invoices(path: str) -> pd.DataFrame:
    """
    Загружает счета из JSON-файла и готовит DataFrame к обработке.

    Returns:
        DataFrame или None, если файл не удалось загрузить.
    """
    logger.info("Загружаю счета из %s", path)

    try:
        df = pd.read_json(path)
    except FileNotFoundError:
        logger.error("Файл %s не найден", path)
        return None
    except ValueError as e:
        logger.error("Файл %s повреждён или не является валидным JSON: %s", path, e)
        return None

    if df.empty:
        logger.error("Файл %s пустой", path)
        return None

    required_columns = {"number", "date", "vendor", "amount", "status"}
    missing = required_columns - set(df.columns)
    if missing:
        logger.error("В файле отсутствуют обязательные колонки: %s", missing)
        return None

    df["date"] = pd.to_datetime(df["date"])
    df["amount_category"] = pd.cut(
        df["amount"],
        bins=[0, 1000, 5000, float("inf")],
        labels=["small", "medium", "large"],
        right=False,
    )
    logger.info("Загружено %d счетов", len(df))
    return df

def build_vendor_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Возвращает сводку по поставщикам: count, sum, mean, unpaid_count.
    """
    summary = (
        df.groupby("vendor")
        .agg(
            invoices_count=("number", "count"),
            total_amount=("amount", "sum"),
            average_amount=("amount", "mean"),
            unpaid_count=("status", lambda s: (s == "unpaid").sum()),
        )
        .round(2)
        .reset_index()
    )
    return summary


def main() -> None:
    """
    Главная функция: загружает данные и строит Excel-отчёт.
    """
    df = load_invoices(
        "/home/valk/projects/ai-automation-course/module_07/invoices.json"
    )
    if df is None:
        logger.error("Не могу продолжить без данных. Завершаю работу.")
        return

    unpaid = df[df["status"] == "unpaid"]
    logger.info("Неоплаченных счетов: %d (сумма %.2f)", len(unpaid), unpaid["amount"].sum())

    vendor_summary = build_vendor_summary(df)
    logger.info("Поставщиков в сводке: %d", len(vendor_summary))

    output_path = "invoice_report.xlsx"
    build_excel_report(df, unpaid, vendor_summary, output_path)
    logger.info("Отчёт сохранён: %s", output_path)


if __name__ == "__main__":
    main()
