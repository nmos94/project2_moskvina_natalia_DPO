#!/usr/bin/env python3
"""Тест автоматической генерации столбца ID"""

from src.primitive_db.core import create_table

# Тест 1: ID не задан пользователем - должен добавиться автоматически
print("Тест 1: ID не задан пользователем")
metadata1 = {}
columns1 = [("name", "str"), ("age", "int")]
metadata1 = create_table(metadata1, "users", columns1)
print(f"Столбцы: {metadata1['tables']['users']['columns']}")
assert "ID" in metadata1["tables"]["users"]["columns"]
assert metadata1["tables"]["users"]["columns"]["ID"] == "int"
print("✅ Тест 1 пройден: ID добавлен автоматически\n")

# Тест 2: ID задан пользователем - не должен дублироваться
print("Тест 2: ID задан пользователем")
metadata2 = {}
columns2 = [("ID", "int"), ("name", "str"), ("age", "int")]
metadata2 = create_table(metadata2, "products", columns2)
print(f"Столбцы: {metadata2['tables']['products']['columns']}")
# Проверяем, что ID встречается только один раз
id_count = list(metadata2["tables"]["products"]["columns"].keys()).count("ID")
assert id_count == 1, f"ID встречается {id_count} раз, ожидалось 1"
print("✅ Тест 2 пройден: ID не дублируется\n")

# Тест 3: ID задан в разном регистре (id, Id, iD)
print("Тест 3: ID задан в разном регистре")
metadata3 = {}
columns3 = [("id", "int"), ("title", "str")]
metadata3 = create_table(metadata3, "articles", columns3)
print(f"Столбцы: {metadata3['tables']['articles']['columns']}")
# Проверяем, что автоматический ID не добавился
columns_list = list(metadata3["tables"]["articles"]["columns"].keys())
print(f"Список столбцов: {columns_list}")
# Должно быть 2 столбца: id и title
assert len(columns_list) == 2, f"Ожидалось 2 столбца, получено {len(columns_list)}"
print("✅ Тест 3 пройден: регистр учитывается корректно\n")

# Тест 4: ID с другим типом данных
print("Тест 4: ID с типом str")
metadata4 = {}
columns4 = [("ID", "str"), ("value", "int")]
metadata4 = create_table(metadata4, "custom", columns4)
print(f"Столбцы: {metadata4['tables']['custom']['columns']}")
assert metadata4["tables"]["custom"]["columns"]["ID"] == "str"
print("✅ Тест 4 пройден: пользовательский тип ID сохранен\n")

print("=" * 50)
print("Все тесты успешно пройдены!")
print("=" * 50)
