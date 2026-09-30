from src.primitive_db.constants import VALID_TYPES
from src.primitive_db.decorators import (
    confirm_action,
    create_cacher,
    handle_db_errors,
    log_time,
)
from src.primitive_db.utils import load_table_data

cache_result = create_cacher()


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Create a table and add its schema to metadata."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_columns = []

    for column in columns:
        if ":" not in column:
            raise ValueError(f"Некорректное значение: {column}")

        column_name, column_type = column.split(":", 1)

        if not column_name or column_type not in VALID_TYPES:
            raise ValueError(f"Некорректное значение: {column}")

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


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Delete a table from metadata."""
    if table_name not in metadata:
        raise KeyError(table_name)

    del metadata[table_name]

    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata


def _is_valid_type(value, column_type):
    """Check whether a value matches the required column type."""
    if column_type == "int":
        return isinstance(value, int) and not isinstance(value, bool)

    if column_type == "str":
        return isinstance(value, str)

    if column_type == "bool":
        return isinstance(value, bool)

    return False


@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    """Insert a new row into a table."""
    if table_name not in metadata:
        raise KeyError(table_name)

    columns = metadata[table_name]

    user_columns = [
        column
        for column in columns
        if column["name"] != "ID"
    ]

    if len(values) != len(user_columns):
        raise ValueError("Некорректное количество значений")

    for column, value in zip(user_columns, values):
        if not _is_valid_type(value, column["type"]):
            raise ValueError(f"Некорректное значение: {value}")

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


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Select table rows, optionally filtering by a condition."""
    data_key = tuple(
        tuple(sorted(row.items()))
        for row in table_data
    )

    where_key = (
        tuple(sorted(where_clause.items()))
        if where_clause
        else None
    )

    key = (data_key, where_key)

    def get_result():
        if where_clause is None:
            return [row.copy() for row in table_data]

        return [
            row.copy()
            for row in table_data
            if all(
                row.get(column) == value
                for column, value in where_clause.items()
            )
        ]

    return cache_result(key, get_result)


@handle_db_errors
def update(table_data, set_clause, where_clause):
    """Update rows matching a condition."""
    updated_ids = []

    for row in table_data:
        if all(
            row.get(column) == value
            for column, value in where_clause.items()
        ):
            row.update(set_clause)
            updated_ids.append(row["ID"])

    return table_data, updated_ids


@handle_db_errors
@confirm_action("удаление записи")
def delete(table_data, where_clause):
    """Delete rows matching a condition."""
    deleted_ids = [
        row["ID"]
        for row in table_data
        if all(
            row.get(column) == value
            for column, value in where_clause.items()
        )
    ]

    new_data = [
        row
        for row in table_data
        if not all(
            row.get(column) == value
            for column, value in where_clause.items()
        )
    ]

    return new_data, deleted_ids