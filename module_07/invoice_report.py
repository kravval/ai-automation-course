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