import prompt


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