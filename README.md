# Primitive DB

Консольное приложение, имитирующее работу простой базы данных.

## Установка

```bash
make install
```

## Запуск

```bash
poetry run database
```

## Управление таблицами

Доступные команды:

- `create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ...` — создать таблицу
- `list_tables` — показать список всех таблиц
- `drop_table <имя_таблицы>` — удалить таблицу
- `help` — показать справочную информацию
- `exit` — выйти из программы

Поддерживаемые типы данных:

- `int`
- `str`
- `bool`

Столбец `ID:int` добавляется автоматически, если пользователь не указал его самостоятельно.

## CRUD-операции

- `insert into <имя_таблицы> values (<значение1>, <значение2>, ...)` — добавить запись
- `select from <имя_таблицы>` — показать все записи
- `select from <имя_таблицы> where <столбец> = <значение>` — выбрать записи
- `update <имя_таблицы> set <столбец> = <значение> where <столбец> = <значение>` — обновить запись
- `delete from <имя_таблицы> where <столбец> = <значение>` — удалить запись
- `info <имя_таблицы>` — информация о таблице

## Декораторы и замыкания

В проекте реализованы:

- `handle_db_errors` — централизованная обработка ошибок
- `confirm_action` — подтверждение опасных операций
- `log_time` — измерение времени выполнения
- `create_cacher` — кэширование одинаковых запросов `select`

Удаление записи и таблицы требует подтверждения пользователя.

## Пример использования

```text
create_table users name:str age:int is_active:bool
insert into users values ("Sergei", 28, true)
select from users
select from users where age = 28
update users set age = 29 where name = "Sergei"
delete from users where ID = 1
info users
drop_table users
```

## Демонстрации

### Управление таблицами

[![asciicast](https://asciinema.org/a/MyICwmW9GlN1jPOD.svg)](https://asciinema.org/a/MyICwmW9GlN1jPOD)

### CRUD-операции

[![asciicast](https://asciinema.org/a/sjZnUzytyjJ58szo.svg)](https://asciinema.org/a/sjZnUzytyjJ58szo)

### Декораторы и финальная версия

[![asciicast](https://asciinema.org/a/IMeobDLNTQWwAjvW.svg)](https://asciinema.org/a/IMeobDLNTQWwAjvW)