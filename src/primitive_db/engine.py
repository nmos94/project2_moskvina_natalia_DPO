import shlex

from src.primitive_db.core import create_table, drop_table, list_tables
from src.primitive_db.utils import load_metadata, save_metadata

# Путь к файлу метаданных
METADATA_FILE = "db_meta.json"


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
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
                    try:
                        metadata = create_table(metadata, table_name, columns)
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
                    except ValueError as e:
                        print(str(e))

            elif command == "drop_table":
                if len(args) < 2:
                    print("Ошибка: укажите имя таблицы")
                    print("Пример: drop_table users")
                    continue

                table_name = args[1]

                try:
                    metadata = drop_table(metadata, table_name)
                    save_metadata(METADATA_FILE, metadata)
                    print(f'Таблица "{table_name}" успешно удалена.')
                except ValueError as e:
                    print(str(e))

            else:
                print(f"Неизвестная команда: '{command}'")
                print("Введите 'help' для справки")

        except KeyboardInterrupt:
            print("\n\nВыход из программы...")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
