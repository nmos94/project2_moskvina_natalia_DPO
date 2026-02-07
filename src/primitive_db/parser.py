"""Парсеры для SQL-подобных команд"""

import re


def parse_values(values_str):
    """
    Парсит строку VALUES.

    Args:
        values_str: строка вида '("value1", 28, true)' или '(value1, 28, true)'

    Returns:
        list: список значений

    Examples:
        >>> parse_values('("Sergei", 28, true)')
        ['Sergei', 28, True]
    """
    # Удаляем скобки и пробелы
    values_str = values_str.strip()
    if values_str.startswith('(') and values_str.endswith(')'):
        values_str = values_str[1:-1]

    # Разбираем по запятым с учетом кавычек
    values = []
    current_value = ""
    in_quotes = False
    quote_char = None

    for char in values_str:
        if char in ('"', "'") and not in_quotes:
            in_quotes = True
            quote_char = char
            current_value += char
        elif char == quote_char and in_quotes:
            in_quotes = False
            current_value += char
            quote_char = None
        elif char == ',' and not in_quotes:
            values.append(parse_single_value(current_value.strip()))
            current_value = ""
        else:
            current_value += char

    # Добавляем последнее значение
    if current_value.strip():
        values.append(parse_single_value(current_value.strip()))

    return values


def parse_single_value(value_str):
    """
    Преобразует строковое представление значения в Python-объект.

    Args:
        value_str: строка значения

    Returns:
        Преобразованное значение (str, int, bool)
    """
    value_str = value_str.strip()

    # Проверяем булевы значения
    if value_str.lower() == 'true':
        return True
    elif value_str.lower() == 'false':
        return False

    # Проверяем строку в кавычках
    if (value_str.startswith('"') and value_str.endswith('"')) or \
       (value_str.startswith("'") and value_str.endswith("'")):
        return value_str[1:-1]

    # Пробуем преобразовать в int
    try:
        return int(value_str)
    except ValueError:
        pass

    # Пробуем преобразовать в float
    try:
        return float(value_str)
    except ValueError:
        pass

    # Возвращаем как строку
    return value_str


def parse_where_clause(where_str):
    """
    Парсит WHERE условие.

    Args:
        where_str: строка вида 'column = value' или
                   'column1 = value1 and column2 = value2'

    Returns:
        dict: словарь условий {column: value}

    Examples:
        >>> parse_where_clause('age = 28')
        {'age': 28}
        >>> parse_where_clause('name = "John"')
        {'name': 'John'}
    """
    where_dict = {}

    # Поддержка AND (простая реализация)
    # Разбиваем по 'and' (регистронезависимо)
    conditions = re.split(r'\s+and\s+', where_str, flags=re.IGNORECASE)

    for condition in conditions:
        # Разбираем условие 'column = value'
        match = re.match(r'\s*(\w+)\s*=\s*(.+)\s*$', condition.strip())
        if not match:
            raise ValueError(f"Неверный формат WHERE условия: '{condition}'")

        column = match.group(1).strip()
        value_str = match.group(2).strip()

        # Парсим значение
        value = parse_single_value(value_str)
        where_dict[column] = value

    return where_dict


def parse_set_clause(set_str):
    """
    Парсит SET условие.

    Args:
        set_str: строка вида 'column = value' или 'column1 = value1, column2 = value2'

    Returns:
        dict: словарь обновлений {column: new_value}

    Examples:
        >>> parse_set_clause('age = 29')
        {'age': 29}
        >>> parse_set_clause('age = 29, name = "John"')
        {'age': 29, 'name': 'John'}
    """
    set_dict = {}

    # Разбиваем по запятым с учетом кавычек
    assignments = []
    current_assignment = ""
    in_quotes = False
    quote_char = None

    for char in set_str:
        if char in ('"', "'") and not in_quotes:
            in_quotes = True
            quote_char = char
            current_assignment += char
        elif char == quote_char and in_quotes:
            in_quotes = False
            current_assignment += char
            quote_char = None
        elif char == ',' and not in_quotes:
            assignments.append(current_assignment.strip())
            current_assignment = ""
        else:
            current_assignment += char

    # Добавляем последнее присваивание
    if current_assignment.strip():
        assignments.append(current_assignment.strip())

    # Парсим каждое присваивание
    for assignment in assignments:
        match = re.match(r'\s*(\w+)\s*=\s*(.+)\s*$', assignment.strip())
        if not match:
            raise ValueError(f"Неверный формат SET условия: '{assignment}'")

        column = match.group(1).strip()
        value_str = match.group(2).strip()

        # Парсим значение
        value = parse_single_value(value_str)
        set_dict[column] = value

    return set_dict
