import json


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
