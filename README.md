# Primitive DB

Консольное приложение, имитирующее работу простой базы данных.

## Запуск

Установка зависимостей:

```bash
make install
```

Запуск базы данных:

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

Доступные команды:

- `insert into <имя_таблицы> values (<значение1>, <значение2>, ...)` — добавить запись
- `select from <имя_таблицы>` — показать все записи
- `select from <имя_таблицы> where <столбец> = <значение>` — выбрать записи по условию
- `update <имя_таблицы> set <столбец> = <значение> where <столбец> = <значение>` — обновить запись
- `delete from <имя_таблицы> where <столбец> = <значение>` — удалить запись
- `info <имя_таблицы>` — показать информацию о таблице
- `help` — показать справочную информацию
- `exit` — выйти из программы

## Пример использования

```text
create_table users name:str age:int is_active:bool
insert into users values ("Sergei", 28, true)
select from users
select from users where age = 28
update users set age = 29 where name = "Sergei"
delete from users where ID = 1
info users
```

## Демонстрация работы

[Посмотреть запись в asciinema](https://asciinema.org/a/sjZnUzytyjJ58szo)