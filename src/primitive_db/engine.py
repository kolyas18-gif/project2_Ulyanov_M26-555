import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    insert,
    list_tables,
    select,
    update,
)
from primitive_db.parser import parse_set, parse_value, parse_where
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

DB_FILE = "db_meta.json"

def run():
    while True:
        metadata = load_metadata(DB_FILE)
        user_input = prompt.string("Введите команду: ")
        args = shlex.split(user_input)
        command = args[0] if args else ""

        print(command, args)

        if command == "exit":
            break

        elif command == "create_table":
            table_name = args[1]
            columns = args[2:]
            try:
                metadata = create_table(metadata, table_name, columns)
                save_metadata(DB_FILE, metadata)
                print(f'Таблица "{table_name}" создана.')
            except ValueError as error:
                print(error)

        elif command == "insert":
            table_name = args[2]

            values_start = user_input.find("(")
            values_end = user_input.rfind(")")

            values_string = user_input[values_start + 1:values_end]

            values = [
                parse_value(value.strip())
                for value in values_string.split(",")
            ]

            try:
                table_data = insert(metadata, table_name, values)
                print(
                    f'Запись с ID={table_data[-1]["ID"]} успешно добавлена '
                    f'в таблицу "{table_name}".'
                )
            except ValueError as error:
                print(error)

        elif command == "select":
            table_name = args[2]
            table_data = load_table_data(table_name)

            if "where" in args:
                where_index = user_input.find(" where ")
                condition = user_input[where_index + 7:]
                where_clause = parse_where(condition)
                result = select(table_data, where_clause)
            else:
                result = select(table_data)

            table = PrettyTable()

            if result:
                table.field_names = result[0].keys()

                for row in result:
                    table.add_row(row.values())

                print(table)
            else:
                print("Записи не найдены.")

        elif command == "update":
            table_name = args[1]
            table_data = load_table_data(table_name)

            set_index = user_input.find(" set ")
            where_index = user_input.find(" where ")

            set_condition = user_input[set_index + 5:where_index]
            where_condition = user_input[where_index + 7:]

            set_clause = parse_set(set_condition)
            where_clause = parse_where(where_condition)

            table_data = update(table_data, set_clause, where_clause)
            save_table_data(table_name, table_data)

            print(f'Данные в таблице "{table_name}" обновлены.')

        elif command == "delete":
            table_name = args[2]
            table_data = load_table_data(table_name)

            where_index = user_input.find(" where ")
            where_condition = user_input[where_index + 7:]

            where_clause = parse_where(where_condition)

            table_data = delete(table_data, where_clause)
            save_table_data(table_name, table_data)

            print(f'Данные из таблицы "{table_name}" удалены.')

        elif command == "list_tables":
            tables = list_tables(metadata)
            print(tables)

        elif command == "drop_table":
            table_name = args[1]
            try:
                metadata = drop_table(metadata, table_name)
                save_metadata(DB_FILE, metadata)
                print(f'Таблица "{table_name}" удалена.')
            except ValueError as error:
                print(error)

        elif command == "help":
            print("\n***Процесс работы с таблицами***")
            print("Функции:")
            print(
            "<command> create_table <имя_таблицы> <столбец>:<тип> ... - создать таблицу"
            )
            print("<command> list_tables - показать список всех таблиц")
            print("<command> drop_table <имя_таблицы> - удалить таблицу")
            print("\nОбщие команды:")
            print("<command> exit - выход из программы")
            print("<command> help - справочная информация")
            print(
                    "<command> insert into <имя_таблицы> values "
                    "(<значение1>, <значение2>, ...) - добавить запись"
                )
            print(
                    "<command> select from <имя_таблицы> where "
                    "<столбец> = <значение> - выбрать записи"
                )
            print(
                    "<command> update <имя_таблицы> set <столбец> = <значение> "
                    "where <столбец> = <значение> - обновить записи"
                )
            print(
                    "<command> delete from <имя_таблицы> where "
                    "<столбец> = <значение> - удалить записи"
                )
            print('<command> select from <имя_таблицы> - показать все записи')

        else:
            print(f'Неизвестная команда: {command}')

def welcome():
    print("Первая попытка запустить проект!")
    print("***")

    while True:
        command = prompt.string("Введите команду: ")

        if command == "exit":
            break

        if command == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")