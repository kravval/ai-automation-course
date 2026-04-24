"""Генерация Excel-отчёта по счетам."""

import pandas as pd
from reports import build_excel_report

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
    right=False,
)

print("\n=== Таблица с категориями ===")

print(df[["number", "vendor", "amount", "amount_category"]])

# Только неплаченные счета
unpaid = df[df["status"] == "unpaid"]

print("\n=== Только неоплаченные счета ===")
print(unpaid[["number", "date", "vendor", "amount"]])
print(f"Всего неплаченных счетов: {len(unpaid)}")
print(f"Сумма долга: {unpaid["amount"].sum():.2f}")

# Неоплаченные и более 5000
critical = df[(df["status"] == "unpaid") & (df["amount"] > 5000)]
print("\n=== Неоплаченные счета выше 5000 ===")
print(critical[["number", "date", "vendor", "amount"]])

# Все счета, отсортированные по дате (новые сверху)
df_sorted = df.sort_values("date", ascending=False)

print("\n=== Все счета, отсортированные по дате (новые сверху) ===")
print(df_sorted[["number", "date", "vendor", "amount", "status"]])

# Простая группировка: сумма счетов по каждому поставщику
vendor_totals = df.groupby("vendor")["amount"].sum()

print("\n=== Сумма счетов по поставщикам ===")
print(vendor_totals)

# Сводка по поставщикам: несколько метрик сразу
vendor_summary = (
    df.groupby("vendor")
    .agg(
        invoices_count=("number", "count"),
        total_amount=("amount", "sum"),
        average_amount=("amount", "mean"),
        unpaid_count=("status", lambda s: (s == "unpaid").sum()),
    )
    .round(2)
)

print("\n=== Сводка по поставщикам ===")
print(vendor_summary)

print("\n=== Тип результата ===")
print(type(vendor_summary))
print(vendor_summary.columns.to_list())

vendor_summary = vendor_summary.reset_index()
print(vendor_summary)

# Простой экспорт - одна таблица, один файл
df.to_excel("invoices_simple.xlsx", index=False)
print("\nФайл invoices_simple.xlsx создан")


build_excel_report(
    df,
    unpaid,
    vendor_summary,
    "invoices_report.xlsx",
)
print("\nФайл invoice_report.xlsx создан")
