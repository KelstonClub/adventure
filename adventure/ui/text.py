def run(adventure):
    while True:
        command = input("What now? ")
        result = adventure.handle_command("user", command)
        print(result)