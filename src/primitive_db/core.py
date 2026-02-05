def create_table(metadata, table_name, columns):
    """
    Создает новую таблицу в метаданных базы данных.

    Args:
        metadata: словарь с метаданными базы данных
        table_name: имя создаваемой таблицы
        columns: список столбцов в формате [("column_name", "type"), ...]

    Returns:
        dict: обновленный словарь metadata

    Raises:
        ValueError: если таблица уже существует или типы данных некорректны

    Note:
        Если столбец ID не задан пользователем, он добавляется автоматически
        как первый столбец с типом int.
    """
    # Инициализируем структуру metadata, если она пустая
    if "tables" not in metadata:
        metadata["tables"] = {}

    # Проверяем, не существует ли уже таблица с таким именем
    if table_name in metadata["tables"]:
        raise ValueError(f"Ошибка: таблица '{table_name}' уже существует")

    # Допустимые типы данных
    valid_types = {"int", "str", "bool"}

    # Проверяем корректность типов данных
    for column_name, column_type in columns:
        if column_type not in valid_types:
            raise ValueError(
                f"Ошибка: недопустимый тип данных '{column_type}' "
                f"для столбца '{column_name}'. "
                f"Разрешены только: {', '.join(valid_types)}"
            )

    # Проверяем, задан ли столбец ID пользователем
    has_id = any(col_name.upper() == "ID" for col_name, _ in columns)

    # Создаем словарь столбцов
    columns_dict = {}

    # Если ID не задан, добавляем его автоматически в начало
    if not has_id:
        columns_dict["ID"] = "int"

    # Добавляем остальные столбцы
    for column_name, column_type in columns:
        columns_dict[column_name] = column_type

    # Добавляем таблицу в metadata
    metadata["tables"][table_name] = {
        "columns": columns_dict
    }

    return metadata


def drop_table(metadata, table_name):
    """
    Удаляет таблицу из метаданных базы данных.

    Args:
        metadata: словарь с метаданными базы данных
        table_name: имя удаляемой таблицы

    Returns:
        dict: обновленный словарь metadata

    Raises:
        ValueError: если таблица не существует
    """
    # Проверяем инициализацию структуры metadata
    if "tables" not in metadata or table_name not in metadata["tables"]:
        raise ValueError(f"Ошибка: таблица '{table_name}' не существует")

    # Удаляем таблицу из metadata
    del metadata["tables"][table_name]

    return metadata


def list_tables(metadata):
    """
    Возвращает список всех таблиц в базе данных.

    Args:
        metadata: словарь с метаданными базы данных

    Returns:
        list: список имен таблиц
    """
    if "tables" not in metadata or not metadata["tables"]:
        return []

    return list(metadata["tables"].keys())
