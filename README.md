# Primitive Database

Простая примитивная база данных на Python с возможностью управления таблицами.

## Описание

Primitive Database - это учебный проект, реализующий базовую систему управления базами данных с поддержкой создания и удаления таблиц. Метаданные о структуре таблиц хранятся в JSON-файле.

## Установка и запуск

```bash
# Запуск программы
python -m src.primitive_db.main
```

## Управление таблицами

### Создание таблицы

**Синтаксис:**
```
create_table <table_name> <column1:type1> <column2:type2> ...
```

**Поддерживаемые типы данных:**
- `int` - целые числа
- `str` - строки
- `bool` - логические значения (true/false)

**Особенности:**
- Столбец `ID:int` добавляется автоматически в начало каждой таблицы
- Имя таблицы должно быть уникальным

**Примеры:**
```
# Создание таблицы пользователей
db> create_table users name:str age:int active:bool

# Создание таблицы товаров
db> create_table products title:str price:int in_stock:bool

# Создание таблицы статей
db> create_table articles title:str content:str views:int
```

**Результат:**
```
Таблица 'users' успешно создана
```

### Удаление таблицы

**Синтаксис:**
```
drop_table <table_name>
```

**Примеры:**
```
# Удаление таблицы пользователей
db> drop_table users
```

**Результат:**
```
Таблица 'users' успешно удалена
```

### Справка

```
db> help
```

Показывает список всех доступных команд с описанием.

### Выход из программы

```
db> exit
```

## Примеры использования

### Сценарий 1: Создание базы данных для блога

```bash
db> create_table users username:str email:str registered:bool
Таблица 'users' успешно создана

db> create_table posts title:str content:str author_id:int published:bool
Таблица 'posts' успешно создана

db> create_table comments post_id:int user_id:int text:str
Таблица 'comments' успешно создана
```

### Сценарий 2: Удаление ненужной таблицы

```bash
db> drop_table comments
Таблица 'comments' успешно удалена
```

### Сценарий 3: Обработка ошибок

```bash
# Попытка создать таблицу с существующим именем
db> create_table users name:str age:int
Ошибка: таблица 'users' уже существует

# Попытка использовать недопустимый тип данных
db> create_table test field:float
Ошибка: недопустимый тип данных 'float' для столбца 'field'. Разрешены только: int, str, bool

# Попытка удалить несуществующую таблицу
db> drop_table nonexistent
Ошибка: таблица 'nonexistent' не существует
```

## Структура проекта

```
project2_moskvina_natalia_DPO/
├── src/
│   └── primitive_db/
│       ├── main.py       # Точка входа в приложение
│       ├── engine.py     # Основной цикл программы
│       ├── core.py       # Функции управления таблицами
│       └── utils.py      # Утилиты для работы с JSON
├── db_meta.json          # Файл метаданных (создается автоматически)
└── README.md
```

## Файл метаданных

Все данные о таблицах хранятся в файле `db_meta.json`:

```json
{
    "tables": {
        "users": {
            "columns": {
                "ID": "int",
                "name": "str",
                "age": "int",
                "active": "bool"
            }
        },
        "products": {
            "columns": {
                "ID": "int",
                "title": "str",
                "price": "int",
                "in_stock": "bool"
            }
        }
    }
}
```

## Требования

- Python 3.6+
- Стандартная библиотека Python (json, shlex)

## Автор

Moskvina Natalia
