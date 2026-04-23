"""Генерация Excel-отчёта по счетам."""
import pandas as pd

# Загрузка JSON прямо в DataFrame - pandas сам парсит файл
df = pd.read_json("/home/valk/projects/ai-automation-course/module_07/invoices.json")

print("=== Размер данных ===")
print(df.shape)

print("\n=== Первые строки ===")
print(df.head())

print("\n=== Типы колонок ===")
print(df.dtypes)

# Категория по сумме: small (< 1000), medium (< 5000), large (>= 5000)

df["amount_category"] = pd.cut(
    df["amount"],
    bins=[0, 1000, 5000, float("inf")],
    labels=["small", "medium", "large"],
    right=False
)

print("\n=== Таблица с категориями ===")

print(df[["number", "vendor", "amount", "amount_category"]])