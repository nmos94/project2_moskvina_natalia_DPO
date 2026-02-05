# Инструкция по загрузке демонстрации на Asciinema

## Шаг 1: Аутентификация в Asciinema

Если вы ещё не аутентифицировались в asciinema, выполните:

```bash
asciinema auth
```

Эта команда выведет URL для аутентификации. Откройте его в браузере и подтвердите установку соединения между вашей машиной и сервером asciinema.org.

## Шаг 2: Загрузка записи

Загрузите созданную запись `demo.cast`:

```bash
asciinema upload demo.cast
```

После успешной загрузки вы получите URL вида:
```
https://asciinema.org/a/XXXXXX
```

Где `XXXXXX` - это уникальный ID вашей записи.

## Шаг 3: Обновление README.md

Откройте файл `README.md` и найдите раздел **Демонстрация**. Замените `XXXXXX` на реальный ID из полученного URL:

```markdown
<!-- Было: -->
[![asciicast](https://asciinema.org/a/XXXXXX.svg)](https://asciinema.org/a/XXXXXX)

<!-- Стало (например, если ID = 123456): -->
[![asciicast](https://asciinema.org/a/123456.svg)](https://asciinema.org/a/123456)
```

## Шаг 4: Проверка

Откройте README.md в браузере или на GitHub, чтобы убедиться, что демонстрация корректно встроена и воспроизводится.

## Альтернативный способ: Прямое встраивание

Asciinema также предоставляет возможность встраивания плеера на страницу:

```html
<script src="https://asciinema.org/a/XXXXXX.js" id="asciicast-XXXXXX" async></script>
```

## Содержание демонстрации

Созданная запись `demo.cast` демонстрирует:

1. ✅ Создание таблицы `users` с колонками `name:str`, `age:int`, `is_active:bool`
2. ✅ Просмотр списка таблиц командой `list_tables`
3. ✅ Создание второй таблицы `products` с колонками `title:str`, `price:int`
4. ✅ Просмотр обновленного списка таблиц
5. ✅ Попытка создать существующую таблицу (ошибка)
6. ✅ Удаление таблицы `users`
7. ✅ Просмотр списка после удаления
8. ✅ Попытка удалить несуществующую таблицу (ошибка)
9. ✅ Вызов справки командой `help`
10. ✅ Выход из программы командой `exit`

## Пересоздание записи

Если нужно пересоздать запись, выполните:

```bash
# Использование expect-скрипта
asciinema rec demo.cast -c "./demo_alternative.exp" --overwrite

# Или вручную (интерактивно)
asciinema rec demo.cast
# ... выполните команды вручную ...
# Нажмите Ctrl+D или введите exit для завершения записи
```

## Полезные ссылки

- [Документация Asciinema](https://asciinema.org/docs/)
- [Как работает Asciinema](https://asciinema.org/docs/how-it-works)
- [API Asciinema](https://asciinema.org/docs/embedding)
