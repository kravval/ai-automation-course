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
