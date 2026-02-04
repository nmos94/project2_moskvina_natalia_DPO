COMMANDS_HELP = """\
<command> exit - выйти из программы
<command> help - справочная информация"""


def welcome():
    print("Первая попытка запустить проект!\n")
    print("***")
    print(COMMANDS_HELP)

    while True:
        command = input("Введите команду: ").strip()
        if command == "exit":
            break
        elif command == "help":
            print(COMMANDS_HELP)
