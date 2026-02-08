import shlex

from prettytable import PrettyTable

from src.primitive_db.constants import METADATA_FILE
from src.primitive_db.core import (
    create_table,
    delete,
    drop_table,
    get_table_info,
    insert,
    list_tables,
    select,
    update,
)
from src.primitive_db.parser import (
    parse_set_clause,
    parse_values,
    parse_where_clause,
)
from src.primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Операции с данными***")
    print("Функции:")
    print(
        "<command> insert into <имя_таблицы> values (<значение1>, ...) "
        "- создать запись"
    )
    print(
        "<command> select from <имя_таблицы> where <столбец> = <значение> "
        "- прочитать записи по условию"
    )
    print(
        "<command> select from <имя_таблицы> "
        "- прочитать все записи"
    )
    print(
        "<command> update <имя_таблицы> set <столбец> = <значение> "
        "where <столбец> = <значение> - обновить запись"
    )
    print(
        "<command> delete from <имя_таблицы> where <столбец> = <значение> "
        "- удалить запись"
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице")

    print("\n***Управление таблицами***")
    print(
        "<command> create_table <имя_таблицы> <столбец1:тип> .. "
        "- создать таблицу"
    )
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def welcome():
    print("Первая попытка запустить проект!\n")
    print("***")
    print_help()

    while True:
        command = input("Введите команду: ").strip()
        if command == "exit":
            break
        elif command == "help":
            print_help()


def run():
    """
    Главная функция, содержащая основной цикл программы.
    Обрабатывает команды пользователя для управления таблицами БД.
    """
    print_help()

    while True:
        try:
            # Загружаем актуальные метаданные
            metadata = load_metadata(METADATA_FILE)

            # Запрашиваем ввод у пользователя
            user_input = input(">>>Введите команду: ").strip()

            # Пропускаем пустой ввод
            if not user_input:
                continue

            # Разбираем введенную строку на команду и аргументы
            try:
                args = shlex.split(user_input)
            except ValueError as e:
                print(f"Ошибка разбора команды: {e}")
                continue

            if not args:
                continue

            command = args[0].lower()

            # Обрабатываем команды
            if command == "exit":
                print("Выход из программы...")
                break

            elif command == "help":
                print_help()

            elif command == "list_tables":
                tables = list_tables(metadata)
                if not tables:
                    print("Нет созданных таблиц")
                else:
                    for table in tables:
                        print(f"- {table}")

            elif command == "create_table":
                if len(args) < 2:
                    print("Ошибка: укажите имя таблицы и хотя бы один столбец")
                    print("Пример: create_table users name:str age:int")
                    continue

                table_name = args[1]

                # Парсим столбцы в формате column_name:type
                columns = []
                for col_arg in args[2:]:
                    if ':' not in col_arg:
                        print(
                            f"Ошибка: неверный формат столбца '{col_arg}'. "
                            f"Используйте формат column_name:type"
                        )
                        break

                    col_name, col_type = col_arg.split(':', 1)
                    columns.append((col_name, col_type))
                else:
                    # Выполняется, если цикл завершился без break
                    result = create_table(metadata, table_name, columns)
                    if result is not None:
                        metadata = result
                        save_metadata(METADATA_FILE, metadata)
                        # Формируем список столбцов для вывода
                        table_columns = metadata["tables"][table_name]["columns"]
                        columns_str = ", ".join(
                            [f"{col}:{typ}" for col, typ in table_columns.items()]
                        )
                        print(
                            f'Таблица "{table_name}" успешно создана '
                            f"со столбцами: {columns_str}"
                        )

            elif command == "drop_table":
                if len(args) < 2:
                    print("Ошибка: укажите имя таблицы")
                    print("Пример: drop_table users")
                    continue

                table_name = args[1]

                result = drop_table(metadata, table_name)
                if result is not None:
                    metadata = result
                    save_metadata(METADATA_FILE, metadata)
                    print(f'Таблица "{table_name}" успешно удалена.')

            elif command == "insert":
                # insert into <table> values (...)
                if (len(args) < 4 or args[1].lower() != "into" or
                        args[3].lower() != "values"):
                    print("Ошибка: неверный синтаксис")
                    print(
                        "Пример: insert into users values "
                        '("Sergei", 28, true)'
                    )
                    continue

                table_name = args[2]
                values_str = " ".join(args[4:])

                # Парсим значения
                values = parse_values(values_str)

                # Загружаем данные таблицы
                table_data = load_table_data(table_name)

                # Вставляем запись
                result = insert(metadata, table_data, table_name, values)
                if result is not None:
                    table_data, new_id = result

                    # Сохраняем данные
                    save_table_data(table_name, table_data)

                    print(
                        f'Запись с ID={new_id} успешно добавлена '
                        f'в таблицу "{table_name}".'
                    )

            elif command == "select":
                # select from <table> [where ...]
                if len(args) < 3 or args[1].lower() != "from":
                    print("Ошибка: неверный синтаксис")
                    print("Пример: select from users where age = 28")
                    print("Или: select from users")
                    continue

                table_name = args[2]

                # Загружаем данные таблицы
                table_data = load_table_data(table_name)

                # Проверяем наличие WHERE
                where_clause = None
                if len(args) > 3 and args[3].lower() == "where":
                    where_str = " ".join(args[4:])
                    try:
                        where_clause = parse_where_clause(where_str)
                    except ValueError as e:
                        print(str(e))
                        continue

                # Выбираем записи
                records = select(table_data, where_clause)

                # Выводим результат с помощью PrettyTable
                if not records:
                    print("Записей не найдено")
                else:
                    # Получаем имена столбцов из первой записи
                    columns = list(records[0].keys())

                    # Создаем таблицу
                    table = PrettyTable(columns)

                    # Добавляем строки
                    for record in records:
                        table.add_row([record.get(col, "") for col in columns])

                    print(table)

            elif command == "update":
                # update <table> set <column> = <value> where <column> = <value>
                has_where = "where" in [a.lower() for a in args]
                if len(args) < 6 or args[2].lower() != "set" or not has_where:
                    print("Ошибка: неверный синтаксис")
                    print(
                        "Пример: update users set age = 29 "
                        'where name = "Sergei"'
                    )
                    continue

                table_name = args[1]

                try:
                    # Находим позицию WHERE
                    where_index = next(
                        i for i, arg in enumerate(args)
                        if arg.lower() == "where"
                    )

                    # Парсим SET и WHERE части
                    set_str = " ".join(args[3:where_index])
                    where_str = " ".join(args[where_index + 1:])

                    set_clause = parse_set_clause(set_str)
                    where_clause = parse_where_clause(where_str)
                except (ValueError, StopIteration) as e:
                    print(str(e) if str(e) else "Ошибка: неверный синтаксис")
                    continue

                # Загружаем данные таблицы
                table_data = load_table_data(table_name)

                # Обновляем записи
                result = update(
                    metadata, table_data, table_name,
                    set_clause, where_clause
                )
                if result is not None:
                    table_data, updated_count = result

                    # Сохраняем данные
                    save_table_data(table_name, table_data)

                    if updated_count > 0:
                        print(
                            f'Обновлено записей: {updated_count} '
                            f'в таблице "{table_name}".'
                        )
                    else:
                        print("Записей для обновления не найдено")

            elif command == "delete":
                # delete from <table> where <column> = <value>
                if (len(args) < 5 or args[1].lower() != "from" or
                        args[3].lower() != "where"):
                    print("Ошибка: неверный синтаксис")
                    print("Пример: delete from users where ID = 1")
                    continue

                table_name = args[2]
                where_str = " ".join(args[4:])

                try:
                    # Парсим WHERE условие
                    where_clause = parse_where_clause(where_str)
                except ValueError as e:
                    print(str(e))
                    continue

                # Загружаем данные таблицы
                table_data = load_table_data(table_name)

                # Удаляем записи
                result = delete(table_data, where_clause)
                if result is not None:
                    table_data, deleted_count = result

                    # Сохраняем данные
                    save_table_data(table_name, table_data)

                    if deleted_count > 0:
                        print(
                            f'Удалено записей: {deleted_count} '
                            f'из таблицы "{table_name}".'
                        )
                    else:
                        print("Записей для удаления не найдено")

            elif command == "info":
                # info <table>
                if len(args) < 2:
                    print("Ошибка: укажите имя таблицы")
                    print("Пример: info users")
                    continue

                table_name = args[1]

                # Загружаем данные таблицы
                table_data = load_table_data(table_name)

                # Получаем информацию о таблице
                info = get_table_info(metadata, table_data, table_name)
                if info is not None:
                    print(f"Таблица: {info['name']}")
                    print(f"Столбцы: {info['columns']}")
                    print(f"Количество записей: {info['record_count']}")

            else:
                print(f"Неизвестная команда: '{command}'")
                print("Введите 'help' для справки")

        except KeyboardInterrupt:
            print("\n\nВыход из программы...")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
