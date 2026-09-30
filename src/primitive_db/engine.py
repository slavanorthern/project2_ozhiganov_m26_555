import shlex

import prompt
from prettytable import PrettyTable

from src.primitive_db.constants import META_FILE
from src.primitive_db.core import (
    create_table,
    delete,
    drop_table,
    insert,
    select,
    update,
)
from src.primitive_db.parser import parse_condition, parse_values
from src.primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help():
    """Print available database commands."""
    print("\n***Операции с данными***")
    print("Функции:")
    print(
        "<command> insert into <имя_таблицы> values "
        "(<значение1>, <значение2>, ...) - создать запись."
    )
    print(
        "<command> select from <имя_таблицы> where "
        "<столбец> = <значение> - прочитать записи по условию."
    )
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print(
        "<command> update <имя_таблицы> set <столбец> = <значение> "
        "where <столбец> = <значение> - обновить запись."
    )
    print(
        "<command> delete from <имя_таблицы> where "
        "<столбец> = <значение> - удалить запись."
    )
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def print_table(rows):
    """Print rows as a formatted console table."""
    if not rows:
        print("Записи не найдены.")
        return

    table = PrettyTable()
    table.field_names = rows[0].keys()

    for row in rows:
        table.add_row(row.values())

    print(table)


def run():
    """Run the main database command loop."""
    print("\n***Операции с данными***")
    print_help()

    while True:
        metadata = load_metadata(META_FILE)
        user_input = prompt.string(">>>Введите команду: ")

        try:
            args = shlex.split(user_input)
        except ValueError:
            print(f"Некорректное значение: {user_input}. Попробуйте снова.")
            continue

        if not args:
            continue

        command = args[0]

        if command == "create_table":
            if len(args) < 3:
                print("Некорректное значение. Попробуйте снова.")
                continue

            table_name = args[1]
            columns = args[2:]

            old_metadata = metadata.copy()
            result = create_table(metadata, table_name, columns)

            if result is not None and result != old_metadata:
                save_metadata(META_FILE, result)

        elif command == "drop_table":
            if len(args) != 2:
                print("Некорректное значение. Попробуйте снова.")
                continue

            old_metadata = metadata.copy()
            result = drop_table(metadata, args[1])

            if result is not None and result != old_metadata:
                save_metadata(META_FILE, result)

        elif command == "list_tables":
            if metadata:
                for table_name in metadata:
                    print(f"- {table_name}")
            else:
                print("Таблиц нет.")

        elif command == "insert":
            if len(args) < 5 or args[1] != "into" or args[3] != "values":
                print("Некорректное значение. Попробуйте снова.")
                continue

            table_name = args[2]
            values_text = " ".join(args[4:]).strip()

            if values_text.startswith("(") and values_text.endswith(")"):
                values_text = values_text[1:-1]

            values = parse_values(values_text)
            table_data = insert(metadata, table_name, values)

            if table_data is not None:
                save_table_data(table_name, table_data)

        elif command == "select":
            if len(args) < 3 or args[1] != "from":
                print("Некорректное значение. Попробуйте снова.")
                continue

            table_name = args[2]
            table_data = load_table_data(table_name)

            if len(args) == 3:
                rows = select(table_data)

            elif len(args) >= 7 and args[3] == "where":
                where_clause = parse_condition(args[4:7])
                rows = select(table_data, where_clause)

            else:
                print("Некорректное значение. Попробуйте снова.")
                continue

            print_table(rows)

        elif command == "update":
            if len(args) < 10 or args[2] != "set" or "where" not in args:
                print("Некорректное значение. Попробуйте снова.")
                continue

            table_name = args[1]
            where_index = args.index("where")

            set_clause = parse_condition(args[3:where_index])
            where_clause = parse_condition(args[where_index + 1:])

            table_data = load_table_data(table_name)
            result = update(
                table_data,
                set_clause,
                where_clause,
            )

            if result is not None:
                table_data, updated_ids = result
                save_table_data(table_name, table_data)

                for row_id in updated_ids:
                    print(
                        f'Запись с ID={row_id} в таблице "{table_name}" '
                        "успешно обновлена."
                    )

        elif command == "delete":
            if len(args) < 7 or args[1] != "from" or args[3] != "where":
                print("Некорректное значение. Попробуйте снова.")
                continue

            table_name = args[2]
            where_clause = parse_condition(args[4:7])

            table_data = load_table_data(table_name)
            result = delete(table_data, where_clause)

            if result is not None:
                table_data, deleted_ids = result
                save_table_data(table_name, table_data)

                for row_id in deleted_ids:
                    print(
                        f'Запись с ID={row_id} успешно удалена '
                        f'из таблицы "{table_name}".'
                    )

        elif command == "info":
            if len(args) != 2:
                print("Некорректное значение. Попробуйте снова.")
                continue

            table_name = args[1]

            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            columns = metadata[table_name]
            table_data = load_table_data(table_name)

            columns_text = ", ".join(
                f'{column["name"]}:{column["type"]}'
                for column in columns
            )

            print(f"Таблица: {table_name}")
            print(f"Столбцы: {columns_text}")
            print(f"Количество записей: {len(table_data)}")

        elif command == "help":
            print_help()

        elif command == "exit":
            break

        else:
            print(f"Функции {command} нет. Попробуйте снова.")