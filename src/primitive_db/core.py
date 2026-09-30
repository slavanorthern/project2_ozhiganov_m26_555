from src.primitive_db.utils import load_table_data

VALID_TYPES = {"int", "str", "bool"}


def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_columns = []

    for column in columns:
        if ":" not in column:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        column_name, column_type = column.split(":", 1)

        if not column_name or column_type not in VALID_TYPES:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata

        table_columns.append(
            {
                "name": column_name,
                "type": column_type,
            }
        )

    has_id = any(column["name"] == "ID" for column in table_columns)

    if not has_id:
        table_columns.insert(
            0,
            {
                "name": "ID",
                "type": "int",
            },
        )

    metadata[table_name] = table_columns

    columns_text = ", ".join(
        f'{column["name"]}:{column["type"]}'
        for column in table_columns
    )

    print(
        f'Таблица "{table_name}" успешно создана '
        f"со столбцами: {columns_text}"
    )

    return metadata


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]

    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata


def _is_valid_type(value, column_type):
    if column_type == "int":
        return isinstance(value, int) and not isinstance(value, bool)

    if column_type == "str":
        return isinstance(value, str)

    if column_type == "bool":
        return isinstance(value, bool)

    return False


def insert(metadata, table_name, values):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    columns = metadata[table_name]
    user_columns = columns[1:]

    if len(values) != len(user_columns):
        print("Некорректное количество значений. Попробуйте снова.")
        return None

    for column, value in zip(user_columns, values):
        if not _is_valid_type(value, column["type"]):
            print(f"Некорректное значение: {value}. Попробуйте снова.")
            return None

    table_data = load_table_data(table_name)

    new_id = max(
        (row["ID"] for row in table_data),
        default=0,
    ) + 1

    row = {"ID": new_id}

    for column, value in zip(user_columns, values):
        row[column["name"]] = value

    table_data.append(row)

    print(
        f'Запись с ID={new_id} успешно добавлена '
        f'в таблицу "{table_name}".'
    )

    return table_data


def select(table_data, where_clause=None):
    if where_clause is None:
        return table_data

    return [
        row
        for row in table_data
        if all(
            row.get(key) == value
            for key, value in where_clause.items()
        )
    ]


def update(table_data, set_clause, where_clause):
    updated_ids = []

    for row in table_data:
        if all(
            row.get(key) == value
            for key, value in where_clause.items()
        ):
            row.update(set_clause)
            updated_ids.append(row["ID"])

    return table_data, updated_ids


def delete(table_data, where_clause):
    deleted_ids = [
        row["ID"]
        for row in table_data
        if all(
            row.get(key) == value
            for key, value in where_clause.items()
        )
    ]

    new_data = [
        row
        for row in table_data
        if not all(
            row.get(key) == value
            for key, value in where_clause.items()
        )
    ]

    return new_data, deleted_ids