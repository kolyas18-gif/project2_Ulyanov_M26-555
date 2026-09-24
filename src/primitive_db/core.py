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