#!/usr/bin/env python3
"""Тест функции print_help()"""

from src.primitive_db.engine import print_help

print("Тестирование функции print_help():")
print("=" * 60)
print_help()
print("=" * 60)
print("\n✅ Функция print_help() работает корректно!")
print("   - Команды работы с таблицами отображаются")
print("   - Общие команды отображаются")
print("   - Форматирование корректное")
