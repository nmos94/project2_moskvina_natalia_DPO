"""Декораторы для улучшения качества кода базы данных"""

import time
from functools import wraps


def handle_db_errors(func):
    """
    Декоратор для централизованной обработки ошибок базы данных.

    Перехватывает исключения:
    - FileNotFoundError: файл данных не найден
    - KeyError: таблица или столбец не найден
    - ValueError: ошибки валидации
    - Exception: непредвиденные ошибки
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. "
                "Возможно, база данных не инициализирована."
            )
            return None
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
            return None
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
            return None
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
            return None
    return wrapper


def confirm_action(action_name):
    """
    Декоратор-фабрика для запроса подтверждения опасных операций.

    Args:
        action_name: название действия для отображения пользователю

    Example:
        @confirm_action("удаление таблицы")
        def drop_table(metadata, table_name):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Запрашиваем подтверждение
            response = input(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            )

            if response.lower() != 'y':
                print("Операция отменена.")
                return None

            # Выполняем функцию
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_time(func):
    """
    Декоратор для измерения времени выполнения функции.

    Выводит время выполнения в консоль после завершения функции.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        elapsed_time = end_time - start_time

        print(f"Функция {func.__name__} выполнилась за {elapsed_time:.3f} секунд")
        return result
    return wrapper


def create_cacher():
    """
    Создает функцию кэширования с замыканием.

    Returns:
        Функция cache_result(key, value_func), которая:
        - Проверяет наличие результата в кэше
        - Если есть - возвращает из кэша
        - Если нет - вызывает value_func, сохраняет и возвращает результат

    Example:
        cache = create_cacher()
        result = cache('users_all', lambda: select(table_data, None))
    """
    # Кэш хранится в замыкании
    cache_storage = {}

    def cache_result(key, value_func):
        """
        Получает результат из кэша или вычисляет его.

        Args:
            key: ключ для кэширования
            value_func: функция для получения значения (если нет в кэше)

        Returns:
            Результат из кэша или вычисленный результат
        """
        if key in cache_storage:
            print(f"[CACHE HIT] Результат получен из кэша для ключа '{key}'")
            return cache_storage[key]

        print(f"[CACHE MISS] Вычисление результата для ключа '{key}'")
        result = value_func()
        cache_storage[key] = result
        return result

    # Добавляем метод для очистки кэша
    def clear_cache():
        """Очищает весь кэш"""
        cache_storage.clear()
        print("[CACHE] Кэш очищен")

    # Добавляем метод для просмотра статистики
    def cache_stats():
        """Возвращает статистику кэша"""
        return {
            'size': len(cache_storage),
            'keys': list(cache_storage.keys())
        }

    # Привязываем методы к функции
    cache_result.clear = clear_cache
    cache_result.stats = cache_stats

    return cache_result
