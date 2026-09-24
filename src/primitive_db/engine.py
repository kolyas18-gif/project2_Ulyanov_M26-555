import shlex

import prompt

from primitive_db.core import create_table, drop_table, list_tables
from primitive_db.utils import load_metadata, save_metadata

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