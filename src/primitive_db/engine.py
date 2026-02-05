import shlex
import os
from src.primitive_db.utils import load_metadata, save_metadata
from src.primitive_db.core import create_table, drop_table


COMMANDS_HELP = """\
Доступные команды:
  create_table <table_name> <column1:type1> <column2:type2> ...
      Создать новую таблицу с указанными столбцами
      Типы данных: int, str, bool
      Пример: create_table users name:str age:int active:bool

  drop_table <table_name>
      Удалить таблицу
      Пример: drop_table users

  help
      Показать справку

  exit
      Выйти из программы
"""

# Путь к файлу метаданных
METADATA_FILE = "db_meta.json"


def welcome():
    print("Первая попытка запустить проект!\n")
    print("***")
    print(COMMANDS_HELP)

    while True:
        command = input("Введите команду: ").strip()
        if command == "exit":
            break
        elif command == "help":
            print(COMMANDS_HELP)


def run():
    """
    Главная функция, содержащая основной цикл программы.
    Обрабатывает команды пользователя для управления таблицами БД.
    """
    print("=== Primitive Database ===")
    print("Введите 'help' для справки\n")

    while True:
        try:
            # Загружаем актуальные метаданные
            metadata = load_metadata(METADATA_FILE)

            # Запрашиваем ввод у пользователя
            user_input = input("db> ").strip()

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
                print(COMMANDS_HELP)

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
                        print(f"Ошибка: неверный формат столбца '{col_arg}'. Используйте формат column_name:type")
                        break

                    col_name, col_type = col_arg.split(':', 1)
                    columns.append((col_name, col_type))
                else:
                    # Выполняется, если цикл завершился без break
                    try:
                        metadata = create_table(metadata, table_name, columns)
                        save_metadata(METADATA_FILE, metadata)
                        print(f"Таблица '{table_name}' успешно создана")
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
                    print(f"Таблица '{table_name}' успешно удалена")
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
