import json
import os

from src.primitive_db.constants import DATA_DIR


def load_metadata(filepath):
    """
    Загружает данные из JSON-файла.
    Если файл не найден, возвращает пустой словарь {}.

    Args:
        filepath: путь к JSON-файлу

    Returns:
        dict: данные из файла или пустой словарь
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """
    Сохраняет переданные данные в JSON-файл.

    Args:
        filepath: путь к JSON-файлу
        data: данные для сохранения
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_table_data(table_name):
    """
    Загружает данные таблицы из JSON-файла.

    Args:
        table_name: имя таблицы

    Returns:
        list: список записей таблицы (список словарей) или пустой список
    """
    # Создаем директорию data, если её нет
    os.makedirs(DATA_DIR, exist_ok=True)

    filepath = f"{DATA_DIR}/{table_name}.json"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """
    Сохраняет данные таблицы в JSON-файл.

    Args:
        table_name: имя таблицы
        data: список записей (список словарей)
    """
    # Создаем директорию data, если её нет
    os.makedirs(DATA_DIR, exist_ok=True)

    filepath = f"{DATA_DIR}/{table_name}.json"
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
