from primitive_db.decorators import confirm_action, handle_db_errors, log_time
from primitive_db.utils import load_table_data, save_table_data


def create_cacher():
    cache = {}

    def cache_result(key, value_func):
        if key not in cache:
            cache[key] = value_func()

        return cache[key]

    return cache_result


select_cache = create_cacher()


@handle_db_errors
def create_table(metadata, table_name, columns):
    if table_name in metadata:
        raise ValueError(f'Таблица "{table_name}" уже существует.')

    valid_types = {"int", "str", "bool"}

    for column in columns:
        _, column_type = column.split(":")

        if column_type not in valid_types:
            raise ValueError(f"Некорректный тип данных: {column_type}")

    columns = ["ID:int"] + columns
    metadata[table_name] = columns

    return metadata

@handle_db_errors
@confirm_action("Удаление таблицы")
def drop_table(metadata, table_name):
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует.')

    del metadata[table_name]

    return metadata

def list_tables(metadata):
    return list(metadata.keys())


@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует.')

    columns = metadata[table_name][1:]

    if len(values) != len(columns):
        raise ValueError("Количество значений не соответствует количеству столбцов.")

    for value, column in zip(values, columns):
        _, column_type = column.split(":")

        if column_type == "int" and not isinstance(value, int):
            raise ValueError(f"Значение {value} должно быть типа int.")

        if column_type == "str" and not isinstance(value, str):
            raise ValueError(f"Значение {value} должно быть типа str.")

        if column_type == "bool" and not isinstance(value, bool):
            raise ValueError(f"Значение {value} должно быть типа bool.")

    table_data = load_table_data(table_name)

    new_id = max((row["ID"] for row in table_data), default=0) + 1

    new_row = {"ID": new_id}

    for column, value in zip(columns, values):
        column_name, _ = column.split(":")
        new_row[column_name] = value

    table_data.append(new_row)
    save_table_data(table_name, table_data)

    return table_data


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    rows_key = tuple(
        tuple(sorted(row.items()))
        for row in table_data
    )
    where_key = (
        tuple(sorted(where_clause.items()))
        if where_clause is not None
        else None
    )
    key = (rows_key, where_key)

    def get_result():
        if where_clause is None:
            return [row.copy() for row in table_data]

        return [
            row.copy()
            for row in table_data
            if all(
                row.get(key) == value
                for key, value in where_clause.items()
            )
        ]

    return select_cache(key, get_result)


@handle_db_errors
def update(table_data, set_clause, where_clause):
    for row in table_data:
        if all(row.get(key) == value for key, value in where_clause.items()):
            for key, value in set_clause.items():
                row[key] = value

    return table_data

@handle_db_errors
@confirm_action("Удаление таблицы")
def delete(table_data, where_clause):
    result = []

    for row in table_data:
        if not all(
            row.get(key) == value
            for key, value in where_clause.items()
        ):
            result.append(row)

    return result