"""Разведка: знакомство с pandas DataFrame."""
import pandas as pd

test_data = [
    {"name": "Alice", "age": 30, "city": "Berlin"},
    {"name":"Bob", "age": 25, "city": "Munich"},
    {"name": "Charlie", "age": 35, "city": "Berlin"},
    {"name": "Dianna", "age": 28, "city": "Hamburg"}
]

df = pd.DataFrame(test_data)
print("=== Таблица целиком ===")
print(df)

print("\n=== Размер (строки, столбцы) ===")
print(df.shape)

print("\n=== Названия колонок ===")
print(df.columns.to_list())

print("\n=== Типы данных в колоках ===")
print(df.dtypes)

print("\n=== Первые две строки ===")
print(df.head(2))

print("\n=== Одна колонка (возраст) ===")
print(df["age"])

print("\n=== Статистика по числовым колонкам ===")
print(df.describe())