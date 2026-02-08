from src.primitive_db.constants import AUTO_ID_COLUMN, AUTO_ID_TYPE, VALID_TYPES
from src.primitive_db.decorators import confirm_action, handle_db_errors, log_time


@handle_db_errors
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

    # Проверяем корректность типов данных
    for column_name, column_type in columns:
        if column_type not in VALID_TYPES:
            raise ValueError(
                f"Ошибка: недопустимый тип данных '{column_type}' "
                f"для столбца '{column_name}'. "
                f"Разрешены только: {', '.join(VALID_TYPES)}"
            )

    # Проверяем, задан ли столбец ID пользователем
    has_id = any(col_name.upper() == AUTO_ID_COLUMN for col_name, _ in columns)

    # Создаем словарь столбцов
    columns_dict = {}

    # Если ID не задан, добавляем его автоматически в начало
    if not has_id:
        columns_dict[AUTO_ID_COLUMN] = AUTO_ID_TYPE

    # Добавляем остальные столбцы
    for column_name, column_type in columns:
        columns_dict[column_name] = column_type

    # Добавляем таблицу в metadata
    metadata["tables"][table_name] = {
        "columns": columns_dict
    }

    return metadata


@handle_db_errors
@confirm_action("удаление таблицы")
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


def validate_value_type(value, expected_type):
    """
    Проверяет соответствие значения ожидаемому типу.

    Args:
        value: значение для проверки
        expected_type: ожидаемый тип ('int', 'str', 'bool')

    Returns:
        tuple: (is_valid, converted_value)
    """
    try:
        if expected_type == "int":
            return True, int(value)
        elif expected_type == "str":
            # Удаляем кавычки если есть
            if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                return True, value[1:-1]
            return True, str(value)
        elif expected_type == "bool":
            if isinstance(value, bool):
                return True, value
            if isinstance(value, str):
                if value.lower() in ('true', '1'):
                    return True, True
                elif value.lower() in ('false', '0'):
                    return True, False
            raise ValueError(f"Невозможно преобразовать '{value}' в bool")
        else:
            return False, None
    except (ValueError, TypeError):
        return False, None


@log_time
@handle_db_errors
def insert(metadata, table_data, table_name, values):
    """
    Добавляет новую запись в таблицу.

    Args:
        metadata: словарь с метаданными базы данных
        table_data: список текущих записей таблицы
        table_name: имя таблицы
        values: список значений для вставки (без ID)

    Returns:
        tuple: (updated_table_data, new_record_id)

    Raises:
        ValueError: при ошибках валидации
    """
    # Проверяем существование таблицы
    if "tables" not in metadata or table_name not in metadata["tables"]:
        raise ValueError(f'Ошибка: таблица "{table_name}" не существует')

    # Получаем схему таблицы
    table_schema = metadata["tables"][table_name]["columns"]
    columns = list(table_schema.keys())

    # Исключаем ID из проверки количества (ID генерируется автоматически)
    columns_without_id = [col for col in columns if col.upper() != AUTO_ID_COLUMN]

    # Проверяем количество значений
    if len(values) != len(columns_without_id):
        raise ValueError(
            f"Ошибка: ожидается {len(columns_without_id)} значений, "
            f"получено {len(values)}"
        )

    # Генерируем новый ID
    if table_data:
        # Находим максимальный ID
        max_id = max(record.get(AUTO_ID_COLUMN, 0) for record in table_data)
        new_id = max_id + 1
    else:
        new_id = 1

    # Создаем новую запись
    new_record = {}

    # Находим имя столбца ID (может быть ID, id, Id)
    id_column = next(
        (col for col in columns if col.upper() == AUTO_ID_COLUMN),
        AUTO_ID_COLUMN
    )
    new_record[id_column] = new_id

    # Валидируем и добавляем значения
    for i, column in enumerate(columns_without_id):
        expected_type = table_schema[column]
        is_valid, converted_value = validate_value_type(values[i], expected_type)

        if not is_valid:
            raise ValueError(
                f"Ошибка: значение '{values[i]}' "
                f"не соответствует типу '{expected_type}' "
                f"для столбца '{column}'"
            )

        new_record[column] = converted_value

    # Добавляем запись в данные таблицы
    table_data.append(new_record)

    return table_data, new_id


@log_time
def select(table_data, where_clause=None):
    """
    Выбирает записи из таблицы.

    Args:
        table_data: список записей таблицы
        where_clause: словарь условий фильтрации {column: value} или None

    Returns:
        list: список записей, соответствующих условию
    """
    if not where_clause:
        # Возвращаем все записи
        return table_data

    # Фильтруем записи по условию
    filtered_records = []
    for record in table_data:
        match = True
        for column, value in where_clause.items():
            if column not in record or record[column] != value:
                match = False
                break
        if match:
            filtered_records.append(record)

    return filtered_records


@handle_db_errors
def update(metadata, table_data, table_name, set_clause, where_clause):
    """
    Обновляет записи в таблице.

    Args:
        metadata: словарь с метаданными базы данных
        table_data: список записей таблицы
        table_name: имя таблицы
        set_clause: словарь значений для обновления {column: new_value}
        where_clause: словарь условий фильтрации {column: value}

    Returns:
        tuple: (updated_table_data, updated_count)

    Raises:
        ValueError: при ошибках валидации
    """
    # Проверяем существование таблицы
    if "tables" not in metadata or table_name not in metadata["tables"]:
        raise ValueError(f'Ошибка: таблица "{table_name}" не существует')

    # Получаем схему таблицы
    table_schema = metadata["tables"][table_name]["columns"]

    # Валидируем столбцы в set_clause
    for column, new_value in set_clause.items():
        if column not in table_schema:
            raise ValueError(f'Ошибка: столбец "{column}" не существует в таблице')

        expected_type = table_schema[column]
        is_valid, converted_value = validate_value_type(new_value, expected_type)

        if not is_valid:
            raise ValueError(
                f"Ошибка: значение '{new_value}' "
                f"не соответствует типу '{expected_type}' "
                f"для столбца '{column}'"
            )

        # Обновляем значение в set_clause на преобразованное
        set_clause[column] = converted_value

    # Находим и обновляем записи
    updated_count = 0
    for record in table_data:
        match = True
        for column, value in where_clause.items():
            if column not in record or record[column] != value:
                match = False
                break

        if match:
            for column, new_value in set_clause.items():
                record[column] = new_value
            updated_count += 1

    return table_data, updated_count


@handle_db_errors
@confirm_action("удаление записи")
def delete(table_data, where_clause):
    """
    Удаляет записи из таблицы.

    Args:
        table_data: список записей таблицы
        where_clause: словарь условий фильтрации {column: value}

    Returns:
        tuple: (updated_table_data, deleted_count)
    """
    if not where_clause:
        raise ValueError("Ошибка: укажите условие WHERE для удаления")

    # Находим записи для удаления
    records_to_keep = []
    deleted_count = 0

    for record in table_data:
        match = True
        for column, value in where_clause.items():
            if column not in record or record[column] != value:
                match = False
                break

        if match:
            deleted_count += 1
        else:
            records_to_keep.append(record)

    return records_to_keep, deleted_count


@handle_db_errors
def get_table_info(metadata, table_data, table_name):
    """
    Получает информацию о таблице.

    Args:
        metadata: словарь с метаданными базы данных
        table_data: список записей таблицы
        table_name: имя таблицы

    Returns:
        dict: информация о таблице

    Raises:
        ValueError: если таблица не существует
    """
    if "tables" not in metadata or table_name not in metadata["tables"]:
        raise ValueError(f'Ошибка: таблица "{table_name}" не существует')

    table_schema = metadata["tables"][table_name]["columns"]
    columns_str = ", ".join([f"{col}:{typ}" for col, typ in table_schema.items()])

    return {
        "name": table_name,
        "columns": columns_str,
        "record_count": len(table_data)
    }
