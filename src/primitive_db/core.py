from primitive_db.utils import load_table_data, save_table_data


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

def drop_table(metadata, table_name):
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует.')

    del metadata[table_name]

    return metadata

def list_tables(metadata):
    return list(metadata.keys())


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


def select(table_data, where_clause=None):
    if where_clause is None:
        return table_data

    result = []

    for row in table_data:
        if all(row.get(key) == value for key, value in where_clause.items()):
            result.append(row)

    return result


def update(table_data, set_clause, where_clause):
    for row in table_data:
        if all(row.get(key) == value for key, value in where_clause.items()):
            for key, value in set_clause.items():
                row[key] = value

    return table_data


def delete(table_data, where_clause):
    result = []

    for row in table_data:
        if not all(
            row.get(key) == value
            for key, value in where_clause.items()
        ):
            result.append(row)

    return result